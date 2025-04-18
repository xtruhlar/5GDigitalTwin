import pandas as pd
import numpy as np
from collections import deque
from joblib import load
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model # type: ignore
import json

# Globálne premenné
SEQUENCE_LENGTH = 60  # počet sekúnd pre LSTM model (input)
SCALER_PATH = "scaler.joblib"
MODEL_PATH = "lstm_model.h5"
FEATURES_PATH = "features.json"

# Načítanie scaleru a modelu
scaler = load(SCALER_PATH)
model = load_model(MODEL_PATH)

# Načítanie vybraných feature-ov
with open(FEATURES_PATH, "r") as f:
    SELECTED_FEATURES = json.load(f)

# Definovanie mapovania pre aplikácie, logy a use cases
APP_MAP = {'0': 0, 'amf': 1, 'gmm': 2, 'udm': 3, 'smf': 4, 'upf': 5}
LOG_MAP = {'0': 0, 'registration': 1, 'number_of_sessions_or_ues': 2, 'nothing': 3, 'remove': 4, 'error': 5}
UC_MAP = {'uc1': 1, 'uc2': 2, 'uc3': 3, 'uc4': 4, 'uc5': 5, 'uc6': 6}

# Inicializácia sliding window buffer
buffer = deque(maxlen=SEQUENCE_LENGTH)

def preprocess_row(df_row: pd.DataFrame):
    df_row = df_row.copy()

    df_row.fillna(df_row.mode().iloc[0], inplace=True)

    if 'timestamp' in df_row.columns:
        df_row['timestamp'] = pd.to_datetime(df_row['timestamp'])

    if 'application' in df_row.columns:
        df_row['application'] = df_row['application'].map(APP_MAP)
    if 'log_type' in df_row.columns:
        df_row['log_type'] = df_row['log_type'].map(LOG_MAP)

    X = df_row[SELECTED_FEATURES]
    X_scaled = scaler.transform(X)
    return X_scaled

def update_buffer(new_scaled_row):
    buffer.append(new_scaled_row.flatten())
    if len(buffer) == SEQUENCE_LENGTH:
        return np.expand_dims(np.array(buffer), axis=0)
    return None

def predict_uc(new_row_df: pd.DataFrame):
    X_scaled = preprocess_row(new_row_df)
    window = update_buffer(X_scaled)
    if window is not None:
        prediction = model.predict(window)
        uc_pred = prediction.argmax(axis=1)[0]
        return f"uc{uc_pred}"
    return None

# Príklad použitia
if __name__ == "__main__":
    #  Načítanie nového riadku z CSV súboru
    df_new = pd.read_csv("sample_input.csv").tail(10)
    for index, row in df_new.iterrows():
        uc = predict_uc(row.to_frame().T)
        if uc:
            print(f"Predikovaný use case: {uc}")
        else:
            print("Čakám na naplnenie sliding window...")