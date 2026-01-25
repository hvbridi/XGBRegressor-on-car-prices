from database import check_state,base,engine,car,session_local
import time
from pydantic import BaseModel
from fastapi import FastAPI
import joblib
import pandas as pd

"""
FastAPI backend for predicting car prices

This script creates a pydantic model and a API that recieves POST requests using the model and preprocessor saved through the notebook
"""

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

@app.get('/health/')
def check_health():
    return {'status':check_state()}


@app.on_event("startup")
def populate_db():
    while True:
        try:
            df = pd.read_csv('/app/my_data/vehicles.csv')
            base.metadata.create_all(bind=engine)
            with session_local() as db:
                for index,row in df.iterrows():
                    new_car=car(
                        price = row['price'],
                        year = row['year'],
                        manufacturer = row['manufacturer'],
                        model = row['model'],
                        fuel = row['fuel'],
                        odometer = row['odometer'],
                        drive = row['drive'],
                        type = row['type'],
                        lat = row['lat'],
                        long = row['long']
                    )
                    db.add(new_car)
                db.commit()
                break
        except:
            time.sleep(5)