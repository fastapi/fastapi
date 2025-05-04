from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse, StreamingResponse
import pandas as pd
import io
import csv
import pyarrow.parquet as pq
import pyarrow.feather as feather
import pyarrow.orc as orc
import avro.schema
import avro.io
import sqlite3
import struct
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import mysql.connector


router = APIRouter()


# Sample data (to be linked with external db)
data = [
    {"id": 1, "name": "George", "age": 35},
    {"id": 2, "name": "Joanna", "age": 22},
    {"id": 3, "name": "Sebastian", "age": 27}
]


@router.get("/export")

async def export_data(format: str = Query("json", enum=["json", "csv", "excel", "pdf", "parquet", "mysql", "avro", "feather", "orc", "sqlite", "protobuf"])):
    df = pd.DataFrame(data)

    # JSON format 
    if format == "json":
        return JSONResponse(content=df.to_dict(orient="records"))

    # CSV format 
    elif format == "csv":
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=df.columns)
        writer.writeheader()
        writer.writerows(df.to_dict(orient="records"))
        output.seek(0)
        return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=data.csv"})

    # Excel format 
    elif format == "excel":
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Sheet1")
        output.seek(0)
        return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                 headers={"Content-Disposition": "attachment; filename=data.xlsx"})

    # PDF format 
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

    # Parquet format 
    elif format == "parquet":
        output = io.BytesIO()
        table = df.to_parquet(output, engine="pyarrow")
        output.seek(0)
        return StreamingResponse(output, media_type="application/octet-stream",
                                 headers={"Content-Disposition": "attachment; filename=data.parquet"})

    # MySQL format 
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


    # AVRO format 
	elif format == "avro":
    	output = io.BytesIO()
    	schema = avro.schema.parse('{"type": "record", "name": "DataRecord", "fields": [{"name": "id", "type": "int"}, {"name": "name", "type": "string"}, {"name": "age", "type": "int"}]}')
    	writer = avro.io.DatumWriter(schema)
    	encoder = avro.io.BinaryEncoder(output)
    	for row in data:
        	writer.write(row, encoder)
    	output.seek(0)
    	return StreamingResponse(output, media_type="application/octet-stream",
                             	headers={"Content-Disposition": "attachment; filename=data.avro"})

    # Feather format 
	elif format == "feather":
    	output = io.BytesIO()
    	feather.write_feather(df, output)
    	output.seek(0)
    	return StreamingResponse(output, media_type="application/octet-stream",
                             	headers={"Content-Disposition": "attachment; filename=data.feather"})

    # ORC format 
	elif format == "orc":
    	output = io.BytesIO()
    	df.to_orc(output, engine="pyarrow")
    	output.seek(0)
    	return StreamingResponse(output, media_type="application/octet-stream",
                             	headers={"Content-Disposition": "attachment; filename=data.orc"})

    # SQLite format 
	elif format == "sqlite":
    	output = io.BytesIO()
    	conn = sqlite3.connect(":memory:")
    	df.to_sql("exported_data", conn, if_exists="replace", index=False)
    	conn.backup(output)
    	output.seek(0)
    	conn.close()
    	return StreamingResponse(output, media_type="application/x-sqlite3",
                             	headers={"Content-Disposition": "attachment; filename=data.db"})

    # Protobuf format 
	elif format == "protobuf":
    	output = io.BytesIO()
    	for row in data:
        	output.write(struct.pack("i", row["id"]))
        	output.write(row["name"].encode('utf-8') + b'\x00')  # Null-terminated string
        	output.write(struct.pack("i", row["age"]))
    	output.seek(0)
    	return StreamingResponse(output, media_type="application/octet-stream",
                             	headers={"Content-Disposition": "attachment; filename=data.proto"})

    
    return JSONResponse(content={"error": "Invalid format"}, status_code=400)
