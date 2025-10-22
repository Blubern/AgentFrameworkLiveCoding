"""
Basic Agent Sample

This sample demonstrates how to create and use a simple AI agent with Azure AI
as the backend. It creates a basic agent using ChatAgent with AzureAIAgentClient
and custom instructions.

Environment Variables Required:
    - AZURE_AI_PROJECT_ENDPOINT: Your Azure AI project endpoint
    - AZURE_AI_MODEL_DEPLOYMENT_NAME: The name of your model deployment
"""

import asyncio
import os
import json
import base64
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from typing import Annotated
from pydantic import Field
from agent_framework import ai_function

@ai_function(name="weather_tool", description="Retrieves weather information for any location")
def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    return f"The weather in {location} is cloudy with a high of 15°C."

async def main() -> None:
    """
    Main function to run the basic agent sample.
    
    Creates a ChatAgent with AzureAIAgentClient and asks it to tell a joke.
    The agent is configured with custom instructions to be good at telling jokes.
    """
    os.environ["AZURE_AI_PROJECT_ENDPOINT"] = "https://azureaifoundryplayground.services.ai.azure.com/api/projects/AiProjectPlayground"
    os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"] = "gpt-4o-mini"

    myCredentials = AzureCliCredential()
    credential = myCredentials
    async with ChatAgent(
        chat_client=AzureAIAgentClient(async_credential=credential),
        instructions="You are a book writer for programmers",
        tools=get_weather
    ) as agent:
        # Get a new thread after agent is created
        thread = agent.get_new_thread()
        
        # Run the agent with a prompt
        result = await agent.run("Write me a book about Python programming for people in Belfast and put the weather in the Book. With 10 pages.", thread=thread)
        print(result.text)

        result = await agent.run("can you summarize the book in 5 bullet points?", thread=thread)
        print(result.text)

        result = await agent.run("What is the weather in Belfast?", thread=thread)
        print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
