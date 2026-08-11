import streamlit as st

from state import refresh
from services.tnved import get_by_code
from ui.components.tnved_search import tnved_search
from services.ai.ui_classifier import classify_product
from services.history import save_calculation
from export import build_pdf, build_excel


# ============================================================
# HELPERS
# ============================================================

def _update(field):
    key = f"ui_{field}"

    if key not in st.session_state:
        return

    st.session_state.cargo[field] = st.session_state[key]

    refresh()


def _money(value):
    return f"{value:,.2f}".replace(",", " ").replace(".", ",")


def _percent(value):
    return f"{value * 100:.2f}%".replace(".", ",")


def _confidence_icon(confidence):

    if confidence >= 90:
        return "⭐"

    if confidence >= 70:
        return "🟢"

    if confidence >= 50:
        return "🟡"

    return "⚪"


# ============================================================
# RESULT CARD
# ============================================================

def _result_card(title, value, subtitle=None):

    html = f"""
    <div class="calc-result-card">
        <div class="calc-result-card-title">
            {title}
        </div>
        <div class="calc-result-card-value">
            {value}
        </div>
    """

    if subtitle:
        html += f"""
        <div class="calc-result-card-subtitle">
            {subtitle}
        </div>
        """

    html += "</div>"

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


# ============================================================
# LEFT COLUMN
# ============================================================

