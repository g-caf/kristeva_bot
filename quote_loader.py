from database import QuoteDatabase
import json
import csv

def load_quotes_from_file(filename: str, source_name: str = None):
    """
    Load quotes from a text file or JSON file into the database.
    
    For text files: Each quote should be on a separate line
    For JSON files: Should be a list of objects with 'text', 'source', and optional 'page' fields
    """
    db = QuoteDatabase()
    
    try:
        if filename.endswith('.json'):
            with open(filename, 'r', encoding='utf-8') as f:
                quotes_data = json.load(f)
                
            for quote_data in quotes_data:
                text = quote_data.get('text', '').strip()
                source = quote_data.get('source', source_name or 'Julia Kristeva')
                page = quote_data.get('page', None)
                
                if text:  # Only add non-empty quotes
                    db.add_quote(text, source, page)
                    print(f"Added quote: {text[:50]}...")
                    
        elif filename.endswith('.csv'):
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)  # Skip header row
                
                for row in reader:
                    if row:  # Skip empty rows
                        text = row[0].strip().strip('"')  # Remove quotes and whitespace
                        if text and len(text) > 10:  # Filter out very short quotes
                            db.add_quote(text, source_name or 'Julia Kristeva - Black Sun')
                            print(f"Added quote: {text[:50]}...")
                    
        else:  # Assume text file
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line in lines:
                text = line.strip()
                if text and len(text) > 10:  # Filter out very short lines
                    db.add_quote(text, source_name or 'Julia Kristeva')
                    print(f"Added quote: {text[:50]}...")
        
        # Show final count
        counts = db.get_quote_count()
        print(f"\nLoading complete!")
        print(f"Total quotes in database: {counts['total']}")
        print(f"Unused quotes: {counts['unused']}")
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except Exception as e:
        print(f"Error loading quotes: {e}")

def add_sample_quotes():
    """Add some sample Kristeva quotes for testing"""
    db = QuoteDatabase()
    
    sample_quotes = [
        "The abject confronts us with our earliest attempts to release the hold of maternal entity before we can even distinguish between subject and object.",
        "Language is a system of signs that express ideas, and is therefore comparable to a system of writing.",
        "The foreigner lives within us: he is the hidden face of our identity.",
        "Abjection preserves what existed in the archaism of pre-objectal relationship, in the immemorial violence of mourning.",
        "Poetry is language's greatest effort to approach the ineffable.",
    ]
    
    for quote in sample_quotes:
        db.add_quote(quote, "Julia Kristeva")
        print(f"Added sample quote: {quote[:50]}...")
    
    counts = db.get_quote_count()
    print(f"\nSample quotes added!")
    print(f"Total quotes in database: {counts['total']}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        source_name = sys.argv[2] if len(sys.argv) > 2 else None
        load_quotes_from_file(filename, source_name)
    else:
        print("Usage: python quote_loader.py <filename> [source_name]")
        print("Or run with no arguments to add sample quotes")
        
        choice = input("Add sample quotes for testing? (y/n): ").lower()
        if choice == 'y':
            add_sample_quotes()
