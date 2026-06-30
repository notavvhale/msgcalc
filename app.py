import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
import xml.etree.ElementTree as ET

# -------------------- НАСТРОЙКИ СТРАНИЦЫ --------------------
st.set_page_config(page_title="Калькулятор доставки | Китай → РФ", page_icon="🚚", layout="wide")
st.title("🚚 Калькулятор стоимости доставки сборного груза из Китая в Россию")
st.markdown("*Инструмент для транспортно-экспедиторских компаний*")

# -------------------- ФУНКЦИЯ ПОЛУЧЕНИЯ КУРСА ЦБ --------------------
@st.cache_data(ttl=3600)
def get_cbr_rates():
    """Получает актуальные курсы USD и CNY с сайта ЦБ РФ"""
    url = "https://www.cbr.ru/scripts/XML_daily.asp"
    try:
        response = requests.get(url, timeout=5)
        response.encoding = 'windows-1251'
        root = ET.fromstring(response.text)
        rates = {}
        for valute in root.findall('Valute'):
            char_code = valute.find('CharCode').text
            if char_code == 'USD':
                value = valute.find('Value').text.replace(',', '.')
                rates['USD'] = float(value)
            elif char_code == 'CNY':
                value = valute.find('Value').text.replace(',', '.')
                rates['CNY'] = float(value)
        rates['date'] = root.get('Date')
        return rates
    except Exception:
        return None

# -------------------- ИНИЦИАЛИЗАЦИЯ СЕССИИ --------------------
if "USD_RUB" not in st.session_state:
    st.session_state.USD_RUB = 71.7318
if "CNY_RUB" not in st.session_state:
    st.session_state.CNY_RUB = 10.5831

