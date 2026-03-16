from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
    api_key= os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=  [
        {"role":"system",
         "content": "You are an expert in maths and only and only ans maths related questions.if query is not related to sub say sorry"},
        { 
         "role" : "user",
         "content": "Hey There! what is 2+2"
         }
    ]
)

print(response.choices[0].message.content)