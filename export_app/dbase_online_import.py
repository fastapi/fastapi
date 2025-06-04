# FastAPI online dbase import by Joanna Karitsioti & George Tsakalos

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from export_app.dbase_converter import fetch_from_sqlite, fetch_from_mysql
from typing import Literal

app = FastAPI(title="Online Database Import API")

@app.get("/import-online-db", summary="Import data from an online database")
async def import_from_database(
    db_type: Literal["sqlite", "mysql"] = Query(..., description="Type of database"),
    host: str = Query(None, description="Database host (for MySQL)"),
    user: str = Query(None, description="Database username (for MySQL)"),
    password: str = Query(None, description="Database password (for MySQL)"),
    database: str = Query(None, description="Database name (for MySQL)"),
    table: str = Query(..., description="Table name to fetch from"),
    url: str = Query(None, description="SQLite database URL (path to .db file)")
):
    try:
        if db_type == "sqlite":
            if not url:
                raise ValueError("SQLite 'url' parameter is required")
            data = fetch_from_sqlite(url=url, table=table)
        elif db_type == "mysql":
            if not all([host, user, password, database]):
                raise ValueError("MySQL requires host, user, password, and database")
            data = fetch_from_mysql(host=host, user=user, password=password, database=database, table=table)
        else:
            raise ValueError("Unsupported database type")

        return JSONResponse(content={"data": data})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
