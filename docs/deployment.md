You can use <a href="https://www.docker.com/" target="_blank">**Docker**</a> for deployment. It has several advantages like security, replicability, development simplicity, etc.

In this section you'll see instructions and links to guides to know how to:

* Make your **FastAPI** application a Docker image/container with maximum performance. In about **5 min**.
* (Optionally) understand what you, as a developer, need to know about HTTPS.
* Set up a Docker Swarm mode cluster with automatic HTTPS, even on a simple $5 USD/month server. In about **20 min**.
* Generate and deploy a full **FastAPI** application, using your Docker Swarm cluster, with HTTPS, etc. In about **10 min**.

---

You can also easily use **FastAPI** in a standard server directly too (without Docker).


## Docker

If you are using Docker, you can use the official Docker image:

### <a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" target="_blank">tiangolo/uvicorn-gunicorn-fastapi</a>

This image has an "auto-tuning" mechanism included, so that you can just add your code and get very high performance automatically. And without making sacrifices.

But you can still change and update all the configurations with environment variables or configuration files.

!!! tip
    To see all the configurations and options, go to the Docker image page: <a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" target="_blank">tiangolo/uvicorn-gunicorn-fastapi</a>.


### Create a `Dockerfile`

* Go to your project directory.
* Create a `Dockerfile` with:

```Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app
```

#### Bigger Applications

If you followed the section about creating <a href="https://fastapi.tiangolo.com/tutorial/bigger-applications/" target="_blank">Bigger Applications with Multiple Files
</a>, your `Dockerfile` might instead look like:

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

```bash
docker build -t myimage .
```

### Start the Docker container

* Run a container based on your image:

```bash
docker run -d --name mycontainer -p 80:80 myimage
```

Now you have an optimized FastAPI server in a Docker container. Auto-tuned for your current server (and number of CPU cores).


### Check it

You should be able to check it in your Docker container's URL, for example: <a href="http://192.168.99.100/items/5?q=somequery" target="_blank">http://192.168.99.100/items/5?q=somequery</a> or <a href="http://127.0.0.1/items/5?q=somequery" target="_blank">http://127.0.0.1/items/5?q=somequery</a> (or equivalent, using your Docker host).

You will see something like:

```JSON
{"item_id": 5, "q": "somequery"}
```


### Interactive API docs

Now you can go to <a href="http://192.168.99.100/docs" target="_blank">http://192.168.99.100/docs</a> or <a href="http://127.0.0.1/docs" target="_blank">http://127.0.0.1/docs</a> (or equivalent, using your Docker host).

You will see the automatic interactive API documentation (provided by <a href="https://github.com/swagger-api/swagger-ui" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)


### Alternative API docs

And you can also go to <a href="http://192.168.99.100/redoc" target="_blank">http://192.168.99.100/redoc</a> or <a href="http://127.0.0.1/redoc" target="_blank">http://127.0.0.1/redoc</a> (or equivalent, using your Docker host).

You will see the alternative automatic documentation (provided by <a href="https://github.com/Rebilly/ReDoc" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)


## HTTPS

### About HTTPS

It is easy to assume that HTTPS is something that is just "enabled" or not.

But it is way more complex than that.

!!! tip
    If you are in a hurry or don't care, continue with the next section for step by step instructions to set everything up.

To learn the basics of HTTPS, from a consumer perspective, check <a href="https://howhttps.works/" target="_blank">https://howhttps.works/</a>.

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
* The HTTPS certificates "certificate" a certain domain, but the protocol and encryption happen at the TCP level, before knowing which domain is being dealt with.
* By default, that would mean that you can only have one HTTPS certificate per IP address.
    * No matter how big is your server and how small each application you have there might be. But...
* There's an extension to the TLS protocol (the one handling the encryption at the TCP level, before HTTP) called <a href="https://en.wikipedia.org/wiki/Server_Name_Indication" target="_blank"><abbr title="Server Name Indication">SNI</abbr></a>.
    * This SNI extension allows one single server (with a single IP address) to have several HTTPS certificates and server multiple HTTPS domains/applications.
    * For this to work, a single component (program) running in the server, listening in the public IP address, must have all the HTTPS certificates in the server.
