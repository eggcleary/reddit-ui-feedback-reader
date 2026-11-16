# reddit-ui-feedback-reader

A small **personal, read-only** script that reads top posts and comments from
these subreddits so I can study recurring UI design feedback while designing a free app:

- UI/UX: r/UI_Design, r/userexperience, r/UXDesign, r/web_design, r/design_critiques
- Game design (interface and onboarding critique): r/truegaming, r/gamedesign, r/gamedev, r/Unity3D, r/IndieDev

## What it does
- Uses Reddit's OAuth API with **application-only (read-only)** authentication.
- Reads up to **100 top posts per subreddit** per run.
- Makes **GET requests only**: `/r/{sub}/top` and `/r/{sub}/comments/{id}`.
- **Never** posts, comments, votes, messages, or acts on behalf of any account.
- Paced at **1 request per second**, with a hard cap of **1,100 requests per run** (about 17 minutes per run).
- Saves text **locally only**. Not republished, shared, sold, or used to train AI models.

## Giving back
After each review cycle I post a credited summary of common UI feedback themes
to r/UI_Design so the community can benefit from the patterns.

## Run
```
export REDDIT_CLIENT_ID=...
export REDDIT_CLIENT_SECRET=...
export REDDIT_USERNAME=...
python3 reader.py
```
