# ChatBot Application with PDF Questioning

This project is a chatbot application that allows users to add PDF files and ask questions based on the content of the PDF. It also provides a graphical user interface built with React, Node.js and Tailwind CSS.

## Getting Started

To run this application , follow these steps:

1. Clone the repository: git clone https://github.com/your-username/your-repository.git
2. Navigate to the project directory: cd your-repository
3. Install the required libraries for the server:
```bash
pip install pypdf==4.2.0
pip install langchain-cohere==0.1.2
pip install pinecone-client==3.2.2
pip install langchain-pinecone==0.1.0
pip install langchain-community==0.0.32
pip install langchain-core==0.1.42
pip install Flask==3.0.3
pip install Flask-Cors==4.0.0
```
4. Add your API keys to the keys.py file. You'll need the Pinecone API key for the vector store database and the Cohere API key to run the llm.
```
PINECONE_API_KEY = "your-pinecone-api-key"
COHERE_API_KEY = "your-cohere-api-key"
```
5. Run the server by executing the main.py file.
6. Install dependencies for frontend.
```
npm install
```

## Usage:

1. Start the frontend development server:
```
npm run
```
2. The application's user interface will be available at http://localhost:3000.
3. Choose and Upload the pdf.
4. Once the file is uploaded, you can start asking questions related to the content of the PDF.
5. The application will process your question and provide a relevant response based on the content of the uploaded PDF.
 

## License

This project is licensed under the [MIT License](LICENSE).
  