* After having a secure connection, the communication protocol is the same HTTP.
    * It goes encrypted, but the encrypted contents are the same HTTP protocol.


It is a common practice to have one program/HTTP server running in the server (the machine, host, etc) and managing all the HTTPS parts, sending the decrypted HTTP requests to the actual HTTP application running in the same server (the **FastAPI** application, in this case), take the HTTP response from the application, encrypt it using the appropriate certificate and sending it back to the client using HTTPS. This server is ofter called a <a href="https://en.wikipedia.org/wiki/TLS_termination_proxy" target="_blank">TLS Termination Proxy</a>.


### Let's Encrypt

Up to some years ago, these HTTPS certificates were sold by trusted third-parties.

The process to acquire one of these certificates used to be cumbersome, require quite some paperwork and the certificates were quite expensive.

But then <a href="https://letsencrypt.org/" target="_blank">Let's Encrypt</a> was created.

It is a project from the Linux Foundation. It provides HTTPS certificates for free. In an automated way. These certificates use all the standard cryptographic security, and are short lived (about 3 months), so, the security is actually increased, by reducing their lifespan.

The domain's are securely verified and the certificates are generated automatically. This also allows automatizing the renewal of these certificates.

The idea is to automatize the acquisition and renewal of these certificates, so that you can have secure HTTPS, free, forever.


### Traefik

<a href="https://traefik.io/" target="_blank">Traefik</a> is a high performance reverse proxy / load balancer. It can do the "TLS Termination Proxy" job (apart from other features).

It has integration with Let's Encrypt. So, it can handle all the HTTPS parts, including certificate acquisition and renewal.

It also has integrations with Docker. So, you can declare your domains in each application configurations and have it read those configurations, generate the HTTPS certificates and serve HTTPS to your application, all automatically. Without requiring any change in its configuration.

---

With this information and tools, continue with the next section to combine everything.


## Docker Swarm mode cluster with Traefik and HTTPS

You can have a Docker Swarm mode cluster set up in minutes (about 20 min) with a main Traefik handling HTTPS (including certificate acquisition and renewal).

By using Docker Swarm mode, you can start with a "cluster" of a single machine (it can even be a $5 USD / month server) and then you can grow as much as you need adding more servers.

To set up a Docker Swarm Mode cluster with Traefik and HTTPS handling, follow this guide:

### <a href="https://medium.com/@tiangolo/docker-swarm-mode-and-traefik-for-a-https-cluster-20328dba6232" target="_blank">Docker Swarm Mode and Traefik for an HTTPS cluster</a>.


### Deploy a FastAPI application

The easiest way to set everything up, would be using the <a href="/project-generation/" target="_blank">FastAPI project generator</a>.

It is designed to be integrated with this Docker Swarm cluster with Traefik and HTTPS described above.

You can generate a project in about 2 min.

The generated project has instructions to deploy it, doing it takes other 2 min.


## Alternatively, deploy **FastAPI** without Docker

You can deploy **FastAPI** directly without Docker too.

You just need to install an ASGI compatible server like:

* <a href="https://www.uvicorn.org/" target="_blank">Uvicorn</a>, a lightning-fast ASGI server, built on uvloop and httptools.

```bash
pip install uvicorn
```

* <a href="https://gitlab.com/pgjones/hypercorn" target="_blank">Hypercorn</a>, an ASGI server also compatible with HTTP/2.

```bash
pip install hypercorn
```

...or any other ASGI server.

And run your application the same way you have done in the tutorials, but without the `--reload` option, e.g.:

```bash
uvicorn main:app --host 0.0.0.0 --port 80
```

or with Hypercorn:

```bash
hypercorn main:app --bind 0.0.0.0:80
```

You might want to set up some tooling to make sure it is restarted automatically if it stops.

You might also want to install <a href="https://gunicorn.org/" target="_blank">Gunicorn</a> and <a href="https://www.uvicorn.org/#running-with-gunicorn" target="_blank">use it as a manager for Uvicorn</a>, or use Hypercorn with multiple workers.

Making sure to fine-tune the number of workers, etc.

But if you are doing all that, you might just use the Docker image that does it automatically.
