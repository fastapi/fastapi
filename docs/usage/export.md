# Export Endpoint Usage

## `/export?format=...`

The `/export` endpoint supports exporting to various formats using a query parameter `format`.

### Available formats:

- `json`
- `csv`
- `excel`
- `pdf`
- `parquet`
- `avro`
- `feather`
- `orc`
- `mysql`
- `sqlite`
- `s3`
- `kafka`
- `rabbitmq`
- `pulsar`

### Example

```http
GET /export?format=csv
```

This returns a CSV download of the exported data.

---

> 💡 Tip: You can test the endpoint interactively in the Swagger UI at `/docs`.


## Code Documentation

::: export_app.main
    options:
      members:
        - export_data
        - export_to_csv
        - export_to_excel
        - export_to_pdf
        - export_to_avro
        - export_to_feather
        - export_to_orc
        - export_to_sqlite
        - export_to_mysql
        - export_to_s3
        - export_to_kafka
        - export_to_rabbitmq
        - export_to_pulsar
