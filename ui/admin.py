import streamlit as st

from auth import auth
from auth.users import (
    get_users,
    create_user,
    update_user,
    delete_user,
    change_password,
)


def show():

    st.title("👥 Пользователи")

    st.divider()

    users = get_users()

    for user in users:

        with st.container(border=True):

            info, actions = st.columns([6, 2])

            with info:

                st.subheader(user["name"])

                st.caption(f"Логин: {user['username']}")

                st.caption(f"Email: {user['email']}")

                badge = {
                    "admin": "🟥 Администратор",
                    "manager": "🟨 Менеджер",
                    "user": "🟩 Пользователь",
                }

                st.caption(badge.get(user["role"], user["role"]))

            with actions:

                if st.button(
                    "✏ Изменить",
                    key=f"edit_{user['id']}",
                    use_container_width=True
                ):
                    st.session_state.edit_user = user["id"]

                if st.button(
                    "🔑 Пароль",
                    key=f"pwd_{user['id']}",
                    use_container_width=True
                ):
                    st.session_state.change_password = user["id"]

                if st.button(
                    "🗑 Удалить",
                    key=f"delete_{user['id']}",
                    use_container_width=True
                ):

                    if user["username"] == auth.username:

                        st.warning("Нельзя удалить текущего пользователя.")

                    else:

                        delete_user(user["id"])

                        st.success("Пользователь удалён.")

                        st.rerun()

        if st.session_state.get("edit_user") == user["id"]:

            with st.container(border=True):

                st.subheader("Редактирование")

                name = st.text_input(
                    "Имя",
                    value=user["name"],
                    key=f"name_{user['id']}"
                )

                email = st.text_input(
                    "Email",
                    value=user["email"],
                    key=f"email_{user['id']}"
                )

                role = st.selectbox(
                    "Роль",
                    [
                        "admin",
                        "manager",
                        "user",
                    ],
                    index=[
                        "admin",
                        "manager",
                        "user",
                    ].index(user["role"]),
                    key=f"role_{user['id']}"
                )

                active = st.checkbox(
                    "Активен",
                    value=bool(user["active"]),
                    key=f"active_{user['id']}"
                )

                c1, c2 = st.columns(2)

                with c1:

                    if st.button(
                        "💾 Сохранить",
                        key=f"save_{user['id']}",
                        use_container_width=True
                    ):

                        update_user(
                            user["id"],
                            name,
                            email,
                            role,
                            active
                        )

                        del st.session_state.edit_user

                        st.success("Изменения сохранены.")

                        st.rerun()

                with c2:

                    if st.button(
                        "❌ Отмена",
                        key=f"cancel_{user['id']}",
                        use_container_width=True
                    ):

                        del st.session_state.edit_user

                        st.rerun()

        if st.session_state.get("change_password") == user["id"]:

            with st.container(border=True):

                st.subheader("Смена пароля")

                password1 = st.text_input(
                    "Новый пароль",
                    type="password",
                    key=f"pass1_{user['id']}"
                )

                password2 = st.text_input(
                    "Повторите пароль",
                    type="password",
                    key=f"pass2_{user['id']}"
                )

                c1, c2 = st.columns(2)

                with c1:

                    if st.button(
                        "💾 Сохранить пароль",
                        key=f"savepwd_{user['id']}",
                        use_container_width=True
                    ):

                        if password1 != password2:

                            st.error("Пароли не совпадают.")

                        elif password1 == "":

                            st.error("Введите пароль.")

                        else:

                            change_password(
                                user["id"],
                                password1
                            )

                            del st.session_state.change_password

                            st.success("Пароль изменён.")

                            st.rerun()

                with c2:

                    if st.button(
                        "❌ Отмена",
                        key=f"cancelpwd_{user['id']}",
                        use_container_width=True
                    ):

                        del st.session_state.change_password

                        st.rerun()

    st.divider()

    st.header("➕ Новый пользователь")

    with st.form("create_user"):

        username = st.text_input("Логин")

        password = st.text_input(
            "Пароль",
            type="password"
        )

        name = st.text_input("Имя")

        email = st.text_input("Email")

        role = st.selectbox(
            "Роль",
            [
                "admin",
                "manager",
                "user",
            ]
        )

        submit = st.form_submit_button(
            "Создать пользователя",
            use_container_width=True
        )

        if submit:

            if not username.strip():

                st.error("Введите логин.")

            elif not password:

                st.error("Введите пароль.")

            elif not name.strip():

                st.error("Введите имя.")

            else:

                create_user(
                    username,
                    password,
                    name,
                    email,
                    role
                )

                st.success("Пользователь создан.")

                st.rerun()