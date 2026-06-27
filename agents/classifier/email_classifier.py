import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

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

def classify_email(subject, body, sender):
    prompt = CLASSIFY_PROMPT.format(
        subject=subject,
        body=body,
        sender=sender
    )
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512
    )
    raw = response.choices[0].message.content.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    result = json.loads(raw)
    return result