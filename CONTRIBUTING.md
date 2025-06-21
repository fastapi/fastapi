# Contributing to FastAPI

Thank you for your interest in contributing! 🎉

Please refer to the complete guide at:  
👉 [Development - Contributing](https://fastapi.tiangolo.com/contributing/)

---

## Code Style and Formatting

Before submitting a Pull Request, please make sure your code matches the project's style guidelines.

### Install `nox`

We use [nox](https://nox.thea.codes/) to run automated sessions like linters and formatters.

Install it using pip:

```bash
pip install nox
```
Then, run the linting session with:

```bash
nox -s lint
```
This command runs the same checks used in the continuous integration (CI) process to ensure your code follows the style conventions of the project.