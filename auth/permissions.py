from . import auth


def is_admin():

    return auth.role == "admin"


def is_manager():

    return auth.role == "manager"


def is_user():

    return auth.role == "user"


def can_manage_users():

    return auth.role == "admin"


def can_edit_tariffs():

    return auth.role in (
        "admin",
        "manager",
    )