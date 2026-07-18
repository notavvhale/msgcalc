from services.tnved_database import get_connection

conn = get_connection()

rows = conn.execute("""
SELECT code, description
FROM tnved
WHERE description LIKE '%портатив%'
""").fetchall()

print(len(rows))

for row in rows[:10]:
    print(row["code"], row["description"])

conn.close()