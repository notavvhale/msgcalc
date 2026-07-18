from services.tnved_database import get_connection

conn = get_connection()

rows = conn.execute("""
SELECT code, description
FROM tnved
LIMIT 20
""").fetchall()

for row in rows:
    print(row["code"])
    print(row["description"])
    print("-" * 80)

conn.close()