import requests
from datetime import datetime, timezone
from config import NEWSAPI_KEY, MAX_NEWS_RESULTS_PER_PERSON, ALIASES

NEWS_URL = "https://newsapi.org/v2/everything"

def search_person(person: str, from_iso_date: str):
    if not NEWSAPI_KEY:
        return []

    queries = [f'"{person}"'] + ALIASES.get(person, [])
    output = []
    seen_urls = set()
    now_iso = datetime.now(timezone.utc).isoformat()

    for q in queries:
        params = {
            "q": q,
            "from": from_iso_date,
            "sortBy": "publishedAt",
            "language": "en",
            "pageSize": MAX_NEWS_RESULTS_PER_PERSON,
            "apiKey": NEWSAPI_KEY,
        }
        r = requests.get(NEWS_URL, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()

        for a in data.get("articles", []):
            url = a.get("url")
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)

            title = a.get("title", "") or ""
            desc = a.get("description", "") or ""
            content = (title + " " + desc).lower()

            tokens = [t.lower().strip(".") for t in person.split() if len(t) > 2]
            if not any(tok in content for tok in tokens):
                continue

            output.append({
                "provider": "news",
                "external_id": url,
                "person": person,
                "title": title,
                "source_name": (a.get("source") or {}).get("name", ""),
                "published_at": a.get("publishedAt", ""),
                "url": url,
                "summary": desc,
                "found_at": now_iso,
            })

    return output
