import streamlit as st

from assets.styles import load_css

from state import init_state

from ui.calculator import show as show_calculator
from ui.lastmile import show as show_lastmile
from ui.tariffs import show as show_tariffs, update_rates
from ui.customs import show as show_customs
from ui.results import show as show_results
from ui.footer import show as show_footer
from ui.admin import show as show_admin

from auth import auth
from auth.permissions import is_admin, is_user
from auth.login_page import show as show_login
from auth.database import initialize_database, initialize_sessions
from auth.bootstrap import bootstrap
from auth.cookies import get_session, delete_session
from services.tnved_database import initialize_database as initialize_tnved_database
from services.import_tnved import import_tnved

# ------------------------------------------------------------
# НАСТРОЙКИ СТРАНИЦЫ
# ------------------------------------------------------------

st.set_page_config(
    page_title="LTLCALC",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🚚 Калькулятор стоимости доставки сборного груза из Китая в Россию")


# ------------------------------------------------------------
# ИНИЦИАЛИЗАЦИЯ
# ------------------------------------------------------------

initialize_database()
initialize_sessions()
initialize_tnved_database()
bootstrap()
init_state()
#st.write(st.session_state)
load_css("light.css")
update_rates()

# ------------------------------------------------------------
# АВТОРИЗАЦИЯ ПО COOKIE
# ------------------------------------------------------------

if not auth.authenticated:

    token = get_session()

    if token:
        auth.restore(token)


# ------------------------------------------------------------
# ЛОГИН
# ------------------------------------------------------------

if not auth.authenticated:

    show_login()

    st.stop()


# ------------------------------------------------------------
# ТЕМА
# ------------------------------------------------------------

theme = st.segmented_control(
    "",
    ["☀ Светлая", "🌙 Тёмная"],
    default="☀ Светлая",
)

if theme == "☀ Светлая":
    load_css("light.css")
else:
    load_css("dark.css")


# ------------------------------------------------------------
# БОКОВАЯ ПАНЕЛЬ
# ------------------------------------------------------------

with st.sidebar:

    st.markdown("# 🚚 LTLCALC")

    st.caption("Logistics Calculator")

    st.caption("Версия 1.0")

    st.divider()

    if is_admin():

        page = st.radio(
            "",
            [
                "📦 Калькулятор",
                "🚛 Последняя миля",
                "📊 Результаты",
                "🛃 Таможня",
                "💵 Тарифы",
                "⚙ Админ-панель",
            ],
            label_visibility="collapsed",
        )

    elif is_user():

        page = st.radio(
            "",
            [
                "📦 Калькулятор",
            ],
            label_visibility="collapsed",
        )

    st.caption("Поддержка")
    st.caption("support@ltlcalc.ru")
    st.caption("+7 (995) 555-35-35")
    st.divider()
    
    st.success(f"👤 {auth.name}")

    if st.button(
        "🚪 Выйти",
        use_container_width=True,
    ):

        delete_session()

        auth.logout()

        st.rerun()


# ------------------------------------------------------------
# СТРАНИЦЫ
# ------------------------------------------------------------

if page == "📦 Калькулятор":
    show_calculator()

elif page == "🚛 Последняя миля":
    show_lastmile()

elif page == "💵 Тарифы":
    show_tariffs()

elif page == "🛃 Таможня":
    show_customs()

elif page == "📊 Результаты":
    show_results()

elif page == "⚙ Админ-панель":
    show_admin()


# ------------------------------------------------------------
# ПОДВАЛ
# ------------------------------------------------------------

show_footer()

st.divider()

rates = st.session_state.rates

st.caption(
    "© 2026 | Калькулятор разработан в рамках выпускной квалификационной работы"
)

st.caption(
    f"Курс ЦБ: USD = {rates['USD_RUB']:.4f} руб., "
    f"CNY = {rates['CNY_RUB']:.4f} руб."
)