"""
reddit-ui-feedback-reader
A personal, read-only script that reads top posts and comments from
ten design and game-design subreddits and saves them locally for UI design study.

- Application-only OAuth (read-only). Never posts, comments, votes, or messages.
- GET requests only.
- Paced at 1 request per second; hard cap of 1,100 requests per run.
- Data is saved locally only. Not republished, sold, or used to train AI models.

Setup: set REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, and REDDIT_USERNAME
as environment variables, then run:  python3 reader.py
"""
import base64, json, os, sys, time, urllib.parse, urllib.request
from datetime import date

SUBREDDITS = [
    "UI_Design", "userexperience", "UXDesign", "web_design", "design_critiques",
    "truegaming", "gamedesign", "gamedev", "Unity3D", "IndieDev",
]
TIME_WINDOW = "month"      # hour, day, week, month, year, all
POSTS_PER_SUB = 100        # Reddit's max per listing request
MAX_REQUESTS = 1100        # 10 subs x 100 threads + 10 listings = 1,010; hard cap per run
PAUSE_SECONDS = 1.0        # at most 1 request per second

CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET")
USERNAME = os.environ.get("REDDIT_USERNAME", "unknown")
USER_AGENT = f"macos:ui-feedback-reader:v1.0 (personal read-only; by /u/{USERNAME})"

requests_made = 0


def get_token():
    """Application-only OAuth: read-only access, no user login."""
    creds = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    req = urllib.request.Request(
        "https://www.reddit.com/api/v1/access_token",
        data=b"grant_type=client_credentials",
        headers={"Authorization": f"Basic {creds}", "User-Agent": USER_AGENT},
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)["access_token"]


def api_get(token, path, params=None):
    """The only call the script makes to Reddit's API: a paced, capped GET."""
    global requests_made
    if requests_made >= MAX_REQUESTS:
        raise RuntimeError("Request cap reached; stopping.")
    url = "https://oauth.reddit.com" + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url, headers={"Authorization": f"bearer {token}", "User-Agent": USER_AGENT}
    )
    time.sleep(PAUSE_SECONDS)
    requests_made += 1
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def flatten_comments(children, depth=0):
    out = []
    for c in children:
        if c.get("kind") != "t1":
            continue
        d = c["data"]
        out.append({"depth": depth, "score": d.get("score"), "body": d.get("body", "")})
        replies = d.get("replies")
        if isinstance(replies, dict):
            out += flatten_comments(replies["data"]["children"], depth + 1)
    return out


def main():
    if not CLIENT_ID or not CLIENT_SECRET:
        sys.exit("Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET first.")
    token = get_token()
    results = []
    for sub in SUBREDDITS:
        listing = api_get(token, f"/r/{sub}/top", {"t": TIME_WINDOW, "limit": POSTS_PER_SUB})
        for p in listing["data"]["children"]:
            d = p["data"]
            try:
                thread = api_get(token, f"/r/{sub}/comments/{d['id']}", {"limit": 100})
            except RuntimeError:
                break
            results.append({
                "subreddit": sub,
                "title": d.get("title"),
                "score": d.get("score"),
                "url": "https://www.reddit.com" + d.get("permalink", ""),
                "text": d.get("selftext", ""),
                "comments": flatten_comments(thread[1]["data"]["children"]),
            })
    os.makedirs("data", exist_ok=True)
    out = f"data/ui_feedback_{date.today()}.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved {len(results)} posts to {out} using {requests_made} API requests.")


if __name__ == "__main__":
    main()
