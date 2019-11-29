---
name: Bug report
about: Create a report to help us improve
title: "[BUG]"
labels: bug
assignees: ''

---

### Describe the bug

Write here a clear and concise description of what the bug is.

### To Reproduce

Steps to reproduce the behavior with a minimum self-contained file.

Replace each part with your own scenario:

1. Create a file with:

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}
```

3. Open the browser and call the endpoint `/`.
4. It returns a JSON with `{"Hello": "World"}`.
5. But I expected it to return `{"Hello": "Sara"}`.

### Expected behavior

Add a clear and concise description of what you expected to happen.

### Screenshots

If applicable, add screenshots to help explain your problem.

### Environment

- OS: [e.g. Linux / Windows / macOS]
- FastAPI Version [e.g. 0.3.0], get it with:

```bash
python -c "import fastapi; print(fastapi.__version__)"
```

- Python version, get it with:

```bash
python --version
```

### Additional context

Add any other context about the problem here.
