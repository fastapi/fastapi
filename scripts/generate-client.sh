#! /usr/bin/env bash

PYTHONPATH=backend python -c "import app.main; import json; print(json.dumps(app.main.app.openapi()))" > openapi.json
node frontend/modify-openapi-operationids.js
mv openapi.json frontend/
cd frontend
npm run generate-client
npx biome format --write ./src/client
