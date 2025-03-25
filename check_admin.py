import sqlite3

# Database se connect karo
conn = sqlite3.connect("database/chatbot.db")
cursor = conn.cursor()

# Admin table se data fetch karo
cursor.execute("SELECT * FROM admin")
rows = cursor.fetchall()

# Result print karo
if rows:
    print("✅ Admin Table Data:")
    for row in rows:
        print(row)
else:
    print("❌ Admin Table में कोई data नहीं है!")

# Database close karo
conn.close()
