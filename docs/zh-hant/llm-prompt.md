### Target language

Translate to Traditional Chinese (繁體中文).

Language code: zh-hant.

### Grammar and tone

1) Use clear, concise technical Traditional Chinese consistent with existing docs.
2) Address the reader naturally (commonly using “你/你的”).

### Headings

1) Follow existing Traditional Chinese heading style (short and descriptive).
2) Do not add trailing punctuation to headings.

### Quotes and punctuation

1) Keep punctuation style consistent with existing Traditional Chinese docs (they often mix English terms like “FastAPI” with Chinese text).
2) Never change punctuation inside inline code, code blocks, URLs, or file paths.
3) For more details, please follow the [Chinese Copywriting Guidelines](https://github.com/sparanoid/chinese-copywriting-guidelines).

### Ellipsis

1) Keep ellipsis style consistent within each document, prefer `...` over `……`.
2) Never change ellipsis in code, URLs, or CLI examples.

### Preferred translations / glossary

1. Should avoid using simplified Chinese characters and terms. Always examine if the translation can be easily comprehended by the Traditional Chinese readers.
2. For some Python-specific terms like "pickle", "list", "dict" etc, we don't have to translate them.
3. Use the following preferred translations when they apply in documentation prose:

- request (HTTP): 請求
- response (HTTP): 回應
- path operation: 路徑操作
- path operation function: 路徑操作函式

### `///` admonitions

1) Keep the admonition keyword in English (do not translate `note`, `tip`, etc.).
2) Many Traditional Chinese docs currently omit titles in `///` blocks; that is OK.
3) If a generic title is present, prefer these canonical titles:

- `/// note | 注意`

Notes:

- `details` blocks exist; keep `/// details` as-is and translate only the title after `|`.
- Example canonical titles used in existing docs:
  - `/// details | 上述指令的含義`
  - `/// details | 關於 `requirements.txt``
