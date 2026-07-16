import streamlit as st
from formulas import calculate
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
    if "cargo_weight_per_unit" not in st.session_state:
        st.session_state.cargo_weight_per_unit = st.session_state.cargo["weight_per_unit"]

    if "cargo_length" not in st.session_state:
        st.session_state.cargo_length = st.session_state.cargo["length"]

    if "cargo_width" not in st.session_state:
        st.session_state.cargo_width = st.session_state.cargo["width"]

    if "cargo_height" not in st.session_state:
        st.session_state.cargo_height = st.session_state.cargo["height"]

    if "cargo_qty" not in st.session_state:
        st.session_state.cargo_qty = st.session_state.cargo["qty"]

    if "cargo_invoice_usd" not in st.session_state:
        st.session_state.cargo_invoice_usd = st.session_state.cargo["invoice_usd"]

    if "cargo_dovoz_km" not in st.session_state:
        st.session_state.cargo_dovoz_km = st.session_state.cargo["dovoz_km"]
    
    if "rate_usd" not in st.session_state:
        st.session_state.rate_usd = st.session_state.rates["USD_RUB"]

    if "rate_cny" not in st.session_state:
        st.session_state.rate_cny = st.session_state.rates["CNY_RUB"]

    if "tariff_thc_sea" not in st.session_state:
        st.session_state.tariff_thc_sea = st.session_state.tariffs["thc_sea_usd_m3"]

    if "tariff_doc_sea" not in st.session_state:
        st.session_state.tariff_doc_sea = st.session_state.tariffs["doc_sea_usd"]

    if "tariff_r_rail" not in st.session_state:
        st.session_state.tariff_r_rail = st.session_state.tariffs["r_rail_usd_m3"]

    if "tariff_r_sea" not in st.session_state:
        st.session_state.tariff_r_sea = st.session_state.tariffs["r_sea_usd_kg"]

    if "tariff_air_kg" not in st.session_state:
        st.session_state.tariff_air_kg = st.session_state.tariffs["air_usd_kg"]

    if "tariff_air_prr" not in st.session_state:
        st.session_state.tariff_air_prr = st.session_state.tariffs["air_prr_rub_kg"]

    if "tariff_rail_kg" not in st.session_state:
        st.session_state.tariff_rail_kg = st.session_state.tariffs["rail_usd_kg"]

    if "tariff_rail_m3" not in st.session_state:
        st.session_state.tariff_rail_m3 = st.session_state.tariffs["rail_usd_m3"]

    if "tariff_rail_doc" not in st.session_state:
        st.session_state.tariff_rail_doc = st.session_state.tariffs["rail_doc_usd"]

    if "tariff_road_kg" not in st.session_state:
        st.session_state.tariff_road_kg = st.session_state.tariffs["road_usd_kg"]

    if "tariff_road_doc" not in st.session_state:
        st.session_state.tariff_road_doc = st.session_state.tariffs["road_doc_usd"]
    if "customs_enabled" not in st.session_state:
        st.session_state.customs_enabled = st.session_state.customs["enabled_flag"]

    if "customs_vat_rate" not in st.session_state:
        st.session_state.customs_vat_rate = st.session_state.customs["vat_rate"]

    if "customs_duty_rate" not in st.session_state:
        st.session_state.customs_duty_rate = st.session_state.customs["duty_rate"]

    if "results" not in st.session_state:
        st.session_state.results = {}

    refresh()

def reset_tariffs():
    st.session_state.tariffs.clear()
    st.session_state.tariffs.update(DEFAULT_TARIFFS)

def refresh():

    st.session_state.calc = calculate(
        st.session_state.cargo,
        st.session_state.tariffs,
        st.session_state.rates,
        st.session_state.customs,
    )

def sync_state():

    cargo = st.session_state.cargo

    cargo["weight_per_unit"] = st.session_state.cargo_weight_per_unit
    cargo["length"] = st.session_state.cargo_length
    cargo["width"] = st.session_state.cargo_width
    cargo["height"] = st.session_state.cargo_height
    cargo["qty"] = st.session_state.cargo_qty
    cargo["invoice_usd"] = st.session_state.cargo_invoice_usd
    cargo["dovoz_km"] = st.session_state.cargo_dovoz_km

    rates = st.session_state.rates

    rates["USD_RUB"] = st.session_state.rate_usd
    rates["CNY_RUB"] = st.session_state.rate_cny

    tariffs = st.session_state.tariffs

    tariffs["thc_sea_usd_m3"] = st.session_state.tariff_thc_sea
    tariffs["doc_sea_usd"] = st.session_state.tariff_doc_sea
    tariffs["r_rail_usd_m3"] = st.session_state.tariff_r_rail
    tariffs["r_sea_usd_kg"] = st.session_state.tariff_r_sea

    tariffs["air_usd_kg"] = st.session_state.tariff_air_kg
    tariffs["air_prr_rub_kg"] = st.session_state.tariff_air_prr

    tariffs["rail_usd_kg"] = st.session_state.tariff_rail_kg
    tariffs["rail_usd_m3"] = st.session_state.tariff_rail_m3
    tariffs["rail_doc_usd"] = st.session_state.tariff_rail_doc

    tariffs["road_usd_kg"] = st.session_state.tariff_road_kg
    tariffs["road_doc_usd"] = st.session_state.tariff_road_doc
    customs = st.session_state.customs

    customs["enabled_flag"] = st.session_state.customs_enabled
    customs["vat_rate"] = st.session_state.customs_vat_rate
    customs["duty_rate"] = st.session_state.customs_duty_rate