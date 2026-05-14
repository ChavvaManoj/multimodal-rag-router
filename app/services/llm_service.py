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
            "estimated_cost": 0,
            "answer": "No relevant information found."
        }

    # Query classification
    query_type = classify_query(query)

    # Router v2 model selection
    if query_type == "simple":
        selected_model = "gpt-4o-mini"
        estimated_cost = "low"
    elif query_type == "moderate":
        selected_model = "gpt-4o"
        estimated_cost = "medium"
    else:
        selected_model = "gpt-4.1"
        estimated_cost = "high"

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
        "estimated_cost": estimated_cost,
        "answer": response.choices[0].message.content
    }