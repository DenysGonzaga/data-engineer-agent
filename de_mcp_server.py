import os
import boto3
import awswrangler as wr
from fastmcp import FastMCP
from dotenv import load_dotenv

mcp = FastMCP("DataEngineerMCPServer")

load_dotenv()

session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
    region_name=os.getenv("AWS_DEFAULT_REGION"),
)


@mcp.tool
def s3_upload_file(local_file_path: str, s3_bucket: str, s3_key: str):
    s3 = session.client("s3")
    return {
        "status": "success",
        "content": [
            {"text": str(s3.upload_file(local_file_path, s3_bucket, s3_key))},
        ],
    }


@mcp.tool
def available_files_to_upload():
    return {
        "status": "success",
        "content": [
            {"json": os.listdir("data")},
        ],
    }


@mcp.tool
def create_table(
    s3_bucket: str, s3_key: str, table_name: str, database_name: str
) -> int:
    """Given a csv file s3 path, creates a Glue table"""
    file_s3_path = f"s3://{s3_bucket}/{s3_key}"
    table_location = f"s3://{s3_bucket}/processed/{table_name}"

    print(file_s3_path, table_name, database_name)
    df = wr.s3.read_csv(file_s3_path, boto3_session=session)
    wr.catalog.delete_table_if_exists(
        database=database_name, table=table_name, boto3_session=session
    )
    temp_path = f"s3://{os.getenv("AWS_DATA_BUCKET")}/athena-temp/"
    wr.athena.to_iceberg(
        df=df,
        database=database_name,
        table=table_name,
        table_location=table_location,
        temp_path=temp_path,
    )
    return {
        "status": "success",
        "content": [
            {"text": f"Table '{table_name}' Created."},
        ],
    }


if __name__ == "__main__":
    mcp.run(
        transport="sse",
        host=os.getenv("MCP_SERVER_HOST"),
        port=int(os.getenv("MCP_SERVER_PORT")),
    )
