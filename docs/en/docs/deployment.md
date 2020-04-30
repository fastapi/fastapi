# Deployment

Deploying a **FastAPI** application is relatively easy.

There are several ways to do it depending on your specific use case and the tools that you use.

You will see more about some of the ways to do it in the next sections.

## FastAPI versions

**FastAPI** is already being used in production in many applications and systems. And the test coverage is kept at 100%. But its development is still moving quickly.

New features are added frequently, bugs are fixed regularly, and the code is still continuously improving.

That's why the current versions are still `0.x.x`, this reflects that each version could potentially have breaking changes. This follows the <a href="https://semver.org/" class="external-link" target="_blank">Semantic Versioning</a> conventions.

You can create production applications with **FastAPI** right now (and you have probably been doing it for some time), you just have to make sure that you use a version that works correctly with the rest of your code.

### Pin your `fastapi` version

The first thing you should do is to "pin" the version of **FastAPI** you are using to the specific latest version that you know works correctly for your application.

For example, let's say you are using version `0.45.0` in your app.

If you use a `requirements.txt` file you could specify the version with:

```txt
fastapi==0.45.0
```

that would mean that you would use exactly the version `0.45.0`.

Or you could also pin it with:

```txt
fastapi>=0.45.0,<0.46.0
```

that would mean that you would use the versions `0.45.0` or above, but less than `0.46.0`, for example, a version `0.45.2` would still be accepted.

If you use any other tool to manage your installations, like Poetry, Pipenv, or others, they all have a way that you can use to define specific versions for your packages.

### Available versions

You can see the available versions (e.g. to check what is the current latest) in the [Release Notes](release-notes.md){.internal-link target=_blank}.

### About versions

Following the Semantic Versioning conventions, any version below `1.0.0` could potentially add breaking changes.

FastAPI also follows the convention that any "PATCH" version change is for bug fixes and non-breaking changes.

!!! tip
    The "PATCH" is the last number, for example, in `0.2.3`, the PATCH version is `3`.

So, you should be able to pin to a version like:

```txt
fastapi>=0.45.0,<0.46.0
```

Breaking changes and new features are added in "MINOR" versions.

!!! tip
    The "MINOR" is the number in the middle, for example, in `0.2.3`, the MINOR version is `2`.

### Upgrading the FastAPI versions

You should add tests for your app.

With **FastAPI** it's very easy (thanks to Starlette), check the docs: [Testing](tutorial/testing.md){.internal-link target=_blank}

After you have tests, then you can upgrade the **FastAPI** version to a more recent one, and make sure that all your code is working correctly by running your tests.

If everything is working, or after you make the necessary changes, and all your tests are passing, then you can pin your `fastapi` to that new recent version.

### About Starlette

You shouldn't pin the version of `starlette`.

Different versions of **FastAPI** will use a specific newer version of Starlette.

So, you can just let **FastAPI** use the correct Starlette version.

### About Pydantic

Pydantic includes the tests for **FastAPI** with its own tests, so new versions of Pydantic (above `1.0.0`) are always compatible with FastAPI.

You can pin Pydantic to any version above `1.0.0` that works for you and below `2.0.0`.

For example:

```txt
pydantic>=1.2.0,<2.0.0
```

## Docker

In this section you'll see instructions and links to guides to know how to:

* Make your **FastAPI** application a Docker image/container with maximum performance. In about **5 min**.
* (Optionally) understand what you, as a developer, need to know about HTTPS.
* Set up a Docker Swarm mode cluster with automatic HTTPS, even on a simple $5 USD/month server. In about **20 min**.
* Generate and deploy a full **FastAPI** application, using your Docker Swarm cluster, with HTTPS, etc. In about **10 min**.

You can use <a href="https://www.docker.com/" class="external-link" target="_blank">**Docker**</a> for deployment. It has several advantages like security, replicability, development simplicity, etc.

If you are using Docker, you can use the official Docker image:

### <a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" class="external-link" target="_blank">tiangolo/uvicorn-gunicorn-fastapi</a>

