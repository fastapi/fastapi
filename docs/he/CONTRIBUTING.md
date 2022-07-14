# Translating tips and guidelines

Please read this document before committing translations!

## Text direction

The `mkdocs` template for hebrew sets the text direction to `rtl`, which mostly works.

In fact, the "hard" part is getting the parts which must remain in `ltr` to behave:

### `termy`

Just add `dir="ltr"` to the div.

    <div **dir="ltr"** class="termy">

    ```console
    $ pip install "uvicorn[standard]"

    ---> 100%
    ```

    </div>

### Inline `monospace`.

Single words mostly work, but for anything with spaces you'll nees a `\<code\>` tag.

    - `app`: האובייקט שנוצר בתוך `main.py` עם השורה <code dir="ltr">app = FastAPI()</code>.


---

## Translations

Not every word is easily translated.

Bellow is the current consensus, which you should stick to as much as possible.

If you find new non-trivial to translate words, add them.

If you disagree with what's written here,
you are **VERY** welcome to start a discussion in the PR,
and if others agree follow up with a commit to this file,
and all files where the word is used :)

### Acronyms

Acronyms like `API` and `CLI` do have Hebrew translations,
but no one wants to read (or write) "ממשק תכנות יישומים" a hundred time.

Write the Hebrew translation once,
put the English acronym in parentheses,
than use the acronym from that point on.


### Leave as is

The following should stay in english:

- Names, e.g. `FastAPI`, `NodeJS`, `main.py`.
- Python keywords, e.g. `async`.
- Testimonials.
- Anything you feel will be clearer in english.
  Some words have a different meaning when used in technical context,
  which usually doesn't translate well.

### Transliterations

Asynchronous becomes "אסינכרוני" and so on.

### Translations

| English         | Hebrew                  |
|-----------------|-------------------------|
| Framework       | תשתית רשת / תשתית פיתוח |
| Production      | סביבת ייצור             |
| Debugging       | ניפוי שגיאות            |
| Types           | טיפוסים                 |
| Path parameter  | פרמטר נתיב              |
| Query parameter | פרמטר שאילתא            |
| Headers         | כותרות                  |
