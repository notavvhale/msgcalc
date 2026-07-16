import pandas as pd
import streamlit as st


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