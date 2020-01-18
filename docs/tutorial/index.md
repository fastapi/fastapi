This tutorial shows you how to use **FastAPI** with most of its features, step by step.

Each section gradually builds on the previous ones, but it's structured to separate topics, so that you can go directly to any specific one to solve your specific API needs.

It is also built to work as a future reference.

So you can come back and see exactly what you need.

## Run the code

All the code blocks can be copied and used directly (they are actually tested Python files).

To run any of the examples, copy the code to a file `main.py`, and start `uvicorn` with:

```bash
uvicorn main:app --reload
```

It is **HIGHLY encouraged** that you write or copy the code, edit it and run it locally.

Using it in your editor is what really shows you the benefits of FastAPI, seeing how little code you have to write, all the type checks, autocompletion, etc.

---

## Install FastAPI

The first step is to install FastAPI.

For the tutorial, you might want to install it with all the optional dependencies and features:

```bash
pip install fastapi[all]
```

...that also includes `uvicorn`, that you can use as the server that runs your code.

!!! note
    You can also install it part by part.

    This is what you would probably do once you want to deploy your application to production:

    ```
    pip install fastapi
    ```

    Also install `uvicorn` to work as the server:

    ```
    pip install uvicorn
    ```

    And the same for each of the optional dependencies that you want to use.

## Advanced User Guide

There is also an **Advanced User Guide** that you can read later after this **Tutorial - User guide**.

The **Advanced User Guide**, builds on this, uses the same concepts, and teaches you some extra features.

But you should first read the **Tutorial - User guide** (what you are reading right now).

It's designed so that you can build a complete application with just the **Tutorial - User guide**, and then extend it in different ways, depending on your needs, using some of the additional ideas from the **Advanced User Guide**.
