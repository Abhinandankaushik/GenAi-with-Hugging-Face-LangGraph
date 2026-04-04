from fastapi import FastAPI,Body
import uvicorn

from ollama import Client



app = FastAPI()
client = Client(
    host="http://localhost:11434"
)



@app.get("/")
def read_root():
    return {"msg": "Hello"}

@app.post("/chat")
def chat(
    message:str = Body(...,description="The Message")
):
    response = client.chat(model="gemma:2b", messages=[
        {"role":"user","content":message}
    ])
    return {"response":response.message.content}

# for manual port configuration
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)