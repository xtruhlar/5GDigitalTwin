"""
LSTM model with custom attention mechanism for multi-class classification
of time-series data in the context of 5G network behavior prediction.

This module defines a deep learning model using TensorFlow and Keras,
integrates a custom attention mechanism, and trains the model
on preprocessed input data with categorical labels.

Expected data format:
- Input: X_train.npy, X_test.npy (shape: [samples, 60, features])
- Labels: y_train.npy, y_test.npy (categorical class indices)
- Class weights: class_weights.json

The trained model is saved as HDF5 and Keras formats.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.layers import Layer, Input, LSTM, Dropout, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import backend as K

# Global variables
BATCH_SIZE = 128
EPOCHS = 100


def train_attention_model():
    with open('class_weights.json', "r") as f:
        class_weight_dict = json.load(f)

    X_train = np.load('preprocessed_data/X_train.npy')
    y_train = np.load('preprocessed_data/y_train.npy')
    X_test = np.load('preprocessed_data/X_test.npy')
    y_test = np.load('preprocessed_data/y_test.npy')

    # Convert labels to categorical
    y_train_cat = to_categorical(y_train, num_classes=len(np.unique(y_train)))
    y_test_cat = to_categorical(y_test, num_classes=len(np.unique(y_train)))

    class AttentionLayer(Layer):
        """
        Custom attention layer compatible with LSTM outputs.
        Outputs a weighted sum across the time dimension.
        """
        def __init__(self, **kwargs):
            super(AttentionLayer, self).__init__(**kwargs)

        def build(self, input_shape):
            self.W = self.add_weight(name='att_weight', shape=(input_shape[-1], 1),
                                    initializer='glorot_uniform', trainable=True)
            self.b = self.add_weight(name='att_bias', shape=(input_shape[1], 1),
                                    initializer='zeros', trainable=True)
            super(AttentionLayer, self).build(input_shape)

        def call(self, x):
            e = K.tanh(K.dot(x, self.W) + self.b)
            a = K.softmax(e, axis=1)
            output = x * a
            return K.sum(output, axis=1)

        def compute_output_shape(self, input_shape):
            return (input_shape[0], input_shape[-1])

    def build_attention_model(input_shape, num_classes):
        """
        Build and return an attention-based LSTM model.

        Parameters:
        - input_shape: tuple, shape of the input data (timesteps, features)
        - num_classes: int, number of output classes

        Returns:
        - Keras Model instance
        """
        inputs = Input(shape=input_shape)
        x = LSTM(64, return_sequences=True)(inputs)
        x = Dropout(0.3)(x)
        x = LSTM(32, return_sequences=True)(x)
        x = Dropout(0.3)(x)
        x = AttentionLayer()(x)
        x = Dense(64, activation='relu')(x)
        x = Dropout(0.3)(x)
        outputs = Dense(num_classes, activation='softmax')(x)
        model = Model(inputs=inputs, outputs=outputs)
        return model

    # Build model
    model = build_attention_model(input_shape=(60, X_train.shape[2]), num_classes=len(np.unique(y_train)))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Train model
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

    # Evaluation
    y_pred = model.predict(X_test).argmax(axis=1)
    y_true = y_test

    # Confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(confusion_matrix(y_true, y_pred), annot=True, fmt='d', cmap='Blues')
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.show()

    # Classification report
    print(classification_report(y_true, y_pred, digits=3))

    # Training history
    plt.plot(history.history['accuracy'], label='train acc')
    plt.plot(history.history['val_accuracy'], label='val acc')
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.title("Training vs Validation Accuracy")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Save model
    model.save('trained_models/lstm_attention_model.h5')
    model.save('trained_models/lstm_attention_model.keras')


if __name__ == "__main__":
    train_attention_model()