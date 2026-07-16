import extra_streamlit_components as stx

COOKIE_NAME = "ltlcalc_session"

_cookie_manager = None


def manager():

    global _cookie_manager

    if _cookie_manager is None:
        _cookie_manager = stx.CookieManager()

    return _cookie_manager


def save_session(token: str):

    manager().set(
        COOKIE_NAME,
        token,
    )


def get_session():

    return manager().get(COOKIE_NAME)


def delete_session():

    manager().delete(COOKIE_NAME)