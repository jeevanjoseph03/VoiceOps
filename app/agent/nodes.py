# app/agent/nodes.py
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from app.core.config import settings

# Import our new real-world tool logic
from app.tools.github_tools import get_latest_commit_logic
from app.tools.jira_tools import create_jira_ticket_logic

@tool
def fetch_latest_commit(repo_name: str) -> str:
    """
    Fetches the latest commit information from a GitHub repository.
    The repo_name must be in the format 'owner/repo' (e.g., 'torvalds/linux').
    """
    return get_latest_commit_logic(repo_name)

@tool
def create_incident_ticket(summary: str, severity: str) -> str:
    """
    Creates a Jira incident ticket for the engineering team.
    Use this strictly when an incident, bug, or failure is reported.
    """
    return create_jira_ticket_logic(summary, severity)

@tool
def notify_slack_channel(channel: str, message: str) -> str:
    """Sends an urgent message to a specific Slack channel."""
    # We will leave Slack mocked just for a moment to test GH and Jira
    return f"Message drafted for {channel}: {message}. (Mocked)"

tools = [fetch_latest_commit, create_incident_ticket, notify_slack_channel]

# Initialize the LLM
llm = ChatOllama(
    model="llama3.1",
    base_url=settings.OLLAMA_BASE_URL,
    temperature=0.1, 
)

llm_with_tools = llm.bind_tools(tools)

async def supervisor_node(state: dict):
    messages = state["messages"]
    response = await llm_with_tools.ainvoke(messages)
    return {"messages": [response]}