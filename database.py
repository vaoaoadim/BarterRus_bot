import sqlite3
import time

conn = sqlite3.connect("barter.sqlite")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS ads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    direction TEXT,
    category TEXT,
    title TEXT,
    description TEXT,
    contact TEXT,
    created_at INTEGER
)
''')

conn.commit()

def add_ad(user_id, direction, category, title, description, contact):
    created_at = int(time.time())
    cursor.execute('''
        INSERT INTO ads (user_id, direction, category, title, description, contact, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, direction, category, title, description, contact, created_at))
    conn.commit()

def get_last_ad_time(user_id):
    cursor.execute('''
        SELECT created_at FROM ads
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT 1
    ''', (user_id,))
    row = cursor.fetchone()
    return row[0] if row else None

def get_ads(direction=None, keyword=None, category=None):
    query = "SELECT * FROM ads WHERE 1=1"
    params = []

    if direction:
        query += " AND direction = ?"
        params.append(direction)

    if keyword:
        query += " AND (title LIKE ? OR description LIKE ?)"
        params += [f"%{keyword}%", f"%{keyword}%"]

    if category:
        query += " AND category = ?"
        params.append(category)

    cursor.execute(query, params)
    return cursor.fetchall()
