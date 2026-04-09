from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
import os

load_dotenv()

# Vector Embeddings
embedding_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name = "Learning RAG",
    embedding=embedding_model,
)

# Take user input
user_query = input("Ask Something...\n")


# Relevant chunks from the vector db
search_result = vector_db.similarity_search(query=user_query)

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


client = OpenAI(
    api_key= os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)



response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=  [
        {"role":"system","content": SYSTEM_PROMPT},
        { "role" : "user","content": user_query}
    ]
)
print("#"*20,"RESPONSE", "#"*20)
print(f"✅: {response.choices[0].message.content}")