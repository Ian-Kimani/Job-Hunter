import requests
from bs4 import BeautifulSoup

def fetch_jobs():
    """Scrapes IT & Software jobs from MyJobMag Kenya."""
    url = "https://www.myjobmag.co.ke/jobs-by-field/information-technology"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    jobs = []
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        job_list = soup.find_all('li', class_='job-info')
        
        for item in job_list:
            try:
                title_tag = item.find('h2')
                if not title_tag:
                    continue
                link_tag = title_tag.find('a')
                if not link_tag:
                    continue
                    
                title = link_tag.text.strip()
                link = "https://www.myjobmag.co.ke" + link_tag.get('href')
                job_id = link.split('/')[-1]
                
                snippet_tag = item.find('li', class_='job-desc')
                snippet = snippet_tag.text.strip()[:250] if snippet_tag else ""
                
                jobs.append({
                    "id": job_id,
                    "title": title,
                    "company": "MyJobMag Listing",
                    "source": "MyJobMag",
                    "link": link,
                    "tags": ["Kenya"],
                    "snippet": snippet
                })
            except Exception:
                continue
                
    except Exception as e:
        print(f"Error fetching MyJobMag: {e}")
        
    return jobs

if __name__ == "__main__":
    jobs = fetch_jobs()
    print(f"Fetched {len(jobs)} jobs from MyJobMag.")
