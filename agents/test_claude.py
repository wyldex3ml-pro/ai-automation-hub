import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_ai(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=1024
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    print("Testing Groq connection...")
    response = ask_ai("Say hello and confirm you are ready to automate businesses with AI.")
    print("\nAI says:")
    print(response)