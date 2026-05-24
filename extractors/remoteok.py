import requests

def fetch_jobs():
    """Fetches programming jobs from RemoteOK API."""
    url = "https://remoteok.com/api"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        jobs = []
        # The first item in RemoteOK API is usually a legal notice, skip it
        for item in data[1:]:
            if item.get("type") != "job":
                continue
            
            # RemoteOK gives us raw HTML in the description
            from bs4 import BeautifulSoup
            description_html = item.get("description", "")
            snippet = BeautifulSoup(description_html, "html.parser").text.strip()[:250] if description_html else ""
            
            jobs.append({
                "id": str(item.get("id")),
                "title": item.get("position", "Unknown"),
                "company": item.get("company", "Unknown"),
                "source": "RemoteOK",
                "link": item.get("url", ""),
                "tags": item.get("tags", []),
                "snippet": snippet
            })
        return jobs
    except Exception as e:
        print(f"Error fetching RemoteOK: {e}")
        return []

if __name__ == "__main__":
    jobs = fetch_jobs()
    print(f"Fetched {len(jobs)} jobs from RemoteOK.")
    if jobs:
        print(jobs[0])
