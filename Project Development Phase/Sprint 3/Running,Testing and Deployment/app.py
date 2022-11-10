import pickle

import numpy as np
import pandas as pd
import requests
from flask import Flask, redirect, render_template, request, url_for


# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "YbH1Jt5lA7lHvNhNPEUuKjdais91dxeOYYnHDbLraG2b"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

#initializing a flask app
app = Flask(__name__)

#Loading the model
model = pickle.load(open('CKD.pkl', 'rb'))

#route to display the homepage
@app.route('/')
def home():
    return render_template('home.html')  #rendering the home page
    
@app.route('/Prediction', methods = ['POST','GET'])
def prediction():  #Route to display the prediction page 
    return render_template('indexnew.html')
@app.route('/Home', methods = ['POST','GET'])
def my_home():
    return render_template('home.html')

@app.route('/predict', methods = ['POST'])  #route to show the predictions in the web UI 
def predict():    
    

    #reading inputs given by the user
    

    input_features = []
    if request.method == 'POST':
        input_features.append(request.form.get("blood_urea"))
        input_features.append(request.form.get("blood glucose random"))
        cad = request.form.get("coronary_artery_disease")
        if cad == 'Yes':
            input_features.append(1)
        else:
            input_features.append(0)
        ane = request.form.get("anemia")
        if ane == 'Yes':
            input_features.append(1)
        else:
            input_features.append(0)
        pc = request.form.get("pus_cell")
        if pc == 'Normal':
            input_features.append(1)
        else:
            input_features.append(0)
        rbc = request.form.get("red_blood_cells")
        if rbc == 'Normal':
            input_features.append(1)
        else:
            input_features.append(0)
        db = request.form.get("diabetesmellitus")
        if db == 'Yes':
            input_features.append(1)
        else:
            input_features.append(0)
        pe = request.form.get("pedal_edema")
        if pe == 'Yes':
            input_features.append(1)
        else:
            input_features.append(0)

    
    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"field": [['blood_urea','blood glucose random','coronary_artery_disease','anemia','pus_cell',
    'red_blood_cells','diabetesmellitus','pedal_edema']], "values": [[129,99,1,0,0,1,0,1]]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/fea5ce93-1b6c-4336-9e52-ff633c33be47/predictions?version=2022-11-09', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions = response_scoring.json()
    prediction = predictions['predictions'][0]['values'][0][0] 
    a = "Happy You Don't Have Chronic kidney disease"
    b = "Oops! You have chronic kidney disease"
    if prediction==1:
        return render_template('result.html',answer=b)
    elif prediction==0:
        return render_template('result.html',answer=a)
    else:
        pass

if __name__ == '__main__':
    app.run(debug = True)   #Running the app
