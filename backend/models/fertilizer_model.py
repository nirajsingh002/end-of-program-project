import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
data = pd.read_csv("../dataset/fertilizer.csv")

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
with open("models/fertilizer_model.pkl", "wb") as f:
    pickle.dump(model, f)

# Save feature columns for prediction
with open("models/fertilizer_columns.pkl", "wb") as f:
    pickle.dump(X.columns, f)

print("Model trained and saved successfully.")
