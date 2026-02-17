import pickle
import pandas as pd

# Load model
with open("models/fertilizer_model.pkl", "rb") as f:
    model = pickle.load(f)

# Load training columns
with open("models/fertilizer_columns.pkl", "rb") as f:
    training_columns = pickle.load(f)

def recommend_fertilizer(input_data):

    # Create dataframe from input
    input_dict = {
        "Temperature": input_data.temperature,
        "Humidity": input_data.humidity,
        "Moisture": 50,  # if not available, set default
        "Nitrogen": input_data.N,
        "Potassium": input_data.K,
        "Phosphorus": input_data.P,
        "Soil_Type": "Sandy",  # must match dataset categories
        "Crop_Type": "Rice"    # dynamic if needed
    }

    input_df = pd.DataFrame([input_dict])

    # One-hot encode
    input_df = pd.get_dummies(input_df)

    # Align with training columns
    input_df = input_df.reindex(columns=training_columns, fill_value=0)

    prediction = model.predict(input_df)

    return prediction[0]