def _show_product_column(cargo):

    st.markdown(
        '<div class="calc-section-title">1. ТОВАР</div>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # Название
    # --------------------------------------------------------

    st.text_input(
        "Название товара",
        value=cargo["product_name"],
        key="ui_product_name",
        placeholder="Например: Электросамокат Kugoo M4",
        on_change=_update,
        args=("product_name",),
    )

    # --------------------------------------------------------
    # Вес
    # --------------------------------------------------------

    st.number_input(
        "Вес одного места (кг)",
        min_value=0.1,
        step=1.0,
        value=float(cargo["weight_per_unit"]),
        key="ui_weight_per_unit",
        on_change=_update,
        args=("weight_per_unit",),
    )

    # --------------------------------------------------------
    # Размеры
    # --------------------------------------------------------

    st.markdown(
        '<div class="calc-subtitle">Размеры одного места</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3, gap="small")

    with c1:

        st.number_input(
            "Длина",
            min_value=100,
            step=10,
            value=int(cargo["length"]),
            key="ui_length",
            on_change=_update,
            args=("length",),
        )

    with c2:

        st.number_input(
            "Ширина",
            min_value=100,
            step=10,
            value=int(cargo["width"]),
            key="ui_width",
            on_change=_update,
            args=("width",),
        )

    with c3:

        st.number_input(
            "Высота",
            min_value=100,
            step=10,
            value=int(cargo["height"]),
            key="ui_height",
            on_change=_update,
            args=("height",),
        )

    # --------------------------------------------------------
    # Количество
    # --------------------------------------------------------

    st.number_input(
        "Количество мест",
        min_value=1,
        step=1,
        value=int(cargo["qty"]),
        key="ui_qty",
        on_change=_update,
        args=("qty",),
    )

    # --------------------------------------------------------
    # Стоимость
    # --------------------------------------------------------

    st.number_input(
        "Стоимость товара (USD)",
        min_value=0.0,
        step=100.0,
        value=float(cargo["invoice_usd"]),
        key="ui_invoice_usd",
        on_change=_update,
        args=("invoice_usd",),
    )

    # ========================================================
    # ТН ВЭД
    # ========================================================

    st.markdown(
        '<div class="calc-section-title calc-section-spacing">2. КОД ТН ВЭД</div>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # AI button
    # --------------------------------------------------------

    if st.button(
        "🤖 Подобрать код ТН ВЭД",
        use_container_width=True,
        key="classify_product",
    ):

        product_name = cargo["product_name"].strip()

        if not product_name:

            st.warning("Введите название товара.")

        else:

            with st.spinner("ИИ анализирует товар..."):

                results = classify_product(product_name)

            if results:

                st.session_state.ai_results = results

                cargo["tnved"] = results[0]["code"]

                refresh()

                st.rerun()

            else:

                st.error(
                    "Не удалось подобрать код ТН ВЭД."
                )

    # --------------------------------------------------------
    # Manual search
    # --------------------------------------------------------

    selected = tnved_search()

    if selected:

        if cargo["tnved"] != selected["code"]:

            cargo["tnved"] = selected["code"]

            refresh()

            st.rerun()

    # --------------------------------------------------------
    # Selected code
    # --------------------------------------------------------

    if cargo["tnved"]:

        item = get_by_code(cargo["tnved"])

        if item:

            st.markdown(
                """
                <div class="calc-selected-tnved">
                    <div class="calc-selected-tnved-label">
                        Выбранный код
                    </div>
                """,
                unsafe_allow_html=True,
            )

            st.code(
                item["code"],
                language=None,
            )

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

            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )


# ============================================================
# CENTER COLUMN
# ============================================================

def _show_result_column(cargo, calc):

    st.markdown(
        '<div class="calc-section-title">РЕЗУЛЬТАТ РАСЧЁТА</div>',
        unsafe_allow_html=True,
    )

    # ========================================================
    # MAIN RESULT
    # ========================================================

    full_cost = calc.get("full_cost", 0)

    st.markdown(
        f"""
        <div class="calc-main-result">
            <div class="calc-main-result-label">
                Полная стоимость
            </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="calc-main-result-value">
            {_money(full_cost)} <span>RUB</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # USD equivalent
    # --------------------------------------------------------

    usd = st.session_state.get(
        "rates",
        {},
    ).get(
        "USD_RUB",
        0,
    )

    if usd:

        usd_value = full_cost / usd

        st.markdown(
            f"""
            <div class="calc-main-result-secondary">
                {_money(usd_value)} USD
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

    # ========================================================
    # COST CARDS
    # ========================================================

    invoice_rub = calc.get(
        "invoice_rub",
        0,
    )

    dovoz_cost = calc.get(
        "dovoz_cost",
        0,
    )

    duty = calc.get(
        "duty",
        0,
    )

    vat = calc.get(
        "vat",
        0,
    )

    fee = calc.get(
        "fee",
        0,
    )

    cards = [
        (
            "Стоимость товара",
            invoice_rub,
        ),
        (
            "Доставка",
            dovoz_cost,
        ),
        (
            "Пошлина",
            duty,
        ),
        (
            "НДС",
            vat,
        ),
        (
            "Сборы",
            fee,
        ),
    ]

    card_columns = st.columns(
        5,
        gap="small",
    )

    for column, (title, value) in zip(
        card_columns,
        cards,
    ):

        with column:

            _result_card(
                title,
                f"{_money(value)} ₽",
            )

    # ========================================================
    # TRANSPORT RESULTS
    # ========================================================

    st.markdown(
        '<div class="calc-section-title calc-section-spacing">ВАРИАНТЫ ДОСТАВКИ</div>',
        unsafe_allow_html=True,
    )

    results = calc.get(
        "results",
        [],
    )

    for result in results:

        if len(result) < 4:
            continue

        title = result[0]
        price = result[1]
        coefficient = result[2]
        weight = result[3]

        st.markdown(
            f"""
            <div class="calc-transport-row">
                <div>
                    <div class="calc-transport-name">
                        {title}
                    </div>
                    <div class="calc-transport-meta">
                        Расчётный вес: {weight}
                    </div>
                </div>
                <div class="calc-transport-price">
                    {_money(price)} ₽
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ========================================================
    # COST DISTRIBUTION
    # ========================================================

    st.markdown(
        '<div class="calc-section-title calc-section-spacing">РАСПРЕДЕЛЕНИЕ СТОИМОСТИ</div>',
        unsafe_allow_html=True,
    )

    if full_cost > 0:

        components = [
            (
                "Товар",
                invoice_rub,
            ),
            (
                "Доставка",
                dovoz_cost,
            ),
            (
                "Пошлина",
                duty,
            ),
            (
                "НДС",
                vat,
            ),
            (
                "Сборы",
                fee,
            ),
        ]

        components = [
            (name, value)
            for name, value in components
            if value > 0
        ]

        bar = ""

        for name, value in components:

            percent = (
                value / full_cost * 100
            )

            bar += f"""
            <div
                class="calc-distribution-segment"
                style="width:{percent:.2f}%"
                title="{name}: {percent:.2f}%"
            >
                {percent:.1f}%
            </div>
            """

        st.markdown(
            f"""
            <div class="calc-distribution">
                {bar}
            </div>
            """,
            unsafe_allow_html=True,
        )

        legend = ""

        for name, value in components:

            percent = (
                value / full_cost * 100
            )

            legend += f"""
            <span>
                <b>{name}</b>
                {percent:.2f}%
            </span>
            """

        st.markdown(
            f"""
            <div class="calc-distribution-legend">
                {legend}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ========================================================
    # INDICATORS
    # ========================================================

    st.markdown(
        '<div class="calc-section-title calc-section-spacing">ПОКАЗАТЕЛИ</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    total_weight = calc.get(
        "total_weight",
        0,
    )

    volume = calc.get(
        "volume",
        0,
    )

    with c1:

        if total_weight:

            cost_per_kg = (
                full_cost / total_weight
            )

            st.metric(
                "Стоимость за кг",
                f"{_money(cost_per_kg)} ₽",
            )

    with c2:

        if volume:

            cost_per_m3 = (
                full_cost / volume
            )

            st.metric(
                "Стоимость за м³",
                f"{_money(cost_per_m3)} ₽",
            )

    with c3:

        qty = cargo.get(
            "qty",
            1,
        )

        if qty:

            cost_per_unit = (
                full_cost / qty
            )

            st.metric(
                "Стоимость за место",
                f"{_money(cost_per_unit)} ₽",
            )

    # ========================================================
    # COST FORMATION
    # ========================================================

    st.markdown(
        '<div class="calc-section-title calc-section-spacing">ФОРМИРОВАНИЕ СТОИМОСТИ</div>',
        unsafe_allow_html=True,
    )

    stages = [
        ("Товар", invoice_rub),
        ("Доставка", dovoz_cost),
        ("Пошлина", duty),
        ("НДС", vat),
        ("Сборы", fee),
        ("Итого", full_cost),
    ]

    stage_columns = st.columns(
        len(stages),
        gap="small",
    )

    for column, (name, value) in zip(
        stage_columns,
        stages,
    ):

        with column:

            st.markdown(
                f"""
                <div class="calc-stage">
                    <div class="calc-stage-name">
                        {name}
                    </div>
                    <div class="calc-stage-value">
                        {_money(value)}
                    </div>
                    <div class="calc-stage-currency">
                        RUB
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# RIGHT COLUMN
# ============================================================

def _show_info_column(cargo, calc):
    duty = calc.get("duty", 0)
    vat = calc.get("vat", 0)
    # ========================================================
    # AI
    # ========================================================

    st.markdown(
        '<div class="calc-section-title">🤖 AI РЕКОМЕНДУЕТ ТН ВЭД</div>',
        unsafe_allow_html=True,
    )

    ai_results = st.session_state.get(
        "ai_results",
        [],
    )

    if ai_results:

        best = ai_results[0]

        st.markdown(
            f"""
            <div class="calc-ai-main">
                <div class="calc-ai-label">
                    Рекомендуемый код
                </div>
                <div class="calc-ai-code">
                    {best["code"]}
                </div>
                <div class="calc-ai-confidence">
                    {_confidence_icon(best["confidence"])}
                    {best["confidence"]}%
                </div>
                <div class="calc-ai-description">
                    {best["description"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if len(ai_results) > 1:

            st.markdown(
                '<div class="calc-ai-alternatives-title">Альтернативные варианты</div>',
                unsafe_allow_html=True,
            )

            for i, ai in enumerate(
                ai_results[1:4],
                start=1,
            ):

                c1, c2 = st.columns(
                    [4, 1],
                )

                with c1:

                    st.markdown(
                        f"**{ai['code']}**"
                    )

                with c2:

                    st.markdown(
                        f"**{ai['confidence']}%**"
                    )

    else:

        st.info(
            "Введите название товара и запустите AI-рекомендацию."
        )

    # ========================================================
    # SHIPMENT SUMMARY
    # ========================================================

    st.markdown(
        '<div class="calc-section-title calc-section-spacing">ПАРАМЕТРЫ ПОСТАВКИ</div>',
        unsafe_allow_html=True,
    )

    rows = [
        (
            "Количество",
            f'{cargo.get("qty", 0):,} шт',
        ),
        (
            "Вес брутто",
            f'{calc.get("total_weight", 0):,.0f} кг',
        ),
        (
            "Объём",
            f'{calc.get("volume", 0):.3f} м³',
        ),
        (
            "Стоимость товара",
            f'{cargo.get("invoice_usd", 0):,.2f} USD',
        ),
        (
            "Курс USD",
            f'{st.session_state.get("rates", {}).get("USD_RUB", 0):.4f}',
        ),
        (
            "Курс CNY",
            f'{st.session_state.get("rates", {}).get("CNY_RUB", 0):.4f}',
        ),
    ]

    for label, value in rows:

        st.markdown(
            f"""
            <div class="calc-info-row">
                <span>{label}</span>
                <strong>{value}</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ========================================================
    # WARNINGS
    # ========================================================

    st.markdown(
        '<div class="calc-section-title calc-section-spacing">⚠ ПРЕДУПРЕЖДЕНИЯ</div>',
        unsafe_allow_html=True,
    )

    st.warning(
        "Проверьте актуальность курса валют."
    )

    if not cargo.get("tnved"):

        st.warning(
            "Код ТН ВЭД не выбран."
        )

    if cargo.get("weight_per_unit", 0) <= 0:

        st.error(
            "Не указан вес груза."
        )

    # ========================================================
    # CUSTOMS
    # ========================================================

    st.markdown(
        '<div class="calc-section-title calc-section-spacing">ТАМОЖЕННЫЕ ПЛАТЕЖИ</div>',
        unsafe_allow_html=True,
    )

    customs = calc.get(
        "total_customs",
        0,
    )

    st.metric(
        "Всего",
        f"{_money(customs)} ₽",
    )

    c1, c2 = st.columns(2, gap="small")

    with c1:
        st.caption("Пошлина")
        st.markdown(
            f"""
            <div class="customs-value">
                {_money(duty)} ₽
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.caption("НДС")
        st.markdown(
            f"""
            <div class="customs-value">
                {_money(vat)} ₽
            </div>
            """,
            unsafe_allow_html=True,
        )

    if "show_save_name" not in st.session_state:
        st.session_state.show_save_name = False
    st.markdown(
        '<div class="save-calculation-anchor"></div>',
        unsafe_allow_html=True,
    )
    if not st.session_state.show_save_name:

        if st.button(
            "💾 Сохранить расчёт",
            key="save_calculation_button",
            use_container_width=True,
        ):
            st.session_state.show_save_name = True
            st.rerun()

    else:

        st.markdown(
            '<div class="save-calculation-title">Название расчёта</div>',
            unsafe_allow_html=True,
        )

        calculation_name = st.text_input(
            "Название расчёта",
            placeholder="Например: Поставка электросамокатов — август",
            key="calculation_name",
            label_visibility="collapsed",
        )

        save_col, cancel_col = st.columns(2)

        with save_col:

            if st.button(
                "✓ Сохранить",
                key="confirm_save_calculation",
                use_container_width=True,
            ):

                if not calculation_name.strip():

                    st.toast(
                        "Введите название расчёта",
                        icon="⚠️",
                    )

                else:

                    history_id = save_calculation(
                        user_id=st.session_state.user["id"],
                        calculation_name=calculation_name.strip(),
                        cargo=st.session_state.cargo,
                        calc=st.session_state.calc,
                        tariffs=st.session_state.tariffs,
                        rates=st.session_state.rates,
                        customs=st.session_state.customs,
                    )

                    st.session_state.show_save_name = False

                    st.toast(
                        f"Расчёт «{calculation_name.strip()}» сохранён",
                        icon="✅",
                    )

                    st.rerun()

        with cancel_col:

            if st.button(
                "Отмена",
                key="cancel_save_calculation",
                use_container_width=True,
            ):

                st.session_state.show_save_name = False

                st.rerun()
    # ========================================================
    # EXPORT
    # ========================================================

    excel_file = build_excel(
        st.session_state.cargo,
        st.session_state.calc,
        st.session_state.tariffs,
        st.session_state.rates,
        st.session_state.customs,
    )

    pdf_file = build_pdf(
        st.session_state.cargo,
        st.session_state.calc,
        st.session_state.tariffs,
        st.session_state.rates,
        st.session_state.customs,
    )

    export_pdf, export_excel = st.columns(
        2,
        gap="small",
    )

    with export_pdf:
        st.download_button(
            "📄 PDF",
            data=pdf_file,
            file_name="LTLCALC_calculation.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="export_pdf",
        )

    with export_excel:
        st.download_button(
            "📊 Excel",
            data=excel_file,
            file_name="LTLCALC_calculation.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            key="export_excel",
        )
# ============================================================
# MAIN
# ============================================================

def show():

    cargo = st.session_state.cargo
    calc = st.session_state.calc

    # ========================================================
    # 3 COLUMN WORKSPACE
    # ========================================================

    product_col, result_col, info_col = st.columns(
        [
            1.0,
            1.45,
            0.90,
        ],
        gap="medium",
    )

    # ========================================================
    # PRODUCT
    # ========================================================

    with product_col:

        _show_product_column(cargo)

    # ========================================================
    # RESULT
    # ========================================================

    with result_col:

        _show_result_column(
            cargo,
            calc,
        )

    # ========================================================
    # INFORMATION
    # ========================================================

    with info_col:

        _show_info_column(
            cargo,
            calc,
        )