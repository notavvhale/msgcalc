import streamlit as st
from state import refresh, sync_state

def show():
    t = st.session_state.tariffs
    st.header("Последняя миля")
    st.number_input(
        "Довоз (км)",
        key="cargo_dovoz_km",
    )
    sync_state()
    refresh()