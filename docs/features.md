
## FastAPI features

**FastAPI** gives you the following:

* Automatic API documentation with the open standard: <a href="https://github.com/OAI/OpenAPI-Specification" target="_blank"><strong>OpenAPI</strong></a>.
* Automatic data model documentation with <a href="http://json-schema.org/" target="_blank"><strong>JSON Schema</strong></a> (as OpenAPI itself is based on JSON Schema).
* Interactive API documentation and exploration web user interface with <a href="https://github.com/swagger-api/swagger-ui" target="_blank"><strong>Swagger UI</strong></a>.

![Swagger UI interaction](img/readme-assets/readme05.png)

* Alternative API documentation with <a href="https://github.com/Rebilly/ReDoc" target="_blank"><strong>ReDoc</strong></a>.

![ReDoc](img/readme-assets/readme06.png)


* All based on standard **Python 3.6 type** declarations (thanks to Pydantic). No new syntax to learn:

```Python
from typing import List, Dict
from datetime import date

from pydantic import BaseModel

# Declare a variable as an int
user_id: int

# Declare the type and set a value
user_id: int = 3

# tags is a list of str
tags: List[str] = ["fast", "easy", "short", "robust"]


# item_tags is a dict with str as keys, and lists of str as values
item_tags: Dict[str, List[str]] = {
    "foo": ["The Foo", "Foo Fighters"], 
    "bar": ["Bar Halen", "Bars N' Roses"]
    }

# A Pydantic model
class User(BaseModel):
    id: int
    name: str
    joined: datetime


my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}


# **second_user_data means "pass the keys and values of the dict directly as arguments
my_second_user: User = User(**second_user_data)
```

* Sensible **defaults** for everything, with optional configurations everywhere.
* Validation for many **data types**, including JSON objects (`dict`) fields, JSON array (`list`) item types, string (`str`) min and max lengths, number (`int`, `float`) min and max values, etc.
* Security and authentication included: all the security schemes defined in OpenAPI, including HTTP Basic, **OAuth2** (also with **JWT tokens**), API keys, etc. Plus the security features from Starlette (including session cookies). All built as reusable tools and components that are easy to integrate with your systems, data stores, databases, etc.
* Extremely easy, but extremely powerful **Dependency Injection** (also known as "components", "resources", "services", "providers"):
    * Even dependencies can have dependencies, creating a hierarchy or **"graph" of dependencies**.
    * All **automatically handled** by the framework. 
    * All the dependencies can **augment the endpoint** parameters and constraints.
    * **Automatic validation** even for parameters from dependencies.
    * Support for complex user authentication systems, **database connections**, etc.
* **No compromise** with databases, frontends, etc. But easy integration with all.
* **Unlimited "plug-ins"**:
    * Or in other way, no need for them, import and use the code you need. 
    * Any integration is designed to be so simple to use (with dependencies) that you can create a "plug-in" for your application in 2 lines of code.
* Fully compatible with (and based on) **Starlette**.
    * Any additional Starlette code you have, will also work.
* Fully compatible with (and based on) **Pydantic**. 
    * Any additional Pydantic code you have will also work.
    * Including external libraries also based on Pydantic.
* 100% test coverage (* not yet, in a couple days).
* 100% type annotated code base.

## Starlette features

Plus **Starlette**'s features (FastAPI is just Starlette on steroids):

* Seriously impressive performance. It is <a href="https://github.com/encode/starlette#performance" target="_blank">one of the fastest Python frameworks available, on par with **NodeJS** and **Go**</a>.
* **WebSocket** support.
* **GraphQL** support.
* In-process background tasks.
* Startup and shutdown events.
* Test client built on `requests`.
* **CORS**, GZip, Static Files, Streaming responses.
* **Session and Cookie** support.
* 100% test coverage.
* 100% type annotated codebase.

## Pydantic features

Plus **Pydantic**'s features:

* **No brainfuck**: 
    * No new schema definition micro-language to learn.
    * If you know Python types you know how to use Pydantic.
* Plays nicely with your **IDE/linter/brain**:
    * Because pydantic data structures are just instances of classes you define; auto-completion, linting, mypy and your intuition should all work properly with your validated data.
* **Fast**:
    * in <a href="https://pydantic-docs.helpmanual.io/#benchmarks-tag" target="_blank">benchmarks</a> Pydantic is faster than all other tested libraries.
* Validate **complex structures**:
    * Use of hierarchical Pydantic models, Python `typing`’s `List` and `Dict`, etc.
    * And validators allow complex data schemas to be clearly and easily defined, checked and documented as JSON Schema.
    * You can have deeply **nested JSON** objects and have them all validated and annotated.
* **Extendible**:
    * Pydantic allows custom data types to be defined or you can extend validation with methods on a model decorated with the validator decorator.
