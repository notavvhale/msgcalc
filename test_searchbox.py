from services.tnved_database import get_connection

conn = get_connection()

print("Количество записей:")
print(conn.execute("SELECT COUNT(*) FROM tnved").fetchone()[0])

print("\nПервые 20 кодов:")

rows = conn.execute("""
SELECT code
FROM tnved
ORDER BY code
LIMIT 20
""").fetchall()

for row in rows:
    print(row["code"])

print("\nПоиск кода 0101900000:")

row = conn.execute("""
SELECT code, description
FROM tnved
WHERE code = ?
""", ("0101900000",)).fetchone()

print(row)

conn.close()