import ollama

def generate_explanation(crop, input_data):

    prompt = f"""
    You are an agricultural expert.

    Soil conditions:
    Nitrogen: {input_data.N}
    Phosphorus: {input_data.P}
    Potassium: {input_data.K}
    Temperature: {input_data.temperature} °C
    Humidity: {input_data.humidity} %
    pH: {input_data.ph}
    Rainfall: {input_data.rainfall} mm

    Explain in 3 clear sentences why {crop} is suitable for this soil.
    """

    response = ollama.chat(
        model='deepseek-llm',   # or 'deepseek-coder'
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    explanation = response['message']['content']

    return explanation
