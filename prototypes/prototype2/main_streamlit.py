import streamlit as st
import numpy as np
import pandas as pd
import txtai
import os
from sentence_transformers import SentenceTransformer

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

dataFile = pd.read_excel('../2025_UTS_Handbook_Data.xlsx')

subjectRawText = dataFile['subjectRawText'].dropna().values
subjectTitle = dataFile['subjectTitle'].dropna().values
subjectID = dataFile['subjectID'].dropna().values

embeddings = SentenceTransformer("nvidia/NV-Embed-v2", trust_remote_code=True)

embeddings.index(subjectRawText)
embeddings.save('unindexed.tar.gz')

result = embeddings.search('48230', 6)

print(result)

actual_results = [f'ID: {subjectID[x[0]]}, Title: {subjectTitle[x[0]]}, index: {x[1]*100:.2f}%' for x in result]

print(actual_results)

# embeddings.load('unindexed.tar.gz')

# # st.cache_data(subjectRawText, subjectTitle, subjectID, embeddings)

# st.title('search engine testing using course data')
# query = st.text_input('enter query:', '')

# if st.button('Search'):
#     if query:
#         result = embeddings.search(query, 5)
#         actual_results = [f'ID: {subjectID[x[0]]}, Title: {subjectTitle[x[0]]}, index: {x[1]*100:.2f}%' for x in result]

#         for res in actual_results:
#             st.write(res)
#         else:
#             st.write('please enter query')
