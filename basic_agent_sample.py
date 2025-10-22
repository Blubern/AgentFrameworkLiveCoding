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
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential


async def main() -> None:
    """
    Main function to run the basic agent sample.
    
    Creates a ChatAgent with AzureAIAgentClient and asks it to tell a joke.
    The agent is configured with custom instructions to be good at telling jokes.
    """
    async with (
        AzureCliCredential() as credential,
        ChatAgent(
            chat_client=AzureAIAgentClient(async_credential=credential),
            instructions="You are good at telling jokes."
        ) as agent,
    ):
        # Run the agent with a prompt
        result = await agent.run("Tell me a joke about a pirate.")
        print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
