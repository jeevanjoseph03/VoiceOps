# app/core/config.py
import os
from dotenv import load_dotenv

# Force dotenv to override the terminal's cached variables
load_dotenv(override=True)

class Settings:
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
    WHISPER_BASE_URL = os.getenv("WHISPER_BASE_URL")
    
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
    JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
    SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

settings = Settings()