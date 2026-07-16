from pathlib import Path
import streamlit as st

BASE_DIR = Path(__file__).parent

def load_css(filename: str):
    css_file = BASE_DIR / filename

    with css_file.open(encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )