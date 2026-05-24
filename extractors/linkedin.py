import requests
from bs4 import BeautifulSoup

def fetch_jobs():
    """Scrapes public Python jobs from LinkedIn Kenya."""
    url = "https://www.linkedin.com/jobs/search/?keywords=Python&location=Kenya"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    jobs = []
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        job_cards = soup.find_all('div', class_='base-card')
        
        for card in job_cards:
            try:
                title_tag = card.find('h3', class_='base-search-card__title')
                company_tag = card.find('h4', class_='base-search-card__subtitle')
                link_tag = card.find('a', class_='base-card__full-link')
                
                if not title_tag or not link_tag:
                    continue
                    
                title = title_tag.text.strip()
                company = company_tag.text.strip() if company_tag else "Unknown"
                link = link_tag.get('href')
                
                # Extract ID from linkedin url
                job_id = link.split('?')[0].split('-')[-1]
                
                jobs.append({
                    "id": job_id,
                    "title": title,
                    "company": company,
                    "source": "LinkedIn",
                    "link": link,
                    "tags": ["Kenya", "LinkedIn"],
                    "snippet": ""
                })
            except Exception:
                continue
                
    except Exception as e:
        print(f"Error fetching LinkedIn: {e}")
        
    return jobs

if __name__ == "__main__":
    jobs = fetch_jobs()
    print(f"Fetched {len(jobs)} jobs from LinkedIn.")
