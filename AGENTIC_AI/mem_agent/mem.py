from mem0 import Memory
import os
from dotenv import load_dotenv
from google import genai
import json

load_dotenv()

GOOGLE_API_KEY = os.environ["GEMINI_API_KEY"]

client = genai.Client(api_key=GOOGLE_API_KEY)


config = {
    "version": "v1.1",
    "embedder": {
        "provider": "gemini",
        "config": {
            "api_key": GOOGLE_API_KEY,
            "model": "gemini-embedding-2-preview"
        }
    },
    "llm": {
        "provider": "gemini",
        "config": {
            "api_key": GOOGLE_API_KEY,
            "model": "gemini-3-flash-preview"
        }
    },
    "vector_store": {
        "provider" : "qdrant",
        "config" : {
            "host" : "localhost",
            "port" : 6333,
            "collection_name": "mem0_gemini2_768",
            "embedding_model_dims": 768
        }
    }
}

mem_client = Memory.from_config(config)

print("Conversation beging...")
print("Note: enter 0 to exit")
print("*"*30,"\n")

while user_query:=input("query >") :
    
    if(user_query == "0"):
        break
    
    search_memory = mem_client.search(query=user_query,user_id="abhi")
    
    memories  =  [ f"ID: {mem.get("id")} \nMemory: {mem.get("memory")}" for mem in search_memory.get("results")]
    
    print("Found Memories: ",memories)
    
    SYSTEM_PROMPT = f"""
You are a helpful AI assistant aware of user's background.

User's memories:
{json.dumps(memories)}

Please respond considering this context."""
    
    # Combine system prompt with user query
    full_prompt = f"{SYSTEM_PROMPT}\n\nUser Query: {user_query}"
    
    ai_response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=full_prompt
    )

    response_text = ai_response.text
    print("AI: ", response_text)

    mem_client.add(
        user_id="abhi",  
        messages=[ 
            {"role": "user", "content" : user_query},
            {"role": "assistant" , "content" : response_text}
        ]
    )

    print("Memory has been saved...")

print("Session Ended...")