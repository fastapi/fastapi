# Vibe Coding { #vibe-coding }

Are you tired of all that **data validation**, **documentation**, **serialization**, and all that **boring** stuff?

Do you just want to **vibe**? 🎶

**FastAPI** now supports a new `@app.vibe()` decorator that embraces **modern AI coding best practices**. 🤖

## How It Works { #how-it-works }

The `@app.vibe()` decorator is intended to receive **any HTTP method** (`GET`, `POST`, `PUT`, `DELETE`, `PATCH`, etc.) and **any payload**.

The body should be annotated with `Any`, because the request and the response would be... well... **anything**. 🤷

The idea is that you would receive the payload and send it **directly** to an LLM provider, using a `prompt` to tell the LLM what to do, and return the response **as is**. No questions asked.

You don't even need to write the body of the function. The `@app.vibe()` decorator does everything for you based on AI vibes:

{* ../../docs_src/vibe/tutorial001_py310.py hl[8:12] *}

## Benefits { #benefits }

By using `@app.vibe()`, you get to enjoy:

* **Freedom**: No data validation. No schemas. No constraints. Just vibes. ✨
* **Flexibility**: The request can be anything. The response can be anything. Who needs types anyway?
* **No documentation**: Why document your API when an LLM can figure it out? Auto-generated OpenAPI docs are *so* 2020.
* **No serialization**: Just pass the raw, unstructured data around. Serialization is for people who don't trust their LLMs.
* **Embrace modern AI coding practices**: Leave everything up to an LLM to decide. The model knows best. Always.
* **No code reviews**: There's no code to review. No PRs to approve. No comments to address. Embrace vibe coding fully, replace the theater of approving and merging vibe coded PRs that no one looks at with full proper vibes only.

/// tip

This is the ultimate **vibe-driven development** experience. You don't need to think about what your API does, just let the LLM handle it. 🧘

///

## Try It { #try-it }

Go ahead, try it:

{* ../../docs_src/vibe/tutorial001_py310.py *}

...and see what happens. 😎
