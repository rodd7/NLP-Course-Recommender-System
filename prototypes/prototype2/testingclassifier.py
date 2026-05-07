import pandas as pd
import spacy

# Load the data
df = pd.read_excel('../2025_UTS_Handbook_Data.xlsx')

# Load a pre-trained NLP model (e.g., spaCy's English model)
nlp = spacy.load('en_core_web_sm')

def extract_keywords(description):
    doc = nlp(description)
    keywords = [chunk.text for chunk in doc.noun_chunks]
    return keywords

# Apply the function to extract keywords for each subject
df['tags'] = df['description'].apply(extract_keywords)

# Export the updated CSV or directly insert into the database
df.to_csv('subjects_with_tags.csv', index=False)