import sqlite3

connection = sqlite3.connect("solutions.db")

cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS solutions (id INTEGER PRIMARY KEY, filename text, url text, sign_lang text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (language text PRIMARY KEY, suffix text, spacy_package text)"
cursor.execute(create_table)

connection.commit()

connection.close()