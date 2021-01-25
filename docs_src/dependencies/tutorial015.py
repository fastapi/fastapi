from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()


@app.exception_handler(DBSessionException)
async def validation_exception_handler(request, exc):
    return HTTPException(
        status_code=503,
        detail=f"Database not available: {exc}",
    )


async def get_session():
    session = DBSession()
    transaction = session.begin_transaction()
    try:
        yield session
        transaction.commit()
    except DBSessionException:
        transaction.rollback()
    finally:
        session.close()


@app.get("/commit-may-fail")
async def read_items(
    session: DBSession = Depends(get_session, exit_before_response=True)
):
    session.add(Table())
