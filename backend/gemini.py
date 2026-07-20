from google import genai 
from dotenv import load_dotenv
import os 

load_dotenv()

api_key=os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

def ask_gemini( context, question,history):
    prompt = f"""
You are a helpful AI assistant that answers questions strictly using the provided PDF, DOCX,TXT context.

## Core Rules
1. Answer ONLY using the information present in the "Context" section below.
2. If the answer is not found in the context, reply exactly:
   "I couldn't find this information in the uploaded document(s)."
   Do NOT use outside knowledge to fill the gap, even if you know the answer.
3. Use the "History" section only to understand conversation flow (e.g. follow-up questions like "explain more" or "give example"). Never use history as a source of facts — facts must always come from Context.
4. If Context is empty, tell the user no relevant document content was found.

## Formatting Rules (Markdown)
- Use "##" for section headings when the answer has multiple parts.
- Use "-" for bullet points and "1." for numbered steps.
- Use markdown tables for comparisons.
- Bold key terms using "**term**".
- Keep a short 1-2 line introduction before details.
- Keep a short 1-2 line conclusion at the end, only for longer answers.
- For simple factual questions, answer directly in 1-3 sentences — do not force headings/bullets on short answers.
- Never pad the answer with unnecessary filler text.

## History (previous conversation, for context only — not a source of facts)
{history}

## Context (retrieved from the document)
{context}

## Question
{question}

## Answer
"""
    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            
        )


        return response.text

    except Exception as e:

        print("Gemini Error:", e)

        return "Error: Unable to generate answer."
    
def generate_chat_title(question):

    prompt = f"""
Generate a short, descriptive chat title based on the user's question.

Rules:
- Maximum 4 words
- No quotes, no punctuation, no trailing period
- Title case (capitalize main words)
- Must reflect the topic, not just repeat the question verbatim

User Question:
{question}

Title:
"""

    response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            
        )

    return response.text.strip()   