from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, StreamingResponse
import pandas as pd
import io
import csv

app = FastAPI()


# Sample data (to be linked with external db)
data = [
    {"id": 1, "name": "George", "age": 35},
    {"id": 2, "name": "Joanna", "age": 22},
]


@app.get("/export")

async def export_data(format: str = Query("json", enum=["json", "csv", "excel", "pdf", "parquet", "mysql"])):
    df = pd.DataFrame(data)

    if format == "json":
        return JSONResponse(content=df.to_dict(orient="records"))


    elif format == "csv":
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=df.columns)
        writer.writeheader()
        writer.writerows(df.to_dict(orient="records"))
        output.seek(0)
        return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=data.csv"})

    elif format == "excel":
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Sheet1")
        output.seek(0)
        return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                 headers={"Content-Disposition": "attachment; filename=data.xlsx"})


    return JSONResponse(content={"error": "Invalid format"}, status_code=400)