import sqlite3

# Database Connection
conn = sqlite3.connect("database/chatbot.db")
cursor = conn.cursor()

# Create chatbot_responses Table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS chatbot_responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT UNIQUE NOT NULL,
        response TEXT NOT NULL
    )
""")

# Create admin_users Table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
""")

# Insert Default Admin (Username: admin, Password: admin123)
cursor.execute("INSERT OR IGNORE INTO admin_users (username, password) VALUES ('admin', 'admin123')")

conn.commit()
conn.close()

print("Database and tables created successfully!")
