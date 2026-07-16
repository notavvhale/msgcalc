import streamlit as st
from state import refresh


def _update():
    st.session_state.cargo["dovoz_km"] = st.session_state.ui_dovoz_km
    refresh()


def show():

    cargo = st.session_state.cargo

    st.header("Последняя миля")

    st.number_input(
        "Довоз (км)",
        min_value=0,
        step=1,
        value=cargo["dovoz_km"],
        key="ui_dovoz_km",
        on_change=_update,
    )