import os
import re
import uuid
import boto3

from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn

from dotenv import load_dotenv

from mcp.client.sse import sse_client

from strands import Agent
from strands.tools.mcp import MCPClient
from strands.models import BedrockModel
from strands.session.file_session_manager import FileSessionManager

load_dotenv()
console = Console()
error_console = Console(stderr=True)

bucket_workdir = os.getenv("AWS_DATA_BUCKET")
reasoning_enabled = True if os.getenv("AWS_DATA_BUCKET", "false") == "true" else False

DE_SYSTEM_PROMPT = f"""You are a data engineer assistant.
You are a {os.getenv("AGENT_LANGUAGE")} speaker assistant.

At this moment, you only authorized to:

Only upload CSV files from ./data/ folder to s3 bucket "{bucket_workdir}" on "landing" key.
Don't verify if file exists.
Table (using create_table) must be created after upload (using s3_upload_file) csv, but you will create it only if requested.
Only uses glue database named "{os.getenv("AWS_GLUE_CATALOG_DATABASE")}"
Explain your reasoning.
You can answer other types of questions.
"""

session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
    region_name=os.getenv("AWS_DEFAULT_REGION"),
)

bedrock_model = BedrockModel(
    model_id=os.getenv("AWS_BEDROCK_MODEL_ID"), boto_session=session
)


def message_callback_controller(**kwargs):
    if "message" in kwargs and kwargs["message"].get("role") == "assistant":
        return kwargs["message"]["content"]


def main():
    sse_mcp_client = MCPClient(
        lambda: sse_client(
            f'http://{os.getenv("MCP_SERVER_HOST")}:{os.getenv("MCP_SERVER_PORT")}/sse'
        )
    )

    with sse_mcp_client:
        session_id = f"de-agent-{uuid.uuid4()}"
        session_manager = FileSessionManager(session_id=session_id, storage_dir='./session_manager/')

        mcp_tools = sse_mcp_client.list_tools_sync()
        console.print(
            f"BEDROCK MODEL: [green]{os.getenv('AWS_BEDROCK_MODEL_ID')}[/green]"
        )

        
        de_agent = Agent(
            model=bedrock_model,
            system_prompt=DE_SYSTEM_PROMPT,
            tools=[mcp_tools],
            callback_handler=message_callback_controller,
            session_manager=session_manager
        )

        err_count = 0
        while True:
            try:
                Prompt.prompt_suffix = " => "
                prompt_input = Prompt.ask(
                    "[bold yellow]Data Engineer Agent[/bold yellow]"
                )

                if len(prompt_input.strip()) == 0:
                    continue


                with Progress(
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(pulse_style="bar.pulse"),
                    TimeElapsedColumn(),
                    transient=True,
                    console=console,
                ) as progress:
                    task = progress.add_task("[cyan]Thinking...", start=False)
                    progress.start_task(task)

                    response = de_agent(prompt_input)
                    progress.update(task, description="[green]Done!")

                m = re.search(r"<thinking>(.*?)</thinking>", str(response), re.DOTALL)
                thinking = m.group(1).strip() if m else None
                message = re.sub(
                    r"<thinking>.*?</thinking>", "", str(response), flags=re.DOTALL
                ).strip()

                print_message = message if message.strip() != "" else thinking
                console.print(
                    f"[bold blue]MESSAGE:[/bold blue] {print_message}",
                    style="white on black",
                )

                if reasoning_enabled:
                    console.print(
                        f"[bold purple]REASONING:[/bold purple] {thinking}",
                        style="white on black",
                    )

                err_count = 0
            except Exception as e:
                error_console.print(f"[red]ERROR: {str(e)}[/red]")
                err_count += 0

            if err_count == 2:
                break


if __name__ == "__main__":
    main()
