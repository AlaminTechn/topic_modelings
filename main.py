import pandas as pd
import requests
import json
import numpy as np
import os

from dotenv import load_dotenv

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


load_dotenv()
# Load the data
df = pd.read_csv('Topic-Modeling-SIMS-v1-Sheet1.csv')

print(df.head())



# Split the data into training and testing sets
train_data = df.sample(frac=0.8, random_state=42)
test_data = df.drop(train_data.index)

# Data preparation

# data = [
#     {"text": "২১ সেপ্টেম্বর, শনিবার, দক্ষিণ-পশ্চিম রাশিয়ার একটি গোলাবারুদের গুদামে আগুন লেগেছে...", "category": "Politics"},
#     {"text": "মোহাম্মাদপুরে ছুরিকাঘাতে তরুণের মৃত্যু...", "category": "Crime"},
# ]   


# df = pd.DataFrame(data)

category_mapping = {
    "Politics": 0,
    "Crime": 1,
    "Corruption": 2,
    "Accident": 3,
    "Others": 4,
}



# reverse the category mapping

reverse_mapping = {
    "Politics":0,
    "Crime":1,
    "Corruption":2,
    "Accident":3,
    "Others":4,
}



df['label'] = df['Broad Category'].map(category_mapping)

# print(df)



# API details

url = os.getenv("TOPIC_MODEL_URL")

headers = {'Content-Type': 'application/json'}

y_true = df['label'].tolist()
y_pred = []


for text in df['text']:
    print("text",text)
    payload = json.dumps({"text": text})
    
    try:
        response = requests.post(url, headers=headers, data=payload)
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            prediction_label = json.loads(response.text).get("topic", {}).get("label")

            # convert the prediction_text to label
            
            if prediction_label in reverse_mapping:
                prediction_label = reverse_mapping[prediction_label]
            else:
                prediction_label = -1
            
            print("prediction_label",prediction_label)
            y_pred.append(prediction_label)
        else:
            print(f"Error: {response.text}")
            y_pred.append(-1) # -1 means the prediction is not found
            continue
            # break
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        y_pred.append(-1) # -1 means the prediction is not found
        continue
        # break
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Response content: {response.text}")
        continue
        # break
      





# ============== filter out the invalid prediction ==============


valid_prediction = [i for i, y in enumerate(y_pred) if y != -1]
filtered_y_true = [y_true[i] for i in valid_prediction]
filtered_y_pred = [y_pred[i] for i in valid_prediction]


# ============== Evaluation ==============


if len(filtered_y_true) == 0 or len(filtered_y_pred) == 0:
    print("No valid prediction found")
    exit()
    
else:   
    accuracy = accuracy_score(filtered_y_true, filtered_y_pred)
    print(f"Accuracy: {accuracy}")



# Generate the classification report and confusion matrix


    report = classification_report(filtered_y_true, filtered_y_pred, 
                               zero_division=1, 
                               labels=list(category_mapping.values()))

    print("classification report", report)





# confusion matrix

    cm = confusion_matrix(filtered_y_true, filtered_y_pred, 
                          labels=list(category_mapping.values()))

    print("confusion matrix", cm)




    #================= Evaluation =================

    # accuracy = accuracy_score(filtered_y_true, filtered_y_pred)
    # print(f"Accuracy: {accuracy}")
    # print("classification report", classification_report(filtered_y_true, filtered_y_pred))
    # print("confusion matrix", confusion_matrix(filtered_y_true, filtered_y_pred))


    # save the result to a csv file



    result = pd.DataFrame({'text': [df['text'][i] for i in valid_prediction], 
                           'true_label': filtered_y_true, 
                           'predicted_label': filtered_y_pred})
    result.to_csv('result.csv', index=False)

