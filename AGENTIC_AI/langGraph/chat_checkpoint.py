from langchain.messages import AnyMessage, HumanMessage
from typing_extensions import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langgraph.checkpoint.mongodb import MongoDBSaver
from pymongo import MongoClient
import operator
import os

load_dotenv()

# ✅ Initialize LLM
llm = init_chat_model(
    model="gemini-2.5-flash",
    model_provider="google_genai"
)

# ✅ Define state
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

# ✅ Node function
def chatbot(state: MessagesState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# ✅ Build graph
graph_builder = StateGraph(MessagesState)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# ✅ Create Mongo client ONCE (important)
client = MongoClient(os.environ["MONGO_CONNECTION_STRING"])

# ✅ Compile graph with checkpointer
def compile_graph_with_checkpointer():
    checkpointer = MongoDBSaver(client)
    return graph_builder.compile(checkpointer=checkpointer)

graph = compile_graph_with_checkpointer()

# ✅ Config (thread_id = memory key)
config = {
    "configurable": {
        "thread_id": "abhi"
    }
}

# ==============================
# 🔹 Step 1: Store memory
# ==============================
graph.invoke(
    MessagesState({
        "messages": [HumanMessage(content="hey, my name is abhi")]
    }),
    config
)


print("Let's chat with AI which have memory \n", "Note: Enter 0 to exit\n","*"*30)

# ==============================
# 🔹 Step 2: Retrieve using memory (stream)
# ==============================

while user_query:=input("\nEnter your query: "):
    if user_query == "0":
        break
    
    for chunk in graph.stream(
    MessagesState({
        "messages": [HumanMessage(content=user_query)]
        }),
        config,
        stream_mode="values"
    ):
        chunk["messages"][-1].pretty_print()

print("\n*"*10,"Session Ended","*"*10) 