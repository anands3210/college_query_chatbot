import sqlite3

# new username and password set karo
NEW_USERNAME = "anand"
NEW_PASSWORD = "anand123"

# Database se connect karo
conn = sqlite3.connect("database/chatbot.db")
cursor = conn.cursor()

# Admin username aur password update karo
cursor.execute("UPDATE admin SET username = ?, password = ? WHERE id = 1", (NEW_USERNAME, NEW_PASSWORD))

# Save aur close karo
conn.commit()
conn.close()

print("✅ Admin credentials updated successfully!")
