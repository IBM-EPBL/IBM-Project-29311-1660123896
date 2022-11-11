import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "YbH1Jt5lA7lHvNhNPEUuKjdais91dxeOYYnHDbLraG2b"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"field": [['blood_urea','blood glucose random','coronary_artery_disease','anemia','pus_cell',
    'red_blood_cells','diabetesmellitus','pedal_edema']], "values": [[44,123,0,0,1,1,0,0]]}]}

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/22964015-8997-4dc4-a352-f309cbc4907c/predictions?version=2022-11-11', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
print(response_scoring.json())