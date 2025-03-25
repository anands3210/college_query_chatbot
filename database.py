import sqlite3

def get_answer(query):
    conn = sqlite3.connect("database/chatbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT answer FROM faq WHERE question=?", (query,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "Sorry, I don't understand."
