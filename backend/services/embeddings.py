import os
from google import genai
from google.genai import types

api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

EMBEDDING_MODEL = "models/gemini-embedding-001"

import time

def get_embedding(text: str, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=text,
                config=types.EmbedContentConfig(
                    task_type="RETRIEVAL_DOCUMENT",
                    output_dimensionality=768
                )
            )
            if response and response.embeddings:
                return response.embeddings[0].values
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)  # thoda wait karke retry karo
            else:
                raise