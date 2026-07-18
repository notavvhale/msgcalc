from collections import defaultdict

from services.tnved_database import get_connection


def search_candidates(features, limit=20):

    conn = get_connection()

    scores = defaultdict(
        lambda: {
            "score": 0,
        }
    )

    queries = []

    if features.product_type:
        queries.append((features.product_type, 40))

    if features.purpose:
        queries.append((features.purpose, 25))

    for feature in features.features:
        queries.append((feature, 10))

    for query, weight in queries:

        # ищем целую фразу
        rows = conn.execute(
            """
            SELECT
                code,
                description,
                duty_text,
                vat
            FROM tnved
            WHERE description LIKE ?
            """,
            (f"%{query}%",),
        ).fetchall()

        for row in rows:

            code = row["code"]

            if "code" not in scores[code]:

                scores[code].update(
                    {
                        "code": row["code"],
                        "description": row["description"],
                        "duty_text": row["duty_text"],
                        "vat": row["vat"],
                    }
                )

            scores[code]["score"] += weight

        # теперь ищем каждое слово отдельно
        words = [
            w
            for w in query.split()
            if len(w) > 3
        ]

        for word in words:

            rows = conn.execute(
                """
                SELECT
                    code,
                    description,
                    duty_text,
                    vat
                FROM tnved
                WHERE description LIKE ?
                """,
                (f"%{word}%",),
            ).fetchall()

            for row in rows:

                code = row["code"]

                if "code" not in scores[code]:

                    scores[code].update(
                        {
                            "code": row["code"],
                            "description": row["description"],
                            "duty_text": row["duty_text"],
                            "vat": row["vat"],
                        }
                    )

                scores[code]["score"] += max(weight // 2, 3)

    # штрафы

    for item in scores.values():

        for word in features.exclude:

            if word in item["description"]:
                item["score"] -= 20

    conn.close()

    return sorted(
        scores.values(),
        key=lambda x: x["score"],
        reverse=True,
    )[:limit]