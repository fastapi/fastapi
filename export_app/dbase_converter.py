# FastAPI dbase conversion by Joanna Karitsioti & George Tsakalos

import csv
import json
from typing import List, Dict
from fastapi import UploadFile



async def convert_to_json(uploaded_file: UploadFile) -> List[Dict]:
    content = await uploaded_file.read()
    filename = uploaded_file.filename.lower()

    if filename.endswith('.json'):
        return json.loads(content.decode())

    elif filename.endswith('.csv'):
        decoded = content.decode()
        reader = csv.DictReader(decoded.splitlines(), delimiter=';')
        return [row for row in reader]

    elif filename.endswith('.txt'):
        decoded = content.decode()
        lines = decoded.strip().splitlines()
        result = []
        for line in lines:
            if ',' in line:
                name, age = [item.strip() for item in line.split(',')]
                result.append({'name': name, 'age': int(age)})
        return result

    else:
        raise ValueError("Unsupported file format. Use .json, .csv or .txt")



def fetch_from_sqlite(url: str, table: str) -> List[Dict]:
    import sqlite3
    try:
        conn = sqlite3.connect(url)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return results
    except Exception as e:
        raise ValueError(f"SQLite fetch error: {str(e)}")



def fetch_from_mysql(
    host: str,
    user: str,
    password: str,
    database: str,
    table: str
) -> List[Dict]:
    import mysql.connector
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return results
    except Exception as e:
        raise ValueError(f"MySQL fetch error: {str(e)}")
