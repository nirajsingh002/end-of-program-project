import React, { useContext, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import axios from "axios";
import { AppContext } from "../store/context";
import "./common.css";

function CropPrediction() {
  const [result, setResult] = useState();
  const [loading, setLoading] = useState(false);
  const { state, dispatch } = useContext(AppContext);
  const { t } = useTranslation();

  useEffect(() => {
    console.log("result", result);
  }, [result]);

  const soilData = {
    N: state.soilData.Nitrogen,
    P: state.soilData.Phosphorus,
    K: state.soilData.Potassium,
    temperature: 25,
    humidity: 80,
    ph: 6.5,
    rainfall: 200,
  };

  const predictCrop = async () => {
    try {
      setLoading(true);
      const response = await axios.post(
        "http://127.0.0.1:8000/predict",
        soilData,
      );

      setResult(response.data);
    } catch (error) {
      console.error("Prediction error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        marginTop: "40px",
        padding: "20px",
        maxWidth: "900px",
        marginLeft: "auto",
        marginRight: "auto",
      }}
    >
      <h2 style={{ textAlign: "center" }}>🌾 Crop Recommendation</h2>

      <div style={{ textAlign: "center", marginBottom: "20px" }}>
        <button
          onClick={predictCrop}
          disabled={!Boolean(state?.soilData?.isGetNPK)}
          className="btn"
        >
          Predict Crop
        </button>
      </div>
      {loading ? "Processing..." : ""}
      {result?.crop && (
        <div
          style={{
            background: "#ffffff",
            padding: "25px",
            borderRadius: "12px",
            boxShadow: "0 4px 15px rgba(0,0,0,0.1)",
          }}
        >
          <h2 style={{ color: "#2E7D32" }}>🌱 {t(`crops.${result.crop}`)}</h2>

          <p style={{ marginTop: "10px", lineHeight: "1.6" }}>
            {t("crop_explanation", {
              crop: t(`crops.${result.crop}`),
              temperature: 25,
              ph: 6.5,
              rainfall: 200,
            })}
          </p>

          <div
            style={{
              marginTop: "20px",
              display: "flex",
              justifyContent: "space-between",
            }}
          >
            <div>
              <strong>Fertilizer:</strong>
              <p>{result.fertilizer}</p>
            </div>

            <div>
              <strong>Confidence:</strong>
              <p>{result.confidence?.toFixed(2)}%</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default CropPrediction;
