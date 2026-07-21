import os
from google import genai
from google.genai import types

# Client initialize karein
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

def get_embedding(text: str):
    # Try text-embedding-004 with exact prefix or fallback
    for model_name in ["text-embedding-004", "models/text-embedding-004"]:
        try:
            response = client.models.embed_content(
                model=model_name,
                contents=text
            )
            return response.embeddings[0].values
        except Exception as err:
            last_err = err
            continue
            
    raise last_err