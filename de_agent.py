import os
import boto3

from rich import print
from rich.prompt import Prompt

from dotenv import load_dotenv

from mcp.client.sse import sse_client
from strands.tools.mcp import MCPClient

from strands import Agent
from strands_tools import use_aws
from strands.models import BedrockModel

load_dotenv()
bucket_workdir = os.getenv("AWS_DATA_BUCKET")

DE_SYSTEM_PROMPT = f"""You are a data engineer assistant.

At this moment, you only authorized to:

Only upload CSV files from ./data/ folder to s3 bucket "{bucket_workdir}" on "landing" key.
Don't verify if file exists.
Table (using create_table) must be created after upload (using s3_upload_file) csv, but you will create it only if requested.
Only uses glue database named "{os.getenv("AWS_GLUE_CATALOG_DATABASE")}" 
"""

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

def main():
    sse_mcp_client = MCPClient(lambda: sse_client("http://127.0.0.1:8000/sse"))

    with sse_mcp_client:
        mcp_tools = sse_mcp_client.list_tools_sync()
        while True:
            print("\n")
            print(f"BEDROCK MODEL: {os.getenv("AWS_BEDROCK_MODEL_ID")}")
            prompt_input = Prompt.ask("data-engineer-agent")
            de_agent = Agent(model=bedrock_model,
                system_prompt=DE_SYSTEM_PROMPT,
                tools=[mcp_tools],
            )
            
            de_agent(prompt_input)

if __name__ == "__main__":
    main()




