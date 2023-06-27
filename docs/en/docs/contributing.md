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

=== "Linux, macOS"

    <div class="termy">

    ```console
    $ source ./env/bin/activate
    ```

    </div>

=== "Windows PowerShell"

    <div class="termy">

    ```console
    $ .\env\Scripts\Activate.ps1
    ```

    </div>

=== "Windows Bash"

    Or if you use Bash for Windows (e.g. <a href="https://gitforwindows.org/" class="external-link" target="_blank">Git Bash</a>):

    <div class="termy">

    ```console
    $ source ./env/Scripts/activate
    ```

    </div>

To check it worked, use:

=== "Linux, macOS, Windows Bash"

    <div class="termy">

    ```console
    $ which pip

    some/directory/fastapi/env/bin/pip
    ```

    </div>

=== "Windows PowerShell"

    <div class="termy">

    ```console
    $ Get-Command pip

    some/directory/fastapi/env/bin/pip
    ```

    </div>

If it shows the `pip` binary at `env/bin/pip` then it worked. 🎉

Make sure you have the latest pip version on your virtual environment to avoid errors on the next steps:

<div class="termy">

```console
$ python -m pip install --upgrade pip

---> 100%
```

</div>

!!! tip
    Every time you install a new package with `pip` under that environment, activate the environment again.

    This makes sure that if you use a terminal program installed by that package, you use the one from your local environment and not any other that could be installed globally.

### pip

After activating the environment as described above:

<div class="termy">

```console
$ pip install -r requirements.txt

---> 100%
```

</div>

It will install all the dependencies and your local FastAPI in your local environment.

#### Using your local FastAPI

If you create a Python file that imports and uses FastAPI, and run it with the Python from your local environment, it will use your local FastAPI source code.

And if you update that local FastAPI source code when you run that Python file again, it will use the fresh version of FastAPI you just edited.

That way, you don't have to "install" your local version to be able to test every change.

!!! note "Technical Details"
    This only happens when you install using this included `requiements.txt` instead of installing `pip install fastapi` directly.

    That is because inside of the `requirements.txt` file, the local version of FastAPI is marked to be installed in "editable" mode, with the `-e` option.

### Format

There is a script that you can run that will format and clean all your code:

<div class="termy">

```console
$ bash scripts/format.sh
```

</div>

It will also auto-sort all your imports.

For it to sort them correctly, you need to have FastAPI installed locally in your environment, with the command in the section above using `-e`.

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

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

</div>

It will serve the documentation on `http://127.0.0.1:8008`.

That way, you can edit the documentation/source files and see the changes live.

!!! tip
    Alternatively, you can perform the same steps that scripts does manually.

    Go into the language directory, for the main docs in English it's at `docs/en/`:

    ```console
    $ cd docs/en/
    ```

    Then run `mkdocs` in that directory:

    ```console
    $ mkdocs serve --dev-addr 8008
    ```

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

#### Tips and guidelines

* Check the currently <a href="https://github.com/tiangolo/fastapi/pulls" class="external-link" target="_blank">existing pull requests</a> for your language and add reviews requesting changes or approving them.

!!! tip
    You can <a href="https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/commenting-on-a-pull-request" class="external-link" target="_blank">add comments with change suggestions</a> to existing pull requests.

    Check the docs about <a href="https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-request-reviews" class="external-link" target="_blank">adding a pull request review</a> to approve it or request changes.

* Check if there's a <a href="https://github.com/tiangolo/fastapi/discussions/categories/translations" class="external-link" target="_blank">GitHub Discussion</a> to coordinate translations for your language. You can subscribe to it, and when there's a new pull request to review, an automatic comment will be added to the discussion.

* Add a single pull request per page translated. That will make it much easier for others to review it.

For the languages I don't speak, I'll wait for several others to review the translation before merging.

* You can also check if there are translations for your language and add a review to them, that will help me know that the translation is correct and I can merge it.
    * You could check in the <a href="https://github.com/tiangolo/fastapi/discussions/categories/translations" class="external-link" target="_blank">GitHub Discussions</a> for your language.
    * Or you can filter the existing PRs by the ones with the label for your language, for example, for Spanish, the label is <a href="https://github.com/tiangolo/fastapi/pulls?q=is%3Apr+is%3Aopen+sort%3Aupdated-desc+label%3Alang-es+label%3A%22awaiting+review%22" class="external-link" target="_blank">`lang-es`</a>.

* Use the same Python examples and only translate the text in the docs. You don't have to change anything for this to work.

* Use the same images, file names, and links. You don't have to change anything for it to work.

* To check the 2-letter code for the language you want to translate you can use the table <a href="https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes" class="external-link" target="_blank">List of ISO 639-1 codes</a>.

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

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

</div>

!!! tip
    Alternatively, you can perform the same steps that scripts does manually.

    Go into the language directory, for the Spanish translations it's at `docs/es/`:

    ```console
    $ cd docs/es/
    ```

    Then run `mkdocs` in that directory:

    ```console
    $ mkdocs serve --dev-addr 8008
    ```

Now you can go to <a href="http://127.0.0.1:8008" class="external-link" target="_blank">http://127.0.0.1:8008</a> and see your changes live.

You will see that every language has all the pages. But some pages are not translated and have a notification about the missing translation.

Now let's say that you want to add a translation for the section [Features](features.md){.internal-link target=_blank}.

* Copy the file at:

```
docs/en/docs/features.md
```

* Paste it in exactly the same location but for the language you want to translate, e.g.:

```
docs/es/docs/features.md
```

!!! tip
    Notice that the only change in the path and file name is the language code, from `en` to `es`.

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
```

</div>

Now you can check in your code editor the newly created directory `docs/ht/`.

That command created a file `docs/ht/mkdocs.yml` with a simple config that inherits everything from the `en` version:

```yaml
INHERIT: ../en/mkdocs.yml
```

!!! tip
    You could also simply create that file with those contents manually.

That command also created a dummy file `docs/ht/index.md` for the main page, you can start by translating that one.

You can continue with the previous instructions for an "Existing Language" for that process.

You can make the first pull request with those two files, `docs/ht/mkdocs.yml` and `docs/ht/index.md`. 🎉

#### Preview the result

You can use the `./scripts/docs.py` with the `live` command to preview the results (or `mkdocs serve`).

Once you are done, you can also test it all as it would look online, including all the other languages.

To do that, first build all the docs:

<div class="termy">

```console
// Use the command "build-all", this will take a bit
$ python ./scripts/docs.py build-all

Building docs for: en
Building docs for: es
Successfully built docs for: es
```

</div>

This builds all those independent MkDocs sites for each language, combines them, and generates the final output at `./site/`.

Then you can serve that with the command `serve`:

<div class="termy">

```console
// Use the command "serve" after running "build-all"
$ python ./scripts/docs.py serve

Warning: this is a very simple server. For development, use mkdocs serve instead.
This is here only to preview a site with translations already built.
Make sure you run the build-all command first.
Serving at: http://127.0.0.1:8008
```

</div>

## Tests

There is a script that you can run locally to test all the code and generate coverage reports in HTML:

<div class="termy">

```console
$ bash scripts/test-cov-html.sh
```

</div>

This command generates a directory `./htmlcov/`, if you open the file `./htmlcov/index.html` in your browser, you can explore interactively the regions of code that are covered by the tests, and notice if there is any region missing.
