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
cols_to_use = ['price', 'year', 'manufacturer', 'model', 'fuel', 'odometer', 'drive', 'type', 'lat', 'long']

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
            df = pd.read_csv('/app/my_data/vehicles.csv', usecols=cols_to_use,chunksize=50000)
            base.metadata.create_all(bind=engine)
            for chunck in df:
                df.to_sql('cars', con=engine, if_exists='append', index=False)
        except Exception as e:
            print(f'error {e}')
            time.sleep(5)