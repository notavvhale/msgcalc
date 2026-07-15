import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
import xml.etree.ElementTree as ET
from state import init_state, reset_tariffs
from formulas import calculate, calculate_ldm, calc_customs_fee

# -------------------- НАСТРОЙКИ СТРАНИЦЫ --------------------
light_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="st-"]{
    font-family: 'Inter', sans-serif !important;

.stApp{
    background:#fffef4;
    color:#222222;
}

div[data-testid="stMetric"]{
    background:#FFFFFF;
    border:1px solid #E5E7EB;
    border-radius:16px;
}

.stButton > button{
    background:#D98A2B;
    color:white;
}
/* ===========================================
   SIDEBAR
=========================================== */
/* Скрыть кнопку сворачивания sidebar */
[data-testid="stSidebarCollapseButton"] {
    display: none;
}
section[data-testid="stSidebar"]{
    background:#173A63;
    width:260px !important;
    min-width:260px !important;
    max-width:260px !important;

    border-right:none;
}

section[data-testid="stSidebar"] > div{
    padding-top:20px;
}

/* Заголовки */

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3{

    color:white;

}

/* Divider */

section[data-testid="stSidebar"] hr{

    border-color:rgba(255,255,255,.08);

}

/* Radio */

div[role="radiogroup"] label{

    background:transparent;

    border-radius:12px;

    padding:10px 14px;

    margin-bottom:6px;

    transition:.2s;

}

div[role="radiogroup"] label:hover{

    background:rgba(255,255,255,.08);

}

div[role="radiogroup"] p{

    color:white;

    font-size:15px;

    font-weight:500;

}

/* выбранный пункт */

div[role="radiogroup"] label:has(input:checked){

    background:#F7941D;

}

div[role="radiogroup"] label:has(input:checked) p{

    color:white;

}

.footer{
    position:fixed;

    left:260px;
    right:0;
    bottom:0;

    height:60px;

    background:#FFFFFF;

    border-top:1px solid #E5E7EB;

    display:flex;
    justify-content:space-between;
    align-items:center;

    padding:0 32px;

    z-index:9999;

    box-shadow:0 -4px 12px rgba(0,0,0,.05);
}
.footer-left,
.footer-right{
    color:#6B7280;
    font-size:14px;
}
    
/* Верхняя панель */
[data-testid="stHeader"]{
    display:none;
}

/* Отступ сверху после скрытия */
.block-container{
    padding-top:1rem;
}
</style>
"""
dark_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="st-"]{
    font-family: 'Inter', sans-serif !important;
.stApp{
    background:#141414;
    color:#141414;
}

div[data-testid="stMetric"]{
    background:#141414;
    border:1px solid #141414;
    border-radius:16px;
}

.stButton > button{
    background:#141414;
    color:black;
}

/* ===========================================
   SIDEBAR
=========================================== */

section[data-testid="stSidebar"]{
    background:#173A63;
    width:260px !important;
    min-width:260px !important;
    max-width:260px !important;

    border-right:none;
}

section[data-testid="stSidebar"] > div{
    padding-top:20px;
}

/* Заголовки */

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3{

    color:white;

}

/* Divider */

section[data-testid="stSidebar"] hr{

    border-color:rgba(255,255,255,.08);

}

/* Radio */

div[role="radiogroup"] label{

    background:transparent;

    border-radius:12px;

    padding:10px 14px;

    margin-bottom:6px;

    transition:.2s;

}

div[role="radiogroup"] label:hover{

    background:rgba(255,255,255,.08);

}

div[role="radiogroup"] p{

    color:white;

    font-size:15px;

    font-weight:500;

}

/* выбранный пункт */

div[role="radiogroup"] label:has(input:checked){

    background:#F7941D;

}

div[role="radiogroup"] label:has(input:checked) p{

    color:white;

}

.footer{
    position:fixed;

    left:260px;
    right:0;
    bottom:0;

    height:60px;

    background:#FFFFFF;

    border-top:1px solid #E5E7EB;

    display:flex;
    justify-content:space-between;
    align-items:center;

    padding:0 32px;

    z-index:9999;

    box-shadow:0 -4px 12px rgba(0,0,0,.05);
}
.footer-left,
.footer-right{
    color:#6B7280;
    font-size:14px;
}
    
/* Верхняя панель */
[data-testid="stHeader"]{
    display:none;
}

/* Отступ сверху после скрытия */
.block-container{
    padding-top:1rem;
}
</style>
"""
# -------------------- ИНИЦИАЛИЗАЦИЯ СОСТОЯНИЯ --------------------
init_state()

cargo = st.session_state.cargo
rates = st.session_state.rates
tariffs = st.session_state.tariffs
customs = st.session_state.customs
calc = calculate(cargo, tariffs, rates, customs)
theme = st.segmented_control(
    "",
    ["☀ Светлая", "🌙 Тёмная"],
    default="☀ Светлая"
)
if theme == "☀ Светлая":
    st.markdown(light_css, unsafe_allow_html=True)
else:
    st.markdown(dark_css, unsafe_allow_html=True)

st.set_page_config(
    page_title="LTLCALC",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)
with st.sidebar:

    st.markdown("# 🚚 LTLCALC")

    st.caption("Logistics Calculator")

    st.divider()

    page = st.radio(
        "",
        [
            "📦 Калькулятор",
            "📊 Результаты",
            "🛃 Таможня",
            "💵 Тарифы",
            "⚙ Настройки"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.caption("Версия 1.0")
st.title("🚚 Калькулятор стоимости доставки сборного груза из Китая в Россию")

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

# -------------------- ВКЛАДКИ --------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Калькулятор", "Прайс-лист", "Таможня","Последняя миля", "Результат"])

# ==================== ВКЛАДКА 1: КАЛЬКУЛЯТОР ====================
    

with tab1:
    col_input,col_input2= st.columns([1, 1])

    with col_input:
        st.header("Параметры груза")

        cargo["weight_per_unit"] = st.number_input("Вес одного места (кг)", min_value=0.1, value=cargo["weight_per_unit"], step=1.0)
        cargo["length"] = st.number_input("Длина места (мм)", min_value=100, value=cargo["length"], step=10)
        cargo["width"] = st.number_input("Ширина места (мм)", min_value=100, value=cargo["width"], step=10)
        cargo["height"] = st.number_input("Высота места (мм)", min_value=100, value=cargo["height"], step=10)
        cargo["qty"] = st.number_input("Количество мест", min_value=1, value=cargo["qty"], step=1)
    with col_input2:
        st.header("Товар")
        cargo["invoice_usd"] = st.number_input("Стоимость товара (USD)", min_value=0.0, value=cargo["invoice_usd"], step=100.0)
        
        st.caption(f"В рублях: {calc["invoice_rub"]:,.2f} ₽")
        st.metric("Общий вес партии", f"{calc["total_weight"]:.0f} кг")
        st.metric("Объём груза", f"{calc["volume"]:.3f} м³")

with tab4:                   
    t = st.session_state.tariffs
    st.header("Последняя миля")
    cargo["dovoz_km"] = st.number_input("Расстояние (км)", min_value=0, value=cargo["dovoz_km"], step=1)

# ==================== ВКЛАДКА 2: ПРАЙС-ЛИСТ ====================
with tab2:
    st.header("💵 Прайс-лист")
    st.markdown("*Измените тарифы — они сразу применятся к расчётам на вкладке «Калькулятор»*")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌊 Море + ЖД (LCL SR)")
        tariffs["thc_sea_usd_m3"] = st.number_input(
            "THC, USD/m³", value=tariffs["thc_sea_usd_m3"], step=1.0, key="price_thc_sea")
        tariffs["doc_sea_usd"] = st.number_input(
            "Doc fee, USD/shpt", value=tariffs["doc_sea_usd"], step=1.0, key="price_doc_sea")
        tariffs["r_rail_usd_m3"] = st.number_input(
            "R rail, USD/m³", value=tariffs["r_rail_usd_m3"], step=0.1, format="%.1f", key="price_r_rail")
        tariffs["r_sea_usd_kg"] = st.number_input(
            "R sea, USD/kg", value=tariffs["r_sea_usd_kg"], step=0.1, format="%.1f", key="price_r_sea")

        st.divider()
        st.subheader("✈️ Авиа (AIR)")
        tariffs["air_usd_kg"] = st.number_input(
            "USD/kg", value=tariffs["air_usd_kg"], step=0.5, format="%.1f", key="price_air_kg")
        tariffs["air_prr_rub_kg"] = st.number_input(
            "ПРР, руб/кг", value=tariffs["air_prr_rub_kg"], step=0.01, format="%.2f", key="price_air_prr")

    with col2:
        st.subheader("🚂 Прямое ЖД (LCL RW)")
        tariffs["rail_usd_kg"] = st.number_input(
            "USD / кг (ЖД)", value=tariffs["rail_usd_kg"], step=0.1, format="%.1f", key="price_rail_kg")
        tariffs["rail_usd_m3"] = st.number_input(
            "USD / м³", value=tariffs["rail_usd_m3"], step=5.0, key="price_rail_m3")
        tariffs["rail_doc_usd"] = st.number_input(
            "USD / shpt (ЖД)", value=tariffs["rail_doc_usd"], step=1.0, key="price_rail_doc")

        st.divider()
        st.subheader("🚛 Автосборка (LTL)")
        tariffs["road_usd_kg"] = st.number_input(
            "USD / кг (Авто)", value=tariffs["road_usd_kg"], step=0.1, format="%.1f", key="price_road_kg")
        tariffs["road_doc_usd"] = st.number_input(
            "USD / shpt (Авто)", value=tariffs["road_doc_usd"], step=1.0, key="price_road_doc")

    st.divider()
    st.subheader("💱 Курсы валют")

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        if st.button("🔄 Загрузить курс ЦБ", key="btn_cbr"):
            cbr_rates = get_cbr_rates()
            if cbr_rates:
                rates["USD_RUB"] = cbr_rates['USD']
                rates["CNY_RUB"] = cbr_rates['CNY']
                st.session_state.cbr_date = cbr_rates['date']
                st.success(f"Курс обновлён! Данные на {cbr_rates['date']}")
            else:
                st.error("Не удалось загрузить курс ЦБ. Проверьте интернет.")

    col_cur1, col_cur2 = st.columns(2)
    with col_cur1:
        rates["USD_RUB"] = st.number_input(
            "USD / RUB", value=rates["USD_RUB"], step=0.01, format="%.4f", key="cur_usd")
    with col_cur2:
        st.session_state.rates["CNY_RUB"] = st.number_input(
            "CNY / RUB", value=rates["CNY_RUB"], step=0.01, format="%.4f", key="cur_cny")

    if "cbr_date" in st.session_state:
        st.caption(f"Последнее обновление с ЦБ: {st.session_state.cbr_date}")

    st.divider()
    if st.button("🔄 Сбросить все тарифы на значения по умолчанию", key="btn_reset"):
        reset_tariffs()
        rates["USD_RUB"] = 71.7318
        rates["CNY_RUB"] = 10.5831
        if "cbr_date" in st.session_state:
            del st.session_state.cbr_date
        st.rerun()
with tab3:
    total_customs = 0
    full_cost = calc["invoice_rub"] + calc["cost_rail_rub"] + total_customs + calc["insurance_rub"]
    st.header("Таможня")
    customs["enabled_flag"] = st.checkbox("Рассчитать таможенные платежи", value=customs["enabled_flag"])

        # Таможня
    if customs["enabled_flag"]:
            st.divider()
            st.header("Таможенные платежи")
            customs["vat_rate"] = st.number_input(
                "Ставка НДС (%)",
                min_value=0.0,
                max_value=100.0,
                value=customs["vat_rate"],
                step=1.0,
                format="%.0f",
                key="vat_rate_input"
                )
            customs["duty_rate"] = st.number_input(
                "Ставка пошлины (%)",
                min_value=0.0,
                max_value=100.0,
                value=customs["duty_rate"],
                step=0.1,
                format="%.1f",
                key="duty_rate_input"
                )
            duty_rate_decimal = customs["duty_rate"] / 100.0
            vat_rate_decimal = customs["vat_rate"] / 100.0

            t_val = (cargo["invoice_usd"] + calc["cost_rail_usd"]) * rates["USD_RUB"]
            duty = t_val * duty_rate_decimal
            vat = (t_val + duty) * vat_rate_decimal
            fee = calc_customs_fee(t_val)
            total_customs = duty + vat + fee

            st.header("Таможня")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Тамож. стоимость", f"{t_val:,.2f} ₽")
            col2.metric(f"Пошлина ({customs["duty_rate"]:.1f}%)", f"{duty:,.2f} ₽")
            col3.metric(f"НДС ({customs["vat_rate"]:.0f}%)", f"{vat:,.2f} ₽")
            col4.metric("Тамож. сбор", f"{fee:,.2f} ₽")

            st.metric("Итого таможенных платежей", f"{total_customs:,.2f} ₽")
            st.metric("Полная себестоимость", f"{full_cost:,.2f} ₽")

            #pie_fig = px.pie(
              #  names=["Пошлина", "НДС", "Сбор"],
               # values=[duty, vat, fee],
               # title="Структура таможенных платежей",
               #pie_fig.update_traces(textposition="inside", textinfo="percent+label+value")
            #st.plotly_chart(pie_fig, use_container_width=True)      

with tab5:
    st.header("Результат")
    df = pd.DataFrame(calc["results"], columns=["Маршрут", "Стоимость (руб.)", "Срок (дн.)", "Оплач. база"])
    min_cost = df["Стоимость (руб.)"].min()

    def highlight_min(val):
        return 'background-color: hsl(32, 78%, 56%)' if val == min_cost else ''

    st.dataframe(df.style.map(highlight_min, subset=["Стоимость (руб.)"]), use_container_width=True, hide_index=True)
    if customs["enabled_flag"]:
        st.header("Таможня")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Тамож. стоимость", f"{t_val:,.2f} ₽")
        col2.metric(f"Пошлина ({customs["duty_rate"]:.1f}%)", f"{duty:,.2f} ₽")
        col3.metric(f"НДС ({customs["vat_rate"]:.0f}%)", f"{vat:,.2f} ₽")
        col4.metric("Тамож. сбор", f"{fee:,.2f} ₽")

        st.metric("Итого таможенных платежей", f"{total_customs:,.2f} ₽")
        st.metric("Полная себестоимость", f"{full_cost:,.2f} ₽")
    else:
        st.metric("Полная себестоимость", f"{full_cost:,.2f} ₽")
# -------------------- ПОДВАЛ --------------------
footer_html = f"""<div class="footer">

<div class="footer-left">
Страховка (0,1%) {calc["insurance_rub"]:,.2f} ₽ |
Стоимость довоза {calc["dovoz_cost"]:,.2f} ₽ 
</div>

<div class="footer-right">
Полная себестоимость {full_cost:,.2f} ₽
</div>

</div>
"""


st.markdown(footer_html, unsafe_allow_html=True)
st.divider()
st.caption("© 2026 | Калькулятор разработан в рамках выпускной квалификационной работы")
st.caption(f"Курс ЦБ: USD = {rates['USD_RUB']:.4f} руб., CNY = {st.session_state.rates['CNY_RUB']:.4f} руб.")
