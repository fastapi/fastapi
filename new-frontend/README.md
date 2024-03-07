# FastAPI Project - Frontend

## Frontend development

* Enter the `frontend` directory, install the NPM packages and start the live server using the `npm` scripts:

```bash
cd frontend
npm install
npm run dev
```

Then open your browser at http://localhost:5173/.

Notice that this live server is not running inside Docker, it is for local development, and that is the recommended workflow. Once you are happy with your frontend, you can build the frontend Docker image and start it, to test it in a production-like environment. But compiling the image at every change will not be as productive as running the local development server with live reload.

Check the file `package.json` to see other available options.

### Removing the frontend

If you are developing an API-only app and want to remove the frontend, you can do it easily:

* Remove the `./frontend` directory.
* In the `docker-compose.yml` file, remove the whole service / section `frontend`.
* In the `docker-compose.override.yml` file, remove the whole service / section `frontend`.

Done, you have a frontend-less (api-only) app. 🤓

---

If you want, you can also remove the `FRONTEND` environment variables from:

* `.env`
* `./scripts/*.sh`

But it would be only to clean them up, leaving them won't really have any effect either way.

## Generate Client

* Start the Docker Compose stack.
* Download the OpenAPI JSON file from `http://localhost/api/v1/openapi.json` and copy it to a new file `openapi.json` next to the `package.json` file.
* To simplify the names in the generated frontend client code, modifying the `openapi.json` file, run:

```bash
node modify-openapi-operationids.js
```

* To generate or update the frontend client, run:

```bash
npm run generate-client
```
