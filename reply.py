import logging
import random
import time

import tweepy
import yaml

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

# Keys that must be present in config.yaml for the bot to run.
REQUIRED_KEYS = (
    "API_KEY",
    "API_SECRET",
    "ACCESS_TOKEN",
    "ACCESS_TOKEN_SECRET",
    "TARGET_USER",
    "REPLY_MESSAGE",
)


def load_config(path="config.yaml"):
    """Load and validate the YAML config, failing with a clear message."""
    try:
        with open(path, "r") as config_file:
            config = yaml.safe_load(config_file) or {}
    except FileNotFoundError:
        raise SystemExit(
            f"Config file '{path}' not found. Create it with the required keys: "
            f"{', '.join(REQUIRED_KEYS)}."
        )

    missing = [key for key in REQUIRED_KEYS if key not in config]
    if missing:
        raise SystemExit(
            f"Config file '{path}' is missing required key(s): {', '.join(missing)}."
        )
    return config


def build_api(config):
    """Construct an authenticated Tweepy v1.1 API client from config."""
    auth = tweepy.OAuthHandler(config["API_KEY"], config["API_SECRET"])
    auth.set_access_token(config["ACCESS_TOKEN"], config["ACCESS_TOKEN_SECRET"])
    return tweepy.API(auth)


def respond_to_mentions(api, target_user, reply_message):
    # Fetch the latest mentions
    mentions = api.mentions_timeline(count=5)  # Adjust count to fit your needs

    for mention in mentions:
        if mention.user.screen_name.lower() == target_user.lower():  # Check if the mention is from the target user
            logger.info("Checking mention from %s...", mention.user.screen_name)

            # Check if we've already replied to this tweet
            replies = api.search_tweets(q=f"to:{mention.user.screen_name}", since_id=mention.id, tweet_mode='extended')
            already_replied = any(reply.in_reply_to_status_id == mention.id and reply_message in reply.full_text for reply in replies)

            if not already_replied:
                logger.info("Replying to %s...", mention.user.screen_name)

                # Generate a random wait time between 60 and 120 seconds
                wait_time = random.randint(60, 120)
                time.sleep(wait_time)  # Wait before responding

                # Reply to the original tweet with the message
                api.update_status(
                    status=f"@{mention.user.screen_name} {reply_message}",
                    in_reply_to_status_id=mention.id
                )
                logger.info("Replied with '%s' after %d seconds.", reply_message, wait_time)
            else:
                logger.info(
                    "Tweet ID: %s, Date: %s, Already replied to this tweet. No new response needed.",
                    mention.id,
                    mention.created_at,
                )


def main():
    config = load_config()
    api = build_api(config)
    target_user = config["TARGET_USER"]
    reply_message = config["REPLY_MESSAGE"]

    while True:
        try:
            respond_to_mentions(api, target_user, reply_message)
        except Exception as e:
            # Log and keep running: a rate limit, network blip, or 5xx
            # must not kill a daemon meant to run unattended for weeks.
            # KeyboardInterrupt/SystemExit still propagate (they are not Exception).
            logger.error("API error, continuing: %s", e)
        time.sleep(60)  # Check for new mentions every 60 seconds


if __name__ == "__main__":
    main()
