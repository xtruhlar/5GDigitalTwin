import os
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import to_categorical


def build_robust_model():

    """
    Trains a robust LSTM model and saves it to the `trained_models/` directory.
    The model consists of 3 LSTM layers with varying dropout rates and 2 Dense layers. 
    It is designed for classifying UC classes based on preprocessed sequential inputs.

    Args
        None
        
    Returns
        None
        
    The function saves the trained model to the `trained_models/` directory and generates visualizations for the confusion matrix and training history.
    """

    BATCH_SIZE = 128
    EPOCHS = 100

    try:
        with open('class_weights.json', "r") as f:
            class_weight_dict = json.load(f)
    except FileNotFoundError:
        print("⚠️ class_weights.json nenájdený, používajú sa rovnaké váhy pre všetky triedy.")
        class_weight_dict = None

    try:
        X_train = np.load('preprocessed_data/X_train.npy')
        y_train = np.load('preprocessed_data/y_train.npy')
        X_test = np.load('preprocessed_data/X_test.npy')
        y_test = np.load('preprocessed_data/y_test.npy')
    except FileNotFoundError as e:
        print(f"❌ Chýbajúci dátový súbor: {e.filename}")
        return

    y_train_cat = to_categorical(y_train, num_classes=len(np.unique(y_train)))
    y_test_cat = to_categorical(y_test, num_classes=len(np.unique(y_train)))

    model = Sequential([
        LSTM(128, return_sequences=True, input_shape=(60, X_train.shape[2])),
        Dropout(0.1),
        LSTM(64, return_sequences=True),
        Dropout(0.1),
        LSTM(32),
        Dropout(0.1),
        Dense(32, activation='relu'),
        Dropout(0.1),
        Dense(32, activation='relu'),
        Dropout(0.15),
        Dense(len(np.unique(y_train)), activation='softmax')
    ])

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

    history = model.fit(
        X_train, y_train_cat,
        validation_data=(X_test, y_test_cat),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        verbose=1,
        class_weight=class_weight_dict,
        callbacks=[early_stop]
    )

    y_pred = model.predict(X_test).argmax(axis=1)
    y_true = y_test

    plt.figure(figsize=(8, 6))
    sns.heatmap(confusion_matrix(y_true, y_pred), annot=True, fmt='d', cmap='Blues')
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.tight_layout()
    plt.show()

    print(classification_report(y_true, y_pred, digits=3))

    plt.figure(figsize=(8, 4))
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.title("Training vs Validation Accuracy")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    os.makedirs('trained_models', exist_ok=True)
    model.save('trained_models/lstm_robust_model.h5')
    model.save('trained_models/lstm_robust_model.keras')
    print("✅ Model uložený.")


if __name__ == "__main__":
    build_robust_model()
