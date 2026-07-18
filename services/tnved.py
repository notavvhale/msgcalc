from services.tnved_database import get_connection


def get_by_code(code: str):
    """
    Получить запись по полному коду ТН ВЭД.
    """

    conn = get_connection()

    row = conn.execute(
        """
        SELECT *
        FROM tnved
        WHERE code = ?
        """,
        (code.strip(),),
    ).fetchone()

    conn.close()

    return dict(row) if row else None


def search_by_code(prefix: str, limit: int = 20):
    """
    Поиск по первым цифрам кода.
    Например:
    8471
    """

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            code,
            description
        FROM tnved
        WHERE code LIKE ?
        ORDER BY code
        LIMIT ?
        """,
        (f"{prefix}%", limit),
    ).fetchall()

    conn.close()

    return [dict(r) for r in rows]


def search_by_name(text: str, limit: int = 20):
    """
    Поиск по части названия.
    """

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            code,
            description
        FROM tnved
        WHERE LOWER(description) LIKE LOWER(?)
        ORDER BY description
        LIMIT ?
        """,
        (f"%{text}%", limit),
    ).fetchall()

    conn.close()

    return [dict(r) for r in rows]


def suggest(text: str, limit: int = 10):
    """
    Универсальный поиск.
    Если введены цифры — ищем по коду.
    Иначе — по названию.
    """
    text = text.strip()

    if not text:
        return []
    
    conn = get_connection()

    count = conn.execute(
        "SELECT COUNT(*) FROM tnved"
    ).fetchone()[0]

    print("COUNT:", count)

    rows = conn.execute(
        """
        SELECT
            code,
            description
        FROM tnved
        WHERE code LIKE ?
        LIMIT 5
        """,
        (f"{text}%",),
    ).fetchall()

    print("ROWS:", rows)

    conn.close()

    return [dict(r) for r in rows]