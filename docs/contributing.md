First, you might want to see the basic ways to <a href="https://fastapi.tiangolo.com/help-fastapi/" target="_blank">help FastAPI and get help</a>.

## Developing

If you already cloned the repository and you know that you need to deep dive in the code, here are some guidelines to set up your environment.


### Pipenv

If you are using <a href="https://pipenv.readthedocs.io/en/latest/" target="_blank">Pipenv</a>, you can create a virtual environment and install the packages with:

```bash
pipenv install --dev
```

Then you can activate that virtual environment with:

```bash
pipenv shell
```


### No Pipenv

If you are not using Pipenv, you can create a virtual environment with your preferred tool, and install the packages listed in the file `Pipfile`.


### Flit

**FastAPI** uses <a href="https://flit.readthedocs.io/en/latest/index.html" target="_blank">Flit</a> to build, package and publish the project.

If you installed the development dependencies with one of the methods above, you already have the `flit` command.

To install your local version of FastAPI as a package in your local environment, run:

```bash
flit install --symlink
```

It will install your local FastAPI in your local environment.


#### Using your local FastAPI

If you create a Python file that imports and uses FastAPI, and run it with the Python from your local environment, it will use your local FastAPI source code.

And if you update that local FastAPI source code, as it is installed with `--symlink`, when you run that Python file again, it will use the fresh version of FastAPI you just edited.

That way, you don't have to "install" your local version to be able to test every change.


### Format

There is a script that you can run that will format and clean all your code:

```bash
bash scripts/lint.sh
```

It will also auto-sort all your imports.

For it to sort them correctly, you need to have FastAPI installed locally in your environment, with the command in the section above:

```bash
flit install --symlink
```


### Docs

The documentation uses <a href="https://www.mkdocs.org/" target="_blank">MkDocs</a>.

All the documentation is in Markdown format in the directory `./docs`.

Many of the tutorials have blocks of code.

In most of the cases, these blocks of code are actual complete applications that can be run as is.

In fact, those blocks of code are not written inside the Markdown, they are Python files in the `./docs/src/` directory.

And those Python files are included/injected in the documentation when generating the site.


#### Docs for tests

Most of the tests actually run against the example source files in the documentation.

This helps making sure that:

* The documentation is up to date.
* The documentation examples can be run as is.
* Most of the features are covered by the documentation, ensured by the coverage tests.

During local development, there is a script that builds the site and checks for any changes, live-reloading:

```bash
bash scripts/docs-live.sh
```

It will serve the documentation on `http://0.0.0.0:8008`.

That way, you can edit the documentation/source files and see the changes live.

#### Apps and docs at the same time

And if you run the examples with, e.g.:

```bash
uvicorn tutorial001:app --debug
```

as Uvicorn by default will use the port `8000`, the documentation on port `8008` won't clash.


### Tests

There is a script that you can run locally to test all the code and generate coverage reports in HTML:

```bash
bash scripts/test-cov-html.sh
```

This command generates a directory `./htmlcov/`, if you open the file `./htmlcov/index.html` in your browser, you can explore interactively the regions of code that are covered by the tests, and notice if there is any region missing.
