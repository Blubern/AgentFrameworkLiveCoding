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


async def main() -> None:
    """
    Main function to run the basic agent sample.
    
    Creates a ChatAgent with AzureAIAgentClient and asks it to tell a joke.
    The agent is configured with custom instructions to be good at telling jokes.
    """
    os.environ["AZURE_AI_PROJECT_ENDPOINT"] = "https://azureaifoundryplayground.services.ai.azure.com/api/projects/AiProjectPlayground"
    os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"] = "gpt-4o-mini"
    # Print environment variables for debugging
    print("=== Environment Variables ===")
    print(f"AZURE_AI_PROJECT_ENDPOINT: {os.getenv('AZURE_AI_PROJECT_ENDPOINT', 'NOT SET')}")
    print(f"AZURE_AI_MODEL_DEPLOYMENT_NAME: {os.getenv('AZURE_AI_MODEL_DEPLOYMENT_NAME', 'NOT SET')}")
    print("============================")
    print()

    myCredentials = AzureCliCredential()
    
    # Print credential information
    print("=== Credential Information ===")
    print(f"Credential Type: {type(myCredentials)}")
    print(f"Credential Object: {myCredentials}")
    
    # Try to get a token to verify authentication
    try:
        token = await myCredentials.get_token("https://management.azure.com/.default")
        print(f"✓ Successfully authenticated!")
        print(f"Token (first 50 chars): {token.token[:50]}...")
        print(f"Token expires on: {token.expires_on}")
        
        # Parse JWT token to extract user information
        print("\n=== User Information ===")
        try:
            # JWT tokens have 3 parts separated by dots: header.payload.signature
            token_parts = token.token.split('.')
            if len(token_parts) >= 2:
                # Decode the payload (second part)
                # Add padding if needed for base64 decoding
                payload = token_parts[1]
                padding = '=' * (4 - len(payload) % 4)
                decoded_payload = base64.b64decode(payload + padding)
                token_data = json.loads(decoded_payload)
                
                # Display user information
                print(f"User Principal Name (upn): {token_data.get('upn', 'N/A')}")
                print(f"Name: {token_data.get('name', 'N/A')}")
                print(f"Email: {token_data.get('email', 'N/A')}")
                print(f"Object ID (oid): {token_data.get('oid', 'N/A')}")
                print(f"Tenant ID (tid): {token_data.get('tid', 'N/A')}")
                print(f"Application ID (appid): {token_data.get('appid', 'N/A')}")
                
                print("\n=== Full Token Payload ===")
                print(json.dumps(token_data, indent=2))
            else:
                print("Unable to parse token - unexpected format")
        except Exception as parse_error:
            print(f"Error parsing token: {parse_error}")
        
    except Exception as e:
        print(f"✗ Authentication failed: {e}")
    
    print("============================")
    print()

    credential = myCredentials
    async with ChatAgent(
        chat_client=AzureAIAgentClient(async_credential=credential),
        instructions="You are good at telling jokes."
    ) as agent:
        # Run the agent with a prompt
        result = await agent.run("Tell me a joke about a pirate.")
        print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
