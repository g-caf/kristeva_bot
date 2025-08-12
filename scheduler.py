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
    
    # Initialize database and load quotes if empty
    from database import QuoteDatabase
    from quote_loader import load_quotes_from_file
    import os
    
    db = QuoteDatabase()
    
    # Clear existing quotes to switch to Levinas
    import sqlite3
    conn = sqlite3.connect(db.db_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM quotes')
    conn.commit()
    conn.close()
    logging.info("Cleared existing quotes for Levinas switch")
    
    counts = db.get_quote_count()
    
    if counts['total'] == 0:
        logging.info("Database is empty, loading quotes from CSV...")
        csv_file = "levinas_quotes_clean.csv"
        if os.path.exists(csv_file):
            load_quotes_from_file(csv_file, "Emmanuel Levinas")
            logging.info("Levinas quotes loaded successfully")
        else:
            logging.error(f"Quote file {csv_file} not found!")
    else:
        logging.info(f"Database contains {counts['total']} quotes")
    
    # Schedule the bot to run every 10 minutes
    schedule.every(10).minutes.do(run_bot)
    
    logging.info("Kristeva bot scheduler started - posting every 10 minutes")
    logging.info("Next run scheduled for: " + str(schedule.next_run()))
    
    # Run immediately on startup to test
    logging.info("Running bot immediately on startup...")
    run_bot()
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()
