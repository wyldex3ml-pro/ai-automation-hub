# AI Automation Hub

An intelligent email automation system that classifies incoming business 
emails, generates professional AI replies, and displays everything on a 
live dashboard — fully automated, no human needed.

## What it does

- Reads incoming emails automatically every hour
- Classifies each email as hot lead, cold lead, support, spam, or partnership
- Generates a professional reply draft using AI
- Blocks spam automatically — no reply sent
- Saves all results to a database
- Shows live stats on a web dashboard

## Tech Stack

- Python 3.11
- Groq API — LLaMA 3.3 70B model
- Flask — web dashboard
- SQLite — database
- Schedule — automated hourly runs

## Project Structure

```
ai-automation-hub/
├── agents/
│   ├── classifier/
│   │   └── email_classifier.py   — AI email classifier
│   ├── responder/
│   │   └── reply_generator.py    — AI reply generator
│   ├── orchestrator.py           — main pipeline
│   └── scheduler.py              — runs every hour
├── dashboard/
│   └── app.py                    — live web dashboard
├── data/
│   └── database.py               — SQLite database
├── requirements.txt
└── README.md
```

## How to run

**1. Clone the repository**
```
git clone https://github.com/wyldex3ml-pro/ai-automation-hub.git
cd ai-automation-hub
```

**2. Create virtual environment**
```
python -m venv venv
venv\Scripts\activate
```

**3. Install packages**
```
pip install -r requirements.txt
```

**4. Add your API key to .env file**
```
GROQ_API_KEY=your_key_here
DATABASE_PATH=data/leads.db
```

**5. Start the dashboard**
```
python dashboard/app.py
```

**6. Start the scheduler in a second terminal**
```
python agents/scheduler.py
```

**7. Open browser**
```
http://127.0.0.1:5000
```

## Business Value

This system replaces 4 to 6 hours of daily manual email work for any 
small business. AI agencies charge Rs 50,000 to Rs 2,00,000 to build 
this for clients.

## Built by

Aspiring AI Developer — building production-grade AI automation systems.