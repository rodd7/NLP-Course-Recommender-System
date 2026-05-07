import pymongo
from dotenv import load_dotenv
import os
import requests
from openai import OpenAI
import tiktoken

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

embedding_url = "https://api.openai.com/v1/embeddings"
HF_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"


mongo_client  = pymongo.MongoClient(f"mongodb+srv://crswebsrvhandle:{os.getenv("MONGODB_PASSWORD")}@cluster0.d9bow.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = mongo_client.subject #remember added 2 collections in db
collection = db.subjects

enc = tiktoken.encoding_for_model("text-embedding-3-large")

def generate_embedding(text: str) -> list[float]:

    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=text
    )
    return response.data[0].embedding

# def generate_embedding(text: str) -> list[float]:

#   response = requests.post(
#     HF_url,
#     headers={"Authorization": f"Bearer {os.getenv("HUGGINGFACE_SECRET_KEY")}"},
#     json={"inputs": text})

#   if response.status_code != 200:
#     raise ValueError(f"Request failed with status code {response.status_code}: {response.text}")

#   return response.json()

count = 0

for document in collection.find():
    subjectTitle = document.get('subjectTitle')
    subjectID = document.get('subjectID')
    subjectDescription = document.get('subjectDescription')
    subjectSLO = document.get('subjectSLO')
    subjectCILO = document.get('subjectCILO')
    subjectContent = document.get('subjectContent')
    subjectAssessment = document.get('subjectAssessment')
    subjectOrganisationalName = document.get('subjectOrganisationalName')
    subjectEmbedding = f"Subject Title: {subjectTitle}, Subject Description: {subjectDescription}, Subject Learning Outcomes: {subjectSLO}, Course Intended Learning Outcomes: {subjectCILO}, Subject Content: {subjectContent}, Subject Assessments: {subjectAssessment}, Subject Faculty: {subjectOrganisationalName}"

    # document['subjectEmbedding'] = generate_embedding(subjectEmbedding)
    # collection.replace_one({'_id': document['_id']}, document)

    # max_tokens = enc.encode(subjectEmbedding)
    count+=1
    print(count)
    # if len(max_tokens) > 2000:
    #     print(len(max_tokens))

    # print(generate_embedding(subjectEmbedding), '\n')

# print("the subjects ", count)