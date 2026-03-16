#Few Shot Prompting

from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
    api_key= os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

#Zero shot Prompting : Directly giving the instruction and few examples to the model
SYSTEM_PROMPT = """You should only and only ans the coding related que. do not answer anything else , your name is Alexa.
If user ask anything beyound them just say sorry

Examples: 
Q: Can you explain the a+b whole  square. ?
A: Sorry, I can only help Coding related Questions.

Q: Hey, Write a code in python for adding two numbers.
A: def(a,b):
     return a+b
     
      
"""

response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=  [
        {"role":"system",
         "content": SYSTEM_PROMPT},
        { 
         "role" : "user",
         "content": "generate python code for multithreading"
         }
    ]
)

print(response.choices[0].message.content)