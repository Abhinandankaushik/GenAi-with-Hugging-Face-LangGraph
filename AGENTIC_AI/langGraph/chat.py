from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START,END
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

llm = init_chat_model(
    model="gemini-2.5-flash",
    model_provider="google_genai"
)

# creating state
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

# creating node/function    
def chatbot(state: MessagesState):
    response = llm.invoke(state.get("messages"))
    return {"messages" : [response]}

def samplenode(state: MessagesState):
    print("Inside Sample node", state)
    return {"messages": ["Sample node message"]}

# init graph builder
graph_builder = StateGraph(MessagesState)

# register node in graph builder
graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("samplenode",samplenode)

# (START) -> chatbot -> samplenode -> (END)
graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot","samplenode")
graph_builder.add_edge("samplenode",END)

# compile the graph
graph = graph_builder.compile()

# run/invoke the graph and you get final state after running all graph node
updated_state = graph.invoke(MessagesState({"messages": ["Hi, This is Agent workflow"]}))
print("updated_state:",updated_state)


""" this is the example how state update after passing from
    one node and accessed by another node:

    # state = {messages: ["hi there"]}
    # node runs: chatbot(state : ["hi there"])-> ["Hi, this is a message from ChatBot Node"]
    # state : {messages : ["hi there","Hi, this is a message from ChatBot Node"]}
"""
