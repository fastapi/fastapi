You can connect the debugger in your editor, for example with Visual Studio Code or PyCharm.

## Call `uvicorn`

In your FastAPI application, import and run `uvicorn` directly:

```Python hl_lines="1 15"
{!./src/debugging/tutorial001.py!}
```

### About `__name__ == "__main__"`

The main purpose of the `__name__ == "__main__"` is to have some code that is executed when your file is called with:

```bash
python myapp.py
```

but is not called when another file imports it, like in:

```Python
from myapp import app
```

#### More details

Let's say your file is named `myapp.py`.

If you run it with:

```bash
python myapp.py
```

then the internal variable `__name__` in your file, created automatically by Python, will have as value the string `"__main__"`.

So, the section:

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

will run.

---

This won't happen if you import that module (file).

So, if you have another file `importer.py` with:

```Python
from myapp import app

# Some more code
```

in that case, the automatic variable inside of `myapp.py` will not have the variable `__name__` with a value of `"__main__"`.

So, the line:

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

will not be executed.

!!! info
    For more information, check <a href="https://docs.python.org/3/library/__main__.html" target="_blank">the official Python docs</a>.

## Run your code with your debugger

Because you are running the Uvicorn server directly from your code, you can call your Python program (your FastAPI application) directly from the debugger.

---

For example, in Visual Studio Code, you can:

* Go to the "Debug" panel.
* "Add configuration...".
* Select "Python"
* Run the debugger with the option "`Python: Current File (Integrated Terminal)`".

It will then start the server with your **FastAPI** code, stop at your breakpoints, etc.

Here's how it might look:

<img src="/img/tutorial/debugging/image01.png">
