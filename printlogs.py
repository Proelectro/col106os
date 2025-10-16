import sqlite3

# You need to define the path to your database file
# For example: DB_PATH = "my_database.db"
DB_PATH = "logs.db" 

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Execute a SELECT query to fetch all columns from the 'logs' table
cursor.execute("SELECT * FROM logs")

# Fetch all the resulting rows into a list
rows = cursor.fetchall()

# Loop through the list of rows and print each one
print("--- All Logs ---")
for row in rows:
    print(row)

# Close the connection (no conn.commit() is needed for SELECT)
conn.close()