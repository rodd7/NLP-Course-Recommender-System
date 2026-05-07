import pymongo
from dotenv import load_dotenv
import os
import requests
from openai import OpenAI
import tiktoken
import json


from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


mongo_client  = pymongo.MongoClient(f"mongodb+srv://crswebsrvhandle:{os.getenv("MONGODB_PASSWORD")}@cluster0.d9bow.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = mongo_client.subject
collection = db.subjects



# query = {
#     "$or": [
#         {"subjectOrganisationalName": {"$regex": "design", "$options": "i"}},
#         {"subjectOrganisationalName": {"$regex": "architecture", "$options": "i"}},
#         {"subjectOrganisationalName": {"$regex": "building", "$options": "i"}}
#     ]
# }

# # Find and print the matching documents
# results = collection.find(query)

# for document in results:
#     print(f"Subject Title: {document.get('subjectTitle')}, Subject Organisational Name: {document.get('subjectOrganisationalName')}")



count = 0

def generate_context_specific_tags(subject_info: str) -> list[str]:
    prompt = (
        f"using the provided data: {subject_info}, generate single words and short phrases into this strict format ONLY with no headings or descriptions: [] | [] | []. the first array should have subject areas and disciplines, the second array for 5 skills learned, and the third array for career pathways. Tags are always seperated by a comma and are encased in quotation marks"
    )

    # using the provided data: {subject_info}, generate single word or a short phrases into this format only: [] | [] | []. the first array should be about subject areas and disciplines, the second array for skills learned, and the third array for career pathways.
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or use "gpt-4" if you have access
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,  # adjust the token limit as necessary
        n=1,
        stop=None,
    )
    return response.choices[0].message.content

for document in collection.find():
    # print(f'{document['subjectID']}, {document['subjectEmbedding']}')
    subjectTitle = document.get('subjectTitle')
    # subjectID = document.get('subjectID')
    subjectDescription = document.get('subjectDescription')
    subjectSLO = document.get('subjectSLO')
    subjectCILO = document.get('subjectCILO')
    subjectContent = document.get('subjectContent')
    subjectAssessment = document.get('subjectAssessment')
    subjectOrganisationalName = document.get('subjectOrganisationalName')
    subjectEmbedding = f"Subject Title: {subjectTitle}, Subject Description: {subjectDescription}, Subject Learning Outcomes: {subjectSLO}, Course Intended Learning Outcomes: {subjectCILO}, Subject Content: {subjectContent}, Subject Assessments: {subjectAssessment}, Subject Faculty: {subjectOrganisationalName}"

    contextTags = document.get('contextTags')
    
    descriptiveTags = document.get('descriptiveTags')
    print(descriptiveTags)
    # #TF-IDF TAGGING
    # vectorizer = TfidfVectorizer(stop_words="english", max_features=20)
    # tfidf_matrix = vectorizer.fit_transform([subjectEmbedding])
    # # print(list(vectorizer.get_feature_names_out()))

    # document['descriptiveTags'] = list(vectorizer.get_feature_names_out())
    # collection.replace_one({'_id': document['_id']}, document)


    # # GPT TAGGING
    # document['contextTags'] = generate_context_specific_tags(subjectEmbedding)
    # collection.replace_one({'_id': document['_id']}, document)
    # # print(generate_context_specific_tags(subjectEmbedding))

    # count+=1
    # print(count)
