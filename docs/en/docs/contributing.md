# Development - Contributing

First, you might want to see the basic ways to [help FastAPI and get help](help-fastapi.md){.internal-link target=_blank}.

## Developing

If you already cloned the repository and you know that you need to deep dive in the code, here are some guidelines to set up your environment.

### Virtual environment with `venv`

You can create a virtual environment in a directory using Python's `venv` module:

<div class="termy">

```console
$ python -m venv env
```

</div>

That will create a directory `./env/` with the Python binaries and then you will be able to install packages for that isolated environment.

### Activate the environment

Activate the new environment with:

<div class="termy">

```console
$ source ./env/bin/activate
```

</div>

Or in Windows' PowerShell:

<div class="termy">

```console
$ .\env\Scripts\Activate.ps1
```

</div>

Or if you use Bash for Windows (e.g. <a href="https://gitforwindows.org/" class="external-link" target="_blank">Git Bash</a>):

<div class="termy">

```console
$ source ./env/Scripts/activate
```

</div>

To check it worked, use:

<div class="termy">

```console
$ which pip

some/directory/fastapi/env/bin/pip
```

</div>

If it shows the `pip` binary at `env/bin/pip` then it worked. 🎉

Or in Windows PowerShell:

<div class="termy">

```console
$ Get-Command pip

some/directory/fastapi/env/bin/pip
```

</div>

!!! tip
    Every time you install a new package with `pip` under that environment, activate the environment again.

    This makes sure that if you use a terminal program installed by that package (like `flit`), you use the one from your local environment and not any other that could be installed globally.

### Flit

**FastAPI** uses <a href="https://flit.readthedocs.io/en/latest/index.html" class="external-link" target="_blank">Flit</a> to build, package and publish the project.

After activating the environment as described above, install `flit`:

<div class="termy">

```console
$ pip install flit

---> 100%
```

</div>

Now re-activate the environment to make sure you are using the `flit` you just installed (and not a global one).

And now use `flit` to install the development dependencies:

<div class="termy">

```console
$ flit install --deps develop --symlink

---> 100%
```

</div>

It will install all the dependencies and your local FastAPI in your local environment.

#### Using your local FastAPI

If you create a Python file that imports and uses FastAPI, and run it with the Python from your local environment, it will use your local FastAPI source code.

And if you update that local FastAPI source code, as it is installed with `--symlink`, when you run that Python file again, it will use the fresh version of FastAPI you just edited.

That way, you don't have to "install" your local version to be able to test every change.

### Format

There is a script that you can run that will format and clean all your code:

<div class="termy">

```console
$ bash scripts/format.sh
```

</div>

It will also auto-sort all your imports.

For it to sort them correctly, you need to have FastAPI installed locally in your environment, with the command in the section above:

<div class="termy">

```console
$ flit install --symlink

---> 100%
```

</div>

### Format imports

There is another script that formats all the imports and makes sure you don't have unused imports:

<div class="termy">

```console
$ bash scripts/format-imports.sh
```

</div>

As it runs one command after the other and modifies and reverts many files, it takes a bit longer to run, so it might be easier to use `scripts/format.sh` frequently and `scripts/format-imports.sh` only before committing.

## Docs

First, make sure you set up your environment as described above, that will install all the requirements.

The documentation uses <a href="https://www.mkdocs.org/" class="external-link" target="_blank">MkDocs</a>.

And there are extra tools/scripts in place to handle translations in `./scripts/docs.py`.

!!! tip
    You don't need to see the code in `./scripts/docs.py`, you just use it in the command line.

All the documentation is in Markdown format in the directory `./docs/en/`.

Many of the tutorials have blocks of code.

In most of the cases, these blocks of code are actual complete applications that can be run as is.

In fact, those blocks of code are not written inside the Markdown, they are Python files in the `./docs_src/` directory.

And those Python files are included/injected in the documentation when generating the site.

### Docs for tests

Most of the tests actually run against the example source files in the documentation.

This helps making sure that:

* The documentation is up to date.
* The documentation examples can be run as is.
* Most of the features are covered by the documentation, ensured by test coverage.

During local development, there is a script that builds the site and checks for any changes, live-reloading:

<div class="termy">

```console
$ python ./scripts/docs.py live

<span style="color: green;">[INFO]</span> Serving on http://0.0.0.0:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

</div>

It will serve the documentation on `http://0.0.0.0:8008`.

That way, you can edit the documentation/source files and see the changes live.

#### Typer CLI (optional)

The instructions here show you how to use the script at `./scripts/docs.py` with the `python` program directly.

But you can also use <a href="https://typer.tiangolo.com/typer-cli/" class="external-link" target="_blank">Typer CLI</a>, and you will get autocompletion in your terminal for the commands after installing completion.

If you install Typer CLI, you can install completion with:

<div class="termy">

```console
$ typer --install-completion

zsh completion installed in /home/user/.bashrc.
Completion will take effect once you restart the terminal.
```

</div>

### Apps and docs at the same time

If you run the examples with, e.g.:

<div class="termy">

