# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(
    title="VoiceOps Orchestrator API",
    description="The central routing hub for the VoiceOps SRE Agent.",
    version="1.0.0"
)
#
# Enterprise standard: Configure CORS properly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include our LangGraph routes
app.include_router(router, prefix="/api")

@app.get("/health")
async def health_check():
    """Simple health check to verify the server is running."""
    return {"status": "healthy", "service": "VoiceOps Core"}