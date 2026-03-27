import React from "react";
import { useTranslation } from "react-i18next";

function Header() {
  const { i18n } = useTranslation();

  const toggleLanguage = () => {
    const newLang = i18n.language === "en" ? "hi" : "en";
    i18n.changeLanguage(newLang);
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "10px 20px",
        backgroundColor: "#f5f5f5",
      }}
    >
      <h2>🌱 Smart Agriculture</h2>

      <div>
        <button onClick={toggleLanguage}>
          {i18n.language === "en" ? "Switch to Hindi" : "Switch to English"}
        </button>

        <p style={{ margin: 0 }}>Current: {i18n.language.toUpperCase()}</p>
      </div>
    </div>
  );
}

export default Header;
