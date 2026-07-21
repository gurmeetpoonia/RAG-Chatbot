from google import genai
from google.genai import types
import os

# API Key env var se uthayega
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

def get_embedding(text: str):
    try:
        response = client.models.embed_content(
            model="models/text-embedding-004",
            contents=text,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT"
            )
        )
        return response.embeddings[0].values
    except Exception as e:
        print(f"Embedding error: {e}")
        raise e