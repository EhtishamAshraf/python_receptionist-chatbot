# a code to create SQL database

import sqlite3

# Connect to SQLite database (this will create a new database if it doesn't exist)
conn = sqlite3.connect('Receptionistbot_database.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Example: Create a table to store card data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Card_data (
        card_number TEXT PRIMARY KEY,
        total_balance INTEGER,
        transactions INTEGER,
        card_holder_name TEXT,
        last_activity_date DATE,
        last_transaction INTEGER
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
