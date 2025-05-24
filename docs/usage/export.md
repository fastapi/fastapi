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
- `sqlite`
- `mysql`
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
