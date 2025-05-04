import json
import warnings
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import to_categorical

warnings.filterwarnings("ignore")

BATCH_SIZE = 128
EPOCHS = 100


def build_base_model(X_train, y_train, X_test, y_test, class_weight_dict):
    
    """
    LSTM Base Model for classification of network use case scenarios.

    This script loads preprocessed training and testing data, defines and trains
    a baseline LSTM model, evaluates its performance, and saves the final model
    in HDF5 and Keras formats. Class balancing is handled using precomputed class weights.

    Usage
        - This script is designed to be executed as a module. Use the function `build_base_model()` to construct and optionally train the model.

    Args
        - X_train (numpy.ndarray): Preprocessed training data.
        - y_train (numpy.ndarray): Labels for the training data.
        - X_test (numpy.ndarray): Preprocessed testing data.
        - y_test (numpy.ndarray): Labels for the testing data.
        - class_weight_dict (dict): Class weights for handling class imbalance.

    Returns
        - model (tensorflow.keras.Model): Trained LSTM model.
    """

    # Transform labels to categorical
    y_train_cat = to_categorical(y_train, num_classes=len(np.unique(y_train)))
    y_test_cat = to_categorical(y_test, num_classes=len(np.unique(y_train)))

    # Define model
    model = Sequential()
    model.add(LSTM(64, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dropout(0.3))
    model.add(LSTM(32))
    model.add(Dropout(0.2))
    model.add(Dense(len(np.unique(y_train)), activation='softmax'))

    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Early stopping
    early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

    # Train model
    history = model.fit(
        X_train, y_train_cat,
        validation_data=(X_test, y_test_cat),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        verbose=1,
        class_weight=class_weight_dict,
        callbacks=[early_stop]
    )

    # Evaluate
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

    # Accuracy plot
    plt.plot(history.history['accuracy'], label='train acc')
    plt.plot(history.history['val_accuracy'], label='val acc')
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.title("Training vs Validation Accuracy")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Save model
    model.save('trained_models/lstm_base_model.h5')
    model.save('trained_models/lstm_base_model.keras')

    return model

if __name__ == "__main__":
    # Load class weights
    with open('class_weights.json', "r") as f:
        class_weight_dict = json.load(f)

    # Load preprocessed data
    X_train = np.load('preprocessed_data/X_train.npy')
    y_train = np.load('preprocessed_data/y_train.npy')
    X_test = np.load('preprocessed_data/X_test.npy')
    y_test = np.load('preprocessed_data/y_test.npy')

    # Build and train the model
    build_base_model(X_train, y_train, X_test, y_test, class_weight_dict)