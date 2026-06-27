import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

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

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512
    )
    return response.choices[0].message.content.strip()