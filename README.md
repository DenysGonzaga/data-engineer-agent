# [Under Construction] Data Engineer Agent

Using Strands Agents and Model Context Protocol (FastMCP) to process small data using AWS SDK for Pandas and Athena.

## Architecture Design

![design](assets/images/de-agent.gif?raw=true)

## Requirements 

Python 3.13.1 under [uv](https://github.com/astral-sh/uv)
```
rich==14.1.0
fastmcp==2.11.3
awswrangler==3.12.1
strands-agents==1.6.0
strands-agents-tools==0.2.5
dynaconf==3.2.11
```

## Configuration file

This app is using DynaConf, you need a file named ```settings.toml``` with all env vars, bellow an example of settings file.

```
MCP_SERVER_HOST="127.0.0.1"
MCP_SERVER_PORT=8000
AGENT_LANGUAGE="Portuguese"
AGENT_SHOW_REASONING="true"
BYPASS_TOOL_CONSENT="true"
AWS_BEDROCK_MODEL_ID="<bedrock model id>"
AWS_GLUE_CATALOG_DATABASE="<glue database>"
AWS_DATA_BUCKET="<bucket used to upload files and for table location>"
AWS_DEFAULT_REGION="us-east-1"
AWS_ACCESS_KEY_ID="<Access Key>"
AWS_SECRET_ACCESS_KEY="<Secret Key>"
AWS_SESSION_TOKEN="<Token>"
```

Bedrock model used must be enabled.
 I won't using any strands tools