import React, { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import axios from "axios";

function CropPrediction() {
  const [result, setResult] = useState({
  crop: "rice",
  confidence: 92.5,
  temperature: 25,
  ph: 6.5,
  rainfall: 200
});
  const { t } = useTranslation();

  useEffect(() => {
    console.log('result', result);
  }, [result]);

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
    <div role="alert">
      <h2>Crop Recommendation System</h2>
      <button onClick={predictCrop}>Predict Crop</button>

      {result && (
        <>
        <h2>{t(`crops.${result.crop}`)}</h2>

      <p>
          {t("crop_explanation", {
          crop: t(`crops.${result.crop}`),
          temperature: 25,
          ph: 6.5,
          rainfall: 200
        })}
      </p>
      <p>Fertilizer: {result.fertilizer}</p>
      <p>Confidence: {result.confidence.toFixed(2)}%</p>
      </>
        // <div>
        //   <p>Confidence: {result.confidence}%</p>
        //   <h3>Recommended Crop: {result.crop}</h3>
        //   <p>Explanation: {result.explanation}</p>
        //   <p>Fertilizer: {result.fertilizer}</p>

        // </div>
      )}
    </div>
  );
}

export default CropPrediction;
