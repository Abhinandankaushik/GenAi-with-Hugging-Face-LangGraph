from langchain.messages import AnyMessage
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START,END
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from typing import Optional,Literal
from openai import OpenAI
import os

load_dotenv()


# creating state
class MessagesState(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]
    
client = OpenAI(
    api_key= os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)



def chatbot(state: MessagesState):
    print("Running Chatbot Node...")
    response = client.chat.completions.create(
        model="gemini-3-flash-preview",
        messages=[
            {"role":"user", "content": state.get("user_query")}
        ]
    )
    
    state["llm_output"] = response.choices[0].message.content
    return state

def quality(state: MessagesState):
    print("Running quality code...")
    response =  client.chat.completions.create(
        model="gemini-3-flash-preview",
        messages=[
            {"role" : "system", "content": """if give user query which is come from another 
             LLM call is very descriptive and understandable for begginer like 1st class students'
             then give response from this two litrals : 
             litrals = ["GOOD", "Excelent"]
             else give "BAD" as response nothing extra 
             """},
            {"role":"user", "content": state.get("user_query")}
        ] 
    )
    return response.choices[0].message.content

def evaluate_response(state: MessagesState) -> Literal["endnode","chat_bot2"]:
    print("Running evaluate_response Node...")
   
    if quality(state) != "BAD":
       return "endnode"    

    return "chat_bot2"

def chat_bot2(state: MessagesState):
    print("Running  chat_bot2 Node...")
    response = client.chat.completions.create(
        model="gemini-3-flash-preview",
        messages=[
            {"role":"system", "content" : "Magnifie this query ansser in very descriptive form for begginers"},
            {"role":"user", "content": state.get("user_query")}
        ]
    )
    state["llm_output"] = response.choices[0].message.content
    return state
  
  
def end_node(state:MessagesState):
    print("Running End Node...")
    return state    
    
# init graph builder
graph_builder = StateGraph(MessagesState)


graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("evaluate_response",evaluate_response)
graph_builder.add_node("endnode",end_node)
graph_builder.add_node("chat_bot2",chat_bot2)


graph_builder.add_edge(START,"chatbot")
graph_builder.add_conditional_edges("chatbot",evaluate_response)
graph_builder.add_edge("chat_bot2","endnode")
graph_builder.add_edge("endnode",END)

graph = graph_builder.compile()

updated_state = graph.invoke(MessagesState({"user_query" : "Hey what is 2+2"}))

print(updated_state)