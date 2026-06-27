import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

REPLY_PROMPT = """You are a professional business assistant writing email replies on behalf of an AI automation agency called "AI Automation Hub".

Write a reply email based on this information:

ORIGINAL EMAIL FROM: {sender}
SUBJECT: {subject}
THEIR MESSAGE: {body}
CLASSIFICATION: {category}
TONE TO USE: {tone}

Rules:
- Keep it under 150 words
- Sound human and warm, not robotic
- Do NOT use "I hope this email finds you well"
- End with a clear call to action
- Sign off as "The AI Automation Hub Team"

Write ONLY the email body. No subject line. No extra explanation.
"""

def call_groq(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 512
    }
    response = requests.post(GROQ_URL, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"].strip()

def generate_reply(email_data, classification):
    if classification["suggested_reply_tone"] == "do_not_reply":
        return None

    prompt = REPLY_PROMPT.format(
        sender=email_data["sender"],
        subject=email_data["subject"],
        body=email_data["body"],
        category=classification["category"],
        tone=classification["suggested_reply_tone"]
    )

    return call_groq(prompt)