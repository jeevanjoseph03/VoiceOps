# app/api/routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from app.agent.graph import voiceops_app

router = APIRouter()

# Pydantic models for strict request/response validation
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    tools_used: list[str] = []

@router.post("/v1/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Takes a text message, runs it through the LangGraph state machine,
    and returns the final AI response.
    """
    try:
        # 1. Format the user input for LangGraph
        initial_state = {
            "messages": [HumanMessage(content=request.message)]
        }
        
        # 2. Invoke the graph asynchronously
        # This will hit your Omen's Llama 3.1 instance over the network
        final_state = await voiceops_app.ainvoke(initial_state)
        
        # 3. Extract the final AI message from the state history
        ai_message = final_state["messages"][-1].content
        
        # (Optional) Extract which tools were called for debugging/UI purposes
        tools_used = []
        for msg in final_state["messages"]:
            if getattr(msg, "name", None) in ["fetch_latest_commit", "create_incident_ticket", "notify_slack_channel"]:
                tools_used.append(msg.name)

        return ChatResponse(response=ai_message, tools_used=tools_used)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))