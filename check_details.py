from services.tnved_database import get_connection

conn = get_connection()

rows = conn.execute("""
SELECT
    code,
    description,
    details
FROM tnved
WHERE code LIKE '8471%'
LIMIT 20
""").fetchall()

for row in rows:

    print("=" * 80)
    print(row["code"])
    print()
    print("DESCRIPTION:")
    print(row["description"])
    print()
    print("DETAILS:")
    print(row["details"])

conn.close()