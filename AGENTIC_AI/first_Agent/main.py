from dotenv import load_dotenv
from openai import OpenAI
import os
import requests
import json
from pydantic import BaseModel,Field
from typing import Optional

load_dotenv()

client = OpenAI(
    api_key= os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)



# external api for whether fetch
# https://wttr.in/{city}?format=%c+%t


def get_weather(city:str):
    url = f"https://wttr.in/{city}?format=%c+%t"
    response = requests.get(url)
    
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    
    return "Something went Wrong"


available_tools = {
    "get_weather" : get_weather
}

SYSTEM_PROMPT = """
You're an expert AI Assistant in resolving user queries using a structured reasoning process.

You must operate using three steps:
START  : The user provides the query.
PLAN   : Think about what needs to be done to solve the query. There can be multiple PLAN steps.
OUTPUT : Provide the final answer for the user.
You can also call a tool if reuired from the list of available tools.
for every tool call wait for the observe for called tool

Rules:
- Strictly follow the given JSON output format.
- Only run one step at a time.
- The sequence of steps must be:
  START -> PLAN (one or more) -> OUTPUT
- Do not skip steps.
- The OUTPUT step must contain the final response intended for the user.
- User Tools if needed

Output JSON Format:
{
  "step": "START" | "PLAN" | "OUTPUT" | "TOOL" ,
  "content": "string", "tool":"string","input":"string"
}

Available Tools : 
- get_weather: Takes city name as a input and  return weather info about the city 

Example Interaction:
    Example-1:
        User Input:
        Hey, can you solve 2 + 3 * 5 / 10 ?

        Assistant reasoning steps:

        {
        "step": "PLAN",
        "content": "User is asking to evaluate a mathematical expression."
        }

        {
        "step": "PLAN",
        "content": "Follow operator precedence: multiplication and division before addition."
        }

        {
        "step": "PLAN",
        "content": "Compute 3 * 5 = 15, then 15 / 10 = 1.5"
        }

        {
        "step": "PLAN",
        "content": "Add remaining value: 2 + 1.5 = 3.5"
        }

        {
        "step": "OUTPUT",
        "content": "The result of 2 + 3 * 5 / 10 is 3.5."
        }
    Example-2:
        User Input:
        Hey, what is weather of Delhi?

        Assistant reasoning steps:

        {
        "step": "PLAN",
        "content": "User is asking to get weather of a Delhi."
        }

        {
        "step": "PLAN",
        "content": "Lets see if i have available tool from available tools list."
        }

        {
        "step": "PLAN",
        "content": "I have tool available for this query"
        }

        {
        "step": "PLAN",
        "content": "I need to call get_weather tool for delhi as input"
        }

        {
        "step": "TOOL",
        "tool": get_weather,
        "input": "delhi"
        }
        
        {
           "step":"OBSERVE",
           "tool":"get_weather",
           "output":"The temp of delhi is cloudy with 20 Celcius
        }
        
        {
            "step" : "PLAN",
            "content":"Greate, I got the weather info about delhi"
        }
        
        {
            "step" : "OUTPUT",
            "content":"The current weather in delhi is 20 celius in cloud sky"
        }
     
"""



class MyOutputFormat(BaseModel):
    step:str = Field(...,description="The ID of the step. Example: PLAN,OUTPUT,TOOL, etc")
    content: Optional[str] = Field(None,description="The optional string content")
    tool : Optional[str] = Field(None,description="The ID of tool call.")
    tool_input : Optional[str] = Field(None,description="The input params for the tool.")

message_history = [
   {"role":"system",  "content": SYSTEM_PROMPT},
]

print("Starting LLM Thinking Mode")
print("="*30)
user_query = input("👉👉")
message_history.append({"role":"user","content":user_query})

while True:
  response = client.chat.completions.parse(
      model="gemini-3-flash-preview",
      response_format=MyOutputFormat,
      messages=message_history
  )
  raw_result = response.choices[0].message.content
  message_history.append({"role":"user","content":raw_result})
  parsed_result = response.choices[0].message.parsed
  
  if isinstance(parsed_result, list):
     parsed_result = parsed_result[0]
  
  if parsed_result.step == "START":
    print("✅",parsed_result.content)
    continue
  if parsed_result.step == "PLAN":
    print("❤️",parsed_result.content)
    continue

  if parsed_result.step == "TOOL":
    tool_to_call = parsed_result.tool
    tool_input = parsed_result.input
    tool_response = available_tools[tool_to_call](tool_input)
    
    print(f"🚀, {tool_to_call} ({tool_input}) = {tool_response}")
    
    message_history.append({"role":"developer","content":json.dumps(
        {"step":"OBSERVE","tool":tool_to_call, "input":tool_input , "output": tool_response})})
    continue

  if parsed_result.step == "OUTPUT":
    print("😍",parsed_result.content)
    break
  



