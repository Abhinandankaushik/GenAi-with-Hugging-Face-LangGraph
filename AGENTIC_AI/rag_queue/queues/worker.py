from openai import OpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
from ..client.rq_client import celery_app
import os

load_dotenv()

client = OpenAI(
    api_key= os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

embedding_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name = "Learning RAG",
    embedding=embedding_model,
)


@celery_app.task
def process_query(query:str):
    print("Searching Chunks ",query)
    search_result = vector_db.similarity_search(query=query)
    context = "\n\n\n".join([f"""Page Content: {result.page_content}\nPage Number:
    {result.metadata['page_label']}\nFile Location:{result.metadata['source']}""" 
    for result in search_result])
    
    SYSTEM_PROMPT = f""" 
    You are  a helpfull AI Assistant who answers user query based on the available context
    retrieved from a PDF file along with page_contents and page number .
    
    You should only ans the user based on the following context and navigate the user toh the right page number to know more.
    
    Context:
    {context}
    
    """
    
    response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=  [
        {"role":"system","content": SYSTEM_PROMPT},
        { "role" : "user","content": query}
    ]
    )
    
    return response.choices[0].message.content



