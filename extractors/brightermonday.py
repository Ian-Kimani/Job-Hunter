import requests
from bs4 import BeautifulSoup

def fetch_jobs():
    """Scrapes Software & Data jobs from BrighterMonday Kenya."""
    url = "https://www.brightermonday.co.ke/jobs/software-data"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    jobs = []
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        # BrighterMonday usually wraps jobs in div or a tags
        job_cards = soup.find_all('div', class_=lambda c: c and ('job-card' in str(c).lower() or 'search-result' in str(c).lower()))
        
        # Fallback if specific classes fail
        if not job_cards:
             job_cards = soup.find_all('a', href=lambda h: h and '/listings/' in h)
             
        for card in job_cards:
            try:
                # Find the link and title
                if card.name == 'a':
                    link_tag = card
                else:
                    link_tag = card.find('a', href=lambda h: h and '/listings/' in h)
                
                if not link_tag:
                    continue
                    
                link = link_tag.get('href')
                title = link_tag.get('title', link_tag.text.strip())
                
                # We extract the ID from the URL (usually at the end)
                job_id = link.split('-')[-1]
                
                snippet_tag = card.find('p')
                snippet = snippet_tag.text.strip()[:250] if snippet_tag else ""
                
                jobs.append({
                    "id": job_id,
                    "title": title[:50] + "...", # Clean up long text
                    "company": "BrighterMonday Listing",
                    "source": "BrighterMonday",
                    "link": link,
                    "tags": ["Kenya"],
                    "snippet": snippet
                })
            except Exception:
                continue
                
    except Exception as e:
        print(f"Error fetching BrighterMonday: {e}")
        
    return jobs

if __name__ == "__main__":
    jobs = fetch_jobs()
    print(f"Fetched {len(jobs)} jobs from BrighterMonday.")
