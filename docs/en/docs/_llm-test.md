# LLM test { #llm-test }

This document tests if the <abbr title="Large Language Model">LLM</abbr> understands the instructions given in the general prompt in `scripts/translate.py` and those in the language specific prompt `docs/{language code}/llm-prompt.md`, (which are appended to the instructions in the general prompt).

Use as follows:

* Do a fresh translation of this document into the desired target language.
* Check if things are mostly okay.
* If some things are not okay, but are fixable by improving the English document or the general or the language specific prompt, do that.
* Then manually fix the remaining issues in the translation, so that it is a good translation.
* Retranslate using the existing, good translation. The ideal result should be that the LLM makes no changes at all. That would mean that the general prompt and the language prompt are as good as they can be (Plot twist: It will usually make a few seemingly random changes, the reason is probably that <a href="https://doublespeak.chat/#/handbook#deterministic-output" class="external-link" target="_blank">LLMs are not deterministic algorithms</a>).

The idea is, that, when working on a translation for a language (assumed one is able to run `scripts/translate.py`), to include examples of found special cases here (not a detailed list, just examples for such special cases) and test with this document, rather than testing with every other single document, translating it multiple times, which costs a few cents per translation. Also, by adding such special cases here, other translation projects will also become aware of such special cases.

## Code snippets { #code-snippets}

This is a code snippet: `foo`. And this is another code snippet: `bar`. And another one: `baz quux`.

## Quotes { #quotes }

Yesterday, my friend wrote: "If you spell incorrectly correctly, you have spelled it incorrectly". To which I answered: "Correct, but 'incorrectly' is incorrectly not '"incorrectly"'".

## Quotes in code snippets { #quotes-in-code-snippets}

`pip install "foo[bar]"`

Examples for string literals in code snippets: `"this"`, `'that'`.

A difficult example for string literals in code snippets: `f"I like {'oranges' if orange else "apples"}"`

Hardcore: `Yesterday my friend wrote: "If you spell incorrectly correctly you have spelled it incorrectly". To which I answered: "Correct, but 'incorrectly' is incorrectly not '"incorrectly"'!"`

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

## Web- and internal links { #web-and-internal-links }

[Link to heading above](#code-snippets)

<a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">External link</a>

<a href="https://fastapi.tiangolo.com/the/link/#target" class="external-link" target="_blank">FastAPI link</a>

<a href="https://fastapi.tiangolo.com/css/styles.css" class="external-link" target="_blank">Link to a style</a>
<a href="https://fastapi.tiangolo.com/js/logic.js" class="external-link" target="_blank">Link to a script</a>
<a href="https://fastapi.tiangolo.com/img/foo.jpg" class="external-link" target="_blank">Link to an image</a>

[Internal link](foo.md#bar){.internal-link target=_blank}

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

* <abbr title="Mozilla Developer Network: Documentation for developers, written by the Firefox people">MDN</abbr>
* <abbr title="Input/Output: disk reading or writing, network communications.">I/O</abbr>.

## Headings { #headings }

### Develop a webapp - a tutorial { #develop-a-webapp-a-tutorial }

Hello.

### Type hints and -annotations { #type-hints-and-annotations }

Hello again.

### Super- and subclasses { #super-and-subclasses }

Hello again.

## Sentences with preferred translations, (maybe) defined in the language prompt { #sentences-with-preferred-translations-maybe-defined-in-the-language-prompt }

I welcome you.
I admire your pullover.
She likes fruits e.g. apples
He likes oranges, bananas, etc.
Read the docs.
Read the Tutorial - User guide.
Then read the Advanced User Guide.
If this env var exists, do something.
Read the `PATH` environment variable.
Which is the same as the `PATH`.
Install from the `requirements.txt`.
Use the API Router.
Start the app.
Create the application.
This is the Authorization-Header.
This is the `Authorization`-Header.
Waiting for the background task.
Press the button.
Try this cloud provider.
Use the CLI.
Which is the command line interface.
The default value is "foo".
The default declaration is "bar".
Dictionaries, or dicts, are useful data structures.
Enumerations, or Enums, have their use too.
The engine will do that.
Return an error response.
Wait for the event.
Raise the exception.
The exception handler handles it.
Defining the form model.
Sending the form body.
Accessing the header.
Modifying the headers.
Spelling in headers.
The forwarded headers are often used in connection with proxies.
Listening to the lifespan event.
Locking means, we lock a thing to safely modify it.
Developing a mobile application.
Defining the model object.
Something waits for the mounting.
It is now mounted.
Another origin.
We have an override for this.
The function has one parameter.
The function parameter is an int.
The function has many parameters.
The default parameter is a bool.
The body parameter contains the body of the request.
Also called the request body parameter.
The path parameter contains a variable in the request path.
The query parameter contains the query parameters in the request path.
The cookie parameter contains the request cookies.
The header parameter contains the request headers.
The form parameter contains the request's form fields.
The payload is the request/response without metadata.
This query asks for items older than a week.
Recap: It's smooth.
The request has been received.
Receiving the request body.
Receiving the request bodies.
Returning the response.
What a function returns has a return value.
And a return type.
We are listening to the startup and shutdown events.
We are waiting for the startup of the server.
Details are described in the SQLModel docs.
Use the SDK.
The tag `Horst` means, Horst has to do it.
This parameter has a type annotation.
Which is a type hint.
The wildcard is `*`.
The worker class does this and that.
The worker process also does things.
I will commit this tomorrow.
Yesterday I modified the code.
Let's serve our app.
Let's serve this page.
Before doing this, upgrade FastAPI.
This is wrapped in an HTML tag.
`foo` as an `int`.
`bar` as a `str`.
`baz` as a `list`.
FastAPI's documentation.
Starlette's performance.
`foo` is case-sensitive.
"Bar" is case-insensitive.
Standard Python classes.
This is deprecated.
