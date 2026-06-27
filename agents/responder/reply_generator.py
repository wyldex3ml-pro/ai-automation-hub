import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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


if __name__ == "__main__":
    from agents.classifier.email_classifier import classify_email

    test_emails = [
        {
            "sender": "rahul@shopfast.in",
            "subject": "Interested in your AI automation services",
            "body": "Hi, I run a small e-commerce business and spending 4 hours a day on emails. Can you automate this? Budget is not an issue. Want to start this week."
        },
        {
            "sender": "spam@random.com",
            "subject": "MAKE MONEY FAST!!!",
            "body": "Click here to earn 10000 per day from home. Limited offer!!!"
        },
        {
            "sender": "priya@marketingpro.com",
            "subject": "Partnership opportunity",
            "body": "Hi, we are a digital marketing agency and would love to explore a partnership with your AI company. Can we schedule a call?"
        }
    ]

    for email in test_emails:
        print(f"\nEmail from: {email['sender']}")
        classification = classify_email(
            subject=email["subject"],
            body=email["body"],
            sender=email["sender"]
        )
        print(f"Category: {classification['category']} | Priority: {classification['priority']}")

        reply = generate_reply(email, classification)

        if reply is None:
            print("Reply: SKIPPED — spam detected")
        else:
            print(f"\nGenerated Reply:\n{reply}")
        print("-" * 60)