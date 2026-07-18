from services.tnved_database import get_connection

conn = get_connection()

count = conn.execute(
    "SELECT COUNT(*) FROM tnved"
).fetchone()[0]

print("Количество записей:", count)

rows = conn.execute("""
SELECT code, description
FROM tnved
ORDER BY code
LIMIT 10
""").fetchall()

print("\nПервые записи:")

for row in rows:
    print(row["code"], row["description"])

conn.close()