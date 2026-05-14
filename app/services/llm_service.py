import os
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_answer(query: str, context_chunks: list):
    if not context_chunks:
        return "No relevant information found."

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
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You answer using only provided document context."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content