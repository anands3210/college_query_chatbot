import sqlite3

# Database se connect karo
conn = sqlite3.connect("database/chatbot.db")
cursor = conn.cursor()

# Admin Table banao (agar pehle se na ho)
cursor.execute('''
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# Default Admin Username and Password set karo
cursor.execute("INSERT INTO admin (username, password) VALUES (?, ?)", ("admin", "admin123"))

# Save and close karo
conn.commit()
conn.close()

print("✅ Admin table created successfully with default login!")
