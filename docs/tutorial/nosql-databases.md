**FastAPI** can also be integrated with any <abbr title="Distributed database (Big Data), also 'Not Only SQL'">NoSQL</abbr>.

Here we'll see an example using **<a href="https://www.couchbase.com/" target="_blank">Couchbase</a>**, a <abbr title="Document here refers to a JSON object (a dict), with keys and values, and those values can also be other JSON objects, arrays (lists), numbers, strings, booleans, etc.">document</abbr> based NoSQL database.

You can adapt it to any other NoSQL database like:

* **MongoDB**
* **Cassandra**
* **CouchDB**
* **ArangoDB**
* **ElasticSearch**, etc.

## Import Couchbase components

For now, don't pay attention to the rest, only the imports:

```Python hl_lines="6 7 8"
{!./tutorial/src/nosql-databases/tutorial001.py!}
```

## Define a constant to use as a "document type"

We will use it later as a fixed field `type` in our documents.

This is not required by Couchbase, but is a good practice that will help you afterwards.

```Python hl_lines="10"
{!./tutorial/src/nosql-databases/tutorial001.py!}
```

## Add a function to get a `Bucket`

In **Couchbase**, a bucket is a set of documents, that can be of different types.

They are generally all related to the same application.

The analogy in the relational database world would be a "database" (a specific database, not the database server).

The analogy in **MongoDB** would be a "collection".

In the code, a `Bucket` represents the main entrypoint of communication with the database.

This utility function will:

* Connect to a **Couchbase** cluster (that might be a single machine).
* Authenticate in the cluster.
* Get a `Bucket` instance.
* Return it.

```Python hl_lines="13 14 15 16 17 18"
{!./tutorial/src/nosql-databases/tutorial001.py!}
```

## Create Pydantic models

As **Couchbase** "documents" are actually just "JSON objects", we can model them with Pydantic.

### `User` model

First, let's create a `User` model:

```Python hl_lines="21 22 23 24 25"
{!./tutorial/src/nosql-databases/tutorial001.py!}
```

We will use this model in our path operation function, so, we don't include in it the `hashed_password`.

### `UserInDB` model

Now, let's create a `UserInDB` model.

This will have the data that is actually stored in the database.

In Couchbase, each document has a document <abbr title="Identification">ID</abbr> or "key".

But it is not part of the document itself.

It is stored as "metadata" of the document.

So, to be able to have that document ID as part of our model without it being part of the attributes (document contents), we can do a simple trick.

We can create an internal `class`, in this case named `Meta`, and declare the extra attribute(s) in that class.

This class doesn't have any special meaning and doesn't provide any special functionality other than not being directly an attribute of our main model:

```Python hl_lines="28 29 30 31 32 33"
{!./tutorial/src/nosql-databases/tutorial001.py!}
```

This `Meta` class won't be included when we generate a `dict` from our model, but we will be able to access it's data with something like:

```Python
my_user.Meta.key
```

!!! note
    Notice that we have a `hashed_password` and a `type` field that will be stored in the database.
    
    But it is not part of the general `User` model (the one we will return in the path operation).


## Get the user

Now create a function that will:

* Take a username.
* Generate a document ID from it.
* Get the document with that ID.
* Put the contents of the document in a `UserInDB` model.
* Add the extracted document `key` to our model.

By creating a function that is only dedicated to getting your user from a `username` (or any other parameter) independent of your path operation function, you can more easily re-use it in multiple parts and also add <abbr title="Automated test, written in code, that checks if another piece of code is working correctly.">unit tests</abbr> for it:

```Python hl_lines="36 37 38 39 40 41 42 43"
{!./tutorial/src/nosql-databases/tutorial001.py!}
```

### f-strings
    
If you are not familiar with the `f"userprofile::{username}"`, it is a Python "<a href="https://docs.python.org/3/glossary.html#term-f-string" target="_blank">f-string</a>".

Any variable that is put inside of `{}` in an f-string will be expanded / injected in the string.

### `dict` unpacking

If you are not familiar with the `UserInDB(**result.value)`, <a href="https://docs.python.org/3/glossary.html#term-argument" target="_blank">it is using `dict` "unpacking"</a>.

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

```Python hl_lines="47"
{!./tutorial/src/nosql-databases/tutorial001.py!}
```

### Create the path operation function

As our code is calling Couchbase and we are not using the <a href="https://docs.couchbase.com/python-sdk/2.5/async-programming.html#asyncio-python-3-5" target="_blank">experimental Python <code>await</code> support</a>, we should declare our function with normal `def` instead of `async def`.

Also, Couchbase recommends not using a single `Bucket` object in multiple "<abbr title="A sequence of code being executed by the program, while at the same time, or at intervals, there can be others being executed too.">thread</abbr>s", so, we can get just get the bucket directly and pass it to our utility functions:

```Python hl_lines="50 51 52 53 54"
{!./tutorial/src/nosql-databases/tutorial001.py!}
```

## Recap

You can integrate any third party NoSQL database, just using their standard packages.

The same applies to any other external tool, system or API.
