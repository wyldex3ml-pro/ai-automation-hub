import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import schedule
import time
from datetime import datetime
from agents.classifier.email_classifier import classify_email
from agents.responder.reply_generator import generate_reply
from data.database import init_db, save_lead, get_stats
from dotenv import load_dotenv

load_dotenv()
init_db()

SAMPLE_INBOX = [
    {
        "sender": "john@retailstore.com",
        "subject": "Automate our inventory emails",
        "body": "We send 200 inventory update emails daily to suppliers. Can AI automate this? We are ready to pay."
    },
    {
        "sender": "maria@clinic.com",
        "subject": "Appointment confirmation automation",
        "body": "Our clinic books 50 appointments daily. We need automated confirmation and reminder emails. Urgent requirement."
    },
    {
        "sender": "free_stuff@promo.net",
        "subject": "You won a prize!!!",
        "body": "Claim your free iPhone now. Click here immediately. Limited time only!!!"
    },
    {
        "sender": "ravi@logistics.in",
        "subject": "Delivery notification system",
        "body": "We need automated emails for 1000 daily deliveries. Each customer needs tracking updates. Can you build this?"
    }
]

def process_inbox():
    print(f"\n{'='*60}")
    print(f"Scheduler running at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Processing {len(SAMPLE_INBOX)} emails...")
    print(f"{'='*60}")

    processed = 0
    skipped = 0

    for email in SAMPLE_INBOX:
        try:
            print(f"\nEmail: {email['subject'][:50]}")
            classification = classify_email(
                subject=email["subject"],
                body=email["body"],
                sender=email["sender"]
            )

            reply = generate_reply(email, classification)

            if reply is None:
                print(f"Skipped — {classification['category']}")
                skipped += 1
                continue

            save_lead(
                sender=email["sender"],
                subject=email["subject"],
                body=email["body"],
                classification=classification,
                reply=reply
            )

            print(f"Saved — {classification['category']} | {classification['priority']} priority")
            processed += 1

        except Exception as e:
            print(f"Error processing email: {e}")

    stats = get_stats()
    print(f"\nBatch complete — Processed: {processed} | Skipped: {skipped}")
    print(f"Database totals: {stats}")
    print(f"Next run in 1 hour. Dashboard: http://localhost:5000")

def run_scheduler():
    print("AI Automation Hub — Scheduler Started")
    print("Running first batch now...")
    process_inbox()

    schedule.every(1).hours.do(process_inbox)

    print("\nScheduler active — runs every 1 hour automatically.")
    print("Press Ctrl+C to stop.\n")

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    run_scheduler()