import pymongo
from dotenv import load_dotenv
import os
import requests
from openai import OpenAI
import tiktoken
import json

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


mongo_client  = pymongo.MongoClient(f"mongodb+srv://crswebsrvhandle:{os.getenv("MONGODB_PASSWORD")}@cluster0.d9bow.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = mongo_client.subject
collection = db.subjects

def generate_embedding(text: str) -> list[float]:

    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=text
    )
    return response.data[0].embedding




test_query = "develop a piece of innovative software as a group using the software engineering cycle and sprint planning"

results = collection.aggregate([
  {"$vectorSearch": {
    "queryVector": generate_embedding(test_query),
    "path": "subjectEmbedding",
    "numCandidates": 500, #optimisation parameter, consider
    "limit": 8, #strong limits
    "index": "EmbeddingSemanticSearch",
    }},
    {
    "$project": {
        "subjectID": 1,
        "subjectTitle": 1,
        "descriptionSnippet": {"$substr": ["$subjectDescription", 0, 100]},
        "score": { "$meta": "vectorSearchScore" }
    }
  }
      
])

results_list = []

for document in results:
    doc_info = {
    "Subject ID": document.get("subjectID"),
    "Subject Title": document.get("subjectTitle"),
    "Vector Search Score": document.get("score"),
    "Snippet": document.get("descriptionSnippet"),
    }
    
    results_list.append(doc_info)

json_output = json.dumps(results_list, indent=4)

print(json_output)