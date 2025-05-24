# Export Data Example with FastAPI 
# by Joanna Karytsioti & George Tsakalos

This FastAPI app demonstrates how to export structured data to a wide variety of formats and systems.

---

## ✅ Supported Export Formats

### 📁 File Formats
- JSON (`?format=json`)
- CSV (`?format=csv`)
- Excel (`?format=excel`)
- PDF (`?format=pdf`)
- Parquet (`?format=parquet`)
- Avro (`?format=avro`)
- Feather (`?format=feather`)
- ORC (`?format=orc`)

### 🗄 Databases & Storage
- MySQL (`?format=mysql`)
- SQLite (`?format=sqlite`)
- AWS S3 (`?format=s3`)

### 🔄 Streaming Systems
- Kafka (`?format=kafka`)
- RabbitMQ (`?format=rabbitmq`)
- Apache Pulsar (`?format=pulsar`)

---

## 🚀 How to Run

1. **Install dependencies**:

```bash
pip install -r requirements_all_exports.txt
```

2. **Start the FastAPI server**:

```bash
uvicorn main:app --reload
```

3. **Visit**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)  
   This will redirect you to Swagger docs (`/docs`) where you can test the `/export` endpoint.

---

## 🔐 Environment Variables

### AWS S3:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_S3_BUCKET`
- `AWS_S3_OBJECT_KEY`

### MySQL:
- `MYSQL_HOST`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_DATABASE`

### Kafka:
- `KAFKA_BOOTSTRAP_SERVERS` (default: `localhost:9092`)
- `KAFKA_TOPIC` (default: `exported_data`)

### RabbitMQ:
- `RABBITMQ_HOST` (default: `localhost`)
- `RABBITMQ_QUEUE` (default: `export_queue`)

### Pulsar:
- `PULSAR_SERVICE_URL` (default: `pulsar://localhost:6650`)
- `PULSAR_TOPIC` (default: `exported_data`)

---

## 📦 Dependencies (see `requirements_all_exports.txt`)

- `fastapi`, `uvicorn`
- `pandas`, `xlsxwriter`, `reportlab`, `pyarrow`, `fastavro`
- `mysql-connector-python`, `boto3`, `kafka-python`, `pika`, `pulsar-client`

---

## 📄 License

MIT – for educational, demonstration, and contribution purposes.

