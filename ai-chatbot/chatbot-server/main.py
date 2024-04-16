from openai import OpenAI
from pypdf import PdfReader 
from langchain_community.llms import Cohere
from langchain_cohere import CohereEmbeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_core.prompts import PromptTemplate
from storeEmbedding import pineconeSetup
import re
from flask import Flask, request, jsonify
from keys import pinecone_key as pineConeKey, cohere_api_key as cohereKey
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
model=None
pc = Pinecone(api_key=pineConeKey)
index_name = 'chat-bot'
index = pc.Index(index_name)
embeddings_model = CohereEmbeddings(cohere_api_key=cohereKey)
def queryFun(query):
    ######################################################
    queryEmb = embeddings_model.embed_query(query)
    # print(queryEmb)
    results=index.query(
        vector=queryEmb,
        top_k=10,
        include_metadata=True
    )
    data=""
    for match in results.matches:
        metadata = match['metadata']
        d = metadata.get('data')
        data+=d
        data+=','

    print(query)
    print(data)
    prompt = PromptTemplate.from_template("""You are a question-answering AI assistant. Your role is to provide responses to queries based exclusively on the text data provided to you and our previous conversation. You do not have access to any external information sources or general world knowledge beyond the given text data.

For each query, you will be provided with one or more relevant text chunks extracted from personal data. These text chunks represent the most pertinent information needed to answer the query.

Given:
- The query to be answered:{query}
- The relevant text data:{data}

You should:

1. Carefully read and analyze the provided text chunk(s) to understand the context and information they contain.
2. Use the information present in the text chunk(s) to construct a thorough and accurate answer to the query.
3. If the provided text chunk(s) do not contain enough information to comprehensively answer the query, politely indicate that you cannot fully answer based on the given data.
4. Never attempt to retrieve additional information from any external sources beyond the provided text chunk(s).
5. Maintain appropriate boundaries and avoid outputting any private or sensitive information not relevant to the query.

Your training objective is to learn to effectively extract relevant information from the given text data and generate satisfactory responses while strictly operating within the scope of that data.

You will be evaluated on:
1. Answer quality: Providing accurate, complete and relevant answers grounded in the provided text chunks.
2. Transparency: Acknowledging when the given data is insufficient to fully answer the query.
3. Data limitation: Strictly using only the provided text chunks without external information lookup.
4. Consistency: Maintaining uniform persona, tone and boundaries across all interactions.""")
    chain = prompt | model
    return chain.invoke({"query": query, "data":data})




@app.route("/")
def home():
    return "Hello, World!"
    
@app.route('/uploadPdf', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF file uploaded'}), 400

    pdf_file = request.files['pdf']
    # Do something with the PDF file, for example, save it to disk
    pdf_file.save('76gdb38fn3.pdf')
    pineconeSetup()
    global model
    model = Cohere(cohere_api_key=cohereKey,model="command", max_tokens=256, temperature=0.2)
    return jsonify({'message': 'PDF uploaded successfully'}), 200

@app.route('/query', methods=['POST'])
def query_example():
    data = request.json
    query=data['query']
    #return queryFun(query)
    return jsonify({'result': queryFun(query)})

if __name__ == "__main__":
    #pineconeSetup()
    app.run(debug=True,port=4000)