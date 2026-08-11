import json

import streamlit as st

from services.history import (
    get_history,
    get_calculation,
    delete_calculation,
)


# ============================================================
# HELPERS
# ============================================================

def _money(value):
    return (
        f"{float(value or 0):,.2f}"
        .replace(",", " ")
        .replace(".", ",")
    )


def _date(value):
    if not value:
        return "—"

    # 2026-08-11T15:22:30
    return str(value).replace("T", " ")[:16]


# ============================================================
# CALCULATION CARD
# ============================================================

def _show_calculation(row, user_id):

    calculation_id = row["id"]

    calculation_name = (
        row["calculation_name"]
        or row["product_name"]
        or "Без названия"
    )

    product_name = (
        row["product_name"]
        or "Без названия"
    )

    tnved = row["tnved"] or "Не указан"

    full_cost = row["full_cost"] or 0

    created_at = _date(
        row["created_at"]
    )

    weight = row["weight"] or 0
    volume = row["volume"] or 0
    qty = row["qty"] or 0

    # --------------------------------------------------------
    # CARD
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="history-card">
            <div class="history-card-main">
                <div class="history-card-title">
                {calculation_name}
                </div>
                <div class="history-card-meta">
                    Товар: {product_name}
                    &nbsp; • &nbsp;
                    ТН ВЭД: {tnved}
                    &nbsp; • &nbsp;
                    {created_at}
                </div>
            </div>
            <div class="history-card-info">
                <div>
                    <span>Количество</span>
                    <strong>{qty} шт.</strong>
                </div>
                <div>
                    <span>Вес</span>
                    <strong>{weight:.0f} кг</strong>
                </div>
                <div>
                    <span>Объём</span>
                    <strong>{volume:.3f} м³</strong>
                </div>
                <div class="history-card-total">
                    <span>Полная стоимость</span>
                    <strong>{_money(full_cost)} ₽</strong>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # ACTIONS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(
        [1, 1, 4],
        gap="small",
    )

    with col1:

        if st.button(
            "Открыть",
            key=f"history_open_{calculation_id}",
            use_container_width=True,
        ):

            _open_calculation(
                user_id,
                calculation_id,
            )

    with col2:

        if st.button(
            "Удалить",
            key=f"history_delete_{calculation_id}",
            use_container_width=True,
        ):

            st.session_state[
                "delete_history_id"
            ] = calculation_id

            st.rerun()


# ============================================================
# OPEN CALCULATION
# ============================================================

def _open_calculation(
    user_id: int,
    calculation_id: int,
):

    row = get_calculation(
        user_id,
        calculation_id,
    )

    if row is None:

        st.error(
            "Расчёт не найден."
        )

        return

    cargo = json.loads(
        row["cargo_json"]
    )

    calc = json.loads(
        row["calc_json"]
    )

    tariffs = {}

    if row["tariffs_json"]:
        tariffs = json.loads(
            row["tariffs_json"]
        )

    rates = {}

    if row["rates_json"]:
        rates = json.loads(
            row["rates_json"]
        )

    customs = {}

    if row["customs_json"]:
        customs = json.loads(
            row["customs_json"]
        )

    # --------------------------------------------------------
    # RESTORE STATE
    # --------------------------------------------------------

    st.session_state.cargo = cargo
    st.session_state.calc = calc

    if tariffs:
        st.session_state.tariffs = tariffs

    if rates:
        st.session_state.rates = rates

    if customs:
        st.session_state.customs = customs

    # --------------------------------------------------------
    # OPEN CALCULATOR
    # --------------------------------------------------------

    st.session_state.main_tab = "Расчёт"

    st.session_state[
        "opened_calculation_id"
    ] = calculation_id

    st.rerun()


# ============================================================
# DELETE CONFIRMATION
# ============================================================

def _show_delete_confirmation(user_id):

    calculation_id = st.session_state.get(
        "delete_history_id"
    )

    if not calculation_id:
        return

    st.warning(
        f"Удалить расчёт №{calculation_id}?"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Да, удалить",
            key="confirm_delete_history",
            use_container_width=True,
        ):

            deleted = delete_calculation(
                user_id,
                calculation_id,
            )

            if deleted:

                st.toast(
                    "Расчёт удалён",
                    icon="🗑️",
                )

            st.session_state.pop(
                "delete_history_id",
                None,
            )

            st.rerun()

    with col2:

        if st.button(
            "Отмена",
            key="cancel_delete_history",
            use_container_width=True,
        ):

            st.session_state.pop(
                "delete_history_id",
                None,
            )

            st.rerun()


# ============================================================
# MAIN
# ============================================================

def show():

    user = st.session_state.get(
        "user"
    )

    if not user:

        st.error(
            "Пользователь не авторизован."
        )

        return

    user_id = user["id"]

    # ========================================================
    # HEADER
    # ========================================================

    st.markdown(
        """
        <div class="history-header">
            <div>
                <div class="history-title">
                    История расчётов
                </div>
                <div class="history-subtitle">
                    Сохранённые расчёты пользователя
                </div>
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # ========================================================
    # FILTERS
    # ========================================================

    search_col, count_col = st.columns(
        [4, 1],
        gap="small",
    )

    with search_col:

        search = st.text_input(
            "Поиск",
            placeholder="Название товара или код ТН ВЭД...",
            key="history_search",
            label_visibility="collapsed",
        )

    rows = get_history(
        user_id=user_id,
        limit=100,
    )

    # ========================================================
    # SEARCH
    # ========================================================

    if search:

        search_lower = search.strip().lower()

        rows = [
            row
            for row in rows
            if search_lower in (
                row["calculation_name"]
                or ""
            ).lower()
            or search_lower in (
                row["product_name"]
                or ""
            ).lower()
            or search_lower in (
                row["tnved"]
                or ""
            ).lower()
        ]

    with count_col:

        st.markdown(
            f"""
            <div class="history-count">
                Расчётов: <strong>{len(rows)}</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ========================================================
    # DELETE CONFIRMATION
    # ========================================================

    _show_delete_confirmation(
        user_id
    )

    # ========================================================
    # EMPTY
    # ========================================================

    if not rows:

        st.markdown(
            """
            <div class="history-empty">
                <div class="history-empty-icon">
                    🧮
                </div>
                <div class="history-empty-title">
                    История расчётов пуста
                </div>
                <div class="history-empty-text">
                    Сохранённые расчёты появятся здесь.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        return

    # ========================================================
    # LIST
    # ========================================================

    for row in rows:

        _show_calculation(
            row,
            user_id,
        )