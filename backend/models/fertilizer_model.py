import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
fertilizer_model_path = os.path.join(BASE_DIR, "fertilizer_model.pkl")
fertilizer_columns_path = os.path.join(BASE_DIR, "fertilizer_columns.pkl")


# Load dataset
data = pd.read_csv("../dataset/fertilizer.csv", encoding='latin1')

# Separate target
y = data["Fertilizer Name"]

# Drop target column
X = data.drop("Fertilizer Name", axis=1)

# Convert categorical columns to numeric
X = pd.get_dummies(X)

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Save model
with open(fertilizer_model_path, "wb") as f:
    pickle.dump(model, f)
# Save feature columns for prediction
with open(fertilizer_columns_path, "wb") as f:
    pickle.dump(X.columns, f)

print("Model trained and saved successfully.")
