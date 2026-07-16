from .database import initialize_database
from .users import get_user
from .users import create_user


def bootstrap():

    initialize_database()

    if get_user("admin") is None:

        create_user(
            username="admin",
            password="admin",
            name="Administrator",
            email="admin@ltlcalc.ru",
            role="admin",
        )