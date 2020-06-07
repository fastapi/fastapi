---
name: Feature request
about: Suggest an idea for this project
title: ""
labels: enhancement
assignees: ''

---

### First check

* [ ] I added a very descriptive title to this issue.
* [ ] I used the GitHub search to find a similar issue and didn't find it.
* [ ] I searched the FastAPI documentation, with the integrated search.
* [ ] I already searched in Google "How to X in FastAPI" and didn't find any information.
* [ ] I already read and followed all the tutorial in the docs and didn't find an answer.
* [ ] I already checked if it is not related to FastAPI but to [Pydantic](https://github.com/samuelcolvin/pydantic).
* [ ] I already checked if it is not related to FastAPI but to [Swagger UI](https://github.com/swagger-api/swagger-ui).
* [ ] I already checked if it is not related to FastAPI but to [ReDoc](https://github.com/Redocly/redoc).
* [ ] After submitting this, I commit to:
    * Read open issues with questions until I find 2 issues where I can help someone and add a comment to help there.
    * Or, I already hit the "watch" button in this repository to receive notifications and I commit to help at least 2 people that ask questions in the future.
    * Implement a Pull Request for a confirmed bug.

<!-- 

I'm asking all this because answering questions and solving problems in GitHub issues consumes a lot of time. I end up not being able to add new features, fix bugs, review Pull Requests, etc. as fast as I wish because I have to spend too much time handling issues.

All that, on top of all the incredible help provided by a bunch of community members that give a lot of their time to come here and help others.

That's a lot of work they are doing, but if more FastAPI users came to help others like them just a little bit more, it would be much less effort for them (and you and me 😅).

-->

### Example

Here's a self-contained [minimal, reproducible, example](https://stackoverflow.com/help/minimal-reproducible-example) with my use case:

<!-- Replace the code below with your own self-contained, minimal, reproducible, example -->

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}
```

### Description

<!-- Replace the content below with your own feature request -->

* Open the browser and call the endpoint `/`.
* It returns a JSON with `{"Hello": "World"}`.
* I would like it to have an extra parameter to teleport me to the moon and back.

### The solution you would like

<!-- Replace this with your own content -->

I would like it to have a `teleport_to_moon` parameter that defaults to `False`, and can be set to `True` to teleport me:

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/", teleport_to_moon=True)
def read_root():
    return {"Hello": "World"}
```

### Describe alternatives you've considered

<!-- Replace this with your own ideas -->

To wait for Space X moon travel plans to drop down long after they release them. But I would rather teleport.

### Environment

* OS: [e.g. Linux / Windows / macOS]:
* FastAPI Version [e.g. 0.3.0]:

To know the FastAPI version use:

```bash
python -c "import fastapi; print(fastapi.__version__)"
```

* Python version:

To know the Python version use:

```bash
python --version
```

### Additional context

<!-- Add any other context or screenshots about the question here. -->
