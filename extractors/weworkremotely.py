import feedparser
import re

def fetch_jobs():
    """Fetches programming jobs from WeWorkRemotely RSS feed."""
    url = "https://weworkremotely.com/categories/remote-programming-jobs.rss"
    
    try:
        feed = feedparser.parse(url)
        jobs = []
        
        for entry in feed.entries:
            # WeWorkRemotely RSS titles are usually "Company: Job Title"
            title_parts = entry.title.split(": ", 1)
            if len(title_parts) == 2:
                company = title_parts[0]
                title = title_parts[1]
            else:
                company = "Unknown"
                title = entry.title

            # WWR uses GUID as unique ID
            job_id = entry.id if hasattr(entry, 'id') else entry.link
            
            # Basic tags extracted from title or categories if available
            tags = []
            if hasattr(entry, 'tags'):
                tags = [t.term for t in entry.tags]
                
            from bs4 import BeautifulSoup
            snippet = BeautifulSoup(entry.summary, "html.parser").text.strip()[:250] if hasattr(entry, 'summary') else ""

            jobs.append({
                "id": job_id,
                "title": title,
                "company": company,
                "source": "WeWorkRemotely",
                "link": entry.link,
                "tags": tags,
                "snippet": snippet
            })
            
        return jobs
    except Exception as e:
        print(f"Error fetching WeWorkRemotely: {e}")
        return []

if __name__ == "__main__":
    jobs = fetch_jobs()
    print(f"Fetched {len(jobs)} jobs from WeWorkRemotely.")
    if jobs:
        print(jobs[0])
