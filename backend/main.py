from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import tensorflow as tf
import joblib
from fastapi.middleware.cors import CORSMiddleware
from ai.transformer import generate_explanation
from services.fertilizer import recommend_fertilizer

app = FastAPI()

# Allow React frontend
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and preprocessors
model = tf.keras.models.load_model("crop_model.h5")
scaler = joblib.load("scaler.save")
encoder = joblib.load("label_encoder.save")

# Define input schema
class SoilInput(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float

@app.post("/predict")
def predict_crop(data: SoilInput):
    features = np.array([[ 
        data.N,
        data.P,
        data.K,
        data.temperature,
        data.humidity,
        data.ph,
        data.rainfall
    ]])

    # Scale input
    scaled_features = scaler.transform(features)

    # Predict
    prediction = model.predict(scaled_features)
    predicted_index = np.argmax(prediction)
    crop_name = encoder.inverse_transform([predicted_index])[0]
    explanation = generate_explanation(crop_name, data)
    fertilizer = recommend_fertilizer(data)

    confidence = float(np.max(prediction)) * 100

    return {
        "crop": crop_name,
        "explanation": explanation,
        "fertilizer": fertilizer,
        "confidence": confidence,
    }
