import streamlit as st

from assets.styles import load_css

from state import init_state

from ui.calculator import show as show_calculator
from ui.history import show as show_history
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
from services.history_database import initialize_database as initialize_history_database
from ui.header import show as show_header
from auth.service import AuthService

auth = AuthService()

st.set_page_config(
    page_title="LTLCALC",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css("light.css")

initialize_database()
initialize_sessions()
initialize_tnved_database()
initialize_history_database()
bootstrap()
init_state()
update_rates()

if not auth.authenticated:
    token = get_session()
    if token:
        auth.restore(token)

if not auth.authenticated:
    show_login()
    st.stop()

st.session_state.user_id = auth.user["id"]
page = show_header(auth)

if page=="Расчёт":
    show_calculator()
elif page=="История":
    show_history()
elif page=="Тест2":
    show_results()
elif page=="Тест1":
    show_customs()
elif page=="Тарифы":
    show_tariffs()
elif page=="Настройки":
    show_admin()

show_footer()

rates=st.session_state.rates
st.caption(
    f"Курс ЦБ: USD = {rates['USD_RUB']:.4f} руб., "
    f"CNY = {rates['CNY_RUB']:.4f} руб."
)