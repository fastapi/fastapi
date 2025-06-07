# FastAPI export app
# by Joanna Karitsioti & George Tsakalos


from typing import Literal
from fastapi import FastAPI, Query, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse, RedirectResponse
import pandas as pd
import io
import csv
import os
import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError
import mysql.connector
from export_app.dbase_converter import convert_to_json, fetch_from_sqlite, fetch_from_mysql
from export_app.dbase_online_import import router as online_db_router
import pulsar
import pika
from kafka import KafkaProducer



app = FastAPI(title="Data Import & Export App")
app.include_router(online_db_router)


# Main files exports
def export_to_csv(df: pd.DataFrame):
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=df.columns)
    writer.writeheader()
    writer.writerows(df.to_dict(orient="records"))
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv",
                             headers={"Content-Disposition": "attachment; filename=data.csv"})


def export_to_excel(df: pd.DataFrame):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
    output.seek(0)
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             headers={"Content-Disposition": "attachment; filename=data.xlsx"})


def export_to_pdf(df: pd.DataFrame):
    output = io.BytesIO()
    doc = SimpleDocTemplate(output, pagesize=A4)

    table_data = [df.columns.tolist()] + df.values.tolist()

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
    ]))

    doc.build([table])
    output.seek(0)
    return StreamingResponse(output, media_type="application/pdf",
                             headers={"Content-Disposition": "attachment; filename=data.pdf"})


def export_to_parquet(df: pd.DataFrame):
    output = io.BytesIO()
    df.to_parquet(output, engine="pyarrow", index=False)
    output.seek(0)
    return StreamingResponse(output, media_type="application/octet-stream",
                             headers={"Content-Disposition": "attachment; filename=data.parquet"})


def export_to_avro(df: pd.DataFrame):
    output = io.BytesIO()
    df.to_avro(output, engine="fastavro", index=False)
    output.seek(0)
    return StreamingResponse(output, media_type="application/octet-stream",
                             headers={"Content-Disposition": "attachment; filename=data.avro"})


def export_to_feather(df: pd.DataFrame):
    output = io.BytesIO()
    df.to_feather(output)
    output.seek(0)
    return StreamingResponse(output, media_type="application/octet-stream",
                             headers={"Content-Disposition": "attachment; filename=data.feather"})


def export_to_orc(df: pd.DataFrame):
    output = io.BytesIO()
    df.to_orc(output)
    output.seek(0)
    return StreamingResponse(output, media_type="application/octet-stream",
                             headers={"Content-Disposition": "attachment; filename=data.orc"})


def export_to_sqlite(df: pd.DataFrame):
    conn = sqlite3.connect("data_export.db")
    df.to_sql("exported_data", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()

    with open("data_export.db", "rb") as f:
        file_data = f.read()

    output = io.BytesIO(file_data)
    return StreamingResponse(output, media_type="application/x-sqlite3",
                             headers={"Content-Disposition": "attachment; filename=data_export.db"})


def export_to_mysql(df: pd.DataFrame):
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "testdb")
    )
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS exported_data (id INT, name VARCHAR(255), age INT)")
    cursor.executemany("INSERT INTO exported_data (id, name, age) VALUES (%s, %s, %s)",
                       [(row["id"], row["name"], row["age"]) for row in df.to_dict(orient="records")])
    conn.commit()
    cursor.close()
    conn.close()
    return JSONResponse(content={"message": "Data successfully exported to MySQL."})


@app.post("/export", summary="Export data to a specified format", description="Upload a .txt, .csv or .json file and choose the desired output format (e.g. Excel, PDF, MySQL, S3, Kafka, etc). The file will be parsed and converted automatically.")
async def export_data(
    file: UploadFile = File(...),
    format: str = Query("json", enum=[
        "json", "csv", "excel", "pdf", "parquet",
        "mysql", "avro", "feather", "orc", "sqlite", "s3", "kafka", "rabbitmq", "pulsar"
    ])
):
    try:
        records = await convert_to_json(file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    df = pd.DataFrame(records)

    if format == "json":
        return JSONResponse(content=df.to_dict(orient="records"))
    elif format == "csv":
        return export_to_csv(df)
    elif format == "excel":
        return export_to_excel(df)
    elif format == "pdf":
        return export_to_pdf(df)
    elif format == "parquet":
        return export_to_parquet(df)
    elif format == "mysql":
        return export_to_mysql(df)
    elif format == "avro":
        return export_to_avro(df)
    elif format == "feather":
        return export_to_feather(df)
    elif format == "orc":
        return export_to_orc(df)
    elif format == "sqlite":
        return export_to_sqlite(df)
    elif format == "s3":
        return export_to_s3(df)
    elif format == "kafka":
        return export_to_kafka(df)
    elif format == "rabbitmq":
        return export_to_rabbitmq(df)
    elif format == "pulsar":
        return export_to_pulsar(df)

    return JSONResponse(content={"error": "Invalid format"}, status_code=400)



@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


# Special formats export
def export_to_s3(df: pd.DataFrame):
    bucket_name = os.getenv("AWS_S3_BUCKET", "your-bucket-name")
    object_key = os.getenv("AWS_S3_OBJECT_KEY", "exported_data.json")

    json_data = df.to_json(orient="records").encode("utf-8")

    try:
        s3 = boto3.client("s3")
        s3.put_object(Bucket=bucket_name, Key=object_key, Body=json_data)
        return JSONResponse(content={"message": f"Data exported to S3: s3://{bucket_name}/{object_key}"})
    except (BotoCoreError, NoCredentialsError) as e:
        return JSONResponse(content={"error": f"S3 upload failed: {str(e)}"}, status_code=500)


def export_to_kafka(df: pd.DataFrame):
    try:
        producer = KafkaProducer(bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"))
        topic = os.getenv("KAFKA_TOPIC", "exported_data")
        for record in df.to_dict(orient="records"):
            producer.send(topic, pd.io.json.dumps(record).encode('utf-8'))
        producer.flush()
        return JSONResponse(content={"message": f"Data sent to Kafka topic '{topic}'"})
    except Exception as e:
        return JSONResponse(content={"error": f"Kafka export failed: {str(e)}"}, status_code=500)


def export_to_rabbitmq(df: pd.DataFrame):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv("RABBITMQ_HOST", "localhost")))
        channel = connection.channel()
        queue = os.getenv("RABBITMQ_QUEUE", "export_queue")
        channel.queue_declare(queue=queue)

        for record in df.to_dict(orient="records"):
            channel.basic_publish(exchange='', routing_key=queue, body=pd.io.json.dumps(record))
        connection.close()
        return JSONResponse(content={"message": f"Data sent to RabbitMQ queue '{queue}'"})
    except Exception as e:
        return JSONResponse(content={"error": f"RabbitMQ export failed: {str(e)}"}, status_code=500)


def export_to_pulsar(df: pd.DataFrame):
    try:
        service_url = os.getenv("PULSAR_SERVICE_URL", "pulsar://localhost:6650")
        topic = os.getenv("PULSAR_TOPIC", "exported_data")
        client = pulsar.Client(service_url)
        producer = client.create_producer(topic)

        for record in df.to_dict(orient="records"):
            producer.send(pd.io.json.dumps(record).encode('utf-8'))
        client.close()
        return JSONResponse(content={"message": f"Data sent to Pulsar topic '{topic}'"})
    except Exception as e:
        return JSONResponse(content={"error": f"Pulsar export failed: {str(e)}"}, status_code=500)
