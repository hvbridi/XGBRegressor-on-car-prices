import os
from sqlalchemy import create_engine

#gets the data from the env variables defined in the yml
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
name = os.getenv('DB_NAME')

#creates the url for the engine
url = f'mysql+pymysql://{user}:{password}@{host}:3306/{name}'

engine = create_engine(url, echo=True)

#tests if the engine can connect

def check_state():
    try:
        with engine.connect() as connection:
            return 'Ok'

    except Exception as error:
        return str(error)