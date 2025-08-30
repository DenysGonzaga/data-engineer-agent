import json
import boto3
from fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP("DataEngineerMCPServer")


if __name__ == "__main__":
    mcp.run()
