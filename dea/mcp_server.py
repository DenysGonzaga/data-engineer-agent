import os
import awswrangler as wr
from fastmcp import FastMCP
from app_settings import settings, session

mcp = FastMCP("DataEngineerMCPServer")


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
    temp_path = f"s3://{settings.AWS_DATA_BUCKET}/athena-temp/"
    wr.athena.to_iceberg(
        df=df,
        database=database_name,
        table=table_name,
        table_location=table_location,
        temp_path=temp_path,
        boto3_session=session,
    )
    return {
        "status": "success",
        "content": [
            {"text": f"Table '{table_name}' Created."},
        ],
    }


@mcp.tool
def run_sql_athena(query: str, database_name: str):
    df = wr.athena.read_sql_query(
        sql=query, database=database_name, ctas_approach=False, boto3_session=session
    )

    return {"content": [{"type": "json", "json": df.to_dict(orient="records")}]}


@mcp.tool
def list_tables_tool(database_name: str) -> dict:
    client = session.client("glue")
    tables = client.get_tables(DatabaseName=database_name)["TableList"]

    return {"content": [{"type": "json", "json": [t["Name"] for t in tables]}]}


if __name__ == "__main__":
    mcp.run(
        transport="sse",
        host=settings.MCP_SERVER_HOST,
        port=settings.MCP_SERVER_PORT,
    )
