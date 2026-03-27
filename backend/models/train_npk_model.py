import pandas as pd
import numpy as np
import pickle
import os

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# -----------------------------
# Load Dataset
# -----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "../dataset/soil_dataset.csv")

data = pd.read_csv(file_path)

# -----------------------------
# Separate Features & Labels
# -----------------------------

X = data[['mean_r','mean_g','mean_b','mean_h','mean_s','mean_v']]
y = data[['N','P','K']]

# -----------------------------
# Split Data
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# Scale Features
# -----------------------------

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -----------------------------
# Apply PCA
# -----------------------------

pca = PCA(n_components=3)
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.transform(X_test_scaled)

# -----------------------------
# Train NPK Model
# -----------------------------

npk_model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

npk_model.fit(X_train_pca, y_train)

# -----------------------------
# Evaluate Model
# -----------------------------

predictions = npk_model.predict(X_test_pca)
score = r2_score(y_test, predictions)

print("Model R2 Score:", score)

# -----------------------------
# Create models folder if not exists
# -----------------------------

models_path = os.path.join(BASE_DIR, "./")

if not os.path.exists(models_path):
    os.makedirs(models_path)

# -----------------------------
# Save Models
# -----------------------------

pickle.dump(scaler, open(os.path.join(models_path, "scaler.pkl"), "wb"))
pickle.dump(pca, open(os.path.join(models_path, "pca_model.pkl"), "wb"))
pickle.dump(npk_model, open(os.path.join(models_path, "npk_model.pkl"), "wb"))

print("Models saved successfully!")
