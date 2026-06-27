import os
from dotenv import load_dotenv
from groq import Groq
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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
    result = json.loads(raw)
    return result

if __name__ == "__main__":
    test_emails = [
        {
            "subject": "Interested in your AI automation services",
            "body": "Hi, I run a small e-commerce business and spending 4 hours a day on emails. Can you automate this? Budget is not an issue. Want to start this week.",
            "sender": "rahul@shopfast.in"
        },
        {
            "subject": "MAKE MONEY FAST!!!",
            "body": "Click here to earn 10000 per day from home. Limited offer!!!",
            "sender": "spam@random.com"
        },
        {
            "subject": "Partnership opportunity",
            "body": "Hi, we are a digital marketing agency and would love to explore a partnership with your AI company. Can we schedule a call?",
            "sender": "priya@marketingpro.com"
        }
    ]

    for email in test_emails:
        print(f"\nProcessing: {email['subject']}")
        print(f"From: {email['sender']}")
        result = classify_email(**email)
        print(f"Result: {json.dumps(result, indent=2)}")
        print("-" * 50)