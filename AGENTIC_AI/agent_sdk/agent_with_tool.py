from dotenv import load_dotenv

from agents import Agent, Runner
from agents import WebSearchTool
load_dotenv()

# Define an agent
hello_agent = Agent[any](
    name="hello world agent",
    instructions="You are an agent which greets user",
    tools=[
        WebSearchTool() # Hosted tool (provided by openai)
    ]
)


result = Runner.run_sync(hello_agent,"I am abhi")

print(result.final_output)