import "./App.css";
import CropPrediction from "./components/CropPrediction";
import SoilUpload from "./components/SoilUpload";
import Header from "./components/Header";

function App() {
  return (
    <div className="App">
      <Header />
      <SoilUpload />
      <CropPrediction />
    </div>
  );
}

export default App;
