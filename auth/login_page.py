import streamlit as st

from . import auth
from auth.cookies import save_session

def show():

    st.title("🔐 Авторизация")

    with st.form("login_form"):

        username = st.text_input(
            "Логин"
        )

        password = st.text_input(
            "Пароль",
            type="password"
        )

        submit = st.form_submit_button(
            "Войти",
            use_container_width=True
        )

    if submit:

        if auth.login(username, password):
            save_session(
            st.session_state.session_token
        )
            st.rerun()

        else:

            st.error("Неверный логин или пароль.")