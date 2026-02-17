import React, { useState } from "react";
import axios from "axios";

function CropPrediction() {
  const [result, setResult] = useState(null);

  const hardcodedSoilData = {
    N: 90,
    P: 42,
    K: 43,
    temperature: 25,
    humidity: 80,
    ph: 6.5,
    rainfall: 200
  };

  const predictCrop = async () => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/predict",
        hardcodedSoilData
      );

      setResult(response.data);
    } catch (error) {
      console.error("Prediction error:", error);
    }
  };

  return (
    <div>
      <h2>Crop Recommendation System</h2>
      <button onClick={predictCrop}>Predict Crop</button>

      {result && (
        <div>
          <p>Confidence: {result.confidence}%</p>
          <h3>Recommended Crop: {result.crop}</h3>
          <p>Explanation: {result.explanation}</p>
          <p>Fertilizer: {result.fertilizer}</p>

        </div>
      )}
    </div>
  );
}

export default CropPrediction;
