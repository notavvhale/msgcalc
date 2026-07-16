import streamlit as st
from formulas import calculate

DEFAULT_TARIFFS = {
    "thc_sea_usd_m3": 40.0,
    "doc_sea_usd": 80.0,
    "r_rail_usd_m3": 1.9,
    "r_sea_usd_kg": 0.8,
    "air_usd_kg": 5.0,
    "air_prr_rub_kg": 6.06,
    "rail_usd_kg": 2.5,
    "rail_usd_m3": 200.0,
    "rail_doc_usd": 50.0,
    "road_usd_kg": 2.5,
    "road_doc_usd": 70.0,
}

DEFAULT_RATES = {
    "USD_RUB": 71.7318,
    "CNY_RUB": 10.5831,
}

DEFAULT_CUSTOMS = {
    "enabled_flag": False,
    "vat_rate": 22.0,
    "duty_rate": 7.5,
}

DEFAULT_CARGO = {
    "weight_per_unit": 500.0,
    "length": 800,
    "width": 1200,
    "height": 1000,
    "qty": 2,
    "invoice_usd": 5000.0,
    "dovoz_km": 50,
}


def init_state():
    """Инициализация состояния приложения."""

    st.session_state.setdefault("cargo", DEFAULT_CARGO.copy())
    st.session_state.setdefault("rates", DEFAULT_RATES.copy())
    st.session_state.setdefault("tariffs", DEFAULT_TARIFFS.copy())
    st.session_state.setdefault("customs", DEFAULT_CUSTOMS.copy())

    refresh()


def refresh():
    """Пересчитать стоимость доставки."""

    st.session_state.calc = calculate(
        cargo=st.session_state.cargo,
        tariffs=st.session_state.tariffs,
        rates=st.session_state.rates,
        customs=st.session_state.customs,
    )


def reset_tariffs():
    """Сбросить тарифы к значениям по умолчанию."""

    st.session_state.tariffs = DEFAULT_TARIFFS.copy()
    refresh()