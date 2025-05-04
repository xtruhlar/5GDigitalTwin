import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import to_categorical

# Global training config
BATCH_SIZE = 128
EPOCHS = 100

def train_batchnorm_model():

    """
    LSTM BatchNorm Model

    This module defines a deep learning model using TensorFlow and Keras with Batch Normalization
    for multi-class classification of time-series data.

    Expected data format:
        - Input: X_train.npy, X_test.npy (shape: [samples, 60, features])
        - Labels: y_train.npy, y_test.npy (categorical class indices)
        - Class weights: class_weights.json

    The trained model is saved as HDF5 and Keras formats.
    """

    # Load class weights
    with open('class_weights.json', "r") as f:
        class_weight_dict = json.load(f)

    # Load data
    X_train = np.load('preprocessed_data/X_train.npy')
    y_train = np.load('preprocessed_data/y_train.npy')
    X_test = np.load('preprocessed_data/X_test.npy')
    y_test = np.load('preprocessed_data/y_test.npy')

    # Convert labels to categorical
    y_train_cat = to_categorical(y_train, num_classes=len(np.unique(y_train)))
    y_test_cat = to_categorical(y_test, num_classes=len(np.unique(y_train)))

    # Build model
    model = Sequential()
    model.add(LSTM(128, return_sequences=True, input_shape=(60, X_train.shape[2])))
    model.add(BatchNormalization())
    model.add(Dropout(0.1))
    model.add(LSTM(64))
    model.add(BatchNormalization())
    model.add(Dropout(0.1))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.05))
    model.add(Dense(len(np.unique(y_train)), activation='softmax'))

    # Compile model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Early stopping
    early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

    # Train
    history = model.fit(
        X_train, y_train_cat,
        validation_data=(X_test, y_test_cat),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        verbose=1,
        class_weight=class_weight_dict,
        callbacks=[early_stop]
    )

    # Predict
    y_pred = model.predict(X_test).argmax(axis=1)

    # Confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues')
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.show()

    # Classification report
    print(classification_report(y_test, y_pred, digits=3))

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
    model.save('trained_models/lstm_batchnorm_model.h5')
    model.save('trained_models/lstm_batchnorm_model.keras')


if __name__ == "__main__":
    train_batchnorm_model()