```console
$ uvicorn tutorial001:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

as Uvicorn by default will use the port `8000`, the documentation on port `8008` won't clash.

### Translations

Help with translations is VERY MUCH appreciated! And it can't be done without the help from the community. 🌎 🚀

Here are the steps to help with translations.

#### Tips

✨ Add a single Pull Request per page translated. That will make it much easier for others to review it.

For the languages I don't speak, I'll wait for several others to review the translation before merging.

✨ You can also check if there are translations for your language and add a review to them, that will help me know that the translation is correct and I can merge it.

✨ To check the 2-letter code for the language you want to translate you can use the table <a href="https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes" class="external-link" target="_blank">List of ISO 639-1 codes</a>.

#### Existing language

Let's say you want to translate a page for a language that already has translations for some pages, like Spanish.

In the case of Spanish, the 2-letter code is `es`. So, the directory for Spanish translations is located at `docs/es/`.

!!! tip
    The main ("official") language is English, located at `docs/en/`.

Now run the live server for the docs in Spanish:

<div class="termy">

```console
// Use the command "live" and pass the language code as a CLI argument
$ python ./scripts/docs.py live es

<span style="color: green;">[INFO]</span> Serving on http://0.0.0.0:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

</div>

Now you can go to <a href="http://0.0.0.0:8008" class="external-link" target="_blank">http://0.0.0.0:8008</a> and see your changes live.

If you look at the FastAPI docs website, you will see that every language has all the pages. But some are not translated and have a notification about the the translation is missing.

But when you run it locally like this, you will only see the pages that are already translated.

Now let's say that you want to add a translation for the section [Advanced User Guide: Extending OpenAPI](advanced/extending-openapi.md){.internal-link target=_blank}.

* Copy the file at:

```
docs/en/docs/advanced/extending-openapi.md
```

* Paste it in exactly the same location but for the language you want to translate, e.g.:

```
docs/es/docs/advanced/extending-openapi.md
```

!!! tip
    Notice that the only change in the path and file name is the language code, from `en` to `es`.

* Now open the MkDocs config file at:

```
docs/en/docs/mkdocs.yml
```

* Find the place where that `advanced/extending-openapi.md` is located in the config file. Somewhere like:

```YAML hl_lines="9"
site_name: FastAPI
# More stuff
nav:
- FastAPI: index.md
# More stuff
- Advanced User Guide:
    # More stuff
    - advanced/testing-dependencies.md
    - advanced/extending-openapi.md
    - advanced/openapi-callbacks.md
```

* Open the MkDocs config file for the language you are editing, e.g.:

```
docs/es/docs/mkdocs.yml
```

* Add the equivalent structure code and add it at the exact same location it would be, e.g.:

```YAML hl_lines="6  9"
site_name: FastAPI
# More stuff
nav:
- FastAPI: index.md
# More stuff
- Guía de Usuario Avanzada:
    # More stuff
    - advanced/testing-dependencies.md
    - advanced/extending-openapi.md
    - advanced/openapi-callbacks.md
```

Notice that the `Advanced User Guide` is translated to `Guía de Usuario Avanzada`.

Also, make sure that if there are other entries, the new entry with your translation is in exactly in the same order as in the English version.

If you go to your browser you will see that now the docs show your new section. 🎉

Now you can translate it all and see how it looks as you save the file.

#### New Language

Let's say that you want to add translations for a language that is not yet translated, not even some pages.

Let's say you want to add translations for Creole, and it's not yet there in the docs.

Checking the link from above, the code for "Creole" is `ht`.

The next step is to run the script to generate a new translation directory:

<div class="termy">

```console
// Use the command new-lang, pass the language code as a CLI argument
$ python ./scripts/docs.py new-lang ht

Successfully initialized: docs/ht
Updating ht
Updating en
```

</div>

Now you can check in your code editor the newly created directory `docs/ht/`.

Start by translating the main page, `docs/ht/index.md`.

Then you can continue with the previous instructions, for an "Existing Language".

##### New Language not supported

If when running the live server script you get an error about the language not being supported, something like:

```
 raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: partials/language/xx.html
```

That means that the theme doesn't support that language (in this case, with a fake 2-letter code of `xx`).

But don't worry, you can set the theme language to English and then translate the content of the docs.

If you need to do that, edit the `mkdocs.yml` for your new language, it will have something like:

```YAML hl_lines="5"
site_name: FastAPI
# More stuff
theme:
  # More stuff
  language: xx
```

Change that language from `xx` (from your language code) to `en`.

Then you can start the live server again.

## Tests

There is a script that you can run locally to test all the code and generate coverage reports in HTML:

<div class="termy">

```console
$ bash scripts/test-cov-html.sh
```

</div>

This command generates a directory `./htmlcov/`, if you open the file `./htmlcov/index.html` in your browser, you can explore interactively the regions of code that are covered by the tests, and notice if there is any region missing.

### Tests in your editor

If you want to use the integrated tests in your editor add `./docs/src` to your `PYTHONPATH` variable.

For example, in VS Code you can create a file `.env` with:

```env
PYTHONPATH=./docs/src
```
