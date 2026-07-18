import streamlit as st

from state import refresh
from services.tnved import get_by_code
from ui.components.tnved_search import tnved_search
from services.ai.ui_classifier import classify_product

def _update(field):
    st.session_state.cargo[field] = st.session_state[f"ui_{field}"]
    refresh()


def show():

    cargo = st.session_state.cargo
    calc = st.session_state.calc

    left, right = st.columns([1, 1])

    # ======================================================
    # Левая колонка
    # ======================================================

    with left:

        st.header("Параметры груза")

        st.text_input(
            "📦 Название товара",
            value=cargo["product_name"],
            key="ui_product_name",
            placeholder="Например: Электросамокат Kugoo M4",
            on_change=_update,
            args=("product_name",),
        )
        if st.button(
            "🤖 Подобрать ТН ВЭД",
            use_container_width=True,
        ):

            if not cargo["product_name"].strip():

                st.warning("Введите название товара.")

            else:

                with st.spinner("ИИ подбирает код ТН ВЭД..."):

                    result = classify_product(
                        cargo["product_name"]
                    )

                if result:

                    cargo["tnved"] = result["code"]

                    st.session_state.ai_result = result

                    refresh()

                    st.rerun()

                else:

                    st.error("Не удалось подобрать код.")

        selected = tnved_search()

        if selected:

            if cargo["tnved"] != selected["code"]:

                cargo["tnved"] = selected["code"]

                refresh()

        item = None

        if cargo["tnved"]:
            item = get_by_code(cargo["tnved"])
            ai = st.session_state.get("ai_result")

            if ai:

                with st.container(border=True):

                    st.subheader("🤖 Результат анализа")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric("Код", ai["code"])

                    with col2:
                        st.metric(
                            "Уверенность",
                            f'{ai["confidence"]}%'
                        )

                    st.write(ai["reason"])

                    with st.expander("Полное описание ТН ВЭД"):

                        st.write(item["description"])

        if item:

            c1, c2 = st.columns(2)

            with c1:
                st.metric(
                    "Пошлина",
                    item["duty_text"],
                )

            with c2:
                st.metric(
                    "НДС",
                    f'{item["vat"] or 20}%',
                )

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

    # ======================================================
    # Правая колонка
    # ======================================================

    with right:

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

        st.caption(f"В рублях: {calc['invoice_rub']:,.2f} ₽")

        st.metric(
            "Общий вес партии",
            f"{calc['total_weight']:.0f} кг",
        )

        st.metric(
            "Объём груза",
            f"{calc['volume']:.3f} м³",
        )