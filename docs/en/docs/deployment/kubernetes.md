# FastAPI in Kubernetes - Liveness and Readiness Probes { #fastapi-in-kubernetes-liveness-and-readiness-probes }

When deploying a **FastAPI** application to **Kubernetes** or similar container orchestration systems (like AWS ECS, Nomad, or others), you will probably want to configure **Probes** (health checks) to monitor the status of your containers.

These systems use probes to know if a container is running, if it is ready to receive requests, or if it has crashed and needs to be restarted.

---

## Types of Probes { #types-of-probes }

Kubernetes has three main types of probes:

* **Startup Probe**: Determines if the application within the container has started up. All other probes (liveness and readiness) are disabled until the startup probe succeeds.
* **Liveness Probe**: Determines if the container needs to be restarted. For example, if your app is stuck or in a deadlocked state and cannot respond, the liveness probe will fail, and Kubernetes will restart the container.
* **Readiness Probe**: Determines if a container is ready to accept traffic. If the readiness probe fails, the load balancer stops sending requests to this container (for example, while it is initializing database connections or loading a machine learning model).

---

## FastAPI Lifespan and Probes { #fastapi-lifespan-and-probes }

When you start a **FastAPI** application, you might have some startup code (like connecting to a database) defined in your [Lifespan events](../advanced/events.md).

FastAPI will **not** start accepting incoming HTTP requests until the lifespan startup code has completed.

Because of this:
* Your **Startup Probe** and **Readiness Probe** should wait until the app is fully started.
* If your database connection or initialization takes a long time, the orchestrator might think the container failed and restart it. You should configure the probe parameters (`initialDelaySeconds`, `failureThreshold`, etc.) to give the application enough time to complete its startup, or use a **Startup Probe** specifically designed for this.

---

## Defining Probe Endpoints in FastAPI { #defining-probe-endpoints-in-fastapi }

To configure HTTP probes, you can create simple endpoints in your FastAPI application that return a success status code (like `200 OK`).

Here is a basic example:

{* ../../docs_src/kubernetes/tutorial001.py *}

In this case:
* The `/healthz` endpoint serves as the URL that the Kubernetes probes will request.
* If it returns a standard `200 OK` status code, Kubernetes will know the container is healthy.

---

## Filtering Probe Logs (Avoiding Log Spam) { #filtering-probe-logs-avoiding-log-spam }

A common issue when deploying web APIs with probes is **log spam**. Since Kubernetes requests these endpoints very frequently (e.g., every 5 or 10 seconds), your server logs (like Uvicorn access logs) can quickly get filled with these repetitive health check requests.

To avoid this, you can write a custom `logging.Filter` to exclude requests matching your probe endpoints from the console logs.

Here is a more complete example with:
* Lifespan startup/cleanup logic.
* A custom filter to remove probe requests from Uvicorn access logs.
* Separate `/healthz` (liveness) and `/readyz` (readiness) endpoints.

{* ../../docs_src/kubernetes/tutorial002.py *}

### How the Log Filter Works { #how-the-log-filter-works }

* The `EndpointFilter` subclass overrides the `filter` method.
* It checks if the logged request path contains one of our probe endpoints (`/healthz`, `/readyz`, or `/livez`).
* If it matches, the filter returns `False`, which prevents that log record from being printed.
* Otherwise, it returns `True`, allowing the log record to pass through as usual.
* We apply this filter to the `"uvicorn.access"` logger, which is responsible for printing HTTP request logs.

---

## Kubernetes Configuration Example { #kubernetes-configuration-example }

Here is an example of how you would configure these probes in your Kubernetes deployment manifest (YAML):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fastapi-app
  template:
    metadata:
      labels:
        app: fastapi-app
    spec:
      containers:
      - name: fastapi-container
        image: my-fastapi-app-image:latest
        ports:
        - containerPort: 8000

        # 1. Startup Probe: Wait for database migration or model loading
        startupProbe:
          httpGet:
            path: /healthz
            port: 8000
          # Allow up to 30 seconds for startup (6 * 5s)
          failureThreshold: 6
          periodSeconds: 5

        # 2. Liveness Probe: Check if the application is still responding
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8000
          periodSeconds: 10

        # 3. Readiness Probe: Check if ready to receive customer traffic
        readinessProbe:
          httpGet:
            path: /readyz
            port: 8000
          periodSeconds: 10
```

By configuring these probes, your FastAPI application will run with high availability and seamless rolling updates in Kubernetes. 🚀
