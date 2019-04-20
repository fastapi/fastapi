<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" target="_blank">CORS or "Cross-Origin Resource Sharing"</a> refers to the situations when a frontend running in a browser has JavaScript code that communicates with a backend, and the backend is in a different "origin" than the frontend.

## Origin

An origin is the combination of protocol (`http`, `https`), domain (`myapp.com`, `localhost`, `localhost.tiangolo.com`), and port (`80`, `443`, `8080`).

So, all these are different origins:

* `http://localhost`
* `https://localhost`
* `http://localhost:8080`

Even if they are all in `localhost`, they use different protocols or ports, so, they are different "origins".

## Steps

So, let's say you have a frontend running in your browser at `http://localhost:8080`, and its JavaScript is trying to communicate with a backend running at `http://localhost` (because we don't specify a port, the browser will assume the default port `80`).

Then, the browser will send an HTTP `OPTIONS` request to the backend, and if the backend sends the appropriate headers authorizing the communication from this different origin (`http://localhost:8080`) then the browser will let the JavaScript in the frontend send its request to the backend.

To achieve this, the backend must have a list of "allowed origins".

In this case, it would have to include `http://localhost:8080` for the frontend to work correctly.

## Wildcards

It's also possible to declare the list as `"*"` (a "wildcard") to say that all are allowed.

But that will only allow certain types of communication, excluding everything that involves credentials: Cookies, Authorization headers like those used with Bearer Tokens, etc.

So, for everything to work correctly, it's better to specify explicitly the allowed origins.

## Use `CORSMiddleware`

You can configure it in your **FastAPI** application using Starlette's <a href="https://www.starlette.io/middleware/#corsmiddleware" target="_blank">`CORSMiddleware`</a>.

* Import it form Starlette.
* Create a list of allowed origins (as strings).
* Add it as a "middleware" to your **FastAPI** application.

You can also specify if your backend allows:

* Credentials (Authorization headers, Cookies, etc).
* Specific HTTP methods (`POST`, `PUT`) or all of them with the wildcard `"*"`.
* Specific HTTP headers or all of them with the wildcard `"*"`.

```Python hl_lines="2 6 7 8 9 10 11 13 14 15 16 17 18 19"
{!./src/cors/tutorial001.py!}
```

## More info

For more details of what you can specify in `CORSMiddleware`, check <a href="https://www.starlette.io/middleware/#corsmiddleware" target="_blank">Starlette's `CORSMiddleware` docs</a>.

For more info about <abbr title="Cross-Origin Resource Sharing">CORS</abbr>, check the <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" target="_blank">Mozilla CORS documentation</a>.