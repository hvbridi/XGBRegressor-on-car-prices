FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD [ "uvicorn", "fastapi_car_prediction:app", "--reload" ]   