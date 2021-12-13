import pickle
import streamlit as st
import requests
import numpy as np
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
st.title("Water Quality : Drinking water potability")
st.image("https://www.harmonyhomeinspectionma.com/wp-content/uploads/2020/06/Water-1920w.jpg")
st.text('Made by Hrishikesh Kini')
st.header('Enter The Values')
ss = pickle.load(open('standardscaler.pkl','rb'))
v1 = st.text_input("ph")
v2 = st.text_input("Hardness")
v3 = st.text_input("Solids")
v4 = st.text_input("Chloramines	")
v5 = st.text_input("Sulfate")
v6 = st.text_input("Conductivity")
v7 = st.text_input("Organic_carbon")
v8 = st.text_input("Trihalomethanes")
v9 = st.text_input("Turbidity")
pred = 2
if st.button('Check Result'):
    data = []
    data.append(int(float(v1)))
    data.append(int(float(v2)))
    data.append(int(float(v3)))
    data.append(int(float(v4)))
    data.append(int(float(v5)))
    data.append(int(float(v6)))
    data.append(int(float(v7)))
    data.append(int(float(v8)))
    data.append(int(float(v9)))
    data = np.array(data).reshape(1,-1)
    data = ss.transform(data)
    import requests
    import json
    # NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
    API_KEY = "2BUeG0Dyug3OIM-iJDYqZoOqzy0YCLKYxlzCZPrH8JZ4"
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]

    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    #payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [array_of_values_to_be_scored, another_array_of_values_to_be_scored]}]}
    payload_scoring = {"input_data": [
        {'fields': ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity',
                    'Organic_carbon', 'Trihalomethanes', 'Turbidity'], 
         'values': [[data[0][0],data[0][1],data[0][2],data[0][3],data[0][4],data[0][5],data[0][6],data[0][7],data[0][8]]]
        }]}
    

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/5a40960c-2088-47cd-96ab-97baf5e729da/predictions?version=2021-12-07', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    predictions = response_scoring.json()
    pred = predictions['predictions'][0]['values'][0][0]
    pred = round(pred)



if pred == 1:
    original_title = '<h3 style="color:Green; font-size: 50px">Water is Drinkable</h3>'
    st.markdown(original_title, unsafe_allow_html=True)
elif pred == 0:
    original_title = '<h3 style="color:Red; font-size: 50px">Water is Polluted</h3>'
    st.markdown(original_title, unsafe_allow_html=True)
else:
    st.header('Enter values for prediction')