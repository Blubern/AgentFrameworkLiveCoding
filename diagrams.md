# Agent Framework Diagrams

This document contains various Mermaid diagrams for the Agent Framework project.

## 1. Use Case Diagram

```mermaid
graph TB
    User((User))
    
    User -->|uses| UC1[Create Basic Agent]
    User -->|uses| UC2[Run Agent with Thread]
    User -->|uses| UC3[Extract Structured Output]
    User -->|uses| UC4[Use Custom Tools]
    
    UC1 -->|extends| UC5[Configure Azure Credentials]
    UC2 -->|extends| UC5
    UC3 -->|extends| UC5
    UC4 -->|extends| UC5
    
    UC2 -->|includes| UC6[Maintain Conversation Context]
    UC3 -->|includes| UC7[Define Pydantic Model]
    UC4 -->|includes| UC8[Register AI Functions]
    
    AzureAI[Azure AI Service]
    
    UC1 -.->|authenticates with| AzureAI
    UC2 -.->|authenticates with| AzureAI
    UC3 -.->|authenticates with| AzureAI
    UC4 -.->|authenticates with| AzureAI
```

## 2. Class Diagram

```mermaid
classDiagram
    class ChatAgent {
        -chat_client: AzureAIAgentClient
        -instructions: str
        -tools: Optional[Function]
        +__init__(chat_client, instructions, tools)
        +run(prompt, thread, response_format) AgentResponse
        +get_new_thread() Thread
        +__aenter__()
        +__aexit__()
    }
    
    class AzureAIAgentClient {
        -async_credential: AzureCliCredential
        -endpoint: str
        -model_deployment: str
        +__init__(async_credential)
        +send_message(message) Response
    }
    
    class AzureCliCredential {
        +get_token(scope) AccessToken
    }
    
    class Thread {
        -thread_id: str
        -messages: List[Message]
        +add_message(message)
        +get_history() List[Message]
    }
    
    class AgentResponse {
        +text: str
        +value: Optional[BaseModel]
    }
    
    class PersonInfo {
        +name: Optional[str]
        +age: Optional[int]
        +occupation: Optional[str]
    }
    
    class AIFunction {
        +name: str
        +description: str
        +function: Callable
        +execute(*args, **kwargs)
    }
    
    BaseModel <|-- PersonInfo
    ChatAgent --> AzureAIAgentClient : uses
    AzureAIAgentClient --> AzureCliCredential : authenticates
    ChatAgent --> Thread : manages
    ChatAgent --> AgentResponse : returns
    ChatAgent --> AIFunction : uses
    AgentResponse --> PersonInfo : contains
```

## 3. Package Diagram

```mermaid
graph TB
    subgraph "Application Layer"
        A1[basic_agent_sample.py]
        A2[basic_agent_with_Thread.py]
        A3[basic_agent_with_structure_output.py]
        A4[basic_agent_with_Thread_and_local_Tool.py]
    end
    
    subgraph "Agent Framework Package"
        B1[ChatAgent]
        B2[Thread]
        B3[AgentResponse]
        B4[ai_function decorator]
    end
    
    subgraph "Azure Integration Package"
        C1[AzureAIAgentClient]
    end
    
    subgraph "Azure Identity Package"
        D1[AzureCliCredential]
    end
    
    subgraph "Data Models Package"
        E1[Pydantic BaseModel]
        E2[PersonInfo]
    end
    
    subgraph "Azure AI Service"
        F1[Azure AI Foundry]
        F2[GPT-4o-mini Model]
    end
    
    A1 --> B1
    A2 --> B1
    A2 --> B2
    A3 --> B1
    A3 --> E2
    A4 --> B1
    A4 --> B2
    A4 --> B4
    
    B1 --> C1
    B1 --> B2
    B1 --> B3
    
    C1 --> D1
    C1 --> F1
    
    E2 -.->|extends| E1
    
    F1 --> F2
```

## 4. Sequence Diagram - Basic Agent Flow

