First, you might want to see the basic ways to [help FastAPI and get help](help-fastapi.md){.internal-link target=_blank}.

## Developing

If you already cloned the repository and you know that you need to deep dive in the code, here are some guidelines to set up your environment.

### Virtual environment with `venv`

You can create a virtual environment in a directory using Python's `venv` module:

```console
$ python -m venv env
```

That will create a directory `./env/` with the Python binaries and then you will be able to install packages for that isolated environment.

### Activate the environment

Activate the new environment with:

```console
$ source ./env/bin/activate
```

Or in Windows' PowerShell:

```console
$ .\env\Scripts\Activate.ps1
```

Or if you use Bash for Windows (e.g. <a href="https://gitforwindows.org/" class="external-link" target="_blank">Git Bash</a>):

```console
$ source ./env/Scripts/activate
```

To check it worked, use:

```console
$ which pip

some/directory/fastapi/env/bin/pip
```

If it shows the `pip` binary at `env/bin/pip` then it worked. 🎉

Or in Windows PowerShell:

```console
$ Get-Command pip

some/directory/fastapi/env/bin/pip
```
!!! tip
    Every time you install a new package with `pip` under that environment, activate the environment again.

    This makes sure that if you use a terminal program installed by that package (like `flit`), you use the one from your local environment and not any other that could be installed globally.

### Flit

**FastAPI** uses <a href="https://flit.readthedocs.io/en/latest/index.html" class="external-link" target="_blank">Flit</a> to build, package and publish the project.

After activating the environment  as described above, install `flit`:

```console
$ pip install flit
```

Now re-activate the environment to make sure you are using the `flit` you just installed (and not a global one).

And now use `flit` to install the development dependencies:

```console
$ flit install --deps develop --symlink
```

It will install all the dependencies and your local FastAPI in your local environment.

#### Using your local FastAPI

If you create a Python file that imports and uses FastAPI, and run it with the Python from your local environment, it will use your local FastAPI source code.

And if you update that local FastAPI source code, as it is installed with `--symlink`, when you run that Python file again, it will use the fresh version of FastAPI you just edited.

That way, you don't have to "install" your local version to be able to test every change.

### Format

There is a script that you can run that will format and clean all your code:

```console
$ bash scripts/format.sh
```

It will also auto-sort all your imports.

For it to sort them correctly, you need to have FastAPI installed locally in your environment, with the command in the section above:

```console
$ flit install --symlink
```

### Format imports

There is another script that formats all the imports and makes sure you don't have unused imports:

```console
$ bash scripts/format-imports.sh
```

As it runs one command after the other and modifies and reverts many files, it takes a bit longer to run, so it might be easier to use `scripts/format.sh` frequently and `scripts/format-imports.sh` only before committing.

## Docs

The documentation uses <a href="https://www.mkdocs.org/" class="external-link" target="_blank">MkDocs</a>.

All the documentation is in Markdown format in the directory `./docs`.

Many of the tutorials have blocks of code.

In most of the cases, these blocks of code are actual complete applications that can be run as is.

In fact, those blocks of code are not written inside the Markdown, they are Python files in the `./docs/src/` directory.

And those Python files are included/injected in the documentation when generating the site.

### Docs for tests

Most of the tests actually run against the example source files in the documentation.

This helps making sure that:

* The documentation is up to date.
* The documentation examples can be run as is.
* Most of the features are covered by the documentation, ensured by test coverage.

During local development, there is a script that builds the site and checks for any changes, live-reloading:

```console
$ bash scripts/docs-live.sh
```

It will serve the documentation on `http://0.0.0.0:8008`.

That way, you can edit the documentation/source files and see the changes live.

### Apps and docs at the same time

If you run the examples with, e.g.:

```console
$ uvicorn tutorial001:app --reload
```

as Uvicorn by default will use the port `8000`, the documentation on port `8008` won't clash.

## Tests

There is a script that you can run locally to test all the code and generate coverage reports in HTML:

```console
$ bash scripts/test-cov-html.sh
```

This command generates a directory `./htmlcov/`, if you open the file `./htmlcov/index.html` in your browser, you can explore interactively the regions of code that are covered by the tests, and notice if there is any region missing.

### Tests in your editor

If you want to use the integrated tests in your editor add `./docs/src` to your `PYTHONPATH` variable.

For example, in VS Code you can create a file `.env` with:

```env
PYTHONPATH=./docs/src
```
