# Strict Content-Type Checking { #strict-content-type-checking }

By default, **FastAPI** uses strict `Content-Type` header checking for JSON request bodies, this means that JSON requests **must** include a valid `Content-Type` header (e.g. `application/json`) in order for the body to be parsed as JSON.

## CSRF Risk { #csrf-risk }

This default behavior provides protection against a class of **Cross-Site Request Forgery (CSRF)** attacks in a very specific scenario.

These attacks exploit the fact that browsers allow scripts to send requests without doing any CORS preflight check when they:

* don't have a `Content-Type` header (e.g. using `fetch()` with a `Blob` body)
* and don't send any authentication credentials.

This type of attack is mainly relevant when:

* the application is running locally (e.g. on `localhost`) or in an internal network
* and the application doesn't have any authentication, it expects that any request from the same network can be trusted.

## Example Attack { #example-attack }

Imagine you build a way to run a local AI agent.

It provides an API at

```
http://localhost:8000/v1/agents/multivac
```

There's also a frontend at

```
http://localhost:8000
```

/// tip

Note that both have the same host.

///

Then using the frontend you can make the AI agent do things on your behalf.

As it's running **locally**, and not in the open internet, you decide to **not have any authentication** set up, just trusting the access to the local network.

Then one of your users could install it and run it locally.

Then they could open a malicious website, e.g. something like

```
https://evilhackers.example.com
```

And that malicious website sends requests using `fetch()` with a `Blob` body to the local API at

```
http://localhost:8000/v1/agents/multivac
```

Even though the host of the malicious website and the local app is different, the browser won't trigger a CORS preflight request because:

* It's running without any authentication, it doesn't have to send any credentials.
* The browser thinks it's not sending JSON (because of the missing `Content-Type` header).

Then the malicious website could make the local AI agent send angry messages to the user's ex-boss... or worse. 😅

## Open Internet { #open-internet }

If your app is in the open internet, you wouldn't "trust the network" and let anyone send privileged requests without authentication.

Attackers could simply run a script to send requests to your API, no need for browser interaction, so you are probably already securing any privileged endpoints.

In that case **this attack / risk doesn't apply to you**.

This risk and attack is mainly relevant when the app runs on the **local network** and that is the **only assumed protection**.

## Allowing Requests Without Content-Type { #allowing-requests-without-content-type }

If you need to support clients that don't send a `Content-Type` header, you can disable strict checking by setting `strict_content_type=False`:

{* ../../docs_src/strict_content_type/tutorial001_py310.py hl[4] *}

With this setting, requests without a `Content-Type` header will have their body parsed as JSON, which is the same behavior as older versions of FastAPI.

/// info

This behavior and configuration was added in FastAPI 0.132.0.

///
