# Deploy with Docker

In this section you'll see instructions and links to guides to know how to:

* Make your **FastAPI** application a Docker image/container with maximum performance. In about **5 min**.
* (Optionally) understand what you, as a developer, need to know about HTTPS.
* Set up a Docker Swarm mode cluster with automatic HTTPS, even on a simple $5 USD/month server. In about **20 min**.
* Generate and deploy a full **FastAPI** application, using your Docker Swarm cluster, with HTTPS, etc. In about **10 min**.

You can use <a href="https://www.docker.com/" class="external-link" target="_blank">**Docker**</a> for deployment. It has several advantages like security, replicability, development simplicity, etc.

If you are using Docker, you can use the official Docker image:

## <a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" class="external-link" target="_blank">tiangolo/uvicorn-gunicorn-fastapi</a>

This image has an "auto-tuning" mechanism included, so that you can just add your code and get very high performance automatically. And without making sacrifices.

But you can still change and update all the configurations with environment variables or configuration files.

!!! tip
    To see all the configurations and options, go to the Docker image page: <a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" class="external-link" target="_blank">tiangolo/uvicorn-gunicorn-fastapi</a>.

## Create a `Dockerfile`

* Go to your project directory.
* Create a `Dockerfile` with:

```Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app
```

### Bigger Applications

If you followed the section about creating [Bigger Applications with Multiple Files](../tutorial/bigger-applications.md){.internal-link target=_blank}, your `Dockerfile` might instead look like:

```Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app/app
```

### Raspberry Pi and other architectures

If you are running Docker in a Raspberry Pi (that has an ARM processor) or any other architecture, you can create a `Dockerfile` from scratch, based on a Python base image (that is multi-architecture) and use Uvicorn alone.

In this case, your `Dockerfile` could look like:

```Dockerfile
FROM python:3.7

RUN pip install fastapi uvicorn

EXPOSE 80

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

## Create the **FastAPI** Code

* Create an `app` directory and enter in it.
* Create a `main.py` file with:

```Python
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

* You should now have a directory structure like:

```
.
├── app
│   └── main.py
└── Dockerfile
```

## Build the Docker image

* Go to the project directory (in where your `Dockerfile` is, containing your `app` directory).
* Build your FastAPI image:

<div class="termy">

```console
$ docker build -t myimage .

---> 100%
```

</div>

## Start the Docker container

* Run a container based on your image:

<div class="termy">

```console
$ docker run -d --name mycontainer -p 80:80 myimage
```

</div>

Now you have an optimized FastAPI server in a Docker container. Auto-tuned for your current server (and number of CPU cores).

## Check it

You should be able to check it in your Docker container's URL, for example: <a href="http://192.168.99.100/items/5?q=somequery" class="external-link" target="_blank">http://192.168.99.100/items/5?q=somequery</a> or <a href="http://127.0.0.1/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1/items/5?q=somequery</a> (or equivalent, using your Docker host).

You will see something like:

```JSON
{"item_id": 5, "q": "somequery"}
```

## Interactive API docs

Now you can go to <a href="http://192.168.99.100/docs" class="external-link" target="_blank">http://192.168.99.100/docs</a> or <a href="http://127.0.0.1/docs" class="external-link" target="_blank">http://127.0.0.1/docs</a> (or equivalent, using your Docker host).

You will see the automatic interactive API documentation (provided by <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

## Alternative API docs

And you can also go to <a href="http://192.168.99.100/redoc" class="external-link" target="_blank">http://192.168.99.100/redoc</a> or <a href="http://127.0.0.1/redoc" class="external-link" target="_blank">http://127.0.0.1/redoc</a> (or equivalent, using your Docker host).

You will see the alternative automatic documentation (provided by <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Traefik

<a href="https://traefik.io/" class="external-link" target="_blank">Traefik</a> is a high performance reverse proxy / load balancer. It can do the "TLS Termination Proxy" job (apart from other features).

It has integration with Let's Encrypt. So, it can handle all the HTTPS parts, including certificate acquisition and renewal.

It also has integrations with Docker. So, you can declare your domains in each application configurations and have it read those configurations, generate the HTTPS certificates and serve HTTPS to your application automatically, without requiring any change in its configuration.

---

With this information and tools, continue with the next section to combine everything.

## Docker Swarm mode cluster with Traefik and HTTPS

You can have a Docker Swarm mode cluster set up in minutes (about 20 min) with a main Traefik handling HTTPS (including certificate acquisition and renewal).

By using Docker Swarm mode, you can start with a "cluster" of a single machine (it can even be a $5 USD / month server) and then you can grow as much as you need adding more servers.

To set up a Docker Swarm Mode cluster with Traefik and HTTPS handling, follow this guide:

### <a href="https://medium.com/@tiangolo/docker-swarm-mode-and-traefik-for-a-https-cluster-20328dba6232" class="external-link" target="_blank">Docker Swarm Mode and Traefik for an HTTPS cluster</a>

### Deploy a FastAPI application

The easiest way to set everything up, would be using the [**FastAPI** Project Generators](../project-generation.md){.internal-link target=_blank}.

It is designed to be integrated with this Docker Swarm cluster with Traefik and HTTPS described above.

You can generate a project in about 2 min.

The generated project has instructions to deploy it, doing it takes another 2 min.
