# [Under Construction] Data Engineer Agent

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv) 
[![MIT License](https://img.shields.io/badge/license-MIT-007EC7.svg?style=flat-square)](/LICENSE)
![python](https://img.shields.io/badge/Python%3A%203.13-blue)

Using [Strands Agents](https://strandsagents.com/latest/) and [Tools](https://github.com/strands-agents/tools), AWS Services (s3, Glue, Athena and Bedrock), Apache Iceberg, Model Context Protocol with FastMCP to process small data using AWS SDK for Pandas and Athena.

This agent mainly helps out in the Sandbox Environment by figuring out schemas, query and loading data, and setting up Iceberg tables.

## Architecture Design

![design](assets/images/de-agent.gif?raw=true)

## Requirements 

🚀 Powered by [uv](https://github.com/astral-sh/uv).

🐍 Everything that you need you will find on pyproject.toml.

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
AWS_PROFILE="<profile name>"
```

BYPASS_TOOL_CONSENT = Used by strands to by pass verification of tool usage.

AWS_PROFILE is optional, if provided, other all credential variables, such as AWS_ACCESS_KEY_ID, will be ignored.

## Amazon Bedrock

Access to Amazon Bedrock foundation models, with the exception of OpenAI gpt-oss-120b and gpt-oss-20b models, isn't granted by default. 

we You can request access, or modify access, to foundation models only by using the Amazon Bedrock console. Read [more](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html).

## Future implementations

* Glue Data Quality Creation, Execution and Show Results.
* Knowledge base with columns information.
* Change schema table and column comments.
* Enable and run Glue Iceberg Optimizations.
* New read data formats. (XLSX, Parquet etc)