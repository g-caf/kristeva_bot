import schedule
import time
from twitter_bot import KristevaBot
import logging

def run_bot():
    """Run the bot and post a quote"""
    try:
        bot = KristevaBot()
        success = bot.post_quote()
        
        if success:
            status = bot.get_status()
            logging.info(f"Bot run successful. Remaining quotes: {status['unused_quotes']}")
        else:
            logging.error("Bot run failed")
            
    except Exception as e:
        logging.error(f"Error in scheduled bot run: {e}")

def main():
    """Main scheduler loop"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Schedule the bot to run every hour
    schedule.every().hour.do(run_bot)
    
    logging.info("Kristeva bot scheduler started - posting every hour")
    logging.info("Next run scheduled for: " + str(schedule.next_run()))
    
    # Run immediately on startup (optional)
    # run_bot()
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()
