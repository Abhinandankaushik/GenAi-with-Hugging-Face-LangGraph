from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv

load_dotenv()

pdf_path = Path(__file__).parent / "demo.pdf"

# Load this file into current program 
loader = PyPDFLoader(pdf_path)  # lazy object creation

docs = loader.load() # actual loading document object page by page

# Split the docs into smaller chunks

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400) #lazy object creation

chunks = text_splitter.split_documents(documents=docs)  # actual chunking 

# chunks = chunks[:3]  #current api key will not have enough limit for embedding

# Vector Embeddings
embedding_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name = "Learning RAG",
    batch_size=10 
 )



print("Index of documents Done...")