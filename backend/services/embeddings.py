import os
from google import genai
from google.genai import types

# Initialize Gemini Client with API Key
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

def get_embedding(text: str):
    """
    Generates text embeddings using Google's active embedding models.
    """
    # Active embedding models in order of priority
    models_to_try = [
        "gemini-embedding-001",
        "text-embedding-005",
        "models/gemini-embedding-001",
        "models/text-embedding-004"
    ]

    last_error = None

    for model_name in models_to_try:
        try:
            response = client.models.embed_content(
                model=model_name,
                contents=text,
                config=types.EmbedContentConfig(
                    task_type="RETRIEVAL_DOCUMENT"
                )
            )
            # Successfully got embedding
            if response and response.embeddings:
                return response.embeddings[0].values
        except Exception as e:
            last_error = e
            print(f"Failed with model {model_name}: {e}")
            continue

    # If all models fail, raise the last encountered error
    print(f"Embedding error: {last_error}")
    raise last_error