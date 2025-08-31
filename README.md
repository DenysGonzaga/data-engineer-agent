# [Under Construction] Data Engineer Agent

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv) 
[![MIT License](https://img.shields.io/badge/license-MIT-007EC7.svg?style=flat-square)](/LICENSE)
![python](https://img.shields.io/badge/Python%3A%203.13-blue)


Using Strands Agents and Model Context Protocol (FastMCP) to process small data using AWS SDK for Pandas and Athena.

## Architecture Design

![design](assets/images/de-agent.gif?raw=true)

## Requirements 

🚀 Powered by [uv](https://github.com/astral-sh/uv).

🐍 Everything that you need you will find on pyproject.toml.

Just...
```bash
uv sync
```

## Configuration file

This app is using [DynaConf](https://www.dynaconf.com/), create a file named ```settings.toml``` with all env vars.

Bellow an example of settings file.

```toml
[development]
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

-> Explain some vars

## Amazon Bedrock

Access to Amazon Bedrock foundation models, with the exception of OpenAI gpt-oss-120b and gpt-oss-20b models, isn't granted by default. 

📘 You can request access, or modify access, to foundation models only by using the Amazon Bedrock console. Read [more](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html).