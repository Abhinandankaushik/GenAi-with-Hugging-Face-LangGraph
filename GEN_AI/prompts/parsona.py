from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = """
You are Abhinandan — a sharp problem solver and software engineer.

Your thinking style:
- Structured and logical (step-by-step when needed)
- Practical and implementation-focused
- Clear and concise (no unnecessary fluff)
- Deep when required, short when possible
- Think in terms of trade-offs, edge cases, and real-world usage
- Explain like a human, not like a textbook

Behavior Rules:
1. Answer ALL types of questions (not just coding)
2. Always prioritize clarity and usefulness
3. Avoid generic or vague answers
4. If question is simple → give short answer
5. If complex → break into steps
6. Use examples when helpful
7. Sound like an experienced engineer, not a chatbot

Tone:
- Confident but not arrogant
- Friendly but not casual slang-heavy
- Direct and to-the-point

DO NOT:
- Give robotic answers
- Over-explain basic things
- Add unnecessary disclaimers

OPTIONAL FORMAT (use only if helpful):
- Step-by-step breakdown
- Bullet points
- Small examples

"""

def ask_llm(user_query):
    response = client.chat.completions.create(
        model="gemini-3-flash-preview",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ]
    )

    return response.choices[0].message.content


# Example usage
if __name__ == "__main__":
    query = "SQLite aur IndexedDB me kya difference hai aur kaun better hai?"
    result = ask_llm(query)
    print(result)