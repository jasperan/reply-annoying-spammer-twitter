# reply-annoying-spammer-twitter

Auto-reply bot for Twitter. Monitors your mentions, filters for a specific user, and fires back a canned response with randomized delay so it doesn't look robotic.

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- A [Twitter Developer](https://developer.twitter.com/) app with **Read and Write** permissions (Elevated access tier)

## Installation

```bash
git clone https://github.com/jasperan/reply-annoying-spammer-twitter.git
cd reply-annoying-spammer-twitter
uv sync
```

## Configuration

Create a `config.yaml` in the project root (already gitignored, so it won't be committed):

```yaml
API_KEY: "your_api_key"
API_SECRET: "your_api_secret"
ACCESS_TOKEN: "your_access_token"
ACCESS_TOKEN_SECRET: "your_access_token_secret"
TARGET_USER: "their_handle"        # Twitter handle without @
REPLY_MESSAGE: "Your reply here"
```

Both the target user and the reply message are read from `config.yaml` — no need to edit the source.

## Usage

```bash
uv run reply.py
```

Runs an infinite loop: checks mentions every 60 seconds, replies to new ones from the target user after a random 60-120 second delay. API errors are logged and the loop keeps running, so it survives rate limits and network blips. Best run inside `tmux` or `screen`.

## How It Works

1. Polls `mentions_timeline` via Tweepy (v1.1 API)
2. Filters mentions whose `screen_name` matches `TARGET_USER` (case-insensitive)
3. Checks if already replied (via `search_tweets`)
4. Waits a random 60-120s, then posts the reply

## License

MIT
