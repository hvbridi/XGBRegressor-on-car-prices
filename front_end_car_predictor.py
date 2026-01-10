import streamlit as st
import requests

st.title('Car price predictor')
st.header('Fill the information about the car you want to predict the price')

col1, col2 = st.columns(2)

with col1:
    year=int(st.number_input('Insert the year of the car',min_value=1900,max_value=2026,value=2000))
    odometer=float(st.number_input('Insert the odometer reading of the car',min_value=0,max_value=50000,step=1000))

with col2:
    lat = st.number_input('Location Latitude', format="%.4f")
    long= st.number_input('Location Longitude', format="%.4f")

st.divider()
model=st.text_input('Model',placeholder='e.g. Compass, Frontier crew cab pro-4x	').lower()
manufacturer=st.text_input('Manufacturer',placeholder='e.g. Chevrolet, Toyota, Ford').lower()

col3,col4,col5=st.columns(3)
with col3:
    fuel=st.selectbox('Fuel type',['gas','diesel', 'hybrid', 'electric', 'other'])

with col4:
    drive=st.selectbox('Drive train',['rwd', '4wd', 'fwd'])

with col5:
    type=st.selectbox('Body type',['pickup', 'truck', 'coupe', 'SUV', 'hatchback', 'mini-van', 'sedan', 'offroad', 'bus', 'van', 'convertible', 'wagon', 'other'])

if st.button('Predict price'):
    if model =='' or manufacturer=='':
        st.error('Please fill all the fields')
    
    else:
        sending_dict= {'year':year,
            'odometer':odometer,
            'lat':lat,
            'long':long,
            'model':model,
            'manufacturer':manufacturer,
            'fuel':fuel,
            'drive':drive,
            'type':type}
        prediction = requests.post('http://127.0.0.1:8000/predict/',json=sending_dict).json()
        st.success(f'The predicted price for your car is {prediction:.2f}')





