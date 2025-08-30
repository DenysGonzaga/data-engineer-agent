import os
import sys
import boto3

from rich import print
from rich.prompt import Prompt

from dotenv import load_dotenv

from strands import tool
from strands import Agent
from strands.models import BedrockModel

load_dotenv()
bucket_workdir = os.getenv("AWS_DATA_BUCKET")

DE_SYSTEM_PROMPT = f"""You are a data engineer assistant.

At this moment, you only authorize to:

1. Only upload CSV files using s3 bucket "{bucket_workdir}" on "landing" key.
2. Parse and Read CSV files using Pandas SDK.
3. Only write data in "{bucket_workdir}" on "processed" key.
4. Query data in Amazon Athena.
5. You aren't authorize to perform no other task in AWS Cloud.
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
    while True:
        print("\n")
        print(f"BEDROCK MODEL: {os.getenv("AWS_BEDROCK_MODEL_ID")}")
        prompt_input = Prompt.ask("data-engineer-agent:>>> ")
        de_agent = Agent(model=bedrock_model,
            system_prompt=DE_SYSTEM_PROMPT,
            tools=[],
        )
        
        de_agent(prompt_input)

if __name__ == "__main__":
    main()