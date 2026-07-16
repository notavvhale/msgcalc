import streamlit as st

from state import refresh, sync_state


def show():

    st.header("Таможня")

    st.checkbox(
        "Рассчитать таможенные платежи",
        key="customs_enabled",
    )

    sync_state()
    refresh()

    calc = st.session_state.calc
    customs = st.session_state.customs

    if customs["enabled_flag"]:

        st.divider()

        st.header("Таможенные платежи")

        st.number_input(
            "Ставка НДС (%)",
            min_value=0.0,
            max_value=100.0,
            step=1.0,
            format="%.0f",
            key="customs_vat_rate",
        )

        st.number_input(
            "Ставка пошлины (%)",
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            format="%.1f",
            key="customs_duty_rate",
        )

        sync_state()
        refresh()

        calc = st.session_state.calc

        st.header("Таможня")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Тамож. стоимость",
            f"{calc['t_val']:,.2f} ₽",
        )

        col2.metric(
            f"Пошлина ({customs['duty_rate']:.1f}%)",
            f"{calc['duty']:,.2f} ₽",
        )

        col3.metric(
            f"НДС ({customs['vat_rate']:.0f}%)",
            f"{calc['vat']:,.2f} ₽",
        )

        col4.metric(
            "Тамож. сбор",
            f"{calc['fee']:,.2f} ₽",
        )

        st.metric(
            "Итого таможенных платежей",
            f"{calc['total_customs']:,.2f} ₽",
        )

        st.metric(
            "Полная себестоимость",
            f"{calc['full_cost']:,.2f} ₽",
        )