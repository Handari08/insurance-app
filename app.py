from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI(
    title="Insurance Cost Prediction API"
)

model = joblib.load(
    "model/insurance_model.pkl"
)

class InsuranceInput(BaseModel):
    age: int
    sex: str
    bmi: float
    children: int
    smoker: str
    region: str


@app.get("/")
def root():
    return {
        "message": "Insurance Prediction API Running"
    }


@app.post("/predict")
def predict(data: InsuranceInput):

    df = pd.DataFrame([{
        "age": data.age,
        "sex": data.sex,
        "bmi": data.bmi,
        "children": data.children,
        "smoker": data.smoker,
        "region": data.region
    }])

    prediction = model.predict(df)[0]

    return {
        "estimated_charge": round(float(prediction), 2)
    }