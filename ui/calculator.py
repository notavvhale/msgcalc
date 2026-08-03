import streamlit as st

from state import refresh
from services.tnved import get_by_code
from ui.components.tnved_search import tnved_search
from services.ai.ui_classifier import classify_product


def _update(field):
    key = f"ui_{field}"

    if "cargo" not in st.session_state:
        return

    if key not in st.session_state:
        return

    st.session_state.cargo[field] = st.session_state[key]
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
            "🤖",
            use_container_width=True,
        ):

            if not cargo["product_name"].strip():

                st.warning("Введите название товара.")

            else:

                with st.spinner("ИИ анализирует товар..."):

                    results = classify_product(
                        cargo["product_name"]
                    )

                if results:

                    st.session_state.ai_results = results

                    # автоматически выбираем лучший вариант
                    cargo["tnved"] = results[0]["code"]

                    refresh()
                    st.rerun()

                else:

                    st.error("Не удалось подобрать код ТН ВЭД.")

        # ======================================================
        # Поиск вручную
        # ======================================================

        selected = tnved_search()

        if selected:

            if cargo["tnved"] != selected["code"]:

                cargo["tnved"] = selected["code"]

                refresh()

        # ======================================================
        # Результаты AI
        # ======================================================

        ai_results = st.session_state.get("ai_results", [])

        if ai_results:

            st.subheader("🤖 AI подобрал несколько вариантов")

            def confidence_icon(confidence):

                if confidence >= 90:
                    return "⭐"

                if confidence >= 70:
                    return "🟢"

                if confidence >= 50:
                    return "🟡"

                return "⚪"

            for i, ai in enumerate(ai_results):

                short_description = ai["description"].replace("\n", " ")

                if len(short_description) > 70:
                    short_description = short_description[:70] + "..."

                left_info, right_button = st.columns([6, 1])

                with left_info:

                    st.markdown(
                        f"""
**{confidence_icon(ai["confidence"])} {ai["code"]}**

{short_description}

Совпадение: **{ai["confidence"]}%**
"""
                    )

                with right_button:

                    if cargo["tnved"] == ai["code"]:

                        st.success("✓")

                    else:

                        if st.button(
                            "Выбрать",
                            key=f"use_ai_{i}",
                            use_container_width=True,
                        ):

                            cargo["tnved"] = ai["code"]

                            refresh()

                            st.rerun()

                with st.expander("Подробнее", expanded=False):

                    st.write(ai["reason"])

                    c1, c2 = st.columns(2)

                    with c1:

                        st.metric(
                            "Пошлина",
                            ai["duty_text"],
                        )

                    with c2:

                        st.metric(
                            "НДС",
                            f'{ai["vat"] or 20}%'
                        )

                    st.write("**Полное описание ТН ВЭД**")

                    st.write(ai["description"])

                st.divider()
        # ======================================================
        # Информация по выбранному коду
        # ======================================================

        item = None

        if cargo["tnved"]:

            item = get_by_code(cargo["tnved"])

        if item:

            st.divider()

            st.subheader("Выбранный код ТН ВЭД")

            st.code(item["code"])

            c1, c2 = st.columns(2)

            with c1:

                st.metric(
                    "Пошлина",
                    item["duty_text"],
                )

            with c2:

                st.metric(
                    "НДС",
                    f'{item["vat"] or 20}%'
                )

        # ======================================================
        # Параметры груза
        # ======================================================

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