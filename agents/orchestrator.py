import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.classifier.email_classifier import classify_email
from agents.responder.reply_generator import generate_reply
from data.database import init_db, save_lead, get_stats
from dotenv import load_dotenv

load_dotenv()
init_db()

def process_email(email):
    print(f"\n{'='*60}")
    print(f"Processing: {email['subject']}")
    print(f"From: {email['sender']}")

    classification = classify_email(
        subject=email["subject"],
        body=email["body"],
        sender=email["sender"]
    )

    print(f"Category : {classification['category']}")
    print(f"Priority : {classification['priority']}")
    print(f"Sentiment: {classification['sentiment']}")
    print(f"Summary  : {classification['summary']}")

    reply = generate_reply(email, classification)

    if reply is None:
        print("Action: SKIPPED — spam")
        return

    save_lead(
        sender=email["sender"],
        subject=email["subject"],
        body=email["body"],
        classification=classification,
        reply=reply
    )

    print(f"\nReply Draft:\n{reply}")
    print("Saved to database.")

if __name__ == "__main__":
    sample_emails = [
        {
            "sender": "amit@techcorp.in",
            "subject": "Need AI automation for our sales team",
            "body": "We have a 20 person sales team drowning in follow up emails. We heard AI can automate this. We have budget approved and need this done in 2 weeks."
        },
        {
            "sender": "newsletter@deals.com",
            "subject": "50% off today only!!!",
            "body": "Buy now get discount click here limited time offer."
        },
        {
            "sender": "sara@hospital.org",
            "subject": "Patient appointment reminders automation",
            "body": "We are a hospital and need to automate appointment reminder emails for 500 patients daily. Can your system handle this?"
        },
        {
            "sender": "dev@startup.io",
            "subject": "Technical support needed",
            "body": "We integrated your API last week but we are getting timeout errors on large batches. Can someone from technical team help us?"
        }
    ]

    for email in sample_emails:
        process_email(email)

    print(f"\n{'='*60}")
    print("FINAL DATABASE STATS:")
    stats = get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")