```mermaid
sequenceDiagram
    participant User
    participant main
    participant ChatAgent
    participant AzureAIAgentClient
    participant AzureCliCredential
    participant AzureAI as Azure AI Service
    
    User->>main: Run script
    main->>AzureCliCredential: Create credential
    activate AzureCliCredential
    AzureCliCredential-->>main: Return credential
    deactivate AzureCliCredential
    
    main->>ChatAgent: Create agent (client, instructions)
    activate ChatAgent
    ChatAgent->>AzureAIAgentClient: Initialize client
    activate AzureAIAgentClient
    AzureAIAgentClient-->>ChatAgent: Client ready
    deactivate AzureAIAgentClient
    
    main->>ChatAgent: run(prompt)
    ChatAgent->>AzureCliCredential: get_token()
    activate AzureCliCredential
    AzureCliCredential-->>ChatAgent: Access token
    deactivate AzureCliCredential
    
    ChatAgent->>AzureAIAgentClient: send_message(prompt)
    activate AzureAIAgentClient
    AzureAIAgentClient->>AzureAI: API call with token
    activate AzureAI
    AzureAI-->>AzureAIAgentClient: Response
    deactivate AzureAI
    AzureAIAgentClient-->>ChatAgent: Response
    deactivate AzureAIAgentClient
    
    ChatAgent-->>main: AgentResponse
    deactivate ChatAgent
    
    main->>User: Display result
```

## 5. Sequence Diagram - Agent with Thread and Tools

```mermaid
sequenceDiagram
    participant User
    participant main
    participant ChatAgent
    participant Thread
    participant WeatherTool as get_weather tool
    participant AzureAI as Azure AI Service
    
    User->>main: Run script
    main->>ChatAgent: Create agent (tools=get_weather)
    activate ChatAgent
    
    main->>ChatAgent: get_new_thread()
    ChatAgent->>Thread: Create new thread
    activate Thread
    Thread-->>ChatAgent: Return thread
    deactivate Thread
    ChatAgent-->>main: Return thread
    
    main->>ChatAgent: run("Write book about Belfast", thread)
    ChatAgent->>AzureAI: Send prompt + available tools
    activate AzureAI
    AzureAI-->>ChatAgent: Request tool call (get_weather)
    deactivate AzureAI
    
    ChatAgent->>WeatherTool: get_weather("Belfast")
    activate WeatherTool
    WeatherTool-->>ChatAgent: "Weather is cloudy, 15°C"
    deactivate WeatherTool
    
    ChatAgent->>AzureAI: Send tool result
    activate AzureAI
    AzureAI-->>ChatAgent: Complete response with weather
    deactivate AzureAI
    
    ChatAgent->>Thread: Store message
    ChatAgent-->>main: AgentResponse (book)
    
    main->>ChatAgent: run("Summarize in 5 points", thread)
    ChatAgent->>Thread: Get conversation history
    activate Thread
    Thread-->>ChatAgent: Previous messages
    deactivate Thread
    
    ChatAgent->>AzureAI: Send with context
    activate AzureAI
    AzureAI-->>ChatAgent: Summary response
    deactivate AzureAI
    
    ChatAgent->>Thread: Store message
    ChatAgent-->>main: AgentResponse (summary)
    deactivate ChatAgent
    
    main->>User: Display results
```

## 6. Activity Diagram - Agent Execution Flow

```mermaid
flowchart TD
    Start([Start]) --> SetEnv[Set Environment Variables]
    SetEnv --> CreateCred[Create Azure CLI Credential]
    CreateCred --> CreateAgent[Create ChatAgent Instance]
    CreateAgent --> CheckThread{Need Thread<br/>Context?}
    
    CheckThread -->|Yes| GetThread[Get New Thread]
    CheckThread -->|No| CheckFormat{Need Structured<br/>Output?}
    GetThread --> CheckFormat
    
    CheckFormat -->|Yes| DefineModel[Define Pydantic Model]
    CheckFormat -->|No| CheckTools{Need Custom<br/>Tools?}
    DefineModel --> CheckTools
    
    CheckTools -->|Yes| RegisterTools[Register AI Functions]
    CheckTools -->|No| RunAgent[Run Agent with Prompt]
    RegisterTools --> RunAgent
    
    RunAgent --> Authenticate[Authenticate with Azure]
    Authenticate --> SendRequest[Send Request to Azure AI]
    SendRequest --> CheckToolCall{Tool Call<br/>Required?}
    
    CheckToolCall -->|Yes| ExecuteTool[Execute Local Tool]
    CheckToolCall -->|No| ProcessResponse[Process Response]
    ExecuteTool --> SendToolResult[Send Tool Result to AI]
    SendToolResult --> ProcessResponse
    
    ProcessResponse --> CheckStructured{Structured<br/>Output?}
    CheckStructured -->|Yes| ParseModel[Parse to Pydantic Model]
    CheckStructured -->|No| ExtractText[Extract Text Response]
    ParseModel --> StoreThread{Thread<br/>Exists?}
    ExtractText --> StoreThread
    
    StoreThread -->|Yes| SaveToThread[Save to Thread History]
    StoreThread -->|No| ReturnResponse[Return Response]
    SaveToThread --> ReturnResponse
    
    ReturnResponse --> MoreQueries{More<br/>Queries?}
    MoreQueries -->|Yes| RunAgent
    MoreQueries -->|No| Cleanup[Cleanup Agent Resources]
    Cleanup --> End([End])
```

