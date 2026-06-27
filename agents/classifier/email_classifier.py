import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

CLASSIFY_PROMPT = """You are an expert business lead classifier.

Analyse this email and return a JSON object with these exact keys:
- category: one of "hot_lead", "cold_lead", "support", "spam", "partnership"
- priority: one of "high", "medium", "low"
- sentiment: one of "positive", "neutral", "negative"
- summary: one sentence describing what this person wants
- suggested_reply_tone: one of "urgent_and_warm", "professional", "brief_and_helpful", "do_not_reply"

Return ONLY the JSON object. No explanation. No markdown. No code blocks.

EMAIL SUBJECT: {subject}
EMAIL BODY: {body}
EMAIL FROM: {sender}
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

def classify_email(subject, body, sender):
    prompt = CLASSIFY_PROMPT.format(
        subject=subject,
        body=body,
        sender=sender
    )
    raw = call_groq(prompt)

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    result = json.loads(raw)
    return result