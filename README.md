# reddit-ui-feedback-reader

A small **personal, read-only** script that reads top posts and comments from
r/UI_Design and r/userexperience so I can study recurring UI design feedback
while designing a free app.

## What it does
- Uses Reddit's OAuth API with **application-only (read-only)** authentication.
- Makes **GET requests only**: `/r/{sub}/top` and `/r/{sub}/comments/{id}`.
- **Never** posts, comments, votes, messages, or acts on behalf of any account.
- Paced at **1 request per second**, with a hard cap of **250 requests per run**.
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
