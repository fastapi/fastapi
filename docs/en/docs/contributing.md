# Development - Contributing

First, you might want to see the basic ways to [help FastAPI and get help](help-fastapi.md){.internal-link target=_blank}.

## Developing

If you already cloned the <a href="https://github.com/fastapi/fastapi" class="external-link" target="_blank">fastapi repository</a> and you want to deep dive in the code, here are some guidelines to set up your environment.

### Install requirements

Create a virtual environment and install the required packages with <a href="https://github.com/astral-sh/uv" class="external-link" target="_blank">`uv`</a>:

<div class="termy">

```console
$ uv sync

---> 100%
```

</div>

It will install all the dependencies and your local FastAPI in your local environment.

### Using your local FastAPI

If you create a Python file that imports and uses FastAPI, and run it with the Python from your local environment, it will use your cloned local FastAPI source code.

And if you update that local FastAPI source code when you run that Python file again, it will use the fresh version of FastAPI you just edited.

That way, you don't have to "install" your local version to be able to test every change.

/// note | Technical Details

This only happens when you install using `uv sync` instead of running `pip install fastapi` directly.

That is because `uv sync` will install the local version of FastAPI in "editable" mode by default.

///

### Format the code

There is a script that you can run that will format and clean all your code:

<div class="termy">

```console
$ bash scripts/format.sh
```

</div>

It will also auto-sort all your imports.

## Tests

There is a script that you can run locally to test all the code and generate coverage reports in HTML:

<div class="termy">

```console
$ bash scripts/test-cov-html.sh
```

</div>

This command generates a directory `./htmlcov/`, if you open the file `./htmlcov/index.html` in your browser, you can explore interactively the regions of code that are covered by the tests, and notice if there is any region missing.

## Docs

First, make sure you set up your environment as described above, that will install all the requirements.

### Docs live

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

/// tip

Alternatively, you can perform the same steps that scripts does manually.

Go into the language directory, for the main docs in English it's at `docs/en/`:

```console
$ cd docs/en/
```

Then run `mkdocs` in that directory:

```console
$ mkdocs serve --dev-addr 127.0.0.1:8008
```

///

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

### Docs Structure

The documentation uses <a href="https://www.mkdocs.org/" class="external-link" target="_blank">MkDocs</a>.

And there are extra tools/scripts in place to handle translations in `./scripts/docs.py`.

/// tip

You don't need to see the code in `./scripts/docs.py`, you just use it in the command line.

///

All the documentation is in Markdown format in the directory `./docs/en/`.

Many of the tutorials have blocks of code.

In most of the cases, these blocks of code are actual complete applications that can be run as is.

In fact, those blocks of code are not written inside the Markdown, they are Python files in the `./docs_src/` directory.

And those Python files are included/injected in the documentation when generating the site.

### Docs for tests

Most of the tests actually run against the example source files in the documentation.

This helps to make sure that:

* The documentation is up-to-date.
* The documentation examples can be run as is.
* Most of the features are covered by the documentation, ensured by test coverage.

#### Apps and docs at the same time

If you run the examples with, e.g.:

<div class="termy">

```console
$ fastapi dev tutorial001.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

as Uvicorn by default will use the port `8000`, the documentation on port `8008` won't clash.

### Translations

Help with translations is VERY MUCH appreciated! And it can't be done without the help from the community. 🌎 🚀

Here are the steps to help with translations.

#### Review Translation PRs

Translation pull requests are made by LLMs guided with prompts designed by the FastAPI team together with the community of native speakers for each supported language.

These translations are normally still reviewed by native speakers, and here's where you can help!

* Check the currently <a href="https://github.com/fastapi/fastapi/pulls" class="external-link" target="_blank">existing pull requests</a> for your language. You can filter the pull requests by the ones with the label for your language. For example, for Spanish, the label is <a href="https://github.com/fastapi/fastapi/pulls?q=is%3Aopen+sort%3Aupdated-desc+label%3Alang-es+label%3Aawaiting-review" class="external-link" target="_blank">`lang-es`</a>.

* When reviewing a pull request, it's better not to suggest changes in the same pull request, because it is LLM generated, and it won't be possible to make sure that small individual changes are replicated in other similar sections, or that they are preserved when translating the same content again.

* Instead of adding suggestions to the translation PR, make the suggestions to the LLM prompt file for that language, in a new PR. For example, for Spanish, the LLM prompt file is at: <a href="https://github.com/fastapi/fastapi/blob/master/docs/es/llm-prompt.md" class="external-link" target="_blank">`docs/es/llm-prompt.md`</a>.

/// tip

Check the docs about <a href="https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-request-reviews" class="external-link" target="_blank">adding a pull request review</a> to approve it or request changes.

///

#### Subscribe to Notifications for Your Language

* Check if there's a <a href="https://github.com/fastapi/fastapi/discussions/categories/translations" class="external-link" target="_blank">GitHub Discussion</a> to coordinate translations for your language. You can subscribe to it, and when there's a new pull request to review, an automatic comment will be added to the discussion.

* To check the 2-letter code for the language you want to translate, you can use the table <a href="https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes" class="external-link" target="_blank">List of ISO 639-1 codes</a>.

#### Request a New Language

Let's say that you want to request translations for a language that is not yet translated, not even some pages. For example, Latin.

* The first step would be for you to find other 2 people that would be willing to be reviewing translation PRs for that language with you.
* Once there are at least 3 people that would be willing to commit to help maintain that language, you can continue the next steps.
* Create a new discussion following the template.
* Tag the other 2 people that will help with the language, and ask them to confirm there they will help.

Once there are several people in the discussion, the FastAPI team can evaluate it and can make it an official translation.

Then the docs will be automatically translated using LLMs, and the team of native speakers can review the translation, and help tweak the LLM prompts.

Once there's a new translation, for example if docs are updated or there's a new section, there will be a comment in the same discussion with the link to the new translation to review.

## Automated Code and AI

You are encouraged to use all the tools you want to do your work and contribute as efficiently as possible, this includes AI (LLM) tools, etc. Nevertheless, contributions should have meaningful human intervention, judgement, context, etc.

If the **human effort** put in a PR, e.g. writing LLM prompts, is **less** than the **effort we would need to put** to **review it**, please **don't** submit the PR.

Think of it this way: we can already write LLM prompts or run automated tools ourselves, and that would be faster than reviewing external PRs.

### Closing Automated and AI PRs

If we see PRs that seem AI generated or automated in similar ways, we'll flag them and close them.

The same applies to comments and descriptions, please don't copy paste the content generated by an LLM.

### Human Effort Denial of Service

Using automated tools and AI to submit PRs or comments that we have to carefully review and handle would be the equivalent of a <a href="https://en.wikipedia.org/wiki/Denial-of-service_attack" class="external-link" target="_blank">Denial-of-service attack</a> on our human effort.

It would be very little effort from the person submitting the PR (an LLM prompt) that generates a large amount of effort on our side (carefully reviewing code).

Please don't do that.

We'll need to block accounts that spam us with repeated automated PRs or comments.

### Use Tools Wisely

As Uncle Ben said:

<blockquote>
With great <strike>power</strike> <strong>tools</strong> comes great responsibility.
</blockquote>

Avoid inadvertently doing harm.

You have amazing tools at hand, use them wisely to help effectively.
