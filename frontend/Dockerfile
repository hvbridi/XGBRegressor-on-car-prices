FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [ "streamlit", "run","front_end_car_predictor.py","--server.port=8501", "--server.address=0.0.0.0"]