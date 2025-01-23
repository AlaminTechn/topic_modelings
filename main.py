import pandas as pd
import requests
import json
import numpy as np
import os

from dotenv import load_dotenv

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# from constant import CATEGORY_MAPPING, REVERSE_CATEGORY_MAPPING

from load_data import load_data
from constant import CATEGORY_MAPPING



load_dotenv()




# ============== Load the data ==============

df = load_data()




# ============== API details ==============

API_URL = os.getenv("TOPIC_MODEL_API_URL")
headers = {'Content-Type': 'application/json'}







# ============== category mapping ==============

def process_categories(df):
    df['label'] = df['Broad Category'].str.lower().str.replace(' ', '')
    return df






# ============== make prediction ==============

def make_prediction(text):
    
    # need to save prediction result in a csv file
    
    payload = json.dumps({"text": text})
    
    try:
        response = requests.post(API_URL, headers=headers, data=payload)
        print(f"Response API Data : {response.text}")
        response.raise_for_status()

        prediction_label = json.loads(response.text).get("topic", {}).get("label")
         
        print(f"Prediction label: {prediction_label}")
        
        return prediction_label.lower().replace(' ', '')
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Response content: {response.text}")
        return None



# ============== evaluate the predictions & Return the accuracy, classification report, confusion matrix ==============

def evaluate_predictions(y_true, y_pred):

    accuracy = accuracy_score(y_true, y_pred)
        
    report = classification_report(y_true, y_pred, zero_division=1,)  

    cm = confusion_matrix(y_true, y_pred)
        
    return accuracy, report, cm 
    
    
    

# ============== save the result ==============


def save_result(df, y_true, y_pred, output_csv, output_report):
    
    
    with open(output_report, 'w') as report_file:
        report_file.write(f"Accuracy: {accuracy}\n")
        report_file.write(f"Classification Report:\n")
        report_file.write(report)
        
        
        
        
    # save prediction text in a txt file 
    
    
    prediction_files = 'prediction_files.txt'
    
    with open(prediction_files, 'w') as prediction_text:
        prediction_text.write("Actual value\tPrediction Text:\n")
        
        for true, predicted in zip(y_true, y_pred):
            prediction_text.write(f"{true}\t{predicted}\n")
    
    
    
    
    result_df = pd.DataFrame({'text': df['text'], 
                               'true_label': y_true, 
                               'predicted_label': y_pred})
    
    result_df.to_csv(output_csv, index=False)
    print(f"Result saved to {output_csv} successfully and report saved to {output_report}")
    
    



# ============== main function ==============



if __name__ == "__main__":
    df = load_data()
    df = process_categories(df)
    
    
    
    
    
    y_true = df['label'].tolist()
    y_pred = [make_prediction(text) for text in df['text']]

    

    # ============== evaluate the predictions ==============

    accuracy, report, cm = evaluate_predictions(y_true, y_pred)
    
    if accuracy is not None:
        print(f"Accuracy: {accuracy}")
        print("classification report:\n", report)
        print("confusion matrix:\n", cm)
        
        
        
        
        
        output_csv = 'result.csv'
        output_report = 'report.txt'
        save_result(df, y_true, y_pred, output_csv, output_report)




