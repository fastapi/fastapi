# LLM test file { #llm-test-file }

This document tests if the <abbr title="Large Language Model">LLM</abbr>, which translates the documentation, understands the `general_prompt` in `scripts/translate.py` and the language specific prompt in `docs/{language code}/llm-prompt.md`. The language specific prompt is appended to `general_prompt`.

Tests added here will be seen by all designers of language specific prompts.

Use as follows:

* Have a language specific prompt – `docs/{language code}/llm-prompt.md`.
* Do a fresh translation of this document into your desired target language (see e.g. the `translate-page` command of the `translate.py`). This will create the translation under `docs/{language code}/docs/_llm-test.md`.
* Check if things are okay in the translation.
* If necessary, improve your language specific prompt, the general prompt, or the English document.
* Then manually fix the remaining issues in the translation, so that it is a good translation.
* Retranslate, having the good translation in place. The ideal result would be that the LLM makes no changes anymore to the translation. That means that the general prompt and your language specific prompt are as good as they can be (It will sometimes make a few seemingly random changes, the reason is that <a href="https://doublespeak.chat/#/handbook#deterministic-output" class="external-link" target="_blank">LLMs are not deterministic algorithms</a>).

The tests:

## Code snippets { #code-snippets}

//// tab | Test

This is a code snippet: `foo`. And this is another code snippet: `bar`. And another one: `baz quux`.

////

//// tab | Info

Content of code snippets should be left as is.

See section `### Content of code snippets` in the general prompt in `scripts/translate.py`.

////

## Quotes { #quotes }

//// tab | Test

Yesterday, my friend wrote: "If you spell incorrectly correctly, you have spelled it incorrectly". To which I answered: "Correct, but 'incorrectly' is incorrectly not '"incorrectly"'".

/// note

The LLM will probably translate this wrong. Interesting is only if it keeps the fixed translation when retranslating.

///

////

//// tab | Info

The prompt designer may choose if they want to convert neutral quotes to typographic quotes. It is okay to leave them as is.

See for example section `### Quotes` in `docs/de/llm-prompt.md`.

////

## Quotes in code snippets { #quotes-in-code-snippets}

//// tab | Test

`pip install "foo[bar]"`

Examples for string literals in code snippets: `"this"`, `'that'`.

A difficult example for string literals in code snippets: `f"I like {'oranges' if orange else "apples"}"`

Hardcore: `Yesterday, my friend wrote: "If you spell incorrectly correctly, you have spelled it incorrectly". To which I answered: "Correct, but 'incorrectly' is incorrectly not '"incorrectly"'"`

////

//// tab | Info

... However, quotes inside code snippets must stay as is.

////

## code blocks { #code-blocks }

//// tab | Test

A Bash code example...

```bash
# Print a greeting to the universe
echo "Hello universe"
```

...and a console code example...

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>
<span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting server
        Searching for package file structure
```

...and another console code example...

```console
// Create a directory "Code"
$ mkdir code
// Switch into that directory
$ cd code
```

...and a Python code example...

```Python
wont_work()  # This won't work 😱
works(foo="bar")  # This works 🎉
```

...and that's it.

////

//// tab | Info

Code in code blocks should not be modified, with the exception of comments.

See section `### Content of code blocks` in the general prompt in `scripts/translate.py`.

////

## Tabs and colored boxes { #tabs-and-colored-boxes }

//// tab | Test

/// info
Some text
///

/// note
Some text
///

/// note | Technical details
Some text
///

/// check
Some text
///

/// tip
Some text
///

/// warning
Some text
///

/// danger
Some text
///

////

//// tab | Info

Tabs and `Info`/`Note`/`Warning`/etc. blocks should have the translation of their title added after a vertical bar (`|`).

See sections `### Special blocks` and `### Tab blocks` in the general prompt in `scripts/translate.py`.

////

## Web- and internal links { #web-and-internal-links }

//// tab | Test

The link text should get translated, the link address should remain unchaged:

