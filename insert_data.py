# a code to insert data to the SQL database

import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('Receptionistbot_database.db')
cursor = conn.cursor()

# Example: Insert sample data into the card_data table
Card_data = [
    ('3742 4545 5400 1267', 19058, 10, 'Mutte', '11/12/2023', 10000),
    ('3743 4545 5400 1266',	84902,	1, 'Asim',	'11/13/2023', -100),
    ('3744 4545 5421 1267',	123, 1,	'Samar',	'11/14/2023', 5000),
    ('3745 4545 5450 1267',	345, 6,	'Ghous', '11/15/2023',	2000),
    ('3746 4545 5400 1267', 546, 8, 'Asad', '11/16/2002', 100),
    ('9087 4545 5400 1267', 444, 4, 'Baha', '11/17/2020', 999),
    ('3748 1285 5400 1267', 0, 5, 'Imtiaz', '11/18/2023', 89000),
    ('1122 4455 8796 1230', 1000, 2, 'Zaar', '11/19/2022', 500),
    ('3742 4545 5400 0000', 8239, 10, 'Fabio', '11/20/2022', -100),
    ('3743 4545 5400 0001', 71, 84, 'Henry', '11/21/2022', 323),
    ('3744 4545 5421 0012', 819, 4, 'Olivier', '11/22/2022', 352),
    ('3745 4545 5450 0015', 1000, 2, 'Laligant', '11/23/2022', 4242),
    ('3746 4545 5060 1267', 732, 14, 'Eric', '11/24/2022', 999),
    ('9087 4545 5161 1267', 819, 8, 'Fuviut', '11/25/2022', -1000),
    ('3748 1285 5890 1267', 6173, 5, 'Sandra', '11/26/2022', 5000),
]

cursor.executemany('INSERT INTO Card_data (card_number, total_balance, transactions, card_holder_name, last_activity_date, last_transaction) VALUES (?, ?, ?, ?, ?, ?)', Card_data)

# Commit the changes and close the connection
conn.commit()
conn.close()
