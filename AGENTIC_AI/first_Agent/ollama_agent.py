import os
import requests
import json
from pydantic import BaseModel, Field
from typing import Optional
from ollama import Client

# ------------------ OLLAMA CLIENT ------------------
client = Client(host="http://localhost:11434")

# ------------------ TOOLS ------------------

def create_folder(path: str):
    try:
        os.makedirs(path, exist_ok=True)
        return f"Folder '{path}' created"
    except Exception as e:
        return str(e)

def create_file(data: str):
    """
    Expecting JSON string:
    {"path": "folder/file.html", "content": "<html>...</html>"}
    """
    try:
        parsed = json.loads(data)
        path = parsed["path"]
        content = parsed["content"]

        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        return f"File '{path}' created"
    except Exception as e:
        return str(e)

def run_cmd(cmd: str):
    return os.system(cmd)

def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=%c+%t"
    res = requests.get(url)
    return res.text if res.status_code == 200 else "Error"

# ------------------ TOOL REGISTRY ------------------

available_tools = {
    "create_folder": create_folder,
    "create_file": create_file,
    "run_command": run_cmd,
    "get_weather": get_weather
}

# ------------------ SYSTEM PROMPT ------------------

SYSTEM_PROMPT = """
You are an AI Agent that can BUILD real projects using tools.

You MUST follow structured reasoning:

Steps:
START -> PLAN -> TOOL -> OBSERVE -> PLAN -> ... -> OUTPUT

Rules:
- Always respond in strict JSON
- One step at a time
- NEVER skip steps
- For building websites:
    1. First create folder
    2. Then create files (index.html, style.css, script.js)
- File creation MUST use JSON input:
    {"path": "...", "content": "..."}
- Do NOT hallucinate tools

Output Format:
{
  "step": "START | PLAN | TOOL | OUTPUT",
  "content": "string",
  "tool": "string",
  "input": "string"
}

Available Tools:
- create_folder(path)
- create_file(json_string)
- run_command(cmd)
- get_weather(city)
"""

# ------------------ OUTPUT SCHEMA ------------------

class MyOutputFormat(BaseModel):
    step: str
    content: Optional[str] = None
    tool: Optional[str] = None
    input: Optional[str] = None

# ------------------ MAIN LOOP ------------------

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

print("🔥 AI AGENT READY")
print("=" * 40)

user_query = input("👉 ")
message_history.append({"role": "user", "content": user_query})

while True:
    try:
        response = client.chat(
            model="gemma:2b",
            messages=message_history,
            format=MyOutputFormat.model_json_schema(),
            stream=False,
            options={
                "temperature": 0.3,
                "top_p": 0.9,
                "num_predict": 500,
                "repeat_penalty": 1.1
            }
        )

        raw = response["message"]["content"]

        try:
            parsed = MyOutputFormat.model_validate_json(raw)
        except:
            print("⚠️ Retrying due to invalid JSON...")
            continue

        message_history.append({"role": "assistant", "content": raw})

        if parsed.step == "START":
            print("✅", parsed.content)
            continue

        if parsed.step == "PLAN":
            print("🧠", parsed.content)
            continue

        if parsed.step == "TOOL":
            tool_name = parsed.tool
            tool_input = parsed.input

            if tool_name not in available_tools:
                print("❌ Tool not found:", tool_name)
                continue

            result = available_tools[tool_name](tool_input)
            print(f"🚀 {tool_name} → {result}")

            message_history.append({
                "role": "user",
                "content": json.dumps({
                    "step": "OBSERVE",
                    "tool": tool_name,
                    "input": tool_input,
                    "output": result
                })
            })
            continue

        if parsed.step == "OUTPUT":
            print("🎯", parsed.content)
            break

    except Exception as e:
        print("❌ Error:", str(e))
        break