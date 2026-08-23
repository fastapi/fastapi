# Kubernetes Probes - Liveness, Readiness, and Startup { #kubernetes-probes-liveness-readiness-and-startup }

When deploying a **FastAPI** application to **Kubernetes** (or other container orchestrators like Nomad, Docker Swarm, or AWS ECS), the orchestrator needs to know the **health and state** of your application containers.

Kubernetes uses **Probes** (health checks) to automate lifecycle tasks like restarting failed containers or routing incoming traffic only to instances that are ready to serve requests. 🚀

---

## The Three Types of Kubernetes Probes { #the-three-types-of-kubernetes-probes }

Kubernetes supports three main probe types:

1. **Liveness Probe (`livenessProbe`)**:
    * **Purpose**: Checks if the container process is still running and able to process HTTP requests (i.e., the Python event loop is alive and not deadlocked).
    * **Action on Failure**: Kubernetes **kills and restarts** the container.
    * **Golden Rule**: Keep it minimal and fast. **Do not** check external dependencies (databases, third-party APIs, queues) here!

2. **Readiness Probe (`readinessProbe`)**:
    * **Purpose**: Checks if the application is currently ready to receive traffic from users (e.g., database connection pool is healthy, caches are connected).
    * **Action on Failure**: Kubernetes **temporarily stops sending traffic** to this Pod by removing it from the Service endpoints / load balancer. The container is **not** restarted.
    * **Golden Rule**: Check essential dependencies with short timeouts. Return `200 OK` when ready, or `503 Service Unavailable` when not ready.

3. **Startup Probe (`startupProbe`)**:
    * **Purpose**: Checks if the application has completed its initial warmup/initialization.
    * **Action on Failure**: Disables liveness and readiness checks until the startup probe succeeds (useful for slow startup tasks like loading large ML models or pre-warming caches).

---

## Common Production Trap: Cascading Restarts { #common-production-trap-cascading-restarts }

/// warning

A very common mistake is checking external dependencies (such as PostgreSQL or Redis) inside the **Liveness Probe**.

If your database experiences a brief network blip or temporary overload:

1. The liveness probe fails across **all** application replicas simultaneously.
2. Kubernetes restarts **every container** at the same time.
3. Upon restarting, all containers attempt to reconnect to the database simultaneously, creating a **thundering herd / restart storm** and causing complete system downtime.

**Always check downstream dependencies in the Readiness Probe, never in the Liveness Probe.**

///

---

## FastAPI Implementation Example { #fastapi-implementation-example }

Here is a practical, production-ready example using FastAPI, `lifespan`, and standard health status responses:

{* ../../docs_src/kubernetes_probes/tutorial001_py310.py *}

### Code Breakdown { #code-breakdown }

* **`lifespan`**: Sets `app_state.is_ready = True` once the application startup tasks complete.
* **`/livez` endpoint**: Returns a simple `{"status": "ok"}`. It does not hit the database. If this fails, the process is deadlocked or crashed, so a container restart is warranted.
* **`/readyz` endpoint**: Checks `app_state.is_ready` and validates the database connection with `check_database()`. If any check fails, it raises an `HTTPException` with status code `503 Service Unavailable`.

---

## Kubernetes Deployment Manifest Example { #kubernetes-deployment-manifest-example }

In your Kubernetes `Deployment` YAML file, configure the probes to point to your FastAPI endpoints:

```yaml hl_lines="13-29"
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
        - name: fastapi-app
          image: my-fastapi-app:latest
          ports:
            - containerPort: 8000
          # Liveness: Restart the container if the event loop / process hangs
          livenessProbe:
            httpGet:
              path: /livez
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 10
            timeoutSeconds: 2
            failureThreshold: 3
          # Readiness: Remove from load balancer if database/dependencies are unhealthy
          readinessProbe:
            httpGet:
              path: /readyz
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 2
            failureThreshold: 2
```

### Parameter Guidelines { #parameter-guidelines }

* **`initialDelaySeconds`**: Time to wait before executing the first probe after the container starts.
* **`periodSeconds`**: How often (in seconds) to perform the probe.
* **`timeoutSeconds`**: Number of seconds after which the probe times out (keep this short, e.g. 2–3 seconds).
* **`failureThreshold`**: Number of consecutive failures before Kubernetes takes action (restarting for liveness, removing from traffic for readiness).

---

## Summary { #summary }

* Use `/livez` for process health and `/readyz` for traffic readiness.
* Never check external services in `/livez` to prevent cascading pod restarts.
* Use FastAPI's `lifespan` context manager to manage startup/warmup state cleanly.
