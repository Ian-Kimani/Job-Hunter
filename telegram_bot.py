import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(text: str):
    """Sends a formatted message to your Telegram Chat."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Error: Missing Telegram credentials in .env file.")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")
        return False

def format_job_message(job: dict) -> str:
    """Formats a job dictionary into a nice Telegram HTML message."""
    tech_stack = ', '.join(job.get('tech_stack', []))
    snippet = job.get('snippet', 'No description snippet available.')[:250] + "..." if job.get('snippet') else ""
    
    return f"""
🚀 <b>NEW JOB MATCH!</b> 🚀

<b>Role:</b> {job.get('title', 'Unknown Title')}
<b>Company:</b> {job.get('company', 'Unknown Company')}

💡 <b>Tech Stack:</b> {tech_stack if tech_stack else 'General / Not Specified'}
📝 <b>Snippet:</b> <i>{snippet}</i>

🔗 <a href="{job.get('link', '#')}">Apply / View Job Here</a>
"""

if __name__ == "__main__":
    # Test the bot
    test_job = {
        "title": "Senior Python Developer (Test)",
        "company": "Antigravity Inc.",
        "source": "System Test",
        "tags": ["Python", "Remote"],
        "tech_stack": ["Python", "Django", "Postgres"],
        "snippet": "We are looking for a highly skilled developer. Experience with Python, Django, and database optimization in Postgres is required.",
        "link": "https://google.com"
    }
    msg = format_job_message(test_job)
    success = send_telegram_message(msg)
    if success:
        print("Test message sent successfully! Check your Telegram.")
    else:
        print("Test message failed.")
