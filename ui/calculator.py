import streamlit as st
from state import refresh


def _update(field):
    """Сохранить значение виджета в cargo и пересчитать калькулятор."""
    st.session_state.cargo[field] = st.session_state[f"ui_{field}"]
    refresh()


def show():

    cargo = st.session_state.cargo

    col_input, col_input2 = st.columns([1, 1])

    with col_input:

        st.header("Параметры груза")

        st.number_input(
            "Вес одного места (кг)",
            min_value=0.1,
            step=1.0,
            value=cargo["weight_per_unit"],
            key="ui_weight_per_unit",
            on_change=_update,
            args=("weight_per_unit",),
        )

        st.number_input(
            "Длина места (мм)",
            min_value=100,
            step=10,
            value=cargo["length"],
            key="ui_length",
            on_change=_update,
            args=("length",),
        )

        st.number_input(
            "Ширина места (мм)",
            min_value=100,
            step=10,
            value=cargo["width"],
            key="ui_width",
            on_change=_update,
            args=("width",),
        )

        st.number_input(
            "Высота места (мм)",
            min_value=100,
            step=10,
            value=cargo["height"],
            key="ui_height",
            on_change=_update,
            args=("height",),
        )

        st.number_input(
            "Количество мест",
            min_value=1,
            step=1,
            value=cargo["qty"],
            key="ui_qty",
            on_change=_update,
            args=("qty",),
        )

    with col_input2:

        st.header("Товар")

        st.number_input(
            "Стоимость товара (USD)",
            min_value=0.0,
            step=100.0,
            value=cargo["invoice_usd"],
            key="ui_invoice_usd",
            on_change=_update,
            args=("invoice_usd",),
        )

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