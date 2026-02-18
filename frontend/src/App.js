import './App.css';
import { useTranslation } from "react-i18next";
import CropPrediction from './components/CropPrediction';
import axios from 'axios';
import { useEffect, useState } from 'react';

function App() {
  const { t, i18n } = useTranslation();
  const [welComeMsg, setWelComeMsg] = useState('');
console.log("Current Language:", i18n.language);
  useEffect(() => {
    // getWelComeMsg();
  }, []);

  const getWelComeMsg = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/hello",{
        headers: {
          "Accept-Language": i18n.language
        }
      }
      );

      setWelComeMsg(response.data.message);
    } catch (error) {
      console.error("Prediction error:", error);
    }
  };
  const toggleLanguage = () => {
    const newLang = i18n.language === "en" ? "hi" : "en";
    i18n.changeLanguage(newLang);
    // getWelComeMsg();
  };
  

  return (
    <div className="App">
      <h1>{t(welComeMsg)}</h1>
      <button onClick={toggleLanguage}>
        {i18n.language === "en" ? "Switch to Hindi" : "Switch to English"}
      </button>
      <p>Current Language: {i18n.language}</p>
      <CropPrediction />
    </div>
  );
}

export default App;
