from google import genai
from dotenv import load_dotenv
from google.genai import types
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def get_embedding(text: str, task_type: str = "RETRIEVAL_DOCUMENT"):
    response = client.models.embed_content(
        model="models/text-embedding-004",
        contents=text,
        config=types.EmbedContentConfig(task_type=task_type)
    )

    return response.embeddings[0].values