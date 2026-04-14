# CLAUDE.md

Twitter auto-reply bot that monitors mentions, filters by a target user, and posts canned responses with randomized delay.

## Tech Stack

- Python 3.9+
- Tweepy (Twitter API v1.1 via OAuth 1.0a)
- PyYAML for config loading

## Setup

```bash
pip install -r requirements.txt
```

Create `config.yaml` in the project root (not committed):

```yaml
API_KEY: "your_api_key"
API_SECRET: "your_api_secret"
ACCESS_TOKEN: "your_access_token"
ACCESS_TOKEN_SECRET: "your_access_token_secret"
```

Twitter app must have **Read and Write** permissions (Elevated access tier).

## Configuration

Edit these two variables at the top of `reply.py`:

```python
target_user = "handle_without_@"
reply_message = "Your reply text"
```

## Run

```bash
python reply.py
```

Runs indefinitely. Use `tmux` or `screen` to keep it alive:

```bash
tmux new -s spammer && python reply.py
```

## Architecture

Single-file (`reply.py`). Main loop runs every 60 seconds:

1. Fetches last 5 mentions via `api.mentions_timeline(count=5)`
2. Filters for `target_user` by `screen_name`
3. Searches for existing replies via `api.search_tweets` to avoid duplicates
4. Waits random 60-120s before posting (anti-bot appearance)
5. Posts reply via `api.update_status`

## Gotchas

- Requires **Elevated** Twitter API access (free Basic tier won't work for `mentions_timeline`)
- `config.yaml` is not gitignored by default — add it manually or it will leak credentials
- `api.search_tweets` duplicate-check can miss replies if the search window is narrow; tune `since_id` if you see double-replies
- No persistent state: if the process restarts, already-replied tweets are re-checked via live search (works, but hits rate limits faster)
