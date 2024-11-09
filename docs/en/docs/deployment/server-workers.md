# Server Workers - Uvicorn with Workers

Let's check back those deployment concepts from before:

* Security - HTTPS
* Running on startup
* Restarts
* **Replication (the number of processes running)**
* Memory
* Previous steps before starting

Up to this point, with all the tutorials in the docs, you have probably been running a **server program**, for example, using the `fastapi` command, that runs Uvicorn, running a **single process**.

When deploying applications you will probably want to have some **replication of processes** to take advantage of **multiple cores** and to be able to handle more requests.

As you saw in the previous chapter about [Deployment Concepts](concepts.md){.internal-link target=_blank}, there are multiple strategies you can use.

Here I'll show you how to use **Uvicorn** with **worker processes** using the `fastapi` command or the `uvicorn` command directly.

/// info

If you are using containers, for example with Docker or Kubernetes, I'll tell you more about that in the next chapter: [FastAPI in Containers - Docker](docker.md){.internal-link target=_blank}.

In particular, when running on **Kubernetes** you will probably **not** want to use workers and instead run **a single Uvicorn process per container**, but I'll tell you about it later in that chapter.

///

## Multiple Workers

You can start multiple workers with the `--workers` command line option:

//// tab | `fastapi`

If you use the `fastapi` command:

<div class="termy">

```console
$ <pre> <font color="#4E9A06">fastapi</font> run --workers 4 <u style="text-decoration-style:single">main.py</u>
<font color="#3465A4">INFO    </font> Using path <font color="#3465A4">main.py</font>
<font color="#3465A4">INFO    </font> Resolved absolute path <font color="#75507B">/home/user/code/awesomeapp/</font><font color="#AD7FA8">main.py</font>
<font color="#3465A4">INFO    </font> Searching for package file structure from directories with <font color="#3465A4">__init__.py</font> files
<font color="#3465A4">INFO    </font> Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

 ╭─ <font color="#8AE234"><b>Python module file</b></font> ─╮
 │                      │
 │  🐍 main.py          │
 │                      │
 ╰──────────────────────╯

<font color="#3465A4">INFO    </font> Importing module <font color="#4E9A06">main</font>
<font color="#3465A4">INFO    </font> Found importable FastAPI app

 ╭─ <font color="#8AE234"><b>Importable FastAPI app</b></font> ─╮
 │                          │
 │  <span style="background-color:#272822"><font color="#FF4689">from</font></span><span style="background-color:#272822"><font color="#F8F8F2"> main </font></span><span style="background-color:#272822"><font color="#FF4689">import</font></span><span style="background-color:#272822"><font color="#F8F8F2"> app</font></span><span style="background-color:#272822">  </span>  │
 │                          │
 ╰──────────────────────────╯

<font color="#3465A4">INFO    </font> Using import string <font color="#8AE234"><b>main:app</b></font>

 <font color="#4E9A06">╭─────────── FastAPI CLI - Production mode ───────────╮</font>
 <font color="#4E9A06">│                                                     │</font>
 <font color="#4E9A06">│  Serving at: http://0.0.0.0:8000                    │</font>
 <font color="#4E9A06">│                                                     │</font>
 <font color="#4E9A06">│  API docs: http://0.0.0.0:8000/docs                 │</font>
 <font color="#4E9A06">│                                                     │</font>
 <font color="#4E9A06">│  Running in production mode, for development use:   │</font>
 <font color="#4E9A06">│                                                     │</font>
 <font color="#4E9A06">│  </font><font color="#8AE234"><b>fastapi dev</b></font><font color="#4E9A06">                                        │</font>
 <font color="#4E9A06">│                                                     │</font>
 <font color="#4E9A06">╰─────────────────────────────────────────────────────╯</font>

<font color="#4E9A06">INFO</font>:     Uvicorn running on <b>http://0.0.0.0:8000</b> (Press CTRL+C to quit)
<font color="#4E9A06">INFO</font>:     Started parent process [<font color="#34E2E2"><b>27365</b></font>]
<font color="#4E9A06">INFO</font>:     Started server process [<font color="#06989A">27368</font>]
<font color="#4E9A06">INFO</font>:     Waiting for application startup.
<font color="#4E9A06">INFO</font>:     Application startup complete.
<font color="#4E9A06">INFO</font>:     Started server process [<font color="#06989A">27369</font>]
<font color="#4E9A06">INFO</font>:     Waiting for application startup.
<font color="#4E9A06">INFO</font>:     Application startup complete.
<font color="#4E9A06">INFO</font>:     Started server process [<font color="#06989A">27370</font>]
<font color="#4E9A06">INFO</font>:     Waiting for application startup.
<font color="#4E9A06">INFO</font>:     Application startup complete.
<font color="#4E9A06">INFO</font>:     Started server process [<font color="#06989A">27367</font>]
<font color="#4E9A06">INFO</font>:     Waiting for application startup.
<font color="#4E9A06">INFO</font>:     Application startup complete.
</pre>
```

</div>

////

//// tab | `uvicorn`

If you prefer to use the `uvicorn` command directly:

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
<font color="#A6E22E">INFO</font>:     Uvicorn running on <b>http://0.0.0.0:8080</b> (Press CTRL+C to quit)
<font color="#A6E22E">INFO</font>:     Started parent process [<font color="#A1EFE4"><b>27365</b></font>]
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27368</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27369</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27370</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27367</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
```

</div>

////

The only new option here is `--workers` telling Uvicorn to start 4 worker processes.

You can also see that it shows the **PID** of each process, `27365` for the parent process (this is the **process manager**) and one for each worker process: `27368`, `27369`, `27370`, and `27367`.

## Deployment Concepts

Here you saw how to use multiple **workers** to **parallelize** the execution of the application, take advantage of **multiple cores** in the CPU, and be able to serve **more requests**.

From the list of deployment concepts from above, using workers would mainly help with the **replication** part, and a little bit with the **restarts**, but you still need to take care of the others:

* **Security - HTTPS**
* **Running on startup**
* ***Restarts***
* Replication (the number of processes running)
* **Memory**
* **Previous steps before starting**

## Containers and Docker

In the next chapter about [FastAPI in Containers - Docker](docker.md){.internal-link target=_blank} I'll explain some strategies you could use to handle the other **deployment concepts**.

I'll show you how to **build your own image from scratch** to run a single Uvicorn process. It is a simple process and is probably what you would want to do when using a distributed container management system like **Kubernetes**.

## Recap

You can use multiple worker processes with the `--workers` CLI option with the `fastapi` or `uvicorn` commands to take advantage of **multi-core CPUs**, to run **multiple processes in parallel**.

You could use these tools and ideas if you are setting up **your own deployment system** while taking care of the other deployment concepts yourself.

Check out the next chapter to learn about **FastAPI** with containers (e.g. Docker and Kubernetes). You will see that those tools have simple ways to solve the other **deployment concepts** as well. ✨
