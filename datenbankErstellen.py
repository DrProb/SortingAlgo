import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS daten (
    zahlOben INTEGER,
    wort TEXT,
    zahlUnten INTEGER
)
""")

with open("data.txt", "r", encoding="utf-8") as datei:
    lines = [line.strip() for line in datei]

rows = [lines[i:i+3] for i in range(0, len(lines), 3)]

cursor.executemany("INSERT INTO daten (zahlOben, wort, zahlUnten) VALUES (?, ?, ?)", rows)

connection.commit()

cursor.execute("SELECT COUNT(wort) FROM daten")
for row in cursor.fetchall():
    print(row)

connection.close()
