import streamlit as st
        
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

def init_state():
    if "rates" not in st.session_state:
        st.session_state.rates = {
            "USD_RUB": 71.7318,
            "CNY_RUB": 10.5831
        }
    if "tariffs" not in st.session_state:
        st.session_state.tariffs = DEFAULT_TARIFFS.copy()
    if "customs" not in st.session_state:
        st.session_state.customs = {
            "enabled_flag": False,
            "vat_rate": 22.0,
            "duty_rate": 7.5
    }
    if "cargo" not in st.session_state:
        st.session_state.cargo = {
            "weight_per_unit": 500.0,
            "length": 800,
            "width": 1200,
            "height": 1000,
            "qty": 2,
            "invoice_usd": 5000.0,
            "dovoz_km": 50
        }
    if "results" not in st.session_state:
        st.session_state.results = {}

def reset_tariffs():
    st.session_state.tariffs.clear()
    st.session_state.tariffs.update(DEFAULT_TARIFFS)