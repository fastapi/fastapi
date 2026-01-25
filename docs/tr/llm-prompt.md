### Target language

Translate to Turkish (Türkçe).

Language code: tr.

### Core principle

Don't translate word-by-word. Rewrite naturally in Turkish as if writing the doc from scratch. Preserve meaning, but prioritize fluency over literal accuracy.

### Grammar and tone

- Use instructional Turkish, consistent with existing Turkish docs.
- Use imperative/guide language (e.g. "açalım", "gidin", "kopyalayalım", "bir bakalım").
- Avoid filler words and overly long sentences.
- Ensure sentences make sense in Turkish context — adjust structure, conjunctions, and verb forms as needed for natural flow (e.g. use "Ancak" instead of "Ve" when connecting contrasting sentences, use "-maktadır/-mektedir" for formal statements).

### Headings

- Follow existing Turkish heading style (Title Case where used; no trailing period).

### Quotes

- Keep quote style consistent with existing Turkish docs (typically ASCII quotes in text).
- Never modify quotes inside inline code, code blocks, URLs, or file paths.

### Ellipsis

- Keep ellipsis style (`...`) consistent with existing Turkish docs.
- Never modify `...` in code, URLs, or CLI examples.

### Consistency

- Use the same translation for the same term throughout the document.
- If you translate a concept one way, keep it consistent across all occurrences.

### Links and references

- Never modify link syntax like `{.internal-link target=_blank}`.
- Keep markdown link structure intact: `[text](url){.internal-link}`.

### Preferred translations / glossary

Do not translate technical terms like path, route, request, response, query, body, cookie, and header, keep them as is.

- Suffixing is very important, when adding Turkish suffixes to the English words, do that based on the pronunciation of the word and with an apostrophe.

- Suffixes also changes based on what word comes next in Turkish too, here is an example:

"Server'a gelen request'leri intercept... " or this could have been "request'e", "request'i" etc.

- Some words are tricky like "path'e" can't be used like "path'a" but it could have been "path'i" "path'leri" etc.

- You can use a more instructional style, that is consistent with the document, you can add the Turkish version of the term in parenthesis if it is not something very obvious, or an advanced concept, but do not over do it, do it only the first time it is mentioned, but keep the English term as the primary word.

### `///` admonitions

- Keep the admonition keyword in English (do not translate `note`, `tip`, etc.).
- If a title is present, prefer these canonical titles:

- `/// note | Not`
- `/// note | Teknik Detaylar`
- `/// tip | İpucu`
- `/// warning | Uyarı`
- `/// info | Bilgi`
- `/// check | Ek bilgi`

Prefer `İpucu` over `Ipucu`.
