import tweepy
import time
import random
import yaml

# Load Twitter API credentials from config.yaml
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

API_KEY = config['API_KEY']
API_SECRET = config['API_SECRET']
ACCESS_TOKEN = config['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = config['ACCESS_TOKEN_SECRET']

# Set up Tweepy authentication
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# The annoying user's Twitter handle (without the '@')
target_user = "m__dominguez" # the annoying socialist scum who's been messaging me for the past 2 weeks while I was in Las Vegas

# Message to reply with
reply_message = "Amargado!"

def respond_to_mentions():
    # Fetch the latest mentions
    mentions = api.mentions_timeline(count=5)  # Adjust count to fit your needs
    
    for mention in mentions:
        if target_user in mention.user.screen_name:  # Check if the mention is from the target user
            print(f"Checking mention from {mention.user.screen_name}...")

            # Check if we've already replied to this tweet
            replies = api.search_tweets(q=f"to:{mention.user.screen_name}", since_id=mention.id, tweet_mode='extended')
            already_replied = any(reply.in_reply_to_status_id == mention.id and reply_message in reply.full_text for reply in replies)

            if not already_replied:
                print(f"Replying to {mention.user.screen_name}...")

                # Generate a random wait time between 60 and 120 seconds
                wait_time = random.randint(60, 120)
                time.sleep(wait_time)  # Wait before responding

                # Reply to the original tweet with the message
                api.update_status(
                    status=f"@{mention.user.screen_name} {reply_message}",
                    in_reply_to_status_id=mention.id
                )
                print(f"Replied with '{reply_message}' after {wait_time} seconds.")
            else:
                print(f"Tweet ID: {mention.id}, Date: {mention.created_at}, Already replied to this tweet. No new response needed.")

if __name__ == "__main__":
    while True:
        respond_to_mentions()
        time.sleep(60)  # Check for new mentions every 60 seconds