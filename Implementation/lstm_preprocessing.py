"""
Module for preparing LSTM input data from preprocessed features.
Includes functionality for loading feature arrays, creating sequences, 
splitting the dataset, and saving the output for training and testing.

This module is intended for use with the Digital Twin of 5G Network project.
"""

import json
import warnings
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
import os

# Potlačenie warningov
warnings.filterwarnings("ignore")

# Globálne konfiguračné premenné
X_PATH = 'X_scaled.npy'
Y_PATH = 'y_labels.npy'
SCALER_PATH = 'scaler.joblib'
FEATURES_PATH = 'selected_features.json'
UC_MAP_PATH = 'uc_map.json'
LABEL_COLUMN = 'current_uc'

# Parametre pre trénovanie a model
TEST_SIZE = 0.2
SEED = 42
SEQUENCE_LENGTH = 60
LSTM_UNITS = 128
DROPOUT_RATE = 0.2
VERBOSE = 1


def load_data(X_path, Y_path, scaler_path, features_path, uc_map_path):

    """
    Loads the preprocessed data from specified paths.

    Args
        - X_path (str): Path to the input features (X)
        - Y_path (str): Path to the target labels (y)
        - scaler_path (str): Path to the scaler object
        - features_path (str): Path to the selected features JSON file
        - uc_map_path (str): Path to the UC map JSON file

    Returns
        - tuple: (X, y, scaler, selected_features, uc_map)
    """
    
    X = np.load(X_path)
    y = np.load(Y_path)
    scaler = joblib.load(scaler_path)

    with open(features_path, 'r') as f:
        features = json.load(f)['features']

    with open(uc_map_path, "r") as f:
        uc_map = json.load(f)

    return X, y, scaler, features, uc_map


def create_sequences(X, y, seq_len):

    """
    Creates sequences of input data for LSTM using a sliding window.

    Parameters:
        X (np.ndarray): Input data (features)
        y (np.ndarray): Target values (classes)
        seq_len (int): Length of the sequence for LSTM

    Returns:
        tuple: (X_seq, y_seq) as ndarray
    """

    Xs, ys = [], []
    for i in range(len(X) - seq_len):
        Xs.append(X[i:i+seq_len])
        ys.append(y[i+seq_len])
    return np.array(Xs), np.array(ys)


def split_and_save_data(X_seq, y_seq, output_dir="preprocessed_data"):

    """
    Splits the dataset into training and testing sets and saves them to disk.

    Args
        - X_seq (np.ndarray): Input features in sequence format
        - y_seq (np.ndarray): Target labels in sequence format
        - output_dir (str): Directory to save the split data

    Returns
        None
    """

    X_train, X_test, y_train, y_test = train_test_split(
        X_seq, y_seq, test_size=TEST_SIZE, random_state=SEED, stratify=y_seq
    )

    os.makedirs(output_dir, exist_ok=True)

    np.save(os.path.join(output_dir, "X_train.npy"), X_train)
    np.save(os.path.join(output_dir, "y_train.npy"), y_train)
    np.save(os.path.join(output_dir, "X_test.npy"), X_test)
    np.save(os.path.join(output_dir, "y_test.npy"), y_test)

    print(f"✅ X_train: {X_train.shape}, y_train: {y_train.shape}")
    print(f"✅ X_test: {X_test.shape}, y_test: {y_test.shape}")


if __name__ == "__main__":
    X, y, scaler, features, uc_map = load_data(
        X_PATH, Y_PATH, SCALER_PATH, FEATURES_PATH, UC_MAP_PATH
    )
    X_seq, y_seq = create_sequences(X, y, SEQUENCE_LENGTH)
    split_and_save_data(X_seq, y_seq)
