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
from pydantic import BaseModel

class PersonInfo(BaseModel):
    """Information about a person."""
    name: str | None = None
    age: int | None = None
    occupation: str | None = None


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
        instructions="You are a helpful assistant that extracts person information from text."
    ) as agent:
        # Get a new thread after agent is created
        thread = agent.get_new_thread()
        
        # Run the agent with a prompt
        response = await agent.run("There is a person named Alex Morgan, who has always been passionate about technology and innovation. At 34 years old, Alex has accumulated a wealth of experience that makes them a trusted expert in the field. Currently, Alex works as a Software Engineer, focusing on building scalable cloud solutions for enterprise environments. Alex’s journey began with a curiosity for how systems operate, which evolved into a career dedicated to solving complex technical challenges. Over the years, Alex has contributed to projects that empower businesses to adopt modern architectures and improve operational efficiency. Known for a meticulous approach and creative problem-solving skills, Alex often mentors junior developers, sharing best practices and guiding them toward writing clean, maintainable code. Outside of work, Alex enjoys exploring emerging technologies, attending developer conferences, and writing technical blogs to help others learn. Whether tackling performance optimization or implementing cutting-edge frameworks, Alex approaches every challenge with enthusiasm and precision. Fill out the person information please", thread=thread,     response_format=PersonInfo)

        if response.value:
            person_info = response.value
            print(f"Name: {person_info.name}, Age: {person_info.age}, Occupation: {person_info.occupation}")
        else:
            print("No structured data found in response")


if __name__ == "__main__":
    asyncio.run(main())
