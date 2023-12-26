# Full Stack FastAPI and PostgreSQL - Frontend

## Generate Client

- Start the Docker Compose stack.
- Download the OpenAPI JSON file from `http://localhost/api/v1/openapi.json` and copy it to a new file `openapi.json` next to the `package.json` file.
- To simplify the names in the generated frontend client code, modifying the `openapi.json` file, run:

```bash
node modify-openapi-operationids.js
```

- To generate or update the frontend client, run:

```bash
npm run generate-client
```
