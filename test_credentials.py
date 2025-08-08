import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

print("Testing Twitter API credentials...")

# Print what we're loading (without showing actual values)
print(f"API Key loaded: {bool(os.getenv('TWITTER_API_KEY'))}")
print(f"API Secret loaded: {bool(os.getenv('TWITTER_API_SECRET'))}")
print(f"Access Token loaded: {bool(os.getenv('TWITTER_ACCESS_TOKEN'))}")
print(f"Access Token Secret loaded: {bool(os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))}")
print(f"Bearer Token loaded: {bool(os.getenv('TWITTER_BEARER_TOKEN'))}")

try:
    client = tweepy.Client(
        bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
        consumer_key=os.getenv('TWITTER_API_KEY'),
        consumer_secret=os.getenv('TWITTER_API_SECRET'),
        access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
        access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
        wait_on_rate_limit=True
    )
    
    # Test connection
    me = client.get_me()
    print(f"✅ Success! Connected as: {me.data.username}")
    
except Exception as e:
    print(f"❌ Error: {e}")
