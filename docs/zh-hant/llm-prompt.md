### Target language

Translate to Traditional Chinese (繁體中文).

Language code: zh-hant.

### Grammar and tone

- Use clear, concise technical Traditional Chinese consistent with existing docs.
- Address the reader naturally (commonly using “你/你的”).

### Headings

- Follow existing Traditional Chinese heading style (short and descriptive).
- Do not add trailing punctuation to headings.

### Quotes and punctuation

- Keep punctuation style consistent with existing Traditional Chinese docs (they often mix English terms like “FastAPI” with Chinese text).
- Never change punctuation inside inline code, code blocks, URLs, or file paths.
- For more details, please follow the [Chinese Copywriting Guidelines](https://github.com/sparanoid/chinese-copywriting-guidelines).

### Ellipsis

- Keep ellipsis style consistent within each document, prefer `...` over `……`.
- Never change ellipsis in code, URLs, or CLI examples.

### Preferred translations / glossary

- Should avoid using simplified Chinese characters and terms. Always examine if the translation can be easily comprehended by the Traditional Chinese readers.
- For some Python-specific terms like "pickle", "list", "dict" etc, we don't have to translate them.
- Use the following preferred translations when they apply in documentation prose:

- request (HTTP): 請求
- response (HTTP): 回應
- path operation: 路徑操作
- path operation function: 路徑操作函式

The translation can optionally include the original English text only in the first occurrence of each page (e.g. "路徑操作 (path operation)") if the translation is hard to be comprehended by most of the Chinese readers.

### `///` admonitions

1) Keep the admonition keyword in English (do not translate `note`, `tip`, etc.).
2) Many Traditional Chinese docs currently omit titles in `///` blocks; that is OK.
3) If a generic title is present, prefer these canonical titles:

- `/// note | 注意`

Notes:

- `details` blocks exist; keep `/// details` as-is and translate only the title after `|`.
- Example canonical titles used in existing docs:

```
/// details | 上述指令的含義
```

```
/// details | 關於 `requirements.txt`
```
