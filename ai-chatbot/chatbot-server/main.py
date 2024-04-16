from openai import OpenAI
from pypdf import PdfReader 
from langchain_community.llms import Cohere
from langchain_cohere import CohereEmbeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_core.prompts import PromptTemplate
from storeEmbedding import pineconeSetup
import re
from flask import Flask, request

app = Flask(__name__)
def queryFun(query):
    pc = Pinecone(api_key='779cf677-7000-4b40-b235-0a0f6bb08aca')
    index_name = 'chat-bot'
    index = pc.Index(index_name)
    embeddings_model = CohereEmbeddings(cohere_api_key="kTfGGm32yJP2tBJZpFl0BZgDZfOZcoaOEIaVTrcT")

    ######################################################
    queryEmb = embeddings_model.embed_query(query)
    # print(queryEmb)
    results=index.query(
        vector=queryEmb,
        top_k=2,
        include_metadata=True
    )
    results
    data=""
    for match in results.matches:
        metadata = match['metadata']
        d = metadata.get('data')
        data+=d
        data+=','

    model = Cohere(cohere_api_key="kTfGGm32yJP2tBJZpFl0BZgDZfOZcoaOEIaVTrcT",model="command", max_tokens=256, temperature=0.5)
    prompt = PromptTemplate.from_template("Give Response to the query:{query} based on the chunks of the data:{data} given only if the data is sufficient to answer the query, otherwise give output 'Insufficient Data' and. Do not give extra salutation, directly give the answer. Give answer to the point")
    chain = prompt | model
    return chain.invoke({"query": query, "data":data})




@app.route("/")
def home():
    pineconeSetup()
    return "Hello, World!"
    
@app.route('/query', methods=['POST'])
def query_example():
    data = request.json
    query=data['query']
    return queryFun(query)

if __name__ == "__main__":
    app.run(debug=True,port=4000)