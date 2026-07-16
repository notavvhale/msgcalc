import streamlit as st

from .users import get_user, get_user_by_id 
from .security import verify_password
from .session import (
    create_session,
    delete_session,
    get_session,
)

class AuthService:

    def login(self, username: str, password: str) -> bool:

        user = get_user(username)

        if user is None:
            return False

        if not verify_password(user["password"], password):
            return False

        if not user["active"]:
            return False

        st.session_state.authentication_status = True
        st.session_state.user = dict(user)
        token = create_session(user["id"])
        st.session_state.session_token = token
        return True
    
    def logout(self):

        token = st.session_state.get(
            "session_token"
        )

        if token:

            delete_session(token)

        st.session_state.clear()

        return

    @property
    def authenticated(self):

        return st.session_state.get(
            "authentication_status",
            False,
        )

    @property
    def user(self):

        return st.session_state.get("user")

    @property
    def username(self):

        if self.user:
            return self.user["username"]

        return None

    @property
    def name(self):

        if self.user:
            return self.user["name"]

        return None

    @property
    def email(self):

        if self.user:
            return self.user["email"]

        return None

    @property
    def role(self):

        if self.user:
            return self.user["role"]

        return None
    
    def restore(self, token):

        session = get_session(token)

        if session is None:
            return False

        user = get_user_by_id(
            session["user_id"]
        )

        if user is None:
            return False

        st.session_state.authentication_status = True

        st.session_state.user = dict(user)

        st.session_state.session_token = token

        return True