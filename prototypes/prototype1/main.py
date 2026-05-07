import txtai
import numpy as np
import pandas as pd
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

dataFile = pd.read_excel('curriculum_data_2020_raw\CASS-MASTER.xlsx', sheet_name='Subject')

# print(dataFile.columns)
# print(dataFile['Full Title'])

# courseTitles = dataFile['Full Title'].dropna().values
courseID = dataFile['Study Package Cd'].dropna().values
courseTitle = dataFile['Full Title'].dropna().values
courseCP = dataFile['Credit Point Value'].dropna().values
courseOrg = dataFile['Owning Organisational Unit Name'].dropna().values

# print(courseTitle)

embeddings = txtai.Embeddings({
    'path' : 'sentence-transformers/all-MiniLM-L6-v2'
})

courseData = [f'\'{id}\',\'{title}\',\'{cp}\',\'{org}\'' for id, title, cp, org in zip(courseID, courseTitle, courseCP, courseOrg)] #combining data together
# courseData = [f'\'{id}\',\'{title}\',\'{cp}\',\'{org}\'' for id, title, cp, org in zip(courseID, courseTitle, courseCP, courseOrg)] #combining data together


embeddings.index(courseData)
embeddings.save('full_embeddings.tar.gz')

result = embeddings.search('48230', 6)

print(result)

actual_results = [courseData[x[0]] for x in result]

print(actual_results)