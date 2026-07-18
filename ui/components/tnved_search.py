from streamlit_searchbox import st_searchbox
from services.tnved import suggest, get_by_code


def search_function(searchterm: str):

    if len(searchterm) < 2:
        return []

    items = suggest(searchterm, 15)

    print("SEARCH:", searchterm)
    print("FOUND:", len(items))

    return [
        f'{item["code"]} — {item["description"]}'
        for item in items
    ]


def tnved_search():

    selected = st_searchbox(
        search_function,
        placeholder="Введите код или название товара...",
        label="Код ТН ВЭД",
        clear_on_submit=False,
        key="tnved_search",
    )

    if not selected:
        return None

    code = selected.split(" — ")[0]

    return get_by_code(code)