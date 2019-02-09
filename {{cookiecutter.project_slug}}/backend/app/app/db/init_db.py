from app.core import config
from app.db.utils import (
    assign_role_to_user,
    create_role,
    create_user,
    get_role_by_name,
    get_user_by_username,
)


def init_db(db_session):
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables uncommenting the next line
    # Base.metadata.create_all(bind=engine)

    role = get_role_by_name("default", db_session)
    if not role:
        role = create_role("default", db_session)

    user = get_user_by_username(config.FIRST_SUPERUSER, db_session)
    if not user:
        user = create_user(
            db_session,
            config.FIRST_SUPERUSER,
            config.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        assign_role_to_user(role, user, db_session)
