import pandas as pd
import requests
import json
import numpy as np
import os

from dotenv import load_dotenv

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# from constant import CATEGORY_MAPPING, REVERSE_CATEGORY_MAPPING

from load_data import load_data



load_dotenv()




# ============== Load the data ==============

df = load_data()


# # ============== split the data into training and testing sets ==============

# train_data = df.sample(frac=0.8, random_state=42)
# test_data = df.drop(train_data.index)



# ============== API details ==============

API_URL = os.getenv("TOPIC_MODEL_API_URL")
headers = {'Content-Type': 'application/json'}




CATEGORY_MAPPING = {
    "Politics": 0,
    "Crime": 1,
    "Corruption": 2,
    "Accident": 3,
    "Others": 4,
}


REVERSE_CATEGORY_MAPPING = {v: k for k, v in CATEGORY_MAPPING.items()}






# ============== category mapping ==============

def map_categories(df):
    df['label'] = df['Broad Category'].map(CATEGORY_MAPPING)
    return df






# ============== make prediction ==============

def make_prediction(text):
    
    payload = json.dumps({"text": text})
    
    try:
        response = requests.post(API_URL, headers=headers, data=payload)
        response.raise_for_status()
        
        prediction_label = json.loads(response.text).get("topic", {}).get("label") 
        print(f"Prediction label: {prediction_label}")
        return CATEGORY_MAPPING.get(prediction_label, -1) # -1 is the default value if the prediction label is not found
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return -1
    
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Response content: {response.text}")
        return -1



# ============== evaluate the predictions & Return the accuracy, classification report, confusion matrix ==============

def evaluate_predictions(y_true, y_pred):
    
    valid_indices = [i for i, y in enumerate(y_pred) if y != -1]
    filtered_y_true = [y_true[i] for i in valid_indices]
    filtered_y_pred = [y_pred[i] for i in valid_indices]
    
    if not filtered_y_true or not filtered_y_pred:
        print("No valid prediction found")
        return None, None, None, []
    
    else:
        accuracy = accuracy_score(filtered_y_true, filtered_y_pred)
        
        report = classification_report(filtered_y_true, filtered_y_pred, 
                                       zero_division=1, # to avoid division by zero
                                       labels=list(CATEGORY_MAPPING.values()))  # to avoid error

        cm = confusion_matrix(filtered_y_true, filtered_y_pred, 
                              labels=list(CATEGORY_MAPPING.values())) # to avoid error
        
        return accuracy, report, cm , valid_indices
    
    
    

# ============== save the result ==============


def save_result(df, valid_indices, y_true, y_pred, output_file):
    
     # Filter texts, true labels, and predicted labels based on valid_indices
    filtered_texts = [df['text'].iloc[i] for i in valid_indices]
    filtered_y_true = [y_true[i] for i in valid_indices]
    filtered_y_pred = [y_pred[i] for i in valid_indices]
    
    
    
    if len(filtered_texts) == len(filtered_y_true) == len(filtered_y_pred):
        result = pd.DataFrame({'text': filtered_texts, 
                               'true_label': filtered_y_true, 
                               'predicted_label': filtered_y_pred})
        result.to_csv(output_file, index=False)
        print(f"Result saved to {output_file}")
        
    else:
        print("Error: Lengths of filtered texts, true labels, and predicted labels do not match.")
    
    
    





if __name__ == "__main__":
    df = load_data()
    df = map_categories(df)
    
    y_true = df['label'].tolist()
    y_pred = [make_prediction(text) for text in df['text']]

    

    # ============== evaluate the predictions ==============

    accuracy, report, cm , valid_indices = evaluate_predictions(y_true, y_pred)
    
    # save_result(y_true, y_pred, valid_indices)
    
    
    if accuracy is not None:
        print(f"Accuracy: {accuracy}")
        print("classification report:\n", report)
        print("confusion matrix:\n", cm)
        
        output_file = 'result.csv'
        save_result(df, valid_indices, y_true, y_pred, output_file)




