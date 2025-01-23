import pandas as pd


def load_data():
    df = pd.read_csv('Topic-Modeling-SIMS-v1-Sheet1.csv')
    # df = df.dropna(subset=['text'])
    return df