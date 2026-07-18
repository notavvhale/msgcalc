import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

import requests
import streamlit as st

from state import refresh, reset_tariffs


# ============================================
# Получение курсов ЦБ
# ============================================

#@st.cache_data(ttl=3600)
def get_cbr_rates():
    url = "https://www.cbr.ru/scripts/XML_daily.asp"

    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10,
        )

        response.raise_for_status()
        response.encoding = "windows-1251"

        root = ET.fromstring(response.text)

        rates = {}

        for valute in root.findall("Valute"):

            code = valute.findtext("CharCode")

            if code not in ("USD", "CNY"):
                continue

            nominal = int(valute.findtext("Nominal"))
            value = float(valute.findtext("Value").replace(",", "."))

            rates[code] = value / nominal

        rates["date"] = root.attrib["Date"]

        return rates

    except Exception:
        return None


# ============================================
# Обновление курса
# ============================================

def update_rates(force=False):
    now = datetime.now()

    need_update = (
        force
        or "last_rate_update" not in st.session_state
        or now - st.session_state.last_rate_update >= timedelta(hours=1)
    )

    if not need_update:
        return False

    cbr = get_cbr_rates()

    if not cbr:
        return False

    rates = st.session_state.rates

    rates["USD_RUB"] = cbr["USD"]
    rates["CNY_RUB"] = cbr["CNY"]

    st.session_state.ui_USD_RUB = cbr["USD"]
    st.session_state.ui_CNY_RUB = cbr["CNY"]

    st.session_state.cbr_date = cbr["date"]
    st.session_state.last_rate_update = now

    return True


# ============================================
# Callback
# ============================================

def _update_tariff(field):
    st.session_state.tariffs[field] = st.session_state[f"ui_{field}"]
    refresh()


def _update_rate(field):
    st.session_state.rates[field] = st.session_state[f"ui_{field}"]
    refresh()


# ============================================
# Страница
# ============================================

def show():
    tariffs = st.session_state.tariffs
    rates = st.session_state.rates

    # Автоматическая синхронизация курсов
    update_rates()

    if "ui_USD_RUB" not in st.session_state:
        st.session_state.ui_USD_RUB = rates["USD_RUB"]

    if "ui_CNY_RUB" not in st.session_state:
        st.session_state.ui_CNY_RUB = rates["CNY_RUB"]

    st.header("💵 Прайс-лист")
    st.markdown("*Измените тарифы — они сразу применятся к расчётам.*")

    col1, col2 = st.columns(2)

    # ====================================================
    # Левая колонка
    # ====================================================

    with col1:

        st.subheader("🌊 Море + ЖД (LCL SR)")

        st.number_input(
            "THC, USD/м³",
            value=tariffs["thc_sea_usd_m3"],
            step=1.0,
            key="ui_thc_sea_usd_m3",
            on_change=_update_tariff,
            args=("thc_sea_usd_m3",),
        )

        st.number_input(
            "Doc fee, USD/shpt",
            value=tariffs["doc_sea_usd"],
            step=1.0,
            key="ui_doc_sea_usd",
            on_change=_update_tariff,
            args=("doc_sea_usd",),
        )

        st.number_input(
            "R rail, USD/м³",
            value=tariffs["r_rail_usd_m3"],
            step=0.1,
            format="%.1f",
            key="ui_r_rail_usd_m3",
            on_change=_update_tariff,
            args=("r_rail_usd_m3",),
        )

        st.number_input(
            "R sea, USD/кг",
            value=tariffs["r_sea_usd_kg"],
            step=0.1,
            format="%.1f",
            key="ui_r_sea_usd_kg",
            on_change=_update_tariff,
            args=("r_sea_usd_kg",),
        )

        st.divider()

        st.subheader("✈️ Авиа")

        st.number_input(
            "USD/кг",
            value=tariffs["air_usd_kg"],
            step=0.5,
            format="%.1f",
            key="ui_air_usd_kg",
            on_change=_update_tariff,
            args=("air_usd_kg",),
        )

        st.number_input(
            "ПРР, руб/кг",
            value=tariffs["air_prr_rub_kg"],
            step=0.01,
            format="%.2f",
            key="ui_air_prr_rub_kg",
            on_change=_update_tariff,
            args=("air_prr_rub_kg",),
        )

    # ====================================================
    # Правая колонка
    # ====================================================

    with col2:

        st.subheader("🚂 Прямое ЖД")

        st.number_input(
            "USD/кг",
            value=tariffs["rail_usd_kg"],
            step=0.1,
            format="%.1f",
            key="ui_rail_usd_kg",
            on_change=_update_tariff,
            args=("rail_usd_kg",),
        )

        st.number_input(
            "USD/м³",
            value=tariffs["rail_usd_m3"],
            step=5.0,
            key="ui_rail_usd_m3",
            on_change=_update_tariff,
            args=("rail_usd_m3",),
        )

        st.number_input(
            "USD/shpt",
            value=tariffs["rail_doc_usd"],
            step=1.0,
            key="ui_rail_doc_usd",
            on_change=_update_tariff,
            args=("rail_doc_usd",),
        )

        st.divider()

        st.subheader("🚛 Автосборка")

        st.number_input(
            "USD/кг",
            value=tariffs["road_usd_kg"],
            step=0.1,
            format="%.1f",
            key="ui_road_usd_kg",
            on_change=_update_tariff,
            args=("road_usd_kg",),
        )

        st.number_input(
            "USD/shpt",
            value=tariffs["road_doc_usd"],
            step=1.0,
            key="ui_road_doc_usd",
            on_change=_update_tariff,
            args=("road_doc_usd",),
        )

    # ====================================================
    # Курсы валют
    # ====================================================

    st.divider()
    st.subheader("💱 Курсы валют")

    col_btn, _ = st.columns([1, 3])

    with col_btn:
        if st.button("🔄 Обновить сейчас"):
            if update_rates(force=True):
                refresh()
                st.success("Курс успешно обновлён.")
            else:
                st.error("Не удалось получить курс ЦБ.")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "USD / RUB",
            f"{rates['USD_RUB']:.4f}"
        )

    with col2:
        st.metric(
            "CNY / RUB",
            f"{rates['CNY_RUB']:.4f}"
        )

    if "cbr_date" in st.session_state:
        st.caption(f"Курс ЦБ на {st.session_state.cbr_date}")

    if "last_rate_update" in st.session_state:
        st.caption(
            f"Последнее обновление: "
            f"{st.session_state.last_rate_update.strftime('%d.%m.%Y %H:%M:%S')}"
        )

    # ====================================================
    # Сброс
    # ====================================================

    st.divider()

    if st.button("🔄 Сбросить тарифы"):

        reset_tariffs()

        st.session_state.rates["USD_RUB"] = 71.7318
        st.session_state.rates["CNY_RUB"] = 10.5831

        st.session_state.ui_USD_RUB = 71.7318
        st.session_state.ui_CNY_RUB = 10.5831

        st.session_state.pop("last_rate_update", None)
        st.session_state.pop("cbr_date", None)

        refresh()