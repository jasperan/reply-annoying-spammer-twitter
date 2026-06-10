# CLAUDE.md

Twitter auto-reply bot that monitors mentions, filters by a target user, and posts canned responses with randomized delay.

## Tech Stack

- Python 3.12+
- uv for environment and dependency management
- Tweepy (Twitter API v1.1 via OAuth 1.0a)
- PyYAML for config loading

## Setup

```bash
uv sync
```

Create `config.yaml` in the project root (gitignored, not committed):

```yaml
API_KEY: "your_api_key"
API_SECRET: "your_api_secret"
ACCESS_TOKEN: "your_access_token"
ACCESS_TOKEN_SECRET: "your_access_token_secret"
TARGET_USER: "handle_without_@"
REPLY_MESSAGE: "Your reply text"
```

Twitter app must have **Read and Write** permissions (Elevated access tier).

## Configuration

All configuration lives in `config.yaml`. `TARGET_USER` and `REPLY_MESSAGE`
are read at startup — no need to edit the source.

## Run

```bash
uv run reply.py
```

Runs indefinitely. Use `tmux` or `screen` to keep it alive:

```bash
tmux new -s spammer && uv run reply.py
```

## Architecture

Single-file (`reply.py`). Main loop runs every 60 seconds:

1. Fetches last 5 mentions via `api.mentions_timeline(count=5)`
2. Filters for `TARGET_USER` by `screen_name` (case-insensitive equality)
3. Searches for existing replies via `api.search_tweets` to avoid duplicates
4. Waits random 60-120s before posting (anti-bot appearance)
5. Posts reply via `api.update_status`

Each iteration of the loop wraps `respond_to_mentions()` in a
`try/except tweepy.TweepyException`, so a rate limit, network blip, or 5xx
is logged and the daemon keeps running.

## Gotchas

- Requires **Elevated** Twitter API access (free Basic tier won't work for `mentions_timeline`)
- `api.search_tweets` duplicate-check can miss replies if the search window is narrow; tune `since_id` if you see double-replies
- No persistent state: if the process restarts, already-replied tweets are re-checked via live search (works, but hits rate limits faster)
