import sqlite3

conn = sqlite3.connect("barter.sqlite")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS ads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    direction TEXT,
    category TEXT,
    title TEXT,
    description TEXT,
    contact TEXT
)
''')
conn.commit()

def add_ad(direction, category, title, description, contact):
    cursor.execute("INSERT INTO ads (direction, category, title, description, contact) VALUES (?, ?, ?, ?, ?)",
                   (direction, category, title, description, contact))
    conn.commit()

def get_ads(direction=None, keyword=None, category=None):
    query = "SELECT * FROM ads WHERE 1=1"
    params = []

    if direction:
        query += " AND direction = ?"
        params.append(direction)
    if keyword:
        query += " AND (title LIKE ? OR description LIKE ?)"
        keyword_param = f"%{keyword}%"
        params.extend([keyword_param, keyword_param])
    if category:
        query += " AND category = ?"
        params.append(category)

    return cursor.execute(query, params).fetchall()
