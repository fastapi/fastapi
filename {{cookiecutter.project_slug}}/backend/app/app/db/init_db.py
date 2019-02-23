from app.core import config
from app.crud import user as crud_user
from app.models.user import UserInCreate


def init_db(db_session):
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables uncommenting the next line
    # Base.metadata.create_all(bind=engine)

    user = crud_user.get_by_email(db_session, email=config.FIRST_SUPERUSER)
    if not user:
        user_in = UserInCreate(
            email=config.FIRST_SUPERUSER,
            password=config.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud_user.create(db_session, user_in=user_in)
