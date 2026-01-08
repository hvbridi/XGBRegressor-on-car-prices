from pydantic import BaseModel
from fastapi import FastAPI,HTTPException
import joblib
import pandas as pd

app=FastAPI()

class car_features(BaseModel):
    year:int
    odometer:float
    lat:float
    long:float
    model:str
    manufacturer:str
    fuel:str
    drive:str
    type:str


model=joblib.load('car_price_model.pkl')
preprocessor=joblib.load('car_preprocessor.pkl')

@app.post('/predict/')
def predict(car_features:car_features)->float:
    features_dict=car_features.model_dump()
    df=pd.DataFrame([features_dict])
    df=preprocessor.transform(df)
    prediction=model.predict(df)
    return float(prediction[0])