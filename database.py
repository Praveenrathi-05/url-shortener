import sqlite3
from pathlib import Path
file_name = Path(__file__).resolve().parent / "url_shortener.db"
from datetime import datetime
import random

connection = sqlite3.connect(file_name, check_same_thread=False)
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS links(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_code TEXT UNIQUE,
                url TEXT,
                date_created TEXT
)
""")

connection.commit()

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encode_base62(number):
    if number == 0:
        return '0'
    decode_text = ""
    while number > 0:
        rem = number % 62
        number = number // 62
        decode_text = ALPHABET[rem] + decode_text
    return decode_text

def create_short_link(url):
    while True:
        code = "".join(random.choices(ALPHABET, k=6))
        try:
            cursor.execute("INSERT INTO links (short_code, url, date_created) VALUES (?,?,?)", (code, url, datetime.now().isoformat()))
            connection.commit()
            return code
        except sqlite3.IntegrityError:
            continue

def get_match(code):
    cursor.execute("SELECT url FROM links WHERE short_code = ?", (code,))
    result = cursor.fetchone()
    if result is None:
        return None
    return result[0]