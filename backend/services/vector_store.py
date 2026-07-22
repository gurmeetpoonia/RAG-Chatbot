import chromadb
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("CHROMA_API_KEY")
tenant = os.getenv("CHROMA_TENANT")
database = os.getenv("CHROMA_DATABASE")

if not api_key or not tenant or not database:
    raise ValueError(f"Missing Chroma config! api_key={bool(api_key)}, tenant={bool(tenant)}, database={bool(database)}")

client = chromadb.CloudClient(
    tenant=tenant,
    database=database,
    api_key=api_key
)

collection = client.get_or_create_collection(name="pdf_data")