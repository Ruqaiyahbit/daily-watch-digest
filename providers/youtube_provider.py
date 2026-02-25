import requests
from datetime import datetime, timezone
from config import YOUTUBE_API_KEY, MAX_YOUTUBE_RESULTS_PER_PERSON, ALIASES

SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

def _search(query: str, published_after_iso: str):
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "order": "date",
        "maxResults": MAX_YOUTUBE_RESULTS_PER_PERSON,
        "publishedAfter": published_after_iso,
        "key": YOUTUBE_API_KEY,
    }
    r = requests.get(SEARCH_URL, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()

    items = []
    now_iso = datetime.now(timezone.utc).isoformat()
    for x in data.get("items", []):
        vid = x.get("id", {}).get("videoId")
        sn = x.get("snippet", {})
        if not vid:
            continue

        items.append({
            "provider": "youtube",
            "external_id": vid,
            "person": "",
            "title": sn.get("title", ""),
            "source_name": sn.get("channelTitle", ""),
            "published_at": sn.get("publishedAt", ""),
            "url": f"https://www.youtube.com/watch?v={vid}",
            "summary": sn.get("description", ""),
            "found_at": now_iso,
        })
    return items

def search_person(person: str, published_after_iso: str):
    queries = [f'"{person}"'] + ALIASES.get(person, [])
    seen = set()
    output = []

    for q in queries:
        for item in _search(q, published_after_iso):
            item["person"] = person
            key = (item["provider"], item["external_id"])
            if key in seen:
                continue
            seen.add(key)

            text = (item["title"] + " " + item.get("summary", "")).lower()
            tokens = [t.lower().strip(".") for t in person.split() if len(t) > 2]
            if any(tok in text for tok in tokens):
                output.append(item)

    return output
