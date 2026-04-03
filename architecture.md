# Project Name: VoiceOps - Voice-Native SRE Automation Hub

## 1. Core Vision
VoiceOps is a local-first, privacy-preserving voice automation hub designed for DevOps and SRE workflows. It allows an engineer to use natural language voice commands to execute complex software workflows across multiple SaaS platforms (GitHub, Jira, Slack). It is built entirely on open-source, locally hosted AI models to guarantee zero data leakage of enterprise code or infrastructure states.

## 2. Hardware & Network Topology
This project relies on a distributed local architecture to maximize performance without incurring cloud compute costs.

* **Node A (Inference Server - Windows/Omen):** Acts as the heavy-compute backend. 
    * Runs `Ollama` hosting the `Llama 3 (8B)` model.
    * Runs the `Faster-Whisper` audio transcription service.
    * Exposes these services via local network REST/WebSocket APIs.
* **Node B (Orchestration Server - M1 MacBook):** Acts as the primary development and application server.
    * Runs the `FastAPI` application.
    * Hosts the `LangGraph` state machine and agent logic.
    * Manages external API integrations (GitHub, Slack, Jira).
    * Handles the audio I/O from the user.

## 3. Technology Stack
**Strict Rule:** Do not deviate from these libraries without explicit user permission.
* **Backend Framework:** `FastAPI` (Python)
* **Agentic Orchestration:** `langchain` and `langgraph`
* **LLM Provider:** Local `Ollama` (Model: `llama3`)
* **Speech-to-Text (STT):** `faster-whisper`
* **Text-to-Speech (TTS):** `edge-tts` (or `piper`)
* **Tool Integrations:** Standard Python `requests` or official SDKs (e.g., `PyGithub`).
* **Environment Management:** `.env` file (strictly ignored in `.gitignore`)

## 4. LangGraph Architecture
The core reasoning engine is a state machine built with LangGraph.

### 4.1 State Schema (TypedDict)
```python
from typing import TypedDict, Annotated, List, Dict, Any
from langchain_core.messages import BaseMessage

class GraphState(TypedDict):
    messages: Annotated[List[BaseMessage], "The conversation history"]
    pending_tool_calls: List[Dict[str, Any]] # Actions awaiting human-in-the-loop approval
    incident_context: Dict[str, Any] # Extracted context (e.g., latest commit, Jira issue ID)
    awaiting_user_confirmation: bool # Flag for the routing edge
```

### 4.2 Nodes
* **supervisor_node:** Prompts Llama 3 with the current state. Outputs either a conversational response or a structured tool call.
* **github_node:** Executes read-only queries (fetch commits, PRs).
* **jira_node:** Executes write actions (create tickets).
* **slack_node:** Executes notification actions.
* **human_approval_node:** Pauses execution, formats the pending action into speech, and awaits user voice confirmation ("yes/no").

### 4.3 Edges
* **supervisor_router:** Conditional edge. If tool_calls exist, route to the specific tool node. If a high-stakes tool is called (Jira/Slack), route to human_approval_node first. If no tool is called, route to END (trigger TTS).

## 5. Folder Structure
Maintain strict separation of concerns:

```
/
├── architecture.md          # This file (Agent Context)
├── requirements.txt         # Project dependencies
├── .env                     # API keys and network IPs
├── /app
│   ├── main.py              # FastAPI entry point & WebSocket handlers
│   ├── /api
│   │   ├── routes.py        # HTTP and WebSocket endpoints
│   ├── /agent
│   │   ├── graph.py         # LangGraph compilation and workflow definition
│   │   ├── nodes.py         # LangGraph node functions
│   │   ├── state.py         # GraphState definition
│   │   ├── prompts.py       # System prompts for Llama 3
│   ├── /tools
│   │   ├── github_tools.py  # GitHub API wrappers
│   │   ├── jira_tools.py    # Jira API wrappers
│   │   ├── slack_tools.py   # Slack Webhook wrappers
│   ├── /audio
│   │   ├── stt.py           # Faster-Whisper integration
│   │   ├── tts.py           # Text-to-Speech generation
│   ├── /core
│       ├── config.py        # Pydantic BaseSettings for env vars
│       ├── logger.py        # Centralized logging configuration
```

## 6. AI Agent Directives
When generating code or suggesting changes for this repository, the AI must strictly adhere to the following rules:

* **Asynchronous by Default:** All FastAPI endpoints, network requests, and tool executions must use async/await to prevent blocking the audio stream.
* **No Cloud LLMs:** Never suggest importing openai or anthropic. Always use ChatOllama from langchain-community.
* **Graceful Degradation:** External API calls (GitHub, Jira) must be wrapped in try/except blocks. If an API fails, the agent state must reflect the error so the LLM can verbally inform the user.
* **Security:** Never hardcode API keys. Always use the app.core.config.settings object to retrieve variables from .env.
* **Small, Testable Functions:** Keep LangGraph nodes small. A node should only execute the tool and update the state. Complex logic belongs in the /tools directory.