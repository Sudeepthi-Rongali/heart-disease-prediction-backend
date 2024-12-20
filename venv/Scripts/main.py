from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib


app = FastAPI()


model_path = "trained_random_forest_model.pkl"
model = joblib.load(model_path)


class HeartDiseaseInput(BaseModel):
    age: int
    sex: int
    resting_bp: int
    cholesterol: int
    fasting_bs: int
    resting_ecg: int
    max_heart_rate: int
    exercise_angina: int
    oldpeak: float
    slope: int
    major_vessels: int
    thalassemia: int
    chest_pain_type: int


@app.get("/")
def read_root():
    return {"message": "Welcome to the Heart Disease Prediction API"}


@app.post("/predict")
def predict_heart_disease(input_data: HeartDiseaseInput):
    try:
        input_values = np.array([[
            input_data.age,
            input_data.sex,
            input_data.resting_bp,
            input_data.cholesterol,
            input_data.fasting_bs,
            input_data.resting_ecg,
            input_data.max_heart_rate,
            input_data.exercise_angina,
            input_data.oldpeak,
            input_data.slope,
            input_data.major_vessels,
            input_data.thalassemia,
            input_data.chest_pain_type
        ]])
        
        prediction = model.predict(input_values)
        result = "Positive for Heart Disease" if prediction[0] == 1 else "Negative for Heart Disease"
        
        return {"prediction": int(prediction[0]), "result": result}
    
    except Exception as e:
        return {"error": str(e)}
