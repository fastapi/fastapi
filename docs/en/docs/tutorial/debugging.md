# Debugging

You can debug FastAPI in your editor, which we want to show here using Visual Studio Code and PyCharm as examples.

## Visual Studio Code

Visual Studio Code (or VS Code for short) already has a debugger configuration specifically for FastAPI.

Let's assume you have placed your FastAPI application in a file `myapp.py`:

{* ../../docs_src/debugging/tutorial001.py *}

In VS Code, you can now debug this application like this:

* Open your `myapp.py`. Also, make sure its editor tab is active.

* Now open the debug panel on the left – the "Run and Debug" panel.

* There, click on the link "create a launch.json file".

* From the dropdown menu, select "Python Debugger".

* Next, choose "FastAPI" from the options.

* In the subsequent dropdown, enter the name of your application file, here `myapp.py` (This is only necessary because VS Code did not find a `main.py` file).

* Now a file `launch.json` will be created in your project, in the subfolder `.vscode/` and opened in the editor. It will look something like this:

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "myapp:app",
                "--reload"
            ],
            "jinja": true,
            "justMyCode": true
        }
    ]
}
```

* All important settings are already made, you do not need to edit this file any further and can close it.

* The debug configuration you just created will now also appear in the debug panel at the top as "Python: FastAPI".

* Click on the green triangle next to your "Python Debugger: FastAPI" configuration, or press the `F5` key.

* Debugging begins. A box appears at the top with buttons, for example to continue debugging after a breakpoint or to end debugging.

* The FastAPI development server is starting, as you can see in the terminal that opens at the bottom.

* Now in `myapp.py`, for example on the last line of the function, add a breakpoint by clicking on the red dot that appears when you hover over the line number.

* In your web browser, visit your application's homepage at <a href="http://127.0.0.1:8000/" class="external-link" target="_blank">http://127.0.0.1:8000/</a>.

* In VS Code, you can now see that the debugger stops at your breakpoint. The web page being accessed doesn't stop loading because you told the debugger to stop before returning the response. On the left, in the debug panel, you can see the currently available local and global variables. It looks something like this:

<img src="/img/tutorial/debugging/image01.png">

* To continue execution, click the "Continue" button in the debug box. Now the response is returned and the website in the browser finishes loading.

* To stop debugging, click (possibly several times) on the Stop button in the same box. The development server is stopped.

Now you know the basics of debugging your application in VS Code! 🚀

## PyCharm

PyCharm does not currently have a debug configuration specifically for FastAPI applications, so we will run the `uvicorn` server directly from our `myapp.py`.

### Call `uvicorn`

Import `uvicorn` and run it directly:

```Python hl_lines="1  15"
{!../../../docs_src/debugging/tutorial002.py!}
```

### About `__name__ == "__main__"`

The main purpose of `__name__ == "__main__"` is to have a block of code that is executed when your file is called with:

<div class="termy">

```console
$ python myapp.py
```

</div>

but which is not executed when another file imports it, as in:

```Python
from myapp import app
```

#### More details

If you run your file with:

<div class="termy">

```console
$ python myapp.py
```

</div>

then the internal variable `__name__` in your file, which is automatically created by Python, will have the string `"__main__"` as its value.

So the section:

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

will be executed.

---

This won't happen if you import that module (file).

So if you have another file `importer.py` with:

```Python
from myapp import app

# More code here
```

in that case, the automatically created variable `__name__` in `myapp.py` will not have the value `"__main__"`.

So the line:

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

will not be executed.

/// info

For more information, check <a href="https://docs.python.org/3/library/__main__.html" class="external-link" target="_blank">the official Python docs</a>.

///


### Run the code with the debugger

Since you are now running the Uvicorn server directly from your code, you can call your Python program (your FastAPI application) directly from the PyCharm debugger (or other editors' debuggers).

* Simply click on the green triangle that appears to the left of the line `if __name__ == "__main__":` and select "Debug 'myapp'".

* The debugger starts. A console window opens at the bottom, showing that the Uvicorn development server is booting.

* Then continue as under [Visual Studio Code](#visual-studio-code): Set breakpoints, load the page in the browser, examine the current state of your application. And again, this time at the bottom, you have buttons to continue debugging, stop debugging, etc. It looks something like this:

<img src="/img/tutorial/debugging/image02.png">

And with that you also know the basics of debugging your application in PyCharm! 🚀
