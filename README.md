# reply-annoying-spammer-twitter

Auto-reply bot for Twitter. Monitors your mentions, filters for a specific user, and fires back a canned response with randomized delay so it doesn't look robotic.

## Prerequisites

- Python 3.9+
- A [Twitter Developer](https://developer.twitter.com/) app with **Read and Write** permissions (Elevated access tier)

## Installation

```bash
git clone https://github.com/jasperan/reply-annoying-spammer-twitter.git
cd reply-annoying-spammer-twitter
pip install -r requirements.txt
```

## Configuration

Create a `config.yaml` in the project root (don't commit this):

```yaml
API_KEY: "your_api_key"
API_SECRET: "your_api_secret"
ACCESS_TOKEN: "your_access_token"
ACCESS_TOKEN_SECRET: "your_access_token_secret"
```

Then edit `reply.py` to set your target:

```python
target_user = "their_handle"      # Twitter handle without @
reply_message = "Your reply here"
```

## Usage

```bash
python reply.py
```

Runs an infinite loop: checks mentions every 60 seconds, replies to new ones from the target user after a random 60-120 second delay. Best run inside `tmux` or `screen`.

## How It Works

1. Polls `mentions_timeline` via Tweepy (v1.1 API)
2. Filters mentions from `target_user`
3. Checks if already replied (via `search_tweets`)
4. Waits a random 60-120s, then posts the reply

## License

MIT

