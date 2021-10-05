# NoSQL (Distributed / Big Data) Databases

**FastAPI** can also be integrated with any <abbr title="Distributed database (Big Data), also 'Not Only SQL'">NoSQL</abbr>.

Here we'll see an example using **<a href="https://www.couchbase.com/" class="external-link" target="_blank">Couchbase</a>**, a <abbr title="Document here refers to a JSON object (a dict), with keys and values, and those values can also be other JSON objects, arrays (lists), numbers, strings, booleans, etc.">document</abbr> based NoSQL database.

You can adapt it to any other NoSQL database like:

* **MongoDB**
* **Cassandra**
* **CouchDB**
* **ArangoDB**
* **ElasticSearch**, etc.

!!! tip
    There is an official project generator with **FastAPI** and **Couchbase**, all based on **Docker**, including a frontend and more tools: <a href="https://github.com/tiangolo/full-stack-fastapi-couchbase" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-fastapi-couchbase</a>

## Import Couchbase components

For now, don't pay attention to the rest, only the imports:

```Python hl_lines="3-5"
{!../../../docs_src/nosql_databases/tutorial001.py!}
```

## Define a constant to use as a "document type"

We will use it later as a fixed field `type` in our documents.

This is not required by Couchbase, but is a good practice that will help you afterwards.

```Python hl_lines="9"
{!../../../docs_src/nosql_databases/tutorial001.py!}
```

## Add a function to get a `Bucket`

In **Couchbase**, a bucket is a set of documents, that can be of different types.

They are generally all related to the same application.

The analogy in the relational database world would be a "database" (a specific database, not the database server).

The analogy in **MongoDB** would be a "collection".

In the code, a `Bucket` represents the main entrypoint of communication with the database.

This utility function will:

* Connect to a **Couchbase** cluster (that might be a single machine).
    * Set defaults for timeouts.
* Authenticate in the cluster.
* Get a `Bucket` instance.
    * Set defaults for timeouts.
* Return it.

```Python hl_lines="12-21"
{!../../../docs_src/nosql_databases/tutorial001.py!}
```

## Create Pydantic models

As **Couchbase** "documents" are actually just "JSON objects", we can model them with Pydantic.

### `User` model

First, let's create a `User` model:

```Python hl_lines="24-28"
{!../../../docs_src/nosql_databases/tutorial001.py!}
```

We will use this model in our *path operation function*, so, we don't include in it the `hashed_password`.

### `UserInDB` model

Now, let's create a `UserInDB` model.

This will have the data that is actually stored in the database.

We don't create it as a subclass of Pydantic's `BaseModel` but as a subclass of our own `User`, because it will have all the attributes in `User` plus a couple more:

```Python hl_lines="31-33"
{!../../../docs_src/nosql_databases/tutorial001.py!}
```

!!! note
    Notice that we have a `hashed_password` and a `type` field that will be stored in the database.

    But it is not part of the general `User` model (the one we will return in the *path operation*).

## Get the user

Now create a function that will:

* Take a username.
* Generate a document ID from it.
* Get the document with that ID.
* Put the contents of the document in a `UserInDB` model.

By creating a function that is only dedicated to getting your user from a `username` (or any other parameter) independent of your *path operation function*, you can more easily re-use it in multiple parts and also add <abbr title="Automated test, written in code, that checks if another piece of code is working correctly.">unit tests</abbr> for it:

```Python hl_lines="36-42"
{!../../../docs_src/nosql_databases/tutorial001.py!}
```

### f-strings

If you are not familiar with the `f"userprofile::{username}"`, it is a Python "<a href="https://docs.python.org/3/glossary.html#term-f-string" class="external-link" target="_blank">f-string</a>".

Any variable that is put inside of `{}` in an f-string will be expanded / injected in the string.

### `dict` unpacking

If you are not familiar with the `UserInDB(**result.value)`, <a href="https://docs.python.org/3/glossary.html#term-argument" class="external-link" target="_blank">it is using `dict` "unpacking"</a>.

It will take the `dict` at `result.value`, and take each of its keys and values and pass them as key-values to `UserInDB` as keyword arguments.

So, if the `dict` contains:

```Python
{
    "username": "johndoe",
    "hashed_password": "some_hash",
}
```

It will be passed to `UserInDB` as:

```Python
UserInDB(username="johndoe", hashed_password="some_hash")
```

## Create your **FastAPI** code

### Create the `FastAPI` app

```Python hl_lines="46"
{!../../../docs_src/nosql_databases/tutorial001.py!}
```

### Create the *path operation function*

As our code is calling Couchbase and we are not using the <a href="https://docs.couchbase.com/python-sdk/2.5/async-programming.html#asyncio-python-3-5" class="external-link" target="_blank">experimental Python <code>await</code> support</a>, we should declare our function with normal `def` instead of `async def`.

Also, Couchbase recommends not using a single `Bucket` object in multiple "<abbr title="A sequence of code being executed by the program, while at the same time, or at intervals, there can be others being executed too.">thread</abbr>s", so, we can just get the bucket directly and pass it to our utility functions:

```Python hl_lines="49-53"
{!../../../docs_src/nosql_databases/tutorial001.py!}
```

## Recap

You can integrate any third party NoSQL database, just using their standard packages.

The same applies to any other external tool, system or API.
