from app import crud
from app.core import config
from app.models.user import UserInCreate


def init_db(db_session):
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = crud.user.get_by_email(db_session, email=config.FIRST_SUPERUSER)
    if not user:
        user_in = UserInCreate(
            email=config.FIRST_SUPERUSER,
            password=config.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(db_session, user_in=user_in)
