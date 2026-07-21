import os
from google import genai
from google.genai import types

api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

EMBEDDING_MODEL = "models/gemini-embedding-001"

def get_embedding(text: str):
    try:
        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT",
                output_dimensionality=768  # match your existing vector DB dimension
            )
        )
        if response and response.embeddings:
            return response.embeddings[0].values
        raise ValueError("Empty embedding response")
    except Exception as e:
        print(f"Embedding error with {EMBEDDING_MODEL}: {e}")
        raise