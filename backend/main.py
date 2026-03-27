from fastapi import FastAPI, Request, UploadFile, File
from pydantic import BaseModel
import numpy as np
import tensorflow as tf
import joblib
from fastapi.middleware.cors import CORSMiddleware
from ai.transformer import generate_explanation
from services.fertilizer import recommend_fertilizer
import gettext
import os
import shutil
import pickle
from utils.image_features import extract_features

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

# Load models
pca = pickle.load(open("models/pca_model.pkl", "rb"))
npk_model = pickle.load(open("models/npk_model.pkl", "rb"))
scaler_npk = pickle.load(open("models/scaler.pkl", "rb"))
# crop_model = pickle.load(open("models/crop_model.pkl", "rb"))

# -------------------------------
# API 1: Upload Image & Get NPK
# -------------------------------
@app.post("/get-npk")
async def upload_image(image: UploadFile = File(...)):

    file_path = f"uploads/{image.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    features = extract_features(file_path)
    features = np.array(features).reshape(1, -1)
    features_scaled = scaler_npk.transform(features)
    features_pca = pca.transform(features_scaled)

    npk = npk_model.predict(features_pca)

    return {
        "Nitrogen": float(npk[0][0]),
        "Phosphorus": float(npk[0][1]),
        "Potassium": float(npk[0][2])
    }

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
    fertilizer = recommend_fertilizer(data, crop_name)

    confidence = float(np.max(prediction)) * 100

    return {
        "crop": crop_name,
        "explanation": explanation,
        "fertilizer": fertilizer,
        "confidence": confidence,
        "ph": data.ph,
        "rainfall": data.rainfall,
        "temperature": data.temperature
    }

# locales testing
def get_translator(lang: str):
    localedir = os.path.join(os.path.dirname(__file__), "translations")
    return gettext.translation(
        "messages",
        localedir=localedir,
        languages=[lang],
        fallback=True
    )

@app.middleware("http")
async def add_language_to_request(request: Request, call_next):
    lang = request.headers.get("Accept-Language", "en")
    request.state.lang = lang.split(",")[0]
    response = await call_next(request)
    return response

@app.get("/hello")
async def hello(request: Request):
    translator = get_translator(request.state.lang)
    _ = translator.gettext

    return {
        "message": _("Welcome to our application")
    }