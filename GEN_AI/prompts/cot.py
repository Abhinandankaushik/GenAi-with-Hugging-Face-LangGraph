# Chain Of Thought Prompting

from dotenv import load_dotenv
from openai import OpenAI
import os
import json

load_dotenv()

client = OpenAI(
    api_key= os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = """
You're an expert AI Assistant in resolving user queries using a structured reasoning process.

You must operate using three steps:
1. START  :  The user provides the query.
2. PLAN   : Think about what needs to be done to solve the query. There can be multiple PLAN steps.
3. OUTPUT : Provide the final answer for the user.

Rules:
- Strictly follow the given JSON output format.
- Only run one step at a time.
- The sequence of steps must be:
  START -> PLAN (one or more) -> OUTPUT
- Do not skip steps.
- The OUTPUT step must contain the final response intended for the user.

Output JSON Format:
{
  "step": "START" | "PLAN" | "OUTPUT",
  "content": "string"
}

Example Interaction:

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


"""

message_history = [
   {"role":"system",  "content": SYSTEM_PROMPT},
]

print("Starting LLM Thinking Mode")
print("="*30)
user_query = input("👉👉")
message_history.append({"role":"user","content":user_query})

while True:
  response = client.chat.completions.create(
      model="gemini-3-flash-preview",
      response_format={"type":"json_object"},
      messages=message_history
  )
  raw_result = response.choices[0].message.content
  message_history.append({"role":"user","content":raw_result})
  parsed_result = json.loads(raw_result)
  
  if parsed_result.get("step") == "START":
    print("✅")
    continue
  if parsed_result.get("step") == "OUTPUT":
    print("😍",parsed_result.get("content"))
    break
  

