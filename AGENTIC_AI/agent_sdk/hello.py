from dotenv import load_dotenv

from agents import Agent, Runner

load_dotenv()

# Define an agent
hello_agent = Agent[any](
    name="hello world agent",
    instructions="You are an agent which greets user"
)


result = Runner.run_sync(hello_agent,"I am abhi")

print(result.final_output)