## 7. State Diagram - Agent Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Uninitialized
    
    Uninitialized --> Initializing: Create Agent
    Initializing --> CredentialSetup: Configure Credentials
    CredentialSetup --> Ready: Authentication Success
    CredentialSetup --> Error: Authentication Failed
    
    Ready --> Processing: Run with Prompt
    Ready --> ThreadCreation: Get New Thread
    
    ThreadCreation --> Ready: Thread Created
    
    Processing --> Authenticating: Request Token
    Authenticating --> SendingRequest: Token Acquired
    Authenticating --> Error: Token Failed
    
    SendingRequest --> WaitingResponse: API Call Made
    WaitingResponse --> ToolExecution: Tool Call Required
    WaitingResponse --> ResponseReceived: Direct Response
    
    ToolExecution --> SendingToolResult: Tool Executed
    SendingToolResult --> WaitingResponse: Tool Result Sent
    ToolExecution --> Error: Tool Failed
    
    ResponseReceived --> ParsingResponse: Process Response
    ParsingResponse --> StructuredOutput: Pydantic Model
    ParsingResponse --> TextOutput: Plain Text
    
    StructuredOutput --> ThreadUpdate: Has Thread
    StructuredOutput --> Completed: No Thread
    TextOutput --> ThreadUpdate: Has Thread
    TextOutput --> Completed: No Thread
    
    ThreadUpdate --> Completed: History Saved
    
    Completed --> Ready: Await Next Request
    Completed --> Cleanup: Close Agent
    
    Error --> Ready: Retry
    Error --> Cleanup: Give Up
    
    Cleanup --> [*]
```

## 8. Component Diagram

```mermaid
graph TB
    subgraph "Application Components"
        App1[Basic Agent Sample]
        App2[Thread-based Agent]
        App3[Structured Output Agent]
        App4[Tool-enabled Agent]
    end
    
    subgraph "Agent Framework Core"
        Core1[ChatAgent Component]
        Core2[Thread Manager]
        Core3[Response Processor]
        Core4[Tool Registry]
    end
    
    subgraph "Azure Integration Layer"
        Azure1[Azure AI Client]
        Azure2[Credential Manager]
    end
    
    subgraph "External Interfaces"
        Ext1[Azure AI Foundry API]
        Ext2[Azure Identity Service]
    end
    
    subgraph "Data Models"
        Data1[PersonInfo Model]
        Data2[Response Models]
    end
    
    subgraph "Custom Tools"
        Tool1[Weather Tool]
        Tool2[User-defined Functions]
    end
    
    App1 --> Core1
    App2 --> Core1
    App2 --> Core2
    App3 --> Core1
    App3 --> Core3
    App3 --> Data1
    App4 --> Core1
    App4 --> Core4
    App4 --> Tool1
    
    Core1 --> Azure1
    Core2 --> Azure1
    Core3 --> Data2
    Core4 --> Tool2
    
    Azure1 --> Azure2
    Azure1 --> Ext1
    Azure2 --> Ext2
    
    Core1 -.->|Manages| Core2
    Core1 -.->|Uses| Core3
    Core1 -.->|Registers| Core4
```

## 9. Block Diagram - System Architecture

```mermaid
graph TB
    subgraph Client["Client Application Layer"]
        direction TB
        Main[Main Entry Point]
        Config[Configuration]
        Env[Environment Setup]
    end
    
    subgraph Framework["Agent Framework Layer"]
        direction TB
        Agent[ChatAgent]
        Thread[Thread Manager]
        Tools[Tool System]
        Response[Response Handler]
    end
    
    subgraph Integration["Azure Integration Layer"]
        direction TB
        Client_Component[AzureAIAgentClient]
        Auth[Authentication]
        API[API Connector]
    end
    
    subgraph Azure["Azure Services"]
        direction TB
        Foundry[Azure AI Foundry]
        Model[GPT-4o-mini]
        Identity[Azure Identity]
    end
    
    subgraph Data["Data Layer"]
        direction TB
        Models[Pydantic Models]
        Schema[Response Schemas]
    end
    
    Main --> Agent
    Config --> Env
    Env --> Auth
    
    Agent --> Thread
    Agent --> Tools
    Agent --> Response
    Agent --> Client_Component
    
    Response --> Models
    Models --> Schema
    
    Client_Component --> Auth
    Client_Component --> API
    
    Auth --> Identity
    API --> Foundry
    Foundry --> Model
    
    Tools -.->|Custom Functions| Agent
    Thread -.->|Context| Client_Component
```

