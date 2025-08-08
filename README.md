# Kristeva Quote Bot

A Twitter bot that posts Julia Kristeva quotes every hour.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   - Copy `.env.example` to `.env`
   - Fill in your Twitter API credentials

3. **Load quotes into database:**
   ```bash
   # Add sample quotes for testing
   python quote_loader.py
   
   # Or load from your own file
   python quote_loader.py quotes.txt "Julia Kristeva"
   python quote_loader.py quotes.json
   ```

4. **Test the bot:**
   ```bash
   python twitter_bot.py
   ```

5. **Run the scheduler:**
   ```bash
   python scheduler.py
   ```

## Deployment on Render

1. Connect your GitHub repo to Render
2. Set environment variables in Render dashboard:
   - `TWITTER_API_KEY`
   - `TWITTER_API_SECRET`
   - `TWITTER_ACCESS_TOKEN`
   - `TWITTER_ACCESS_TOKEN_SECRET`
   - `TWITTER_BEARER_TOKEN`
3. Deploy as a Background Worker

## File Structure

- `twitter_bot.py` - Main bot logic
- `database.py` - SQLite database handling
- `scheduler.py` - Hourly posting scheduler
- `quote_loader.py` - Utility to load quotes from files
- `render.yaml` - Render deployment configuration

## Quote Formats

The bot accepts quotes in two formats:

**Text file:** One quote per line
```
Language is a system of signs that express ideas.
The foreigner lives within us: he is the hidden face of our identity.
```

**JSON file:** Array of quote objects
```json
[
  {
    "text": "Language is a system of signs that express ideas.",
    "source": "Julia Kristeva",
    "page": 42
  }
]
```
