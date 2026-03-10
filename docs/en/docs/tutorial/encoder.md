# JSON Compatible Encoder { #json-compatible-encoder }

There are some cases where you might need to convert a data type (like a Pydantic model) to something compatible with JSON (like a `dict`, `list`, etc).

For example, if you need to store it in a database.

For that, **FastAPI** provides a `jsonable_encoder()` function.

## Using the `jsonable_encoder` { #using-the-jsonable-encoder }

Let's imagine that you have a database `fake_db` that only receives JSON compatible data.

For example, it doesn't receive `datetime` objects, as those are not compatible with JSON.

So, a `datetime` object would have to be converted to a `str` containing the data in [ISO format](https://en.wikipedia.org/wiki/ISO_8601).

The same way, this database wouldn't receive a Pydantic model (an object with attributes), only a `dict`.

You can use `jsonable_encoder` for that.

It receives an object, like a Pydantic model, and returns a JSON compatible version:

{* ../../docs_src/encoder/tutorial001_py310.py hl[4,21] *}

In this example, it would convert the Pydantic model to a `dict`, and the `datetime` to a `str`.

The result of calling it is something that can be encoded with the Python standard [`json.dumps()`](https://docs.python.org/3/library/json.html#json.dumps).

It doesn't return a large `str` containing the data in JSON format (as a string). It returns a Python standard data structure (e.g. a `dict`) with values and sub-values that are all compatible with JSON.

/// note

`jsonable_encoder` is actually used by **FastAPI** internally to convert data. But it is useful in many other scenarios.

///

## Working with Pandas DataFrames { #working-with-pandas-dataframes }

**Pandas** is commonly used in FastAPI applications for data science, analytics APIs, and ML inference backends. However, returning data from a Pandas DataFrame requires care — Pandas uses **NumPy types** internally (`numpy.int64`, `numpy.float64`, `numpy.nan`, `pandas.NaT`), which are **not natively JSON serializable**.

Calling `.to_dict(orient="records")` on a DataFrame returns a list of dicts where numeric columns are still NumPy types, not standard Python `int` or `float`. This causes a `TypeError` at runtime:

```
TypeError: Object of type int64 is not JSON serializable
```

Additionally, `numpy.nan` and `pandas.NaT` are not valid JSON values and will cause serialization errors or malformed output.

### Safe Pattern: Use `jsonable_encoder` { #safe-pattern-use-jsonable-encoder }

Wrap the result of `.to_dict()` with `jsonable_encoder()` to safely convert all NumPy types to JSON-compatible Python types, and convert `NaT`/`nan` to `null`:

```python
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import pandas as pd

app = FastAPI()


@app.get("/encounters")
def get_encounters():
    df = pd.read_csv("healthcare_data.csv")

    # ❌ May raise TypeError — numpy.int64 / numpy.float64 / NaN not JSON serializable
    # return df.to_dict(orient="records")

    # ✅ jsonable_encoder converts numpy types and NaT/NaN -> null
    return jsonable_encoder(df.to_dict(orient="records"))
```

### Alternative: Pandas Native JSON Serialization { #alternative-pandas-native-json-serialization }

Pandas has its own JSON serializer that handles NumPy types and dates natively. Use `df.to_json()` with `json.loads()` to produce a clean Python list:

```python
import json
from fastapi import FastAPI
import pandas as pd

app = FastAPI()


@app.get("/encounters")
def get_encounters():
    df = pd.read_csv("healthcare_data.csv")

    # ✅ Pandas handles numpy types + datetime columns with ISO format
    return json.loads(df.to_json(orient="records", date_format="iso"))
```

/// tip

Use the `date_format="iso"` parameter with `df.to_json()` to ensure datetime columns are serialized as ISO 8601 strings (e.g., `"2024-01-15T00:00:00"`), consistent with how `jsonable_encoder` handles Python `datetime` objects.

///

/// note

Both approaches produce `null` for missing values (`NaN`, `NaT`), which is the correct JSON representation for missing data.

///
