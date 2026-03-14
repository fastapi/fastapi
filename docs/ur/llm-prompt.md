### Target language

Translate to Urdu (اردو).

Language code: ur.

### Core principle

Don't translate word-by-word. Rewrite naturally in Urdu as if writing the doc from scratch. Preserve meaning, but prioritize fluency over literal accuracy. Write in a way that feels natural to an Urdu-speaking developer.

### Grammar and tone

- Use instructional Urdu, consistent with technical documentation style.
- Use polite imperative/guide language (e.g. "استعمال کریں", "چلائیں", "دیکھیں", "کاپی کریں").
- Avoid overly formal or literary Urdu — keep it accessible and modern.
- Ensure sentences make sense in Urdu context — adjust structure, conjunctions, and verb forms as needed for natural flow.
- Urdu is written right-to-left (RTL), ensure text flows naturally.
- Use simple and clear Urdu that a developer comfortable with both Urdu and English would understand.

### Headings

- Follow existing Urdu heading style (no trailing period).
- Keep headings concise and descriptive.

### Quotes

- Keep quote style consistent with existing Urdu docs (typically ASCII quotes in text).
- Never modify quotes inside inline code, code blocks, URLs, or file paths.

### Ellipsis

- Keep ellipsis style (`...`) consistent with existing docs.
- Never modify `...` in code, URLs, or CLI examples.

### Consistency

- Use the same translation for the same term throughout the document.
- If you translate a concept one way, keep it consistent across all occurrences.

### Links and references

- Never modify link syntax like `{.internal-link target=_blank}`.
- Keep markdown link structure intact: `[text](url){.internal-link}`.

### Preferred translations / glossary

Do not translate technical terms like path, route, request, response, query, body, cookie, header, endpoint, middleware, decorator, dependency, schema, model, type hint, async, await — keep them as is in English.

- When adding Urdu postpositions or suffixes to English technical terms, use them naturally in the sentence flow.

- Some common translations to use:
  - "function" → "function" (keep in English)
  - "parameter" → "parameter" (keep in English)
  - "import" → "import" (keep in English)
  - "install" → "انسٹال"
  - "run" → "چلائیں"
  - "create" → "بنائیں"
  - "file" → "فائل"
  - "code" → "کوڈ"
  - "application" → "ایپلیکیشن"
  - "documentation" → "دستاویزات"
  - "example" → "مثال"
  - "feature" → "خصوصیت"
  - "performance" → "کارکردگی"
  - "error" → "خرابی" or "ایرر"
  - "warning" → "انتباہ"
  - "note" → "نوٹ"
  - "tip" → "مشورہ"
  - "information" → "معلومات"
  - "security" → "سیکیورٹی"
  - "database" → "ڈیٹابیس"
  - "server" → "سرور"
  - "client" → "کلائنٹ"
  - "browser" → "براؤزر"
  - "developer" → "ڈویلپر"
  - "framework" → "فریم ورک"
  - "library" → "لائبریری"
  - "package" → "پیکیج"
  - "tutorial" → "ٹیوٹوریل"
  - "chapter" → "باب"
  - "section" → "سیکشن"
  - "data" → "ڈیٹا"
  - "value" → "ویلیو"
  - "string" → "string" (keep in English)
  - "integer" → "integer" (keep in English)
  - "boolean" → "boolean" (keep in English)
  - "default" → "ڈیفالٹ"

- You can provide the Urdu meaning of a term in parentheses when it first appears, but keep the English term as primary. Do not overdo this — only for less obvious terms, and only the first time.

### `///` admonitions

- Keep the admonition keyword in English (do not translate `note`, `tip`, etc.).
- If a title is present, prefer these canonical titles:

- `/// note | نوٹ`
- `/// note | تکنیکی تفصیلات`
- `/// tip | مشورہ`
- `/// warning | انتباہ`
- `/// info | معلومات`
- `/// check | اضافی معلومات`
