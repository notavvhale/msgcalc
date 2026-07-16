from .database import get_connection
from .security import hash_password

#СОЗХДАНИЕ ПОЛЬЗВАТЕЛЯ
def create_user(
    username,
    password,
    name,
    email,
    role="user"
):

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO users
        (
            username,
            password,
            name,
            email,
            role
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            username,
            hash_password(password),
            name,
            email,
            role,
        ),
    )

    conn.commit()
    conn.close()

#ПОЛУЧЕНИЕ ПОЛЬЗОВАТЕЛЯ
def get_user(username):

    conn = get_connection()

    row = conn.execute(
        "SELECT * FROM users WHERE username=?",
        (username,),
    ).fetchone()

    conn.close()

    return row
#ПОЛУЧЕНИЕ СПИСКА ПОЛЬЗОВАТЕЛЕЙ
def get_users():

    conn = get_connection()

    rows = conn.execute(
        "SELECT * FROM users ORDER BY name"
    ).fetchall()

    conn.close()

    return rows

#ПОЛУЧЕНИЕ ПОРЛЬЗОВАТЕЛЯ ПО АЙДИ
def get_user_by_id(user_id):

    conn = get_connection()

    row = conn.execute(
        """
        SELECT *
        FROM users
        WHERE id=?
        """,
        (user_id,)
    ).fetchone()

    conn.close()

    return row

#ИЗМЕНЕНИЕ
def update_user(
    user_id,
    name,
    email,
    role,
    active
):

    conn = get_connection()

    conn.execute("""
        UPDATE users
        SET
            name=?,
            email=?,
            role=?,
            active=?
        WHERE id=?
    """,
    (
        name,
        email,
        role,
        int(active),
        user_id
    ))

    conn.commit()
    conn.close()

#ИЗМЕНЕНИЕ ПАРОЛЯ   
def change_password(
    user_id,
    password
):

    conn = get_connection()

    conn.execute("""
        UPDATE users
        SET password=?
        WHERE id=?
    """,
    (
        hash_password(password),
        user_id
    ))

    conn.commit()
    conn.close()

#УДАЛЕНИЕ
def delete_user(user_id):

    conn = get_connection()

    conn.execute(
        "DELETE FROM users WHERE id=?",
        (user_id,),
    )

    conn.commit()
    conn.close()