This image has an "auto-tuning" mechanism included, so that you can just add your code and get very high performance automatically. And without making sacrifices.

But you can still change and update all the configurations with environment variables or configuration files.

!!! tip
    To see all the configurations and options, go to the Docker image page: <a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" class="external-link" target="_blank">tiangolo/uvicorn-gunicorn-fastapi</a>.

### Create a `Dockerfile`

* Go to your project directory.
* Create a `Dockerfile` with:

```Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app
```

#### Bigger Applications

If you followed the section about creating [Bigger Applications with Multiple Files](tutorial/bigger-applications.md){.internal-link target=_blank}, your `Dockerfile` might instead look like:

```Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app/app
```

#### Raspberry Pi and other architectures

If you are running Docker in a Raspberry Pi (that has an ARM processor) or any other architecture, you can create a `Dockerfile` from scratch, based on a Python base image (that is multi-architecture) and use Uvicorn alone.

In this case, your `Dockerfile` could look like:

```Dockerfile
FROM python:3.7

RUN pip install fastapi uvicorn

EXPOSE 80

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

### Create the **FastAPI** Code

* Create an `app` directory and enter in it.
* Create a `main.py` file with:

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

* You should now have a directory structure like:

```
.
├── app
│   └── main.py
└── Dockerfile
```

### Build the Docker image

* Go to the project directory (in where your `Dockerfile` is, containing your `app` directory).
* Build your FastAPI image:

<div class="termy">

```console
$ docker build -t myimage .

---> 100%
```

</div>

### Start the Docker container

* Run a container based on your image:

<div class="termy">

```console
$ docker run -d --name mycontainer -p 80:80 myimage
```

</div>

Now you have an optimized FastAPI server in a Docker container. Auto-tuned for your current server (and number of CPU cores).

### Check it

You should be able to check it in your Docker container's URL, for example: <a href="http://192.168.99.100/items/5?q=somequery" class="external-link" target="_blank">http://192.168.99.100/items/5?q=somequery</a> or <a href="http://127.0.0.1/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1/items/5?q=somequery</a> (or equivalent, using your Docker host).

You will see something like:

```JSON
{"item_id": 5, "q": "somequery"}
```

### Interactive API docs

Now you can go to <a href="http://192.168.99.100/docs" class="external-link" target="_blank">http://192.168.99.100/docs</a> or <a href="http://127.0.0.1/docs" class="external-link" target="_blank">http://127.0.0.1/docs</a> (or equivalent, using your Docker host).

You will see the automatic interactive API documentation (provided by <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternative API docs

And you can also go to <a href="http://192.168.99.100/redoc" class="external-link" target="_blank">http://192.168.99.100/redoc</a> or <a href="http://127.0.0.1/redoc" class="external-link" target="_blank">http://127.0.0.1/redoc</a> (or equivalent, using your Docker host).

You will see the alternative automatic documentation (provided by <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## HTTPS

### About HTTPS

It is easy to assume that HTTPS is something that is just "enabled" or not.

But it is way more complex than that.

!!! tip
    If you are in a hurry or don't care, continue with the next section for step by step instructions to set everything up.

To learn the basics of HTTPS, from a consumer perspective, check <a href="https://howhttps.works/" class="external-link" target="_blank">https://howhttps.works/</a>.

Now, from a developer's perspective, here are several things to have in mind while thinking about HTTPS:

* For HTTPS, the server needs to have "certificates" generated by a third party.
    * Those certificates are actually acquired from the third-party, not "generated".
* Certificates have a lifetime.
    * They expire.
    * And then they need to be renewed, acquired again from the third party.
* The encryption of the connection happens at the TCP level.
    * That's one layer below HTTP.
    * So, the certificate and encryption handling is done before HTTP.
* TCP doesn't know about "domains". Only about IP addresses.
    * The information about the specific domain requested goes in the HTTP data.
* The HTTPS certificates "certify" a certain domain, but the protocol and encryption happen at the TCP level, before knowing which domain is being dealt with.
* By default, that would mean that you can only have one HTTPS certificate per IP address.
    * No matter how big your server is or how small each application you have on it might be.
    * There is a solution to this, however.
* There's an extension to the TLS protocol (the one handling the encryption at the TCP level, before HTTP) called <a href="https://en.wikipedia.org/wiki/Server_Name_Indication" class="external-link" target="_blank"><abbr title="Server Name Indication">SNI</abbr></a>.
    * This SNI extension allows one single server (with a single IP address) to have several HTTPS certificates and serve multiple HTTPS domains/applications.
    * For this to work, a single component (program) running on the server, listening on the public IP address, must have all the HTTPS certificates in the server.
* After obtaining a secure connection, the communication protocol is still HTTP.
    * The contents are encrypted, even though they are being sent with the HTTP protocol.

It is a common practice to have one program/HTTP server running on the server (the machine, host, etc.) and managing all the HTTPS parts : sending the decrypted HTTP requests to the actual HTTP application running in the same server (the **FastAPI** application, in this case), take the HTTP response from the application, encrypt it using the appropriate certificate and sending it back to the client using HTTPS. This server is often called a <a href="https://en.wikipedia.org/wiki/TLS_termination_proxy" class="external-link" target="_blank">TLS Termination Proxy</a>.

### Let's Encrypt

Before Let's Encrypt, these HTTPS certificates were sold by trusted third-parties.

The process to acquire one of these certificates used to be cumbersome, require quite some paperwork and the certificates were quite expensive.

But then <a href="https://letsencrypt.org/" class="external-link" target="_blank">Let's Encrypt</a> was created.

It is a project from the Linux Foundation. It provides HTTPS certificates for free. In an automated way. These certificates use all the standard cryptographic security, and are short lived (about 3 months), so the security is actually better because of their reduced lifespan.

The domains are securely verified and the certificates are generated automatically. This also allows automating the renewal of these certificates.

The idea is to automate the acquisition and renewal of these certificates, so that you can have secure HTTPS, for free, forever.

### Traefik

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

The easiest way to set everything up, would be using the [**FastAPI** Project Generators](project-generation.md){.internal-link target=_blank}.

It is designed to be integrated with this Docker Swarm cluster with Traefik and HTTPS described above.

You can generate a project in about 2 min.

The generated project has instructions to deploy it, doing it takes another 2 min.

## Alternatively, deploy **FastAPI** without Docker

You can deploy **FastAPI** directly without Docker too.

You just need to install an ASGI compatible server like:

=== "Uvicorn"

    * <a href="https://www.uvicorn.org/" class="external-link" target="_blank">Uvicorn</a>, a lightning-fast ASGI server, built on uvloop and httptools.

    <div class="termy">

    ```console
    $ pip install uvicorn

    ---> 100%
    ```

    </div>

=== "Hypercorn"

    * <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>, an ASGI server also compatible with HTTP/2.

    <div class="termy">

    ```console
    $ pip install hypercorn

    ---> 100%
    ```

    </div>

    ...or any other ASGI server.

And run your application the same way you have done in the tutorials, but without the `--reload` option, e.g.:

=== "Uvicorn"

    <div class="termy">

    ```console
    $ uvicorn main:app --host 0.0.0.0 --port 80

    <span style="color: green;">INFO</span>:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
    ```

    </div>

=== "Hypercorn"

    <div class="termy">

    ```console
    $ hypercorn main:app --bind 0.0.0.0:80

    Running on 0.0.0.0:8080 over http (CTRL + C to quit)
    ```

    </div>

You might want to set up some tooling to make sure it is restarted automatically if it stops.

You might also want to install <a href="https://gunicorn.org/" class="external-link" target="_blank">Gunicorn</a> and <a href="https://www.uvicorn.org/#running-with-gunicorn" class="external-link" target="_blank">use it as a manager for Uvicorn</a>, or use Hypercorn with multiple workers.

Making sure to fine-tune the number of workers, etc.

But if you are doing all that, you might just use the Docker image that does it automatically.
