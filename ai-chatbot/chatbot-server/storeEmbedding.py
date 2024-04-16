from pypdf import PdfReader 
from langchain_cohere import CohereEmbeddings
from pinecone import Pinecone, ServerlessSpec
import re


def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
            return text
    return text

def split_text_into_chunks(text, chunk_size=100):
    # Split text into words
    words = re.findall(r'\b\w+\b', text)
    # Initialize variables
    chunks = []
    current_chunk = ""
    word_count = 0
    # Iterate over words
    for word in words:
        current_chunk += word + " "
        word_count += 1
        # Check if chunk size reached
        if word_count >= chunk_size:
            chunks.append(current_chunk)
            current_chunk = ""
            word_count = 0
    # Add the last chunk if not empty
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

def pineconeSetup():
    pdf_path = './chatbot-server/doc.pdf'
    pdf_text = extract_text_from_pdf(pdf_path)
    chunks = split_text_into_chunks(pdf_text, chunk_size=100)

    #Pinecone
    pc = Pinecone(api_key='779cf677-7000-4b40-b235-0a0f6bb08aca')
    spec = ServerlessSpec(cloud='aws', region='us-east-1')
    index_name = 'chat-bot'

    if index_name in pc.list_indexes().names():
        pc.delete_index(index_name)

    pc.create_index(
            index_name,
            dimension=4096,
            metric='cosine',
            spec=spec
        )
    index = pc.Index(index_name)

    #Embeddings
    embeddings_model = CohereEmbeddings(cohere_api_key="kTfGGm32yJP2tBJZpFl0BZgDZfOZcoaOEIaVTrcT")
    embeddings = embeddings_model.embed_documents(chunks)
    array_of_objects = []
    for idx, values in enumerate(embeddings):
        timestamp = str(idx)
        obj = {
            "id": timestamp,
            "values": values,
            "metadata": {
                "data": chunks[idx]
            }
        }
        array_of_objects.append(obj)

    index.upsert(array_of_objects)