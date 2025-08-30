import os
import awswrangler as wr
from fastmcp import FastMCP
from dotenv import load_dotenv

mcp = FastMCP("DataEngineerMCPServer")

load_dotenv()

@mcp.tool
def create_table(path:str, table_name: str, database_name:str) -> int:
    """Given a csv file s3 path, creates a Glue table"""
    df = wr.s3.read_csv("s3://your-bucket-name/your-file.csv")
    wr.catalog.delete_table_if_exists(database=database_name, table=table_name)
    temp_path = f"s3://{os.getenv("AWS_DATA_BUCKET")}/athena-temp/"
    wr.athena.to_iceberg(
        df=df,
        database=database_name,
        table=table_name,
        table_location=path,
        temp_path=temp_path,
    )

if __name__ == "__main__":
    mcp.run(transport="sse", host="127.0.0.1", port=8000)
