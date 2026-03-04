import sqlite3 as sq

conn = sq.connect('hotel.db')
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS customers (
    room_no INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    phone TEXT NOT NULL,
    adharcardno TEXT NOT NULL,
    room_type INTEGER NOT NULL,
    check_in_date TEXT NOT NULL,
    room_service INTEGER DEFAULT 0
)
""")
try:
    cur.execute(
        "INSERT INTO customers VALUES (?,?,?,?,?,?,?,?)",
        (101, "Shital", "Solapur", "9876543210", "123412341234", 1, "2026-03-04", 0)
    )
    conn.commit()  # Important! Save changes
    print("Data inserted successfully")
except Exception as e:
    print("Error:", e)

# 5️⃣ Fetch data
cur.execute("SELECT * FROM customers")
rows = cur.fetchall()
for row in rows:
    print(row)
conn.commit()
conn.close()

