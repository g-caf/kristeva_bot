import sqlite3
import random
from typing import Optional, List

class QuoteDatabase:
    def __init__(self, db_path: str = "quotes.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with quotes table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                source TEXT,
                page_number INTEGER,
                used BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_quote(self, text: str, source: str = None, page_number: int = None):
        """Add a new quote to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO quotes (text, source, page_number)
            VALUES (?, ?, ?)
        ''', (text, source, page_number))
        
        conn.commit()
        conn.close()
    
    def get_random_unused_quote(self) -> Optional[dict]:
        """Get a random unused quote"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, text, source, page_number
            FROM quotes
            WHERE used = FALSE
            ORDER BY RANDOM()
            LIMIT 1
        ''')
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'text': result[1],
                'source': result[2],
                'page_number': result[3]
            }
        return None
    
    def mark_quote_used(self, quote_id: int):
        """Mark a quote as used"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE quotes
            SET used = TRUE
            WHERE id = ?
        ''', (quote_id,))
        
        conn.commit()
        conn.close()
    
    def reset_all_quotes(self):
        """Reset all quotes to unused (for when we run out)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('UPDATE quotes SET used = FALSE')
        
        conn.commit()
        conn.close()
    
    def get_quote_count(self) -> dict:
        """Get count of used vs unused quotes"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM quotes WHERE used = TRUE')
        used_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM quotes WHERE used = FALSE')
        unused_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'used': used_count,
            'unused': unused_count,
            'total': used_count + unused_count
        }
