import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# ===============================
# 1. Load CSV
# ===============================
csv_file = "meu_dataset.csv"   # 🔧 change to your file path
target_col = "target"          # 🔧 change to your dependent variable

df = pd.read_csv(csv_file)

# Separate X and y
X_raw = df.drop(columns=[target_col]).values
y = df[target_col].values
n_features_orig = X_raw.shape[1]

# ===============================
# 2. Create sliding windows
# ===============================
def create_sliding_windows(X, y, window_size=3):
    """
    Create dataset with sliding windows.
    X: (n_samples, n_features_orig)
    y: target vector
    window_size: size of window
    """
    n_samples, n_features = X.shape
    X_windows, y_windows = [], []

    for i in range(window_size, n_samples):
        X_window = X[i - window_size:i].flatte_]()_
