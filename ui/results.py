import pandas as pd
import streamlit as st
from export import build_pdf, build_excel

def show():

    calc = st.session_state.calc
    customs = st.session_state.customs

    st.header("Результаты")

    df = pd.DataFrame(
        calc["results"],
        columns=[
            "Маршрут",
            "Стоимость (руб.)",
            "Срок (дн.)",
            "Оплач. база",
        ],
    )

    min_cost = df["Стоимость (руб.)"].min()

    def highlight_min(value):
        if value == min_cost:
            return "background-color: hsl(32, 78%, 56%)"
        return ""

    st.dataframe(
        df.style.map(
            highlight_min,
            subset=["Стоимость (руб.)"],
        ),
        use_container_width=True,
        hide_index=True,
    )

    if customs["enabled_flag"]:

        st.divider()
        st.header("Таможенные платежи")

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
    excel = build_excel(
    st.session_state.cargo,
    st.session_state.calc,
    st.session_state.tariffs,
    st.session_state.rates,
    st.session_state.customs,
    )
    pdf = build_pdf(
    st.session_state.cargo,
    st.session_state.calc,
    st.session_state.tariffs,
    st.session_state.rates,
    st.session_state.customs,
    )
    col_pdf, col_excel = st.columns([1, 2])
    with col_pdf:
        st.download_button(
            "📄 Скачать PDF",
            pdf,
            "LTLCALC_commercial_offer.pdf",
            "application/pdf",
        )
    with col_excel:
        st.download_button(
            "📊 Скачать Excel",
            excel,
            "LTLCALC-calculation_excel.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )