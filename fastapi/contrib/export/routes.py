from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, StreamingResponse
import pandas as pd
import io
import csv
import pyarrow.parquet as pq
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import mysql.connector


router = FastAPI()


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

    
     elif format == "pdf":
        output = io.BytesIO()
        pdf = canvas.Canvas(output, pagesize=letter)
        pdf.drawString(100, 750, "Exported Data")
        y = 730
        for row in df.to_dict(orient="records"):
            pdf.drawString(100, y, str(row))
            y -= 20
        pdf.save()
        output.seek(0)
        return StreamingResponse(output, media_type="application/pdf",
                                 headers={"Content-Disposition": "attachment; filename=data.pdf"})

    elif format == "parquet":
        output = io.BytesIO()
        table = df.to_parquet(output, engine="pyarrow")
        output.seek(0)
        return StreamingResponse(output, media_type="application/octet-stream",
                                 headers={"Content-Disposition": "attachment; filename=data.parquet"})

    elif format == "mysql":
        conn = mysql.connector.connect(
            host="your_mysql_host",
            user="your_mysql_user",
            password="your_mysql_password",
            database="your_database"
        )
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS exported_data (id INT, name VARCHAR(255), age INT)")
        cursor.executemany("INSERT INTO exported_data (id, name, age) VALUES (%s, %s, %s)",
                           [(row["id"], row["name"], row["age"]) for row in data])
        conn.commit()
        cursor.close()
        conn.close()
        return JSONResponse(content={"message": "Data successfully exported to MySQL."})
    
    return JSONResponse(content={"error": "Invalid format"}, status_code=400)
