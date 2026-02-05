# Test translation fixer tool { #test-translation-fixer }

## Code blocks with and without comments { #code-blocks-with-and-without-comments }

This is a test page for the translation fixer tool.

### Code blocks with comments { #code-blocks-with-comments }

The following code blocks include comments in different styles.
Fixer tool should fix content, but preserve comments correctly.

```python
# This is a sample Python code block
def hello_world():
    # Comment with indentation
    print("Hello, world!")  # Print greeting
```

```toml
# This is a sample TOML code block
title = "TOML Example"  # Title of the document
```

```console
// Use the command "live" and pass the language code as a CLI argument
$ python ./scripts/docs.py live es

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

```json
{
    // This is a sample JSON code block
    "greeting": "Hello, world!" // Greeting
}
```


### Code blocks with comments where language uses different comment styles { #code-blocks-with-different-comment-styles }

The following code blocks include comments in different styles based on the language.
Fixer tool will not preserve comments in these blocks.

```json
{
    # This is a sample JSON code block
    "greeting": "Hello, world!" # Print greeting
}
```

```console
# This is a sample console code block
$ echo "Hello, world!"  # Print greeting
```

```toml
// This is a sample TOML code block
title = "TOML Example"  // Title of the document
```


### Code blocks with comments with unsupported languages or without language specified { #code-blocks-with-unsupported-languages }

The following code blocks use unsupported languages for comment preservation.
Fixer tool will not preserve comments in these blocks.

```javascript
// This is a sample JavaScript code block
console.log("Hello, world!"); // Print greeting
```

```
# This is a sample console code block
$ echo "Hello, world!"  # Print greeting
```

```
// This is a sample console code block
$ echo "Hello, world!"  // Print greeting
```


### Code blocks with comments that don't follow pattern { #code-blocks-with-comments-without-pattern }

Fixer tool expects comments that follow specific pattern:

- For hash-style comments: comment starts with `# ` (hash following by whitespace) in the beginning of the string or after a whitespace.
- For slash-style comments: comment starts with `// ` (two slashes following by whitespace) in the beginning of the string or after a whitespace.

If comment doesn't follow this pattern, fixer tool will not preserve it.

```python
#Function declaration
def hello_world():# Print greeting
    print("Hello, world!")  #Print greeting without space after hash
```

```console
//Function declaration
def hello_world():// Print greeting
    print("Hello, world!")  //Print greeting without space after slashes
```

## Code blocks with quadruple backticks { #code-blocks-with-quadruple-backticks }

The following code block uses quadruple backticks.

````python
# Hello world function
def hello_world():
    print("Hello, world!")  # Print greeting
````

### Backticks number mismatch is fixable { #backticks-number-mismatch-is-fixable }

The following code block has triple backticks in the original document, but quadruple backticks in the translated document.
It will be fixed by the fixer tool (will convert to triple backticks).

```Python
# Some Python code
```

### Triple backticks inside quadruple backticks { #triple-backticks-inside-quadruple-backticks }

Comments inside nested code block will NOT be preserved.

````
Here is a code block with quadruple backticks that contains triple backticks inside:

```python
# This is a sample Python code block
def hello_world():
    print("Hello, world!")  # Print greeting
```

````

# Code includes { #code-includes }

## Simple code includes { #simple-code-includes }

{* ../../docs_src/python_types/tutorial001_py39.py *}

{* ../../docs_src/python_types/tutorial002_py39.py *}


## Code includes with highlighting { #code-includes-with-highlighting }

{* ../../docs_src/python_types/tutorial002_py39.py hl[1] *}

{* ../../docs_src/python_types/tutorial006_py39.py hl[10] *}


## Code includes with line ranges { #code-includes-with-line-ranges }

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[19:21] *}

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[30:38] *}


## Code includes with line ranges and highlighting { #code-includes-with-line-ranges-and-highlighting }

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[30:38] hl[31:33] *}

{* ../../docs_src/dependencies/tutorial015_an_py310.py ln[10:15] hl[12:14] *}


## Code includes qith title { #code-includes-with-title }

{* ../../docs_src/bigger_applications/app_an_py39/routers/users.py hl[1,3] title["app/routers/users.py"] *}

{* ../../docs_src/bigger_applications/app_an_py39/internal/admin.py hl[3] title["app/internal/admin.py"] *}

## Code includes with unknown attributes { #code-includes-with-unknown-attributes }

{* ../../docs_src/python_types/tutorial001_py39.py unknown[123] *}

## Some more code includes to test fixing { #some-more-code-includes-to-test-fixing }

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[19:21] *}

{* ../../docs_src/bigger_applications/app_an_py39/internal/admin.py hl[3] title["app/internal/admin.py"] *}

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[30:38] hl[31:33] *}



# Links { #links }

## Markdown-style links { #markdown-style-links }

This is a [Markdown link](https://example.com) to an external site.

This is a link with attributes: [**FastAPI** Project Generators](project-generation.md){.internal-link target=_blank}

This is a link to the main FastAPI site: [FastAPI](https://fastapi.tiangolo.com) - tool should add language code to the URL.

This is a link to one of the pages on FastAPI site: [How to](https://fastapi.tiangolo.com/how-to/) - tool should add language code to the URL.

Link to test wrong attribute: [**FastAPI** Project Generators](project-generation.md){.internal-link} - tool should fix the attribute.

Link with a title: [Example](https://example.com "Example site") - URL will be fixed, title preserved.

### Markdown link to static assets { #markdown-link-to-static-assets }

These are links to static assets:

* [FastAPI Logo](https://fastapi.tiangolo.com/img/fastapi-logo.png)
* [FastAPI CSS](https://fastapi.tiangolo.com/css/fastapi.css)
* [FastAPI JS](https://fastapi.tiangolo.com/js/fastapi.js)

Tool should NOT add language code to their URLs.

## HTML-style links { #html-style-links }

This is an <a href="https://example.com" target="_blank" class="external-link">HTML link</a> to an external site.

This is an <a href="https://fastapi.tiangolo.com">link to the main FastAPI site</a> - tool should add language code to the URL.

This is an <a href="https://fastapi.tiangolo.com/how-to/">link to one of the pages on FastAPI site</a> - tool should add language code to the URL.

Link to test wrong attribute: <a href="project-generation.md" class="internal-link">**FastAPI** Project Generators</a> - tool should fix the attribute.

### HTML links to static assets { #html-links-to-static-assets }

These are links to static assets:

* <a href="https://fastapi.tiangolo.com/img/fastapi-logo.png">FastAPI Logo</a>
* <a href="https://fastapi.tiangolo.com/css/fastapi.css">FastAPI CSS</a>
* <a href="https://fastapi.tiangolo.com/js/fastapi.js">FastAPI JS</a>

Tool should NOT add language code to their URLs.

# Header (with HTML link to <a href="https://tiangolo.com">tiangolo.com</a>) { #header-with-html-link-to-tiangolo-com }

#Not a header

```Python
# Also not a header
```

Some text
