
import json
import os
from dotenv import load_dotenv

# Local
from prompt import SYSTEM_PROMPT
from tools import get_greeting

# Utils
from langchain.agents import create_agent
from langchain.tools import tool

# Models
from langchain.messages import HumanMessage, AIMessage, SystemMessage


load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


# AI Agent
agent = create_agent(
    "openai:gpt-4o-mini",
    system_prompt=SYSTEM_PROMPT,
    tools=[get_greeting]
)

def main():
    display_format = "\n[AGENT]: {0}\n\n[USER]: "
    request = input(display_format.format("I am here to make up your day. Ask me anything"))
    while True:
        messages = [HumanMessage(request)]
        new_messages = agent.invoke({"messages": messages})
        request = input(display_format.format(new_messages["messages"][-1].content))


if __name__ == "__main__":
    main()