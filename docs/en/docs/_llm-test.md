# LLM test file { #llm-test-file }

This document tests if the <abbr title="Large Language Model">LLM</abbr> understands the instructions given in the general prompt in `scripts/translate.py` and those in the language specific prompt `docs/{language code}/llm-prompt.md`, (which are appended to the instructions in the general prompt). By adding special cases here, translation projects will become aware of them easier.

Use as follows:

* Do a fresh translation of this document into the desired target language.
* Check if things are mostly okay.
* If some things are not okay, but are fixable by improving the English document or the general or the language specific prompt, do that.
* Then manually fix the remaining issues in the translation, so that it is a good translation.
* Retranslate using the existing, good translation. The ideal result would be that the LLM makes no changes at all. That would mean that the general prompt and the language prompt are as good as they can be (It will sometimes make a few seemingly random changes, the reason is that <a href="https://doublespeak.chat/#/handbook#deterministic-output" class="external-link" target="_blank">LLMs are not deterministic algorithms</a>).


## Code snippets { #code-snippets}

This is a code snippet: `foo`. And this is another code snippet: `bar`. And another one: `baz quux`.


## Quotes { #quotes }

Yesterday, my friend wrote: "If you spell incorrectly correctly, you have spelled it incorrectly". To which I answered: "Correct, but 'incorrectly' is incorrectly not '"incorrectly"'".


## Quotes in code snippets { #quotes-in-code-snippets}

`pip install "foo[bar]"`

Examples for string literals in code snippets: `"this"`, `'that'`.

A difficult example for string literals in code snippets: `f"I like {'oranges' if orange else "apples"}"`

Hardcore: `Yesterday, my friend wrote: "If you spell incorrectly correctly, you have spelled it incorrectly". To which I answered: "Correct, but 'incorrectly' is incorrectly not '"incorrectly"'"`


## code blocks { #code-blocks }

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


## Tabs and colored boxes { #tabs-and-colored-boxes }

//// tab | This is a tab

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

//// tab | Here another tab

Hello

////


## Web- and internal links { #web-and-internal-links }

The link text should get translated, the link target should remain unchaged:

* [Link to heading above](#code-snippets)
* [Internal link](foo.md#bar){.internal-link target=_blank}
* <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">External link</a>
* <a href="https://fastapi.tiangolo.com/css/styles.css" class="external-link" target="_blank">Link to a style</a>
* <a href="https://fastapi.tiangolo.com/js/logic.js" class="external-link" target="_blank">Link to a script</a>
* <a href="https://fastapi.tiangolo.com/img/foo.jpg" class="external-link" target="_blank">Link to an image</a>

The link text should get translated, the link target should be the translation, not the English text:

* <a href="https://fastapi.tiangolo.com/" class="external-link" target="_blank">FastAPI link</a>


## HTML "abbr" elements { #html-abbr-elements }

Here some things wrapped in HTML "abbr" elements (Some are invented):

### Full phrase { #full-phrase }

* <abbr title="Getting Things Done">GTD</abbr>
* <abbr title="less than"><code>lt</code></abbr>
* <abbr title="XML Web Token">XWT</abbr>
* <abbr title="Parallel Server Gateway Interface">PSGI</abbr>

### Explanation { #explanation }

* <abbr title="A group of machines that are configured to be connected and work together in some way.">cluster</abbr>
* <abbr title="A method of machine learning that uses artificial neural networks with numerous hidden layers between input and output layers, thereby developing a comprehensive internal structure">Deep Learning</abbr>

### Full phrase: Explanation { #full-phrase-explanation }

* <abbr title="Mozilla Developer Network: documentation for developers, written by the Firefox people">MDN</abbr>
* <abbr title="Input/Output: disk reading or writing, network communications.">I/O</abbr>.


## Headings { #headings }

### Develop a webapp - a tutorial { #develop-a-webapp-a-tutorial }

Hello.

### Type hints and -annotations { #type-hints-and-annotations }

Hello again.

### Super- and subclasses { #super-and-subclasses }

Hello again.


## Terms used in the docs { #terms-used-in-the-docs }

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
