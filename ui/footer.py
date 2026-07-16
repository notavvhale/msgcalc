import streamlit as st


def show():

    calc = st.session_state.calc

    footer_html = f"""
<div class="footer">
    <div class="footer-left">
        Страховка {calc["insurance_rub"]:,.2f} ₽ |
        Стоимость довоза {calc["dovoz_cost"]:,.2f} ₽
    </div>
    <div class="footer-right">
        Полная себестоимость {calc["full_cost"]:,.2f} ₽
    </div>
</div>
"""

    st.markdown(
        footer_html,
        unsafe_allow_html=True,
    )