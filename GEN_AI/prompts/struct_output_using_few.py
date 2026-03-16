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

Rule:
- Strictly follow the output in JSON format

Output Format: 
{{
    "code" : "string",
    "isCodingQuestion" : boolean
}}

Examples: 
Q: Can you explain the a+b whole  square. ?
A: {{"code":null, "isCodingQuestion":flase}}

Q: Hey, Write a code in python for adding two numbers.
A: {{
    "code": "def(a,b): return a+b",
    "isCodingQuestion" : true    
}}
      
"""

response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=  [
        {"role":"system",
         "content": SYSTEM_PROMPT},
        { 
         "role" : "user",
         "content": "write a code to add n number in JS"
         }
    ]
)

print(response.choices[0].message.content)