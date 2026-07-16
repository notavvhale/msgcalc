import xml.etree.ElementTree as ET

import requests
import streamlit as st

from state import refresh, reset_tariffs, sync_state


# -------------------- КУРСЫ ЦБ --------------------

@st.cache_data(ttl=3600)
def get_cbr_rates():
    """Получить актуальные курсы USD и CNY с сайта ЦБ РФ"""

    url = "https://www.cbr.ru/scripts/XML_daily.asp"

    try:
        response = requests.get(url, timeout=5)
        response.encoding = "windows-1251"

        root = ET.fromstring(response.text)

        rates = {}

        for valute in root.findall("Valute"):

            code = valute.find("CharCode").text
            value = float(valute.find("Value").text.replace(",", "."))

            if code == "USD":
                rates["USD"] = value

            elif code == "CNY":
                rates["CNY"] = value

        rates["date"] = root.get("Date")

        return rates

    except Exception:

        return None


# -------------------- СТРАНИЦА --------------------

def show():

    st.header("💵 Прайс-лист")

    st.markdown(
        "*Измените тарифы — они сразу применятся к расчётам.*"
    )

    col1, col2 = st.columns(2)

    # -------------------------------------------------

    with col1:

        st.subheader("🌊 Море + ЖД (LCL SR)")

        st.number_input(
            "THC, USD/м³",
            step=1.0,
            key="tariff_thc_sea",
        )

        st.number_input(
            "Doc fee, USD/shpt",
            step=1.0,
            key="tariff_doc_sea",
        )

        st.number_input(
            "R rail, USD/м³",
            step=0.1,
            format="%.1f",
            key="tariff_r_rail",
        )

        st.number_input(
            "R sea, USD/кг",
            step=0.1,
            format="%.1f",
            key="tariff_r_sea",
        )

        st.divider()

        st.subheader("✈️ Авиа")

        st.number_input(
            "USD/кг",
            step=0.5,
            format="%.1f",
            key="tariff_air_kg",
        )

        st.number_input(
            "ПРР, руб/кг",
            step=0.01,
            format="%.2f",
            key="tariff_air_prr",
        )

    # -------------------------------------------------

    with col2:

        st.subheader("🚂 Прямое ЖД")

        st.number_input(
            "USD/кг",
            step=0.1,
            format="%.1f",
            key="tariff_rail_kg",
        )

        st.number_input(
            "USD/м³",
            step=5.0,
            key="tariff_rail_m3",
        )

        st.number_input(
            "USD/shpt",
            step=1.0,
            key="tariff_rail_doc",
        )

        st.divider()

        st.subheader("🚛 Автосборка")

        st.number_input(
            "USD/кг",
            step=0.1,
            format="%.1f",
            key="tariff_road_kg",
        )

        st.number_input(
            "USD/shpt",
            step=1.0,
            key="tariff_road_doc",
        )

    # -------------------------------------------------

    st.divider()

    st.subheader("💱 Курсы валют")

    col_btn, _ = st.columns([1, 3])

    with col_btn:

        if st.button(
            "🔄 Загрузить курс ЦБ",
            key="btn_cbr",
        ):

            cbr = get_cbr_rates()

            if cbr:

                st.session_state.rate_usd = cbr["USD"]
                st.session_state.rate_cny = cbr["CNY"]
                st.session_state.cbr_date = cbr["date"]

                st.success(
                    f"Курс обновлён ({cbr['date']})"
                )

            else:

                st.error(
                    "Не удалось получить курс ЦБ."
                )

    col_cur1, col_cur2 = st.columns(2)

    with col_cur1:

        st.number_input(
            "USD / RUB",
            step=0.01,
            format="%.4f",
            key="rate_usd",
        )

    with col_cur2:

        st.number_input(
            "CNY / RUB",
            step=0.01,
            format="%.4f",
            key="rate_cny",
        )

    if "cbr_date" in st.session_state:

        st.caption(
            f"Последнее обновление: {st.session_state.cbr_date}"
        )

    # -------------------------------------------------

    st.divider()

    if st.button(
        "🔄 Сбросить тарифы",
        key="btn_reset",
    ):

        reset_tariffs()

        st.session_state.rate_usd = 71.7318
        st.session_state.rate_cny = 10.5831

        st.session_state.tariff_thc_sea = 40.0
        st.session_state.tariff_doc_sea = 80.0
        st.session_state.tariff_r_rail = 1.9
        st.session_state.tariff_r_sea = 0.8

        st.session_state.tariff_air_kg = 5.0
        st.session_state.tariff_air_prr = 6.06

        st.session_state.tariff_rail_kg = 2.5
        st.session_state.tariff_rail_m3 = 200.0
        st.session_state.tariff_rail_doc = 50.0

        st.session_state.tariff_road_kg = 2.5
        st.session_state.tariff_road_doc = 70.0

        if "cbr_date" in st.session_state:
            del st.session_state.cbr_date

    sync_state()
    refresh()