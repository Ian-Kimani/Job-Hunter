import time
from extractors import remoteok, weworkremotely, brightermonday, linkedin, myjobmag
from db_manager import is_job_seen, add_job, init_db
from telegram_bot import send_telegram_message, format_job_message

# Keywords to trigger an alert
TARGET_KEYWORDS = [
    "python", "django", "flask", "fastapi",
    "postgres", "postgresql", "express", "react", "node", "pern",
    "backend", "full stack", "fullstack", "frontend",
    "internship", "attachment", "junior",
    "kenya", "nairobi", "remote", "contract"
]

def run_scraper():
    init_db()          
    print("Starting Job Hunt Engine...")

def contains_keywords(text: str) -> bool:
    """Checks if a string contains any of our target keywords."""
    if not text:
        return False
    text_lower = text.lower()
    for keyword in TARGET_KEYWORDS:
        if keyword in text_lower:
            return True
    return False

def detect_tech_stack(text: str) -> list:
    """Finds all tech stack matches in the text."""
    if not text:
        return []
    text_lower = text.lower()
    found = []
    # Key technologies to explicitly tag
    tech_keywords = ["python", "django", "flask", "fastapi", "react", "node", "postgres", "express", "aws", "docker", "pern", "javascript", "sql"]
    for tech in tech_keywords:
        if tech in text_lower:
            found.append(tech.capitalize())
    return list(set(found))

def is_relevant_job(job: dict) -> bool:
    """Determines if a job is relevant based on title and tags, and updates tech stack."""
    # Build a combined text to search
    combined_text = str(job.get('title', '')) + " " + str(job.get('snippet', ''))
    
    # Auto-detect stack
    job['tech_stack'] = detect_tech_stack(combined_text)
    
    # Check title
    if contains_keywords(job.get('title', '')):
        return True
    
    # Check tags
    tags = job.get('tags', [])
    for tag in tags:
        if contains_keywords(str(tag)):
            return True
            
    return False

def run_scraper():
    print("Starting Job Hunt Engine...")
    
    # 1. Collect jobs from all sources
    all_jobs = []
    print("Fetching from RemoteOK...")
    all_jobs.extend(remoteok.fetch_jobs())
    print("Fetching from WeWorkRemotely...")
    all_jobs.extend(weworkremotely.fetch_jobs())
    print("Fetching from BrighterMonday...")
    all_jobs.extend(brightermonday.fetch_jobs())
    print("Fetching from LinkedIn...")
    all_jobs.extend(linkedin.fetch_jobs())
    print("Fetching from MyJobMag...")
    all_jobs.extend(myjobmag.fetch_jobs())
    
    print(f"Total jobs collected: {len(all_jobs)}")
    
    new_matches = 0
    
    # 2. Process and Filter
    for job in all_jobs:
        job_id = job['id']
        
        # Skip if already in database
        if is_job_seen(job_id):
            continue
            
        # Check if job matches our PERN/Python/Remote/Kenya keywords
        if is_relevant_job(job):
            # Save to database to prevent duplicate alerts
            add_job(job_id, job['title'], job['company'], job['source'])
            
            # Send Telegram Alert
            msg = format_job_message(job)
            send_telegram_message(msg)
            print(f"ALERT SENT: {job['title']} at {job['company']}")
            new_matches += 1
            
            # Sleep briefly to avoid Telegram rate limits
            time.sleep(1)
        else:
            # Save non-relevant jobs to DB too, so we don't process them again
            add_job(job_id, job['title'], job['company'], job['source'])

    print(f"Finished. Found {new_matches} new matching jobs.")

if __name__ == "__main__":
    run_scraper()
