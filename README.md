# Agent Framework Sample

This sample demonstrates how to create and use a simple AI agent with Azure AI as the backend.

## Setup

1. **Create a virtual environment** (already done):
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

2. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   
   Create a `.env` file from the example:
   ```powershell
   Copy-Item .env.example .env
   ```
   
   Then edit `.env` and set:
   - `AZURE_AI_PROJECT_ENDPOINT`: Your Azure AI project endpoint
   - `AZURE_AI_MODEL_DEPLOYMENT_NAME`: The name of your model deployment

   Alternatively, set them directly in your shell:
   ```powershell
   $env:AZURE_AI_PROJECT_ENDPOINT = "your-endpoint-here"
   $env:AZURE_AI_MODEL_DEPLOYMENT_NAME = "your-deployment-name-here"
   ```

4. **Authenticate with Azure CLI**:
   ```powershell
   az login
   ```

## Running the Sample

```powershell
python basic_agent_sample.py
```

## What the Sample Does

The sample creates a ChatAgent with:
- **Backend**: AzureAIAgentClient using Azure CLI credentials
- **Instructions**: "You are good at telling jokes."
- **Prompt**: Asks the agent to tell a joke about a pirate

The agent will respond with a pirate-themed joke using the configured Azure AI model.
