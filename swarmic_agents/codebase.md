# Files

swarmic_agents/                              # Main source code package directory
├── test_chat.py                             # Unit tests for chat module with mocked send_payload function
├── chat/                                    # Chat and LLM communication module
│   ├── chat.py                              # LM Studio API client with payload creation, simple_chat, and file_chat functions
│   └── type.py                              # Pydantic models for chat requests, responses, messages, tool calls, and errors
└── jobber/                                  # Job processing system directory
    └── jobber.py                            # Job queue processor that reads agent inbox, sends to LLM, writes to outbox with UUID tracking
    
# chat.py
| function                                           | description                                                |
|----------------------------------------------------|------------------------------------------------------------|
| make_payload(texts: list[str]) -> ChatRequest      | Create a chat request payload from a list of text strings. |
| simple_chat(query: str) -> ChatResponse            | Send a simple text query to the chat API.                  |
| file_chat(file_paths: list[str], query: list[str]) | Send file contents along with queries to the chat API.     |
| send_payload(payload: ChatRequest) -> ChatResponse | Send a chat request payload to the API endpoint.           |

# jobber.py

| Class       | Description                                                             |
|-------------|-------------------------------------------------------------------------|
| Job         | Represents an agent job with inbox/outbox directories and prompt files. |
| JobInfo     | Metadata for a completed job execution.                                 |
| UUIDEncoder | Custom JSON encoder that converts UUID objects to strings.              |

| Function               | Description                                                            |
|------------------------|------------------------------------------------------------------------|
| Job.agent_dir          | Returns the base directory path for the agent.                         |
| Job.inbox              | Returns the inbox directory path for the agent.                        |
| Job.outbox             | Returns the outbox directory path for the agent.                       |
| Job.prompt_dir         | Returns the prompt directory path for the agent.                       |
| Job.get_payload        | Creates a chat request payload from prompt files and an inbox item.    |
| Job.create_directories | Creates the inbox, outbox, and prompt directories for the job.         |
| init_jobs              | Initializes directory structure for all configured jobs.               |
| write_job_db           | Appends job execution metadata to the job database file.               |
| run_jobber             | Processes all inbox items for all jobs and sends them to the chat API. |