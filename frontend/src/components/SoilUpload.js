import React, { useContext, useEffect, useState } from "react";
import { AppContext } from "../store/context";

function SoilUpload() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [preview, setPreview] = useState(null);
  const { state, dispatch } = useContext(AppContext);

  useEffect(() => {
    console.log("state", state);
  }, [state]);

  useEffect(() => {
    return () => {
      if (preview) {
        URL.revokeObjectURL(preview);
      }
    };
  }, [preview]);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    if (file) {
      const imageUrl = URL.createObjectURL(file);
      setPreview(imageUrl);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select an image first.");
      return;
    }

    const formData = new FormData();
    formData.append("image", selectedFile);

    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/get-npk", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      dispatch({
        type: "SET_SOIL_DATA",
        payload: {
          Nitrogen: data.Nitrogen,
          Phosphorus: data.Phosphorus,
          Potassium: data.Potassium,
          isGetNPK: true,
        },
      });
    } catch (error) {
      console.error("Error:", error);
      alert("Error uploading image");
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "30px", maxWidth: "1100px", margin: "auto" }}>
      <h2 style={{ textAlign: "center", marginBottom: "20px" }}>
        Upload Soil Image
      </h2>

      <div
        style={{
          display: "flex",
          gap: "30px",
          alignItems: "stretch",
        }}
      >
        {/* LEFT CARD */}
        <div
          style={{
            flex: 1,
            padding: "20px",
            borderRadius: "12px",
            background: "#ffffff",
            boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
          }}
        >
          <input type="file" accept="image/*" onChange={handleFileChange} />

          <br />
          <br />

          <button
            onClick={handleUpload}
            disabled={loading}
            style={{
              padding: "10px 20px",
              backgroundColor: "#4CAF50",
              color: "#fff",
              border: "none",
              borderRadius: "6px",
              cursor: "pointer",
            }}
          >
            {loading ? "Processing..." : "Get NPK Values"}
          </button>

          {preview && (
            <div style={{ marginTop: "20px" }}>
              <img
                src={preview}
                alt="Soil"
                style={{
                  width: "100%",
                  borderRadius: "10px",
                  marginTop: "10px",
                }}
              />
            </div>
          )}
        </div>

        {/* RIGHT CARD */}
        <div
          style={{
            flex: 1,
            padding: "20px",
            borderRadius: "12px",
            background: "#f8fafc",
            boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
          }}
        >
          <h3>NPK Analysis</h3>

          {!state.soilData && <p>No data available</p>}

          {state.soilData && (
            <div style={{ marginTop: "10px" }}>
              <p>
                🧪 Nitrogen: <strong>{state.soilData.Nitrogen}</strong>
              </p>
              <p>
                🧪 Phosphorus: <strong>{state.soilData.Phosphorus}</strong>
              </p>
              <p>
                🧪 Potassium: <strong>{state.soilData.Potassium}</strong>
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default SoilUpload;
