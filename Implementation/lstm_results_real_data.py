"""
evaluate_and_finetune_models.py

================================

Modul na vyhodnotenie viacerých LSTM modelov (base, robust, batchnorm, attention)
na reálnych dátach a možnosť dodatočného finetuningu attention modelu.

Obsahuje:
- definíciu attention vrstvy,
- výpočet váh tried z reálnych dát,
- generovanie sekvenčných dát,
- vyhodnotenie klasifikačnej presnosti,
- možnosť jemného dotrénovania attention modelu na reálnych dátach.
"""

import os
import json
import joblib
import warnings

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Layer
from tensorflow.keras import backend as K
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical

warnings.filterwarnings("ignore")

# --- Attention Layer Definition ---
class AttentionLayer(Layer):
    """
    Custom Attention Layer pre LSTM architektúru.
    """
    def __init__(self, **kwargs):
        super(AttentionLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        self.W = self.add_weight(name='att_weight', shape=(input_shape[-1], 1),
                                 initializer='glorot_uniform', trainable=True)
        self.b = self.add_weight(name='att_bias', shape=(input_shape[1], 1),
                                 initializer='zeros', trainable=True)
        super().build(input_shape)

    def call(self, x):
        e = K.tanh(K.dot(x, self.W) + self.b)
        a = K.softmax(e, axis=1)
        return K.sum(x * a, axis=1)

    def compute_output_shape(self, input_shape):
        return (input_shape[0], input_shape[-1])

# --- Configuration ---
UC_MAP = {"uc1": 0, "uc2": 1, "uc3": 2, "uc4": 3, "uc5": 4, "uc6": 5}
APP_MAP = {'0': 0, 'amf': 1, 'gmm': 2, 'udm': 3, 'smf': 4, 'upf': 5}
LOG_MAP = {'0': 0, 'registration': 1, 'number_of_sessions_or_ues': 2,
           'nothing': 3, 'remove': 4, 'error': 5}

def create_sequences(X, y, seq_len=60):
    """
    Transformácia plochých vstupov na sekvenčné okná pre LSTM modely.
    """
    X_seq, y_seq = [], []
    for i in range(len(X) - seq_len):
        X_seq.append(X[i:i + seq_len])
        y_seq.append(y[i + seq_len])
    return np.array(X_seq), np.array(y_seq)

def evaluate_model(model, X_seq, y_seq, name):
    """
    Vyhodnotenie modelu pomocou klasifikačnej správy.
    """
    y_pred = model.predict(X_seq).argmax(axis=1)
    print(f"--- {name} ---")
    print(classification_report(y_seq, y_pred, target_names=list(UC_MAP.keys())))

def load_and_preprocess_data():
    """
    Načíta a spracuje reálne dáta + zmapuje kategórie.
    """
    data = pd.read_csv("../real_data.csv")
    data['application'] = data['application'].map(APP_MAP)
    data['log_type'] = data['log_type'].map(LOG_MAP)
    data['current_uc'] = data['current_uc'].map(UC_MAP)
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    return data

def run_evaluation_and_finetuning():
    """
    Hlavná funkcia – vyhodnotenie 4 modelov + voliteľný finetuning attention modelu.
    """
    # Load data and assets
    data = load_and_preprocess_data()
    scaler = joblib.load("scaler.joblib")

    with open('selected_features.json', 'r') as f:
        selected_features = json.load(f)['features']

    X = data[selected_features]
    y = data['current_uc']
    X_scaled = scaler.transform(X)

    X_seq, y_seq = create_sequences(X_scaled, y, seq_len=60)

    # Load models
    model_base = load_model('trained_models/lstm_base_model.h5')
    model_robust = load_model('trained_models/lstm_robust_model.h5')
    model_batchnorm = load_model('trained_models/lstm_batchnorm_model.h5')
    model_attention = load_model('trained_models/lstm_attention_model.h5',
                                 custom_objects={'AttentionLayer': AttentionLayer})

    # Compile for evaluation
    for m in [model_base, model_robust, model_batchnorm, model_attention]:
        m.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

    # Evaluate all models
    evaluate_model(model_base, X_seq, y_seq, "Base Model")
    evaluate_model(model_robust, X_seq, y_seq, "Robust Model")
    evaluate_model(model_batchnorm, X_seq, y_seq, "Batchnorm Model")
    evaluate_model(model_attention, X_seq, y_seq, "Attention Model")

    # Fine-tuning
    print("\nStarting fine-tuning of Attention Model...\n")

    X_full = data[selected_features]
    y_full = data['current_uc']
    X_scaled_full = scaler.transform(X_full)
    X_seq_full, y_seq_full = create_sequences(X_scaled_full, y_full, 60)

    X_train, X_val, y_train, y_val = train_test_split(
        X_seq_full, y_seq_full, test_size=0.8, stratify=y_seq_full, random_state=42
    )

    y_train_cat = to_categorical(y_train, num_classes=len(np.unique(y_train)))
    y_val_cat = to_categorical(y_val, num_classes=len(np.unique(y_val)))

    class_weights = compute_class_weight("balanced", classes=np.unique(y_train), y=y_train)
    class_weight_dict = dict(zip(np.unique(y_train), class_weights))

    model_attention.compile(
        optimizer=Adam(learning_rate=0.01),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    model_attention.fit(
        X_train, y_train_cat,
        validation_data=(X_val, y_val_cat),
        epochs=10,
        batch_size=128,
        class_weight=class_weight_dict,
        callbacks=[EarlyStopping(patience=50, restore_best_weights=True)],
        verbose=1,
        shuffle=True
    )

    print("\n📈 Evaluation after fine-tuning:")
    evaluate_model(model_attention, X_seq, y_seq, "Attention Model (Fine-tuned)")

if __name__ == "__main__":
    run_evaluation_and_finetuning()
