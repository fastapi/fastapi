For the simplest cases, you can use HTTP Basic Auth.

In HTTP Basic Auth, the application expects a header that contains a username and a password.

If it doesn't receive it, it returns an HTTP 401 "Unauthorized" error.

And returns a header `WWW-Authenticate` with a value of `Basic`, and an optional `realm` parameter.

That tells the browser to show the integrated prompt for a username and password.

Then, when you type that username and password, the browser sends them in the header automatically.

## Simple HTTP Basic Auth

* Import `HTTPBasic` and `HTTPBasicCredentials`.
* Create a "`security` scheme" using `HTTPBasic`.
* Use that `security` with a dependency in your *path operation*.
* It returns an object of type `HTTPBasicCredentials`:
    * It contains the `username` and `password` sent.


```Python hl_lines="2 6 10"
{!./src/security/tutorial006.py!}
```

When you try to open the URL for the first time (or click the "Execute" button in the docs) the browser will ask you for your username and password:

<img src="/img/tutorial/security/image12.png">

## Check the username

Here's a more complete example.

Use a dependency to check if the username and password are correct.

If the credentials are incorrect, return an `HTTPException` with a status code 401 (the same returned when no credentials are provided) and add the header `WWW-Authenticate` to make the browser show the login prompt again:

```Python hl_lines="10 11 12 13 14 15 16 17 21"
{!./src/security/tutorial007.py!}
```
