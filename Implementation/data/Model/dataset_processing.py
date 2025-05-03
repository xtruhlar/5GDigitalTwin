# %% [markdown]
# # Predspracovanie dát

# %%
import json

import numpy as np
import pandas as pd
from joblib import dump
from sklearn.preprocessing import StandardScaler

# %% [markdown]
# Vybrané metriky z EDA:

# %%
# 📄 Load selected features from JSON file
SELECTED_FEATURES_JSON = 'selected_features.json'
with open(SELECTED_FEATURES_JSON, 'r') as f:
    SELECTED_FEATURES = json.load(f)['features']

# %% [markdown]
# <div class="alert alert-block alert-warning">  
# <b>Upozornenie:</b> Ak by sa v priebehu bežania digitálneho dvojčaťa menili dôležité metriky, týmto spôsobom ich neodchytíme.  
# </div>

# %% [markdown]
# Mapovanie katégorických premenných na číselné hodnoty:

# %%
# 📄 Load mapping dictionaries for log_type, application, and current_uc
with open('log_map.json', 'r') as f:
    LOG_MAP = json.load(f)

with open('app_map.json', 'r') as f:
    APP_MAP = json.load(f)

with open('uc_map.json', 'r') as f:
    UC_MAP = json.load(f)

# %%
def preprocess_df(df: pd.DataFrame, scaler=None, fit_scaler=False):

    """
    Preprocess the input DataFrame by handling missing values, mapping categorical fields,
    selecting important features, and normalizing them.
    """
    
    df = df.copy()

    # Handle missing values
    df.fillna(df.mode().iloc[0], inplace=True)

    # Parse timestamps if available
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Mapping for application, log_type, and current_uc
    if 'application' in df.columns:
        df['application'] = df['application'].map(APP_MAP)

    if 'log_type' in df.columns:
        df['log_type'] = df['log_type'].map(LOG_MAP)

    if 'current_uc' in df.columns:
        df['current_uc'] = df['current_uc'].map(UC_MAP)

    # Remove rows with missing values in selected features
    df.dropna(subset=SELECTED_FEATURES, inplace=True)
    df.dropna(subset=SELECTED_FEATURES, inplace=True)

    # Select only the important features
    X = df[SELECTED_FEATURES]

    # Normalization
    if scaler is None:
        scaler = StandardScaler()

    if fit_scaler:
        X_scaled = scaler.fit_transform(X)
    else:
        X_scaled = scaler.transform(X)

    return X_scaled, df.get('current_uc'), scaler


# %% [markdown]
# <div class="alert alert-block alert-info">  
# <b>Predspracovanie dát:</b> Dáta predspracujeme tak, ako sme to robili v súbore EDA. 
# </div>

# %%
# 🧪 Example usage:
df = pd.read_csv("../synthetic_data.csv")
X_scaled, y_scaled, fitted_scaler = preprocess_df(df, fit_scaler=True)

# 📁 Save preprocessed data
np.save("X_scaled.npy", X_scaled)
np.save("y_labels.npy", y_scaled)

# 📁 Save the fitted scaler for later real-time inference use
dump(fitted_scaler, 'scaler.joblib')

# %% [markdown]
# <div class="alert alert-block alert-success">  
# <b>'scaler.joblib':</b> Uložíme aj scaler, aby sme mohli normalizovať dáta pred ich nahratím do digitálneho dvojčaťa.
# </div>


