<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI framework, high performance, easy to learn, fast to code, ready for production</em>
</p>
<p align="center">
<a href="https://github.com/fastapi/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/fastapi/fastapi/actions/workflows/test.yml/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/fastapi" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/fastapi.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Documentation**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Source Code**: <a href="https://github.com/fastapi/fastapi" target="_blank">https://github.com/fastapi/fastapi</a>

---

# Overview

FastAPI is a modern, fast (high‑performance) web framework for building APIs with Python 3.8+ based on standard Python type hints. It combines the speed of **Node.js** and **Go** with the developer friendliness of **Python**, delivering:

* **Performance** – on par with the fastest Python frameworks because it is built on **Starlette** for the web parts and **Pydantic** for the data parts.
* **Fast to code** – increase development speed by 200 %–300 % thanks to automatic request validation, serialization, interactive API docs, and editor autocompletion.
* **Reduced bugs** – data validation and type checking catch many errors at runtime, lowering the chance of human‑introduced bugs.
* **Intuitive** – editors provide instant completion and type checking for request bodies, query parameters, headers, and more.
* **Production ready** – OpenAPI, JSON‑Schema, automatic interactive documentation (Swagger UI & ReDoc), dependency injection, security utilities, and extensive testing support.

# Installation

FastAPI is released on PyPI and can be installed with **pip**. It has no external runtime dependencies besides **uvicorn** (or another ASGI server) for development and production.

```bash
pip install "fastapi[all]"   # includes optional dependencies such as python‑multipart, email‑validator, jinja2
# Or, if you only need the core framework:
pip install fastapi
```

> **Note**: FastAPI requires Python **3.8** or newer.

# Quick start

Below is a minimal example that demonstrates the core concepts:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.post("/items/")
async def create_item(item: Item):
    return {"item_id": 1, **item.dict()}
```

Run the application with **uvicorn**:

```bash
uvicorn myapp:app --reload   # where `myapp.py` contains the code above
```

Open your browser at <http://127.0.0.1:8000/docs> to see the automatically generated Swagger UI, or at <http://127.0.0.1:8000/redoc> for ReDoc.

For a more detailed tutorial, see the official documentation: <https://fastapi.tiangolo.com/tutorial/>.

# Documentation

The full documentation lives at <https://fastapi.tiangolo.com>. It covers:

* **Tutorial** – step‑by‑step guide for beginners.
* **Advanced user guide** – dependency injection, background tasks, websockets, security, testing, etc.
* **Reference** – exhaustive API reference for `fastapi`, `starlette`, and `pydantic` integration.
* **API OpenAPI schema** – automatically generated and customizable.

# Contributing

Contributions are welcome! Please read our [CONTRIBUTING guide](https://github.com/fastapi/fastapi/blob/master/CONTRIBUTING.md) before submitting a pull request. All contributors are expected to follow the code of conduct and ensure that new code is covered by tests and adheres to the project's style guidelines.

# License

FastAPI is licensed under the MIT License. See the `LICENSE` file for the full text.

---

*FastAPI – The modern, fast (high‑performance) web framework for building APIs with Python.*