if "tariffs" not in st.session_state:
    st.session_state.tariffs = {
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

# -------------------- КОНСТАНТЫ --------------------
K_RAIL = 500
K_AIR = 167
K_SEA = 1000
K_LDM = 1850
TRUCK_WIDTH = 2.4

DOVOZ_BASE = 5000
DOVOZ_ADD_KM = 90

FEE_SCHEDULE = [
    (200000, 1231), (450000, 2462), (1200000, 4924),
    (2700000, 13541), (4200000, 18465), (5500000, 21344),
    (10000000, 49240), (float('inf'), 73860)
]

# -------------------- ФУНКЦИИ --------------------
def calc_volume(l_m, w_m, h_m, qty):
    return round((l_m * w_m * h_m) * qty, 4)

def calc_ldm(l_m, w_m, qty):
    ldm_unit = (l_m * w_m) / TRUCK_WIDTH
    if l_m <= 1.2 and w_m <= 0.8:
        ldm_unit = 0.4
    return round(ldm_unit * qty, 2)

def calc_dovoz(km):
    return DOVOZ_BASE if km <= 20 else DOVOZ_BASE + (km - 20) * DOVOZ_ADD_KM

def calc_customs_fee(t_val_rub):
    for limit, fee in FEE_SCHEDULE:
        if t_val_rub <= limit:
            return fee

# -------------------- ВКЛАДКИ --------------------
tab1, tab2 = st.tabs(["📦 Калькулятор", "💵 Прайс-лист"])

# ==================== ВКЛАДКА 1: КАЛЬКУЛЯТОР ====================
with tab1:
    col_input, col_result = st.columns([1, 2])

    with col_input:
        st.header("📦 Параметры груза")

        weight_per_unit = st.number_input("Вес одного места (кг)", min_value=0.1, value=500.0, step=1.0)
        length = st.number_input("Длина места (мм)", min_value=100, value=800, step=10)
        width = st.number_input("Ширина места (мм)", min_value=100, value=1200, step=10)
        height = st.number_input("Высота места (мм)", min_value=100, value=1000, step=10)
        qty = st.number_input("Количество мест", min_value=1, value=2, step=1)

        l_m = length / 1000
        w_m = width / 1000
        h_m = height / 1000

        total_weight = weight_per_unit * qty
        volume = calc_volume(l_m, w_m, h_m, qty)

        st.metric("Общий вес партии", f"{total_weight:.0f} кг")
        st.metric("Объём груза", f"{volume:.3f} м³")

        st.divider()
        st.header("🚚 Довоз")
        dovoz_km = st.number_input("Расстояние довоза (км)", min_value=0, value=50, step=1)

        st.divider()
        st.header("💰 Товар")
        invoice_usd = st.number_input("Стоимость товара (USD)", min_value=0.0, value=5000.0, step=100.0)
        invoice_rub = invoice_usd * st.session_state.USD_RUB
        st.caption(f"В рублях: {invoice_rub:,.2f} ₽")

        st.divider()
        st.header("📋 Таможня")
        calc_customs_flag = st.checkbox("Рассчитать таможенные платежи", value=False)

        if calc_customs_flag:
            duty_rate = st.number_input(
                "Ставка пошлины (%)",
                min_value=0.0,
                max_value=100.0,
                value=7.5,
                step=0.1,
                format="%.1f",
                key="duty_rate_input"
            )
            vat_rate = st.number_input(
                "Ставка НДС (%)",
                min_value=0.0,
                max_value=100.0,
                value=22.0,
                step=1.0,
                format="%.0f",
                key="vat_rate_input"
            )

    with col_result:
        st.header("📊 Результаты")

        t = st.session_state.tariffs
        usd = st.session_state.USD_RUB

        dovoz_cost = calc_dovoz(dovoz_km)
        insurance_rub = invoice_usd * usd * 0.001

        # 1. Прямое ЖД
        vw_rail = volume * K_RAIL
        cw_rail = max(total_weight, vw_rail)
        cost_rail_usd = max(cw_rail * t["rail_usd_kg"], volume * t["rail_usd_m3"]) + t["rail_doc_usd"]
        cost_rail_rub = cost_rail_usd * usd + dovoz_cost

        # 2. Авиа
        vw_air = volume * K_AIR
        cw_air = max(total_weight, vw_air)
        cost_air_usd = max(cw_air * t["air_usd_kg"], 200)
        cost_air_rub = cost_air_usd * usd
        terminal_air = total_weight * t["air_prr_rub_kg"] + 1481.92 + 724.95 + 1240.74
        cost_air_total_rub = cost_air_rub + terminal_air + dovoz_cost

        # 3. Авто LTL
        ldm_total = calc_ldm(l_m, w_m, qty)
        vw_road = ldm_total * K_LDM
        cw_road = max(total_weight, vw_road)
        cost_road_usd = cw_road * t["road_usd_kg"] + t["road_doc_usd"]
        cost_road_rub = cost_road_usd * usd + dovoz_cost

        # 4. Море+ЖД
        cw_sea_multi = max(total_weight, volume * K_SEA)
        cw_rail_multi = max(total_weight, volume * K_RAIL)
        thc_rub = volume * t["thc_sea_usd_m3"] * usd
        doc_sea_rub = t["doc_sea_usd"] * usd
        f_rail_rub = cw_rail_multi * t["r_rail_usd_m3"] * usd
        f_sea_rub = cw_sea_multi * t["r_sea_usd_kg"] * usd
        cost_multi_rub = thc_rub + doc_sea_rub + f_rail_rub + f_sea_rub + dovoz_cost

        # Таблица
        results = [
            ("🚂 Ж/Д прямая (LCL RW)", cost_rail_rub, 25, f"{cw_rail:.0f} кг"),
            ("✈️ Авиа прямая (AIR)", cost_air_total_rub, 5, f"{cw_air:.0f} кг"),
            ("🚛 Авто LTL (LDM)", cost_road_rub, 22, f"{cw_road:.0f} кг (LDM {ldm_total} м)"),
            ("🚢 Море+ЖД (LCL SR)", cost_multi_rub, 35, f"Море: {cw_sea_multi:.0f} кг / ЖД: {cw_rail_multi:.0f} кг"),
        ]

        df = pd.DataFrame(results, columns=["Маршрут", "Стоимость (руб.)", "Срок (дн.)", "Оплач. база"])
        min_cost = df["Стоимость (руб.)"].min()

        def highlight_min(val):
            return 'background-color: #90EE90' if val == min_cost else ''

        st.dataframe(df.style.map(highlight_min, subset=["Стоимость (руб.)"]), use_container_width=True, hide_index=True)

        # График
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="Стоимость (руб.)", x=df["Маршрут"], y=df["Стоимость (руб.)"],
            text=[f"{x:,.0f} ₽" for x in df["Стоимость (руб.)"]], textposition="outside",
            marker_color="steelblue"
        ))
        fig.add_trace(go.Scatter(
            name="Срок (дней)", x=df["Маршрут"], y=df["Срок (дн.)"],
            yaxis="y2", mode="lines+markers",
            line=dict(color="red", width=3), marker=dict(size=12)
        ))
        fig.update_layout(
            title="Сравнение маршрутов доставки",
            yaxis_title="Стоимость (руб.)",
            yaxis2=dict(title="Срок (дней)", overlaying="y", side="right"),
            template="plotly_white", height=500
        )
        st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Страховка (0,1%)", f"{insurance_rub:,.2f} ₽")
        with col2:
            st.metric("Стоимость довоза", f"{dovoz_cost:,.2f} ₽")

        # Таможня
        if calc_customs_flag:
            st.divider()
            st.header("🏛️ Таможенные платежи")

            duty_rate_decimal = duty_rate / 100.0
            vat_rate_decimal = vat_rate / 100.0

            t_val = (invoice_usd + cost_rail_usd) * usd
            duty = t_val * duty_rate_decimal
            vat = (t_val + duty) * vat_rate_decimal
            fee = calc_customs_fee(t_val)
            total_customs = duty + vat + fee

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Тамож. стоимость", f"{t_val:,.2f} ₽")
            col2.metric(f"Пошлина ({duty_rate:.1f}%)", f"{duty:,.2f} ₽")
            col3.metric(f"НДС ({vat_rate:.0f}%)", f"{vat:,.2f} ₽")
            col4.metric("Тамож. сбор", f"{fee:,.2f} ₽")

            st.metric("### Итого таможенных платежей", f"{total_customs:,.2f} ₽")

            pie_fig = px.pie(
                names=["Пошлина", "НДС", "Сбор"],
                values=[duty, vat, fee],
                title="Структура таможенных платежей",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            pie_fig.update_traces(textposition="inside", textinfo="percent+label+value")
            st.plotly_chart(pie_fig, use_container_width=True)

            full_cost = invoice_rub + cost_rail_rub + total_customs + insurance_rub
            st.metric("### 💰 Полная себестоимость", f"{full_cost:,.2f} ₽")

# ==================== ВКЛАДКА 2: ПРАЙС-ЛИСТ ====================
with tab2:
    st.header("💵 Прайс-лист")
    st.markdown("*Измените тарифы — они сразу применятся к расчётам на вкладке «Калькулятор»*")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌊 Море + ЖД (LCL SR)")
        st.session_state.tariffs["thc_sea_usd_m3"] = st.number_input(
            "THC, USD/m³", value=st.session_state.tariffs["thc_sea_usd_m3"], step=1.0, key="price_thc_sea")
        st.session_state.tariffs["doc_sea_usd"] = st.number_input(
            "Doc fee, USD/shpt", value=st.session_state.tariffs["doc_sea_usd"], step=1.0, key="price_doc_sea")
        st.session_state.tariffs["r_rail_usd_m3"] = st.number_input(
            "R rail, USD/m³", value=st.session_state.tariffs["r_rail_usd_m3"], step=0.1, format="%.1f", key="price_r_rail")
        st.session_state.tariffs["r_sea_usd_kg"] = st.number_input(
            "R sea, USD/kg", value=st.session_state.tariffs["r_sea_usd_kg"], step=0.1, format="%.1f", key="price_r_sea")

        st.divider()
        st.subheader("✈️ Авиа (AIR)")
        st.session_state.tariffs["air_usd_kg"] = st.number_input(
            "USD/kg", value=st.session_state.tariffs["air_usd_kg"], step=0.5, format="%.1f", key="price_air_kg")
        st.session_state.tariffs["air_prr_rub_kg"] = st.number_input(
            "ПРР, руб/кг", value=st.session_state.tariffs["air_prr_rub_kg"], step=0.01, format="%.2f", key="price_air_prr")

    with col2:
        st.subheader("🚂 Прямое ЖД (LCL RW)")
        st.session_state.tariffs["rail_usd_kg"] = st.number_input(
            "USD / кг (ЖД)", value=st.session_state.tariffs["rail_usd_kg"], step=0.1, format="%.1f", key="price_rail_kg")
        st.session_state.tariffs["rail_usd_m3"] = st.number_input(
            "USD / м³", value=st.session_state.tariffs["rail_usd_m3"], step=5.0, key="price_rail_m3")
        st.session_state.tariffs["rail_doc_usd"] = st.number_input(
            "USD / shpt (ЖД)", value=st.session_state.tariffs["rail_doc_usd"], step=1.0, key="price_rail_doc")

        st.divider()
        st.subheader("🚛 Автосборка (LTL)")
        st.session_state.tariffs["road_usd_kg"] = st.number_input(
            "USD / кг (Авто)", value=st.session_state.tariffs["road_usd_kg"], step=0.1, format="%.1f", key="price_road_kg")
        st.session_state.tariffs["road_doc_usd"] = st.number_input(
            "USD / shpt (Авто)", value=st.session_state.tariffs["road_doc_usd"], step=1.0, key="price_road_doc")

    st.divider()
    st.subheader("💱 Курсы валют")

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        if st.button("🔄 Загрузить курс ЦБ", key="btn_cbr"):
            rates = get_cbr_rates()
            if rates:
                st.session_state.USD_RUB = rates['USD']
                st.session_state.CNY_RUB = rates['CNY']
                st.session_state.cbr_date = rates['date']
                st.success(f"Курс обновлён! Данные на {rates['date']}")
            else:
                st.error("Не удалось загрузить курс ЦБ. Проверьте интернет.")

    col_cur1, col_cur2 = st.columns(2)
    with col_cur1:
        st.session_state.USD_RUB = st.number_input(
            "USD / RUB", value=st.session_state.USD_RUB, step=0.01, format="%.4f", key="cur_usd")
    with col_cur2:
        st.session_state.CNY_RUB = st.number_input(
            "CNY / RUB", value=st.session_state.CNY_RUB, step=0.01, format="%.4f", key="cur_cny")

    if "cbr_date" in st.session_state:
        st.caption(f"Последнее обновление с ЦБ: {st.session_state.cbr_date}")

    st.divider()
    if st.button("🔄 Сбросить все тарифы на значения по умолчанию", key="btn_reset"):
        st.session_state.tariffs = {
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
        st.session_state.USD_RUB = 71.7318
        st.session_state.CNY_RUB = 10.5831
        if "cbr_date" in st.session_state:
            del st.session_state.cbr_date
        st.rerun()

# -------------------- ПОДВАЛ --------------------
st.divider()
st.caption("© 2026 | Калькулятор разработан в рамках выпускной квалификационной работы")
st.caption(f"Курс ЦБ: USD = {st.session_state.USD_RUB:.4f} руб., CNY = {st.session_state.CNY_RUB:.4f} руб.")
