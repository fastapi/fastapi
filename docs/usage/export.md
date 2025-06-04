
# Export & Import Endpoint Usage

## `/export` (POST)

Upload a `.txt`, `.csv`, or `.json` file and export it to your desired format.

### Query Parameters
- `format`: Choose from one of the supported export formats:  
  `json`, `csv`, `excel`, `pdf`, `parquet`, `avro`, `feather`, `orc`, `mysql`, `sqlite`, `s3`, `kafka`, `rabbitmq`, `pulsar`

### Example (via Swagger UI)
1. Click `/export`
2. Upload a file (e.g. `.csv`)
3. Select format: `excel`
4. Click **Execute**

---

## `/import-online-db` (GET)

Import data directly from a remote **SQLite** or **MySQL** database.

### Query Parameters:
- `db_type`: `sqlite` or `mysql`
- If using `sqlite`:
  - `url`: Full path to `.db` file
  - `table`: Table name to fetch
- If using `mysql`:
  - `host`, `user`, `password`, `database`, `table`: Required MySQL credentials

### Example:
```http
GET /import-online-db?db_type=mysql&host=example.com&user=admin&password=1234&database=testdb&table=users
```

---

> 💡 Use Swagger UI to interactively test both endpoints at `/docs`.
