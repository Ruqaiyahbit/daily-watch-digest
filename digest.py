import requests
from collections import defaultdict
from config import RESEND_API_KEY, DIGEST_FROM_EMAIL, DIGEST_TO_EMAIL, DIGEST_TO_EMAILS

def build_digest_html(items):
    grouped = defaultdict(lambda: defaultdict(list))
    for item in items:
        grouped[item["person"]][item["provider"]].append(item)

    provider_order = ["youtube", "tiktok", "instagram", "news"]

    html = []
    html.append("<html><body style='font-family:Arial,sans-serif; line-height:1.4;'>")
    html.append("<h2>Daily Watch Digest</h2>")
    html.append("<p>New mentions across YouTube, TikTok, Instagram, and news.</p>")

    if not items:
        html.append("<p><strong>No new items today.</strong></p>")
        html.append("</body></html>")
        return "".join(html)

    for person in sorted(grouped.keys()):
        html.append(f"<hr><h3>{person}</h3>")
        for provider in provider_order:
            entries = grouped[person].get(provider, [])
            if not entries:
                continue
            html.append(f"<h4 style='text-transform:capitalize'>{provider} ({len(entries)})</h4>")
            html.append("<ul>")
            for e in sorted(entries, key=lambda x: x.get("published_at", ""), reverse=True):
                title = (e.get("title") or "(untitled)").replace("<", "&lt;").replace(">", "&gt;")
                source = (e.get("source_name") or "").replace("<", "&lt;").replace(">", "&gt;")
                published = e.get("published_at") or ""
                url = e.get("url") or "#"
                summary = (e.get("summary") or "")[:220].replace("<", "&lt;").replace(">", "&gt;")

                html.append(
                    f"<li style='margin-bottom:8px'>"
                    f"<a href='{url}'><strong>{title}</strong></a><br>"
                    f"<span style='color:#555'>{source} | {published}</span><br>"
                    f"<span style='color:#333'>{summary}</span>"
                    f"</li>"
                )
            html.append("</ul>")

    html.append("</body></html>")
    return "".join(html)

def send_via_resend(subject: str, html: str):
    # Build recipient list from DIGEST_TO_EMAILS, fallback to DIGEST_TO_EMAIL
    to_list = [e.strip() for e in (DIGEST_TO_EMAILS or "").split(",") if e.strip()]
    if not to_list and DIGEST_TO_EMAIL:
        to_list = [DIGEST_TO_EMAIL.strip()]

    if not (RESEND_API_KEY and DIGEST_FROM_EMAIL and to_list):
        raise RuntimeError("Missing RESEND_API_KEY / DIGEST_FROM_EMAIL / DIGEST_TO_EMAILS (or DIGEST_TO_EMAIL)")

    r = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "from": DIGEST_FROM_EMAIL,
            "to": to_list,
            "subject": subject,
            "html": html,
        },
        timeout=30,
    )
    r.raise_for_status()
    return r.json()
