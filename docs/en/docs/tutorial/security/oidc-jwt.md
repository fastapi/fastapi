# OpenID Connect (OIDC) with JWT Access Tokens

For this tutorial we will be using OpenID Connect (OIDC) as an *authentication* layer that builds on top of the OAuth2 *authorization* layer.

We will be using the Swagger UI to serve the OpenID Connect authentication flow. The **FastAPI** (default) router will implement a OAuth2 resource server that validates the JWT access tokens and grant access to the router's endpoints.

We will use a custom claim to grant permission to endpoints for users with specific roles which are represented as a claim in the access token (there is no standard defined what the claim name is, so it has a configurable or *custom* name). Typically, the authorization server exposes the user's group membership in a specific claim in the JWT Access Token, which defaults to 'groups' in the tutorial.

Note that the Swagger UI mirrors the OIDC main flow of the frontend that would be used in a production environment. Therefore the OIDC security scheme, as represented in the openAPI definition, is separate from the OAuth2 scheme.

# Configure Requirements

First, you will need to select an OpenID provider if you do not have one already. There are ones that offer free trials or free tiers to experiment with [here](https://identitymanagementinstitute.org/identity-and-access-management-vendor-list/).


## Setup OpenID provder

First, we will need to configure an Applicaton (i.e. Relying Party in OpenID-speak) in the OpenID provider. This application allows the **FastAPI** client that logs in to the OpenID Connect provider:

/// check | Step 1 - Create Application

* Create an Application of type SPA
* Select Authorization Code, Refresh Token, Require PKCE
* Configure sign-in redirect URIs: `http://localhost:8080/docs/oauth2-redirect`
* Configure sign-out redirect URIs: `http://localhost:8080/docs/`
* *Write down the client id*

///

Then, we will select an authorization server to verify user identities and issue tokens for secure authentication and authorization of login requests:

/// check | Step 2 - Configure authorization server to return a custom claim

* Select/create a custom authorization server for the abovementioned application
* Create a custom claim with the name "`groups`".
* Map the values to the groups of which the authenticated user is member of
* *Write down issuer URL*
* *Write down audience*

///

Finally, we will need to create a user and a group named "`Foo`" to

/// check | Step 3 - Create a user and group

* Create a group called "`Foo`"
* Create a user
* Assign the "`Foo`"` group to the user
* Assign the application of step 1 to the user
* *Write down user/password as you will need to authenticate with it later*

///

## Configure your **FastAPI** Application

We assume a running pip environment with **FastAPI** installed (see [here](../../index.md#installation)).

This example contains a `AccessTokenValidator` that validates the JWT access tokens using the jwks url that is part of the oidc well known configuration. It requires a Python JavaScript Object Signing and Encryprion (JOSE) library, a HTTP client to fetch keysets and some cache utilities.


/// check | Step 4 - Install AccessTokenValidator Dependencies

```console
pip install jose cachetools types-cachetools httpx
```

///

You need to fill in the values in the .env file that you wrote down from the previous steps:

/// check | Step 5 - Configure **FastAPI** environment

```
client_id = "Client Id of Step 1 here"
issuer = "Issuer URL of Step 2 here"
audience = "Audience of Step 2 here"
```

///

This was the final step of the configuration.

# Running the **FastAPI** Application

Finally we come to the actual **FastAPI** code:


{* ../../docs_src/security/tutorial008_an_py39.py hl[112:124,127:129,134] *}


/// check | some small tweaks necessary?

* line 118, set usePkceWithAuthorizationCodeGrant if you require PKCE authentication (configured when you set up your application)
* line 116, add additional scopes to "openid" if your authorization requires this

///

If you save this file as `main.py`, you can run the app [as normal](../../index.md#run-it), for instance:

```bash
uvicorn main:app --port 8080 --reload
```

(*If you do not specify the correct port defined in Step 1, the authentication flow will fail*)


# Test the **FastAPI** Application

When the application is running, you can then point your browser to the [Interactive API Docs](../../index.md#interactive-api-docs):
`http://localhost:8080/docs/`

Authenticate first in the Swagger UI using the 'Authorize' button at the top and scroll to the topmost authentication flow named **'OpenIdConnect (OAuth2, authorization_code with PKCE)'**:

<img src="/img/tutorial/security/image13.png">

Then press the 'Authorize' button.

When successfully authenticated, you will see that your session is 'authorized':

<img src="/img/tutorial/security/image14.png">

Press the 'Close' button to close this screen.

Then execute the /hello endpoint with your user if part of the "`Foo`" group:

<img src="/img/tutorial/security/image15.png">

If you see "Hi!" as a response, your user was successfully authenticated and had the "`Foo`" role in the claim as required by the /hello endpoint.

To understand the code step by step, it will help if you step through the code using a [Debugger](../debugging.md#run-your-code-with-your-debugger).

Good luck!

# Appendix - References

* OIDC Terminology: https://openid.net/specs/openid-connect-core-1_0.html#Terminology
