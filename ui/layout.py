import streamlit as st


# ==========================================================
# Layout
# ==========================================================

LEFT_RATIO = 3.5
CENTER_RATIO = 6
RIGHT_RATIO = 2.5


def page():
    """
    Основная сетка приложения.

    Возвращает:
        left    - панель ввода
        center  - результаты
        right   - вспомогательная информация
    """

    return st.columns(
        [LEFT_RATIO, CENTER_RATIO, RIGHT_RATIO],
        gap="large",
        vertical_alignment="top",
    )


# ==========================================================
# Карточка
# ==========================================================

def card(title: str, icon: str = "", border: bool = True):
    """
    Создаёт визуальную карточку.

    Использование:

    with card("Товар", "📦"):
        ...
    """

    css = "logic-card"

    if not border:
        css += " logic-card-flat"

    st.markdown(
        f"""
        <div class="{css}">
            <div class="logic-card-title">
                <span class="logic-card-icon">{icon}</span>
                <span>{title}</span>
            </div>
        """,
        unsafe_allow_html=True,
    )

    container = st.container()

    class _Card:
        def __enter__(self):
            return container

        def __exit__(self, exc_type, exc_val, exc_tb):
            st.markdown("</div>", unsafe_allow_html=True)

    return _Card()


# ==========================================================
# Заголовок раздела
# ==========================================================

def section(title: str):
    st.markdown(
        f"""
        <div class="logic-section">
            {title}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==========================================================
# Toolbar
# ==========================================================

def toolbar():

    c1, c2, c3, c4, c5, _ = st.columns(
        [1.4, 1.2, 1.2, 1.2, 1.4, 6]
    )

    with c1:
        st.button("🧮 Рассчитать", use_container_width=True)

    with c2:
        st.button("💾 Сохранить", use_container_width=True)

    with c3:
        st.button("📄 Excel", use_container_width=True)

    with c4:
        st.button("📑 КП", use_container_width=True)

    with c5:
        st.button("🖨 Печать", use_container_width=True)


# ==========================================================
# Большое число
# ==========================================================

def hero(title: str, value: str):

    st.markdown(
        f"""
        <div class="logic-hero">

            <div class="logic-hero-title">
                {title}
            </div>

            <div class="logic-hero-value">
                {value}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ==========================================================
# Информационная строка
# ==========================================================

def info(label: str, value: str):

    st.markdown(
        f"""
        <div class="logic-info">

            <span class="logic-info-label">
                {label}
            </span>

            <span class="logic-info-value">
                {value}
            </span>

        </div>
        """,
        unsafe_allow_html=True,
    )