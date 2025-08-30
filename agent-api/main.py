import os
import boto3
import logging

from fastapi import FastAPI
from typing import Dict, Any
from pydantic import BaseModel
from dotenv import load_dotenvs

from strands import Agent
from strands_tools import http_request
from strands.models import BedrockModel

app = FastAPI() 

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


DE_SYSTEM_PROMPT = """You are a data engineer assistant.

At this moment, you only authorize to:

1. Parse and Read csv files.
2. Process and save date on s3.
3. Query data in Amazon Athena.]
"""

class AgentPrompt(BaseModel):
    prompt: str


session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
    region_name=os.getenv("AWS_DEFAULT_REGION")
)

bedrock_model = BedrockModel(
    model_id=os.getenv("AWS_BEDROCK_MODEL_ID"),
    boto_session=session
)





def handler(event: Dict[str, Any], _context) -> str:
    leaflet_agent = Agent(model=bedrock_model,
        system_prompt=LEAFLET_SYSTEM_PROMPT,
        tools=[http_request],
    )
    
    response = leaflet_agent(event.get('prompt'))
    return str(response)


handler({'prompt': 'For what omeprazol is indicated ?'}, None)