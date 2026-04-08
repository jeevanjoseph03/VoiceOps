# app/agent/state.py
from typing import TypedDict, Annotated, List, Dict, Any
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class GraphState(TypedDict):
    # add_messages ensures new messages are appended to the list
    messages: Annotated[List[BaseMessage], add_messages]
    
    # We will use these later for our human-in-the-loop and incident tracking
    pending_tool_calls: List[Dict[str, Any]]
    incident_context: Dict[str, Any]
    awaiting_user_confirmation: bool