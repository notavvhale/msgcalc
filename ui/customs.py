import streamlit as st

from state import refresh


def _update_enabled():
    st.session_state.customs["enabled_flag"] = st.session_state.ui_enabled_flag
    refresh()


def _update_vat():
    st.session_state.customs["vat_rate"] = st.session_state.ui_vat_rate
    refresh()


def _update_duty():
    st.session_state.customs["duty_rate"] = st.session_state.ui_duty_rate
    refresh()


def show():

    customs = st.session_state.customs
    calc = st.session_state.calc

    st.header("Таможня")

    st.checkbox(
        "Рассчитать таможенные платежи",
        value=customs["enabled_flag"],
        key="ui_enabled_flag",
        on_change=_update_enabled,
    )

    if customs["enabled_flag"]:

        st.divider()

        st.header("Таможенные платежи")

        st.number_input(
            "Ставка НДС (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(customs["vat_rate"]),
            step=1.0,
            format="%.0f",
            key="ui_vat_rate",
            on_change=_update_vat,
        )

        st.number_input(
            "Ставка пошлины (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(customs["duty_rate"]),
            step=0.1,
            format="%.1f",
            key="ui_duty_rate",
            on_change=_update_duty,
        )

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