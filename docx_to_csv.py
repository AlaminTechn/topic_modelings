import pandas as pd
from docx import Document

def docx_to_csv(docx_path, csv_path):
    doc = Document(docx_path)
    data = []
    for para in doc.paragraphs:
        row = para.text.split(', ')
        data.append(row)
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)

# Example usage
docx_to_csv('Topic for SIMS V2.docx', 'Topic_for_SIMS_V2.csv')