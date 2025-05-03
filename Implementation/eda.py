"""
EDA module for exploratory analysis of synthetic and real 5G network datasets.

This module contains functions to load data, preprocess it, visualize it,
and perform feature selection using multiple strategies including RF, RFE,
RFECV, SFS and permutation importance.

Functions in this module should be called explicitly from a main script or notebook.
"""

import json
import math
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFE, RFECV, SequentialFeatureSelector
from sklearn.inspection import permutation_importance
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.utils.class_weight import compute_class_weight

warnings.filterwarnings("ignore")

def load_dataset(path: str) -> pd.DataFrame:

    """
    Load dataset from CSV file.
    
    Args
        - path (str): Path to the CSV file.

    Returns
        - pd.DataFrame: Loaded dataset.
    """

    return pd.read_csv(path)

def load_maps(log_map_path='log_map.json', app_map_path='app_map.json', uc_map_path='uc_map.json'):

    """
    Load mapping dictionaries from JSON files.

    Args
        - log_map_path (str): Path to the log type mapping JSON file.
        - app_map_path (str): Path to the application mapping JSON file.
        - uc_map_path (str): Path to the use case mapping JSON file.

    Returns
        - tuple: A tuple containing three dictionaries:
            - log_map (dict): Mapping of log types to integers.
            - app_map (dict): Mapping of applications to integers.
            - uc_map (dict): Mapping of use cases to integers.
    
    """
    with open(log_map_path, 'r') as f:
        log_map = json.load(f)
    with open(app_map_path, 'r') as f:
        app_map = json.load(f)
    with open(uc_map_path, 'r') as f:
        uc_map = json.load(f)
    return log_map, app_map, uc_map

def preprocess_data(df: pd.DataFrame, log_map: dict, app_map: dict, uc_map: dict):

    """
    Preprocess dataset: fill NA, map strings to ints, scale numeric columns.
    
    Args
        - df (pd.DataFrame): Input DataFrame to preprocess.
        - log_map (dict): Mapping of log types to integers.
        - app_map (dict): Mapping of applications to integers.
        - uc_map (dict): Mapping of use cases to integers.

    Returns
        - tuple: A tuple containing:
            - X_scaled (np.ndarray): Scaled feature matrix.
            - X (pd.DataFrame): Original feature matrix.
            - y (pd.Series): Target variable.

    """
    df = df.copy()
    df.fillna(df.mode().iloc[0], inplace=True)
    df['application'] = df['application'].map(app_map)
    df['log_type'] = df['log_type'].map(log_map)
    df['current_uc'] = df['current_uc'].map(uc_map)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    X = df.drop(columns=['timestamp', 'current_uc'], errors='ignore')
    X = X.select_dtypes(include=[np.number])
    y = df['current_uc'].astype(int)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, X, y

def compute_class_weights(y):

    """
    Compute class weights for imbalanced classes.
    
    Args
        - y (pd.Series): Target variable.

    Returns
        - dict: Dictionary mapping class labels to their corresponding weights.
    """

    classes = np.unique(y)
    weights = compute_class_weight(class_weight='balanced', classes=classes, y=y)
    return dict(zip(classes, weights))

def random_forest_importance(X_scaled, X, y):

    """
    Train Random Forest and return feature importances.
    
    Args
        - X_scaled (np.ndarray): Scaled feature matrix.
        - X (pd.DataFrame): Original feature matrix.
        - y (pd.Series): Target variable.

    Returns
        - pd.Series: Feature importances sorted in descending order.
        - RandomForestClassifier: Trained Random Forest model.
    """

    rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_scaled, y)
    rf_importances = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
    return rf_importances, rf

def rfe_selection(X_scaled, y, X, rf):

    """
    Recursive Feature Elimination.
    
    Args
        - X_scaled (np.ndarray): Scaled feature matrix.
        - y (pd.Series): Target variable.
        - X (pd.DataFrame): Original feature matrix.
        - rf (RandomForestClassifier): Trained Random Forest model.

    Returns
        - pd.Series: Boolean mask indicating selected features.
    """

    rfe = RFE(estimator=rf, n_features_to_select=10)
    rfe.fit(X_scaled, y)
    return pd.Series(rfe.support_, index=X.columns)

def rfecv_selection(X_scaled, y, X, rf):

    """
    RFECV - RFE with cross-validation.
    
    Args
        - X_scaled (np.ndarray): Scaled feature matrix.
        - y (pd.Series): Target variable.
        - X (pd.DataFrame): Original feature matrix.
        - rf (RandomForestClassifier): Trained Random Forest model.

    Returns
        - pd.Series: Boolean mask indicating selected features.
    """

    rfecv = RFECV(estimator=rf, step=1, cv=StratifiedKFold(5), scoring='f1_weighted', n_jobs=-1)
    rfecv.fit(X_scaled, y)
    return pd.Series(rfecv.support_, index=X.columns)

def sfs_selection(X_scaled, y, X, rf):

    """
    Sequential Feature Selector.
    
    Args
        - X_scaled (np.ndarray): Scaled feature matrix.
        - y (pd.Series): Target variable.
        - X (pd.DataFrame): Original feature matrix.
        - rf (RandomForestClassifier): Trained Random Forest model.

    Returns
        - pd.Series: Boolean mask indicating selected features.
    """

    sfs = SequentialFeatureSelector(rf, n_features_to_select=10, direction='forward',
                                     scoring='f1_weighted', cv=5, n_jobs=-1)
    sfs.fit(X_scaled, y)
    return pd.Series(sfs.get_support(), index=X.columns)

def permutation_importance_stable(X, y, selected_features, n_runs=10):

    """
    Calculate stable permutation importances over multiple runs.

    Args
        - X (pd.DataFrame): Feature matrix.
        - y (pd.Series): Target variable.
        - selected_features (list): List of selected feature names.
        - n_runs (int): Number of runs for stability.

    Returns
        - pd.DataFrame: DataFrame containing mean and std of importances.
    """

    X_scaled = StandardScaler().fit_transform(X)
    importances = []

    for i in range(n_runs):
        model = RandomForestClassifier(n_estimators=100, random_state=i)
        model.fit(X_scaled, y)
        result = permutation_importance(model, X_scaled, y, n_repeats=5, random_state=i)
        importances.append(result.importances_mean)

    importances = np.array(importances)
    mean_importance = np.mean(importances, axis=0)
    std_importance = np.std(importances, axis=0)

    return pd.DataFrame({
        'Feature': selected_features,
        'Mean_Importance': mean_importance,
        'Std_Importance': std_importance
    }).sort_values(by='Mean_Importance', ascending=False)
