# FastAPI Export App

Export structured data to multiple formats and systems with FastAPI.  
By Joanna Karytsioti & George Tsakalos (AUEB DMST – Spinelis SEIP)

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fastapi-code-generator)](https://pypi.python.org/pypi/fastapi-code-generator)
![license](https://img.shields.io/github/license/koxudaxi/fastapi-code-generator.svg)

---

## 📦 Features

This FastAPI application supports exporting data to:

### 📁 File Formats

This app supports uploading your own `.txt`, `.csv`, or `.json` file (via Swagger UI),  
automatically converting it to structured data for export.

You can also fetch data directly from an **online SQLite or MySQL database** by calling the `/import-online-db` endpoint.


This app supports uploading your own `.txt`, `.csv`, or `.json` file (via Swagger UI),
automatically converting it to structured data for export.


- **JSON** → `?format=json`  
- **CSV** → `?format=csv`  
- **Excel** → `?format=excel`  
- **PDF** → `?format=pdf`  
- **Parquet** → `?format=parquet`  
- **Avro** → `?format=avro`  
- **Feather** → `?format=feather`  
- **ORC** → `?format=orc`  

### 🗄 Databases & Storage

- **MySQL** → `?format=mysql`  
- **SQLite** → `?format=sqlite`  
- **AWS S3** → `?format=s3`  

### 🔄 Streaming Systems

- **Kafka** → `?format=kafka`  
- **RabbitMQ** → `?format=rabbitmq`  
- **Apache Pulsar** → `?format=pulsar`  

---

## 🛠 Installation

Install the required dependencies:

```bash
pip install -r requirements-export-app.txt
```

---

## ▶️ Usage

Start the development server:

```bash
uvicorn main:app --reload
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) to access the Swagger UI and test the `/export` endpoint.

You can upload your own database file as input (in `.json`, `.csv`, or `.txt` format)
and export it to any supported format. The conversion happens automatically.

You can also use the `/import-online-db` GET endpoint to fetch data from remote SQLite or MySQL databases.

---

## 🔐 Environment Variables

Set the following environment variables depending on your export target:

### AWS S3

```env
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_S3_BUCKET=...
AWS_S3_OBJECT_KEY=...
```

### MySQL

```env
MYSQL_HOST=...
MYSQL_USER=...
MYSQL_PASSWORD=...
MYSQL_DATABASE=...
```

### Kafka

```env
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC=exported_data
```

### RabbitMQ

```env
RABBITMQ_HOST=localhost
RABBITMQ_QUEUE=export_queue
```

### Pulsar

```env
PULSAR_SERVICE_URL=pulsar://localhost:6650
PULSAR_TOPIC=exported_data
```

---

## 🧰 Tech Stack

- **FastAPI**, **Uvicorn**
- **Pandas**, **XlsxWriter**, **ReportLab**
- **PyArrow**, **FastAvro**
- **MySQL Connector**, **Boto3**, **Kafka-Python**
- **Pika**, **Pulsar-Client**

See [`requirements-export-app.txt`](./requirements-export-app.txt) for full details.

---

### Export app changed files vs. FastAPI

```
├── /fastapi                              # Official FastAPI root directory
│   ├── /export_app                       # Our "export app" files package
│   │   ├── main.py                       # export app main module
│   │   ├── README.md                     # our export app readme doc
│   │   ├── requirements-export-app.md    # our export app modules run requirements
│   │   └── test_export_app.py            # Export app pytest
│   ├── /docs                             # FastAPI docs
│   │   ├── index.md                      # Export app index doc
│   │   └── /usage
│   │       └── export.md                 # Export app markdown (for endpoint usage)
│   └── /.github
│       └── /workflows
│           └── test-export-app.yml       # Export app test workflow
├── mkdocs-export.yml                     # Export app makedocs YAML
└── requirements*.py                      # FastAPI official run requirements
```

---

## 📄 License

MIT License – for educational and contribution purposes.
