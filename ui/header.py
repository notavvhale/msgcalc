import streamlit as st

from auth.cookies import delete_session


def show(auth):
    rates = st.session_state.get("rates", {})

    usd = rates.get("USD_RUB", 0.0)
    cny = rates.get("CNY_RUB", 0.0)

    left, right = st.columns([7, 3], gap="small")

    with left:
        st.markdown(
            """
            <div class="topbar-title">
                🚚 LTLCALC
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        c1, c2, c3, c4 = st.columns(
            [1.1, 1.1, 1.6, 0.45],
            gap="small",
        )

        with c1:
            st.markdown(
                f"""
                <div class="topbar-item">
                    USD <b>{usd:.2f}</b>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c2:
            st.markdown(
                f"""
                <div class="topbar-item">
                    CNY <b>{cny:.2f}</b>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c3:
            st.markdown(
                f"""
                <div class="topbar-user">
                    👤 {auth.username}
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c4:
            if st.button("⎋", key="logout", help="Выйти"):
                delete_session()
                auth.logout()
                st.rerun()

    page = st.segmented_control(
        label="",
        options=[
            "Расчёт",
            "История",
            "Справочники",
            "Тарифы",
            "Отчёты",
            "Курсы валют",
            "Настройки",
        ],
        default="Расчёт",
        key="main_tab",
    )

    return page