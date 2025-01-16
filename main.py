import pandas as pd
import requests
import json
import numpy as np

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report



# Load the data
df = pd.read_csv('Topic-Modeling-SIMS-v1-Sheet1.csv')

print(df.head())



# Split the data into training and testing sets
train_data = df.sample(frac=0.8, random_state=42)
test_data = df.drop(train_data.index)

# Data preparation

data = [
    {"text": "২১ সেপ্টেম্বর, শনিবার, দক্ষিণ-পশ্চিম রাশিয়ার একটি গোলাবারুদের গুদামে আগুন লেগেছে...", "category": "Politics"},
    {"text": "মোহাম্মাদপুরে ছুরিকাঘাতে তরুণের মৃত্যু...", "category": "Crime"},
]   


# df = pd.DataFrame(data)

category_mapping = {
    "Politics": 0,
    "Crime": 1,
    "Corruption": 2,
    "Accident": 3,
    "Others": 4
}



# reverse the category mapping

reverse_mapping = {
    "Politics":0,
    "Crime": 1,
    "Corruption": 2,
    "Accident": 3,
    "Others": 4,
}



df['label'] = df['Broad Category'].map(category_mapping)

# print(df)



# API details
url = "http://192.168.200.21:9002/api/v1/topic"
# url = "http://103.113.152.82:9000/api/v1/topic"
# url = "http://103.113.152.82:9002/"

headers = {'Content-Type': 'application/json'}

y_true = df['label'].tolist()
y_pred = []


for text in df['text']:
    
    payload = json.dumps({"text": text})
    try:
        response = requests.post(url, headers=headers, data=payload)
        print(f"Response status code: {response.status_code}")
        print(f"Response text: {response.text}")
        
        if response.status_code == 200:
            prediction_label = json.loads(response.text).get("topic", {}).get("label", None)
            
            y_pred.append(reverse_mapping.get(prediction_label, -1))
        else:
            print(f"Error: {response.text}")
            y_pred.append(-1) # -1 means the prediction is not found
            break
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        y_pred.append(-1) # -1 
        break
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Response content: {response.text}")
        break
    
    
    


#Evaluation 

accuracy = accuracy_score(y_true, y_pred)
print(f"Accuracy: {accuracy}")
print("classification report", classification_report(y_true, y_pred))
print("confusion matrix", confusion_matrix(y_true, y_pred))


