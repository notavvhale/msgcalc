import streamlit as st
from state import refresh, sync_state


def show():

    col_input, col_input2 = st.columns([1, 1])

    with col_input:

        st.header("Параметры груза")

        st.number_input(
            "Вес одного места (кг)",
            min_value=0.1,
            step=1.0,
            key="cargo_weight_per_unit",
        )

        st.number_input(
            "Длина места (мм)",
            min_value=100,
            step=10,
            key="cargo_length",
        )

        st.number_input(
            "Ширина места (мм)",
            min_value=100,
            step=10,
            key="cargo_width",
        )

        st.number_input(
            "Высота места (мм)",
            min_value=100,
            step=10,
            key="cargo_height",
)

        st.number_input(
            "Количество мест",
            min_value=1,
            step=1,
            key="cargo_qty",
        )
    with col_input2:

        st.header("Товар")

        st.number_input(
            "Стоимость товара (USD)",
            min_value=0.0,
            step=100.0,
            key="cargo_invoice_usd",
        )
    sync_state()
    refresh()

    calc = st.session_state.calc
    st.caption(f"В рублях: {calc['invoice_rub']:,.2f} ₽")

    st.metric(
        "Общий вес партии",
        f"{calc['total_weight']:.0f} кг",
    )

    st.metric(
        "Объём груза",
        f"{calc['volume']:.3f} м³",
    )