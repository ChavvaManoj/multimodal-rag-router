import os
from openai import OpenAI
from dotenv import load_dotenv

from app.services.router_service import classify_query

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_answer(query: str, context_chunks: list):
    if not context_chunks:
        return {
            "query_type": "unknown",
            "model_used": "none",
            "answer": "No relevant information found."
        }

    # Classify query
    query_type = classify_query(query)

    # Model Routing
    if query_type == "simple":
        selected_model = "gpt-4o-mini"
    else:
        selected_model = "gpt-4.1"

    context = "\n\n".join(context_chunks)

    prompt = f"""
You are an AI assistant answering strictly from provided document context.

Context:
{context}

Question:
{query}

Instructions:
- Answer clearly and concisely
- Use only provided context
- If answer is not in context, say so
"""

    response = client.chat.completions.create(
        model=selected_model,
        messages=[
            {
                "role": "system",
                "content": "You answer strictly from provided context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return {
        "query_type": query_type,
        "model_used": selected_model,
        "answer": response.choices[0].message.content
    }