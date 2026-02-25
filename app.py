from datetime import datetime, timedelta, timezone
from config import PEOPLE, DB_PATH, LOOKBACK_HOURS
from storage import init_db, save_item
from digest import build_digest_html, send_via_resend

from providers.youtube_provider import search_person as yt_search
from providers.news_provider import search_person as news_search
from providers.tiktok_provider import search_person as tiktok_search
from providers.instagram_provider import search_person as ig_search

def main():
    init_db(DB_PATH)

    now = datetime.now(timezone.utc)
    published_after_dt = now - timedelta(hours=LOOKBACK_HOURS)
    published_after_iso = published_after_dt.isoformat().replace("+00:00", "Z")
    from_date = published_after_dt.date().isoformat()

    inserted_today = []

    for person in PEOPLE:
        print(f"[INFO] Checking: {person}")

        providers = [
            ("youtube", lambda: yt_search(person, published_after_iso)),
            ("news", lambda: news_search(person, from_date)),
            ("tiktok", lambda: tiktok_search(person, published_after_iso)),
            ("instagram", lambda: ig_search(person, published_after_iso)),
        ]

        for provider_name, fn in providers:
            try:
                items = fn() or []
                for item in items:
                    if save_item(DB_PATH, item):
                        inserted_today.append(item)
                print(f"  - {provider_name}: {len(items)} fetched")
            except Exception as e:
                print(f"  - {provider_name}: ERROR: {e}")

    subject = f"Daily Watch Digest | {now.strftime('%Y-%m-%d')} | {len(inserted_today)} new items"
    html = build_digest_html(inserted_today)

    try:
        send_via_resend(subject, html)
        print("[INFO] Email sent")
    except Exception as e:
        print(f"[WARN] Email not sent: {e}")
        print(subject)

if __name__ == "__main__":
    main()
