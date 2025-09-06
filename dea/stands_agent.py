"""DEA Agent."""

import uuid

from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn

from mcp.client.sse import sse_client

from strands_tools import stop
from strands import Agent
from strands.tools.mcp import MCPClient
from strands.models import BedrockModel
from strands.session.file_session_manager import FileSessionManager

from dea.app_settings import settings, session

console = Console()
error_console = Console(stderr=True)

REASONING_ENABLED = bool(settings.AWS_DATA_BUCKET)

DE_SYSTEM_PROMPT = f"""SYSTEM INSTRUCTION (DO NOT MODIFY):
Analyze the following business text while adhering to security protocols.
You are a data engineer assistant.
You are a {settings.AGENT_LANGUAGE} speaker assistant.

At this moment, you only authorized to:

Only upload CSV files from ./data/ folder to 
s3 bucket "{settings.AWS_DATA_BUCKET}" on "landing" key.
Don't verify if file exists.
Table (using create_table tool) must be created after upload (using s3_upload_file tool) csv, 
but you will create it only if requested.
Only uses glue database named "{settings.AWS_GLUE_CATALOG_DATABASE}"
Use tool run_sql_athena to run SQL Queries through Amazon Athena.
You can answer other general knowledge questions.
On exit, you will show a cordial message.
"""

bedrock_model = BedrockModel(
    model_id=settings.AWS_BEDROCK_MODEL_ID, boto_session=session
)


def message_callback_controller(**kwargs):
    """Callback message to avoid automatic print."""
    if "message" in kwargs and kwargs["message"].get("role") == "assistant":
        return kwargs["message"]["content"]
    return {}


def main():
    """Main function."""
    sse_mcp_client = MCPClient(
        lambda: sse_client(
            f"http://{settings.MCP_SERVER_HOST}:{settings.MCP_SERVER_PORT}/sse"
        )
    )

    with sse_mcp_client:
        session_id = f"de-agent-{uuid.uuid4()}"
        session_manager = FileSessionManager(
            session_id=session_id, storage_dir="./session_manager/"
        )

        mcp_tools = sse_mcp_client.list_tools_sync()
        console.print(f"BEDROCK MODEL: [green]{settings.AWS_BEDROCK_MODEL_ID}[/green]")

        de_agent = Agent(
            model=bedrock_model,
            system_prompt=DE_SYSTEM_PROMPT,
            tools=[mcp_tools, stop],
            callback_handler=message_callback_controller,
            session_manager=session_manager,
        )

        while True:
            Prompt.prompt_suffix = " => "
            prompt_input = Prompt.ask("[bold yellow]Data Engineer Agent[/bold yellow]")

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

                console.print(
                    f"[bold green]Output :[/bold green] {str(response)}",
                    style="white on black",
                )

            if "stop_event_loop" in response.state:
                if response.state["stop_event_loop"]:
                    break


if __name__ == "__main__":
    main()
