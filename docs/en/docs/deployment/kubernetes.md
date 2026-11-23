
# Kubernetes { #kubernetes }

Kubernetes is a container orchestration platform that helps deploy, manage, and scale applications.

When deploying a FastAPI application on Kubernetes, it is important to make sure that the application is running correctly and is ready to handle incoming requests.

Kubernetes provides three types of health probes to monitor containers:

* **Liveness probes**: Determine whether a container should be restarted.
* **Readiness probes**: Determine whether a container is ready to receive traffic.
* **Startup probes**: Determine whether an application has finished starting.

These probes help Kubernetes manage application availability and recover from failures.


## Liveness Probes { #liveness-probes }

A liveness probe checks whether an application is still functioning correctly.

If a liveness probe repeatedly fails, Kubernetes considers the container unhealthy and restarts it.

For a FastAPI application, an HTTP liveness probe can be configured to send requests to a dedicated health-check endpoint.

For example, an application could expose a `/health/live` endpoint that returns a successful HTTP response when the application is functioning.

Liveness probes should detect situations where an application cannot recover without being restarted. They should not be used to check the availability of external services such as databases, as temporary dependency failures could cause unnecessary container restarts.


## Readiness Probes { #readiness-probes }

A readiness probe checks whether an application is ready to handle incoming requests.

If a readiness probe fails, Kubernetes marks the Pod as not ready and stops sending traffic to it through Services. The container is not restarted because of a readiness probe failure.

For a FastAPI application, a dedicated endpoint such as `/health/ready` can be used to report whether the application is ready to serve requests.

For example, an application might use this endpoint to check whether it has completed initialization and established the connections required to handle requests.

Readiness probes are useful when an application needs time to initialize or temporarily becomes unable to serve requests.

## Startup Probes { #startup-probes }

A startup probe checks whether an application has completed its startup process.

It is particularly useful for applications that require more time to initialize, such as applications that load large machine learning models or perform time-consuming initialization tasks.

When a startup probe is configured, Kubernetes delays liveness and readiness probe checks until the startup probe succeeds.

If the startup probe repeatedly fails beyond its configured failure threshold, Kubernetes restarts the container.

For a FastAPI application, an HTTP endpoint such as `/health/startup` can be used to indicate when the application has completed initialization.

Startup probes help prevent Kubernetes from restarting applications that simply need more time to start.


## Health Check Endpoints in FastAPI { #health-check-endpoints-in-fastapi }

FastAPI does not provide built-in Kubernetes health-check endpoints. These endpoints can be created using standard FastAPI path operations.

For example:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health/live")
async def liveness():
    return {"status": "alive"}

@app.get("/health/ready")
async def readiness():
    # Add application readiness checks here.
    return {"status": "ready"}

@app.get("/health/startup")
async def startup():
    # Add application startup checks here.
    return {"status": "started"}
```

Each endpoint should return an HTTP 200 response when its corresponding check succeeds. If a check fails, the endpoint should return an appropriate unsuccessful HTTP response, such as HTTP 503 Service Unavailable. The example above shows the endpoint structure; implement the actual application-specific checks before using these endpoints in production.

A liveness endpoint should generally check whether the application process is functioning, without depending on external services. This helps prevent unnecessary restarts when a dependency is temporarily unavailable.

For example, a readiness endpoint can check whether required resources and dependencies are available before reporting that the application is ready to receive traffic.

## Kubernetes Deployment Configuration { #kubernetes-deployment-configuration }

After creating the health-check endpoints, configure Kubernetes to use them in the application Deployment.

The following example demonstrates how to configure all three probes for a FastAPI application running on port `8000`.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: fastapi-app
  template:
    metadata:
      labels:
        app: fastapi-app
    spec:
      containers:
        - name: fastapi
          image: your-fastapi-image:latest
          ports:
            - containerPort: 8000

          startupProbe:
            httpGet:
              path: /health/startup
              port: 8000
            periodSeconds: 10
            failureThreshold: 30

          livenessProbe:
            httpGet:
              path: /health/live
              port: 8000
            periodSeconds: 10
            failureThreshold: 3

          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8000
            periodSeconds: 5
            failureThreshold: 3
```

In this configuration:

* The startup probe checks the application every 10 seconds and allows up to 30 consecutive failures before Kubernetes restarts the container. This provides approximately 300 seconds of startup time.
* The liveness probe checks whether the application is functioning correctly.
* The readiness probe checks whether the application can receive traffic.

While the startup probe has not succeeded, Kubernetes does not run the liveness and readiness probes.

Replace `your-fastapi-image:latest` with the actual container image used by your application.


## Testing and Troubleshooting { #testing-and-troubleshooting }

After deploying the application, verify that the health-check endpoints return the expected HTTP responses.

You can test the endpoints using `curl`:

```console
$ curl http://localhost:8000/health/live
$ curl http://localhost:8000/health/ready
$ curl http://localhost:8000/health/startup
```

To inspect the status of the application Pods, use:

```console
$ kubectl get pods
```

To inspect probe failures and other events, use:

```console
$ kubectl describe pod <pod-name>
```

If a probe fails, check the following:

* Make sure the health-check endpoint is available.
* Verify that the configured port matches the port used by the application.
* Check the application logs for errors.
* Ensure that the probe timing settings allow sufficient time for application startup and response.
* Verify that the readiness endpoint reports success only when the application can handle requests.

These checks can help identify common problems with Kubernetes health probes.
