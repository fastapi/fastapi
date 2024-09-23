#! /usr/bin/env bash

set -e
set -x

cd backend
python -c "import app.main; import json; print(json.dumps(app.main.app.openapi()))" > ../openapi.json
cd ..
node frontend/modify-openapi-operationids.js
mv openapi.json frontend/
cd frontend
npm run generate-client
npx biome format --write ./src/client