* [Link to heading above](#code-snippets)
* [Internal link](index.md#installation){.internal-link target=_blank}
* <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">External link</a>
* <a href="https://fastapi.tiangolo.com/css/styles.css" class="external-link" target="_blank">Link to a style</a>
* <a href="https://fastapi.tiangolo.com/js/logic.js" class="external-link" target="_blank">Link to a script</a>
* <a href="https://fastapi.tiangolo.com/img/foo.jpg" class="external-link" target="_blank">Link to an image</a>

The link text should get translated, the link address should point to the translation:

* <a href="https://fastapi.tiangolo.com/" class="external-link" target="_blank">FastAPI link</a>

////

//// tab | Info

Links should be translated, but their address shall remain unchanged. An exception are absolute links to pages of the FastAPI documentation. In that case it should link to the translation.

See section `### Links` in the general prompt in `scripts/translate.py`.

////

## HTML "abbr" elements { #html-abbr-elements }

//// tab | Test

Here some things wrapped in HTML "abbr" elements (Some are invented):

### The abbr gives a full phrase { #the-abbr-gives-a-full-phrase }

* <abbr title="Getting Things Done">GTD</abbr>
* <abbr title="less than"><code>lt</code></abbr>
* <abbr title="XML Web Token">XWT</abbr>
* <abbr title="Parallel Server Gateway Interface">PSGI</abbr>

### The abbr gives an explanation { #the-abbr-gives-an-explanation }

* <abbr title="A group of machines that are configured to be connected and work together in some way.">cluster</abbr>
* <abbr title="A method of machine learning that uses artificial neural networks with numerous hidden layers between input and output layers, thereby developing a comprehensive internal structure">Deep Learning</abbr>

### The abbr gives a full phrase and an explanation { #the-abbr-gives-a-full-phrase-and-an-explanation }

* <abbr title="Mozilla Developer Network: documentation for developers, written by the Firefox people">MDN</abbr>
* <abbr title="Input/Output: disk reading or writing, network communications.">I/O</abbr>.

////

//// tab | Info

"title" attributes of "abbr" elements are translated following some specific instructions.

Translations can add their own "abbr" elements which the LLM should not remove. E.g. to explain English words.

See section `### HTML abbr elements` in the general prompt in `scripts/translate.py`.

////

## Headings { #headings }

//// tab | Test

### Develop a webapp - a tutorial { #develop-a-webapp-a-tutorial }

Hello.

### Type hints and -annotations { #type-hints-and-annotations }

Hello again.

### Super- and subclasses { #super-and-subclasses }

Hello again.

////

//// tab | Info

The only hard rule for headings is that the LLM leaves the hash part inside curly brackets unchanged, which ensures that links do not break.

See section `### Headings` in the general prompt in `scripts/translate.py`.

For some language specific instructions, see e.g. section `### Headings` in `docs/de/llm-prompt.md`.

////

## Terms used in the docs { #terms-used-in-the-docs }

//// tab | Test

* you
* your

* e.g.
* etc.

* `foo` as an `int`
* `bar` as a `str`
* `baz` as a `list`

* the Tutorial - User guide
* the Advanced User Guide
* the SQLModel docs
* the API docs
* the automatic docs

* Data Science
* Deep Learning
* Machine Learning
* Dependency Injection
* HTTP Basic authentication
* HTTP Digest
* ISO format
* the JSON Schema standard
* the JSON schema
* the schema definition
* Password Flow
* Mobile

* deprecated
* designed
* invalid
* on the fly
* standard
* default
* case-sensitive
* case-insensitive

* to serve the application
* to serve the page

* the app
* the application

* the request
* the response
* the error response

* the path operation
* the path operation decorator
* the path operation function

* the body
* the request body
* the response body
* the JSON body
* the form body
* the file body
* the function body

* the parameter
* the body parameter
* the path parameter
* the query parameter
* the cookie parameter
* the header parameter
* the form parameter
* the function parameter

* the event
* the startup event
* the startup of the server
* the shutdown event
* the lifespan event

* the handler
* the event handler
* the exception handler
* to handle

* the model
* the Pydantic model
* the data model
* the database model
* the form model
* the model object

* the class
* the base class
* the parent class
* the subclass
* the child class
* the sibling class
* the class method

* the header
* the headers
* the authorization header
* the `Authorization` header
* the forwarded header

* the dependency injection system
* the dependency
* the dependable
* the dependant

* I/O bound
* CPU bound
* concurrency
* parallelism
* multiprocessing

* the env var
* the environment variable
* the `PATH`
* the `PATH` variable

* the authentication
* the authentication provider
* the authorization
* the authorization form
* the authorization provider
* the user authenticates
* the system authenticates the user

* the CLI
* the command line interface

* the server
* the client

* the cloud provider
* the cloud service

* the development
* the development stages

* the dict
* the dictionary
* the enumeration
* the enum
* the enum member

* the encoder
* the decoder
* to encode
* to decode

* the exception
* to raise

* the expression
* the statement

* the frontend
* the backend

* the GitHub discussion
* the GitHub issue

* the performance
* the performance optimization

* the return type
* the return value

* the security
* the security scheme

* the task
* the background task
* the task function

* the template
* the template engine

* the type annotation
* the type hint

* the server worker
* the Uvicorn worker
* the Gunicorn Worker
* the worker process
* the worker class
* the workload

* the deployment
* to deploy

* the SDK
* the software development kit

* the `APIRouter`
* the `requirements.txt`
* the Bearer Token
* the breaking change
* the bug
* the button
* the callable
* the code
* the commit
* the context manager
* the coroutine
* the database session
* the disk
* the domain
* the engine
* the fake X
* the HTTP GET method
* the item
* the library
* the lifespan
* the lock
* the middleware
* the mobile application
* the module
* the mounting
* the network
* the origin
* the override
* the payload
* the processor
* the property
* the proxy
* the pull request
* the query
* the RAM
* the remote machine
* the status code
* the string
* the tag
* the web framework
* the wildcard
* to return
* to validate

////

//// tab | Info

This is a not complete and not normative list of (mostly) technical terms seen in the docs. It may be helpful for the prompt designer to figure out for which terms the LLM needs a helping hand. For example when it keeps reverting a good translation to a suboptimal translation. Or when it has problems conjugating/declinating a term in your language.

See e.g. section `### List of English terms and their preferred German translations` in `docs/de/llm-prompt.md`.

////
