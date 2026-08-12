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

    # =====================================================
# HEADER
# =====================================================

    left, right = st.columns([7, 3], gap="small")

    with left:

        st.markdown(
            """
            <div class="ltl-brand">
                <span class="ltl-logo">🚚</span>
                <span>LTLCALC</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


    with right:

        c1, c2, c3, c4 = st.columns(
            [1.1, 1.1, 1.5, 1.4],
            gap="small",
        )

        with c1:

            st.markdown(
                f"""
                <div class="ltl-rate">
                    USD <strong>{usd:.2f}</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c2:

            st.markdown(
                f"""
                <div class="ltl-rate">
                    CNY <strong>{cny:.2f}</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c4:

            with st.popover(
                f"👤 {auth.username} ▾",
                use_container_width=True,
            ):

                st.caption(
                    auth.email or ""
                )

                if st.button(
                    "🚪 Выйти",
                    key="header_logout",
                    use_container_width=True,
                ):

                    delete_session()
                    auth.logout()
                    st.rerun()

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

    with st.container(key="main-navigation"):

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

    return st.session_state.main_tab