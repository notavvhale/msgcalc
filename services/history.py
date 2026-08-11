import json
from datetime import datetime

from services.history_database import get_connection


def save_calculation(
    user_id: int,
    calculation_name: str,
    cargo: dict,
    calc: dict,
    tariffs: dict,
    rates: dict,
    customs: dict,
):
    conn = get_connection()
    print("SAVE CALCULATION NAME:", repr(calculation_name))
    cursor = conn.execute(
        """
        INSERT INTO calculation_history
        (
            user_id,
            calculation_name,
            product_name,
            tnved,

            qty,
            weight,
            volume,
            invoice_usd,

            usd_rub,
            cny_rub,

            full_cost,
            total_customs,

            created_at,

            cargo_json,
            calc_json,
            tariffs_json,
            rates_json,
            customs_json
        )
        VALUES (
            ?, ?,
            ?, ?,
            ?, ?, ?, ?,
            ?, ?,
            ?, ?,
            ?,
            ?, ?, ?, ?, ?
        )
        """,
        (
            user_id,
            calculation_name,
            cargo.get("product_name", ""),
            cargo.get("tnved", ""),

            cargo.get("qty", 0),
            cargo.get("weight_per_unit", 0),
            calc.get("volume", 0),
            cargo.get("invoice_usd", 0),

            rates.get("USD_RUB", 0),
            rates.get("CNY_RUB", 0),

            calc.get("full_cost", 0),
            calc.get("total_customs", 0),

            datetime.now().isoformat(timespec="seconds"),

            json.dumps(cargo, ensure_ascii=False, default=str),
            json.dumps(calc, ensure_ascii=False, default=str),
            json.dumps(tariffs, ensure_ascii=False, default=str),
            json.dumps(rates, ensure_ascii=False, default=str),
            json.dumps(customs, ensure_ascii=False, default=str),
        ),
    )

    conn.commit()

    history_id = cursor.lastrowid

    conn.close()

    return history_id

def get_history(user_id: int, limit: int = 100):
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            id,
            calculation_name,
            product_name,
            tnved,
            qty,
            weight,
            volume,
            invoice_usd,
            usd_rub,
            cny_rub,
            full_cost,
            total_customs,
            created_at
        FROM calculation_history
        WHERE user_id = ?
        ORDER BY datetime(created_at) DESC
        LIMIT ?
        """,
        (user_id, limit),
    ).fetchall()

    conn.close()

    return rows


def get_calculation(user_id: int, calculation_id: int):
    conn = get_connection()

    row = conn.execute(
        """
        SELECT *
        FROM calculation_history
        WHERE id = ?
          AND user_id = ?
        """,
        (calculation_id, user_id),
    ).fetchone()

    conn.close()

    if row is None:
        return None

    return row


def delete_calculation(user_id: int, calculation_id: int):
    conn = get_connection()

    cursor = conn.execute(
        """
        DELETE FROM calculation_history
        WHERE id = ?
          AND user_id = ?
        """,
        (calculation_id, user_id),
    )

    conn.commit()

    deleted = cursor.rowcount > 0

    conn.close()

    return deleted