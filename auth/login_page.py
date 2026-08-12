import streamlit as st

from . import auth
from auth.cookies import save_session


def show():

    st.markdown(
        """
        <div class="auth-page">
            <div class="auth-title">
                🔐 Авторизация
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Центральная колонка
    left, center, right = st.columns(
        [1, 2, 1],
        gap="small",
    )

    with center:

        with st.form("login_form"):

            username = st.text_input(
                "Логин",
                key="login_username",
            )

            password = st.text_input(
                "Пароль",
                type="password",
                key="login_password",
            )

            submit = st.form_submit_button(
                "Войти",
                use_container_width=True,
            )

    if submit:

        if auth.login(username, password):

            save_session(
                st.session_state.session_token
            )

            st.rerun()

        else:

            st.error(
                "Неверный логин или пароль."
            )