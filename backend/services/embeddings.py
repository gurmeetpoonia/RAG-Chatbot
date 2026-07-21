import os
from google import genai
from google.genai import types

# Client initialize karein
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

def get_embedding(text: str):
    try:
        # Client direct embed_content method use karein
        response = client.models.embed_content(
            model="text-embedding-004",  # Agar ye tab bhi fail ho, toh below alternative try karein
            contents=text,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT"
            )
        )
        return response.embeddings[0].values
    except Exception as e:
        print(f"Embedding error: {e}")
        # Secondary fallback if 'text-embedding-004' fails
        try:
            response = client.models.embed_content(
                model="gemini-embedding-2",
                contents=text
            )
            return response.embeddings[0].values
        except Exception as fallback_err:
            raise fallback_err