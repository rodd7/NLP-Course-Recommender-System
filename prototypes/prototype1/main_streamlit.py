import streamlit as st
import numpy as np
import pandas as pd
import txtai
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

def load_data_and_embeddings():
    dataFile = pd.read_excel('..\curriculum_data_2020_raw\CASS-MASTER.xlsx', sheet_name='Subject')
    courseID = dataFile['Study Package Cd'].dropna().values
    courseTitle = dataFile['Full Title'].dropna().values
    courseCP = dataFile['Credit Point Value'].dropna().values
    courseOrg = dataFile['Owning Organisational Unit Name'].dropna().values

    embeddings = txtai.Embeddings({
    'path' : 'sentence-transformers/all-MiniLM-L6-v2'
    })

    embeddings.load('full_embeddings.tar.gz')

    return courseID, courseTitle, courseCP, courseOrg, embeddings

courseID, courseTitle, courseCP, courseOrg, embeddings = st.cache_data(load_data_and_embeddings)()

# frontend stuff
st.title('search engine testing using course data')
query = st.text_input('enter query:', '')

if st.button('Search'):
    if query:
        result = embeddings.search(query, 5)
        actual_results = [f'ID: {courseID[x[0]]}, Title: {courseTitle[x[0]]}, CP: {courseCP[x[0]]}, courseOrg: {courseOrg[x[0]]}, index: {x[1]*100:.2f}%' for x in result]

        for res in actual_results:
            st.write(res)
        else:
            st.write('please enter query')


# run using: streamlit run main_streamlit.py

# site:www.handbook.uts.edu.au inurl:sitemap

#note: the loading may not work due to moving the directories around. all protoype1 files were on root initially