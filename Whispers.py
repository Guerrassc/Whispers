import sqlite3     # Module to interact with SQLite databases
import random      # Module to pick random items (for random quotes and entries)
import datetime    # Module to handle dates and times

# List of meaningful quotes shown after saving an entry
QUOTES = [
    "Every memory preserved is a life remembered.",
    "The act of recording is the act of honoring.",
    "In small moments, entire worlds are hidden.",
    "Words hold the weight of time.",
    "To remember is to live twice."
]

# Function to set up the database (only runs once when app starts)
def initialize_database():
    conn = sqlite3.connect('whispers.db')  # Connect to (or create) the database file
    c = conn.cursor()                      # Create a cursor object to run SQL commands
    c.execute('''
        CREATE TABLE IF NOT EXISTS entries (  -- Create a table called 'entries' if it doesn't exist
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique ID for each entry
            date TEXT NOT NULL,                    -- Date and time of the entry
            content TEXT NOT NULL                  -- The journal text itself
        )
    ''')
    conn.commit()    # Save changes
    conn.close()     # Close the connection

# Function to allow the user to write a new journal entry
def write_entry():
    print("\n--- New Entry ---\n")
    content = input("Enter your journal entry:\n\n")  # Ask the user for their journal text
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current date and time

    conn = sqlite3.connect('whispers.db')   # Connect to the database
    c = conn.cursor()
    c.execute('INSERT INTO entries (date, content) VALUES (?, ?)', (date, content))  # Save the new entry
    conn.commit()
    conn.close()

    print("\nEntry saved successfully.")    # Confirm save
    print(random.choice(QUOTES))             # Display a random serious quote
    print()

# Function to read a random journal entry
def read_random_entry():
    conn = sqlite3.connect('whispers.db')   # Connect to the database
    c = conn.cursor()
    c.execute('SELECT content, date FROM entries')   # Fetch all entries
    entries = c.fetchall()                 # Store all entries in a list
    conn.close()

    if entries:
        entry = random.choice(entries)     # Pick a random entry
        print("\n--- Random Entry ---\n")
        print(f"Date: {entry[1]}\n")        # Print the date
        print(f"{entry[0]}\n")              # Print the content
    else:
        print("\nNo entries found. Start writing to build your archive.\n")

# Function to search for entries containing a specific keyword
def search_entries():
    keyword = input("\nEnter a keyword to search for: ")  # Ask for a search word

    conn = sqlite3.connect('whispers.db')   # Connect to the database
    c = conn.cursor()
    # Find entries where the content contains the keyword
    c.execute('SELECT content, date FROM entries WHERE content LIKE ?', ('%'+keyword+'%',))
    entries = c.fetchall()                  # Get all matching entries
    conn.close()

    if entries:
        print(f"\n--- {len(entries)} Entries Found ---\n")
        for content, date in entries:
            print(f"Date: {date}")
            print(f"{content}\n---\n")
    else:
        print("\nNo matching entries found.\n")

# The main menu loop
def main():
    initialize_database()   # Make sure the database and table exist before anything
    print("\nWhispers - A Personal Archive\n")
    while True:
        # Display the menu
        print("Menu:")
        print("1. Write a new entry")
        print("2. Read a random entry")
        print("3. Search entries")
        print("4. Exit")

        choice = input("\nChoose (1-4): ")  # Ask for user choice

        if choice == '1':
            write_entry()           # Write a new entry
        elif choice == '2':
            read_random_entry()      # Read a random entry
        elif choice == '3':
            search_entries()         # Search entries
        elif choice == '4':
            print("\nExiting Whispers. Your words are preserved.\n")
            break                    # Exit the app
        else:
            print("\nInvalid choice. Please select 1-4.\n")

# If this script is run directly (not imported), start the app
if __name__ == "__main__":
    main()
