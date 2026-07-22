import chromadb
import os
from dotenv import load_dotenv
load_dotenv()
client = chromadb.CloudClient(
    tenant=os.getenv("CHROMA_TENANT"),
    database=os.getenv("CHROMA_DATABASE"),
    api_key=os.getenv("CHROMA_API_KEY")
)

collection = client.get_or_create_collection(name="pdf_data")