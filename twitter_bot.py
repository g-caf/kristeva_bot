import tweepy
import os
from dotenv import load_dotenv
from database import QuoteDatabase
import logging

load_dotenv()

class KristevaBot:
    def __init__(self):
        self.setup_logging()
        self.db = QuoteDatabase()
        self.setup_twitter_api()
    
    def setup_logging(self):
        """Set up logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_twitter_api(self):
        """Initialize Twitter API connection"""
        try:
            # Twitter API v2 authentication
            self.client = tweepy.Client(
                bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
                consumer_key=os.getenv('TWITTER_API_KEY'),
                consumer_secret=os.getenv('TWITTER_API_SECRET'),
                access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
                access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
                wait_on_rate_limit=True
            )
            
            # Test the connection
            self.client.get_me()
            self.logger.info("Twitter API connection successful")
            
        except Exception as e:
            self.logger.error(f"Failed to connect to Twitter API: {e}")
            raise
    
    def format_quote(self, quote_data: dict) -> str:
        """Format quote for Twitter with source attribution"""
        text = quote_data['text']
        source = quote_data.get('source', 'Julia Kristeva')
        
        # Clean up the quote text
        text = text.strip()
        if not text.endswith(('.', '!', '?')):
            text += '.'
        
        # Add attribution
        formatted = f'"{text}"\n\n— {source}'
        
        # Ensure it fits Twitter's character limit (280)
        if len(formatted) > 280:
            # Truncate the quote text to fit
            max_quote_length = 280 - len(f'"\n\n— {source}') - 3  # 3 for "..."
            truncated_text = text[:max_quote_length] + "..."
            formatted = f'"{truncated_text}"\n\n— {source}'
        
        return formatted
    
    def post_quote(self) -> bool:
        """Post a random Kristeva quote to Twitter"""
        try:
            # Check if we have unused quotes
            quote_counts = self.db.get_quote_count()
            
            if quote_counts['unused'] == 0:
                if quote_counts['total'] > 0:
                    self.logger.info("No unused quotes left, resetting all quotes")
                    self.db.reset_all_quotes()
                else:
                    self.logger.error("No quotes in database")
                    return False
            
            # Get a random unused quote
            quote_data = self.db.get_random_unused_quote()
            if not quote_data:
                self.logger.error("Failed to retrieve quote from database")
                return False
            
            # Format the quote
            tweet_text = self.format_quote(quote_data)
            
            # Post to Twitter
            response = self.client.create_tweet(text=tweet_text)
            
            if response.data:
                # Mark quote as used
                self.db.mark_quote_used(quote_data['id'])
                self.logger.info(f"Successfully posted tweet: {response.data['id']}")
                self.logger.info(f"Quote used: {quote_data['text'][:50]}...")
                return True
            else:
                self.logger.error("Failed to post tweet - no response data")
                return False
                
        except Exception as e:
            self.logger.error(f"Error posting quote: {e}")
            return False
    
    def get_status(self) -> dict:
        """Get bot status information"""
        quote_counts = self.db.get_quote_count()
        return {
            'total_quotes': quote_counts['total'],
            'unused_quotes': quote_counts['unused'],
            'used_quotes': quote_counts['used']
        }

if __name__ == "__main__":
    bot = KristevaBot()
    
    # Test posting a quote
    success = bot.post_quote()
    if success:
        print("Quote posted successfully!")
        status = bot.get_status()
        print(f"Status: {status}")
    else:
        print("Failed to post quote")
