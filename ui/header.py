import textwrap

import streamlit as st

from auth.cookies import delete_session


TABS = [
    "Расчёт",
    "История",
    "Тарифы",
    "Настройки",
]


def show(auth):

    rates = st.session_state.get("rates", {})

    usd = rates.get("USD_RUB", 0.0)
    cny = rates.get("CNY_RUB", 0.0)

    if "main_tab" not in st.session_state:
        st.session_state.main_tab = "Расчёт"

    # =====================================================
    # HEADER
    # =====================================================

    header_html = textwrap.dedent(
        f"""
        <div class="ltl-header">
            <div class="ltl-brand">
                <span class="ltl-logo">🚚</span>
                <span>LTLCALC</span>
            </div>
            <div class="ltl-header-right">
                <span class="ltl-rate">
                    USD <strong>{usd:.2f}</strong>
                </span>
                <span class="ltl-rate">
                    CNY <strong>{cny:.2f}</strong>
                </span>
                <span class="ltl-user">
                    👤 <strong>{auth.username}</strong>
                </span>
            </div>
        </div>
        """
    )

    st.markdown(
        header_html,
        unsafe_allow_html=True,
    )

    # =====================================================
    # РАЗДЕЛИТЕЛЬ
    # =====================================================

    st.markdown(
        '<div class="ltl-header-divider"></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
    '<div class="ltl-nav-spacer"></div>',
    unsafe_allow_html=True,
    )   
    # =====================================================
    # NAVIGATION
    # =====================================================

    nav = st.columns(
        [
            0.85,
            0.95,
            1.25,
            0.85,
            0.85,
            1.2,
            0.95,
            0.45,
        ],
        gap="small",
    )

    for index, tab in enumerate(TABS):

        with nav[index]:

            if st.button(
                tab,
                key=f"main_nav_{index}",
                use_container_width=True,
            ):
                st.session_state.main_tab = tab
                st.rerun()

    # =====================================================
    # LOGOUT
    # =====================================================

    with nav[-1]:

        if st.button(
            "⎋",
            key="logout",
            help="Выйти",
            use_container_width=True,
        ):
            delete_session()
            auth.logout()
            st.rerun()

    return st.session_state.main_tab