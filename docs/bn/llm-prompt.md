### Target language

Translate to Bengali (বাংলা).

Language code: bn.

### Grammar and tone

* Use standard colloquial Bengali (প্রমিত চলিত বাংলা), not সাধু ভাষা.
* Write natural, everyday standard Bangladeshi Bengali, the way a Bangladeshi developer explains things to a colleague. Avoid bookish, Sanskrit-heavy words. Prefer: "কারণে" or "সুবাদে" (not "কল্যাণে"), "সমান" (not "সমতুল্য"), "দিয়ে তৈরি" (not "দ্বারা প্রদত্ত"), "নিজে থেকেই" (not "স্বয়ংক্রিয়ভাবে"), "automatic" for the adjective (not "স্বয়ংক্রিয়"), "নেয়" (not "গ্রহণ করে"), "এর মধ্যে আছে" (not "অন্তর্ভুক্ত"), "খুবই" (not "অত্যন্ত"), "এরই মধ্যে" (not "ইতিমধ্যে"), "শেষ করা" (not "সম্পন্ন করা"), "পুরো" (not "পূর্ণাঙ্গ"), "বদলাবে না" (not "অপরিবর্তিত থাকবে"). Keep it standard (প্রমিত), not slang or regional dialect, and keep using "আপনি".
* Address the reader formally with "আপনি", never "তুমি".
* End prose sentences with the Bengali দাঁড়ি "।". Never add "।" inside code, inline code, or at the end of headings.
* Use ASCII digits (0-9) for all numbers, including versions, ports, status codes and counts (for example "3টি"), never Bengali digits (০-৯).

### Technical terms

Keep all technical terms in English, written in Latin script. Do not transliterate them into Bengali script and do not translate them into Bengali words. Developers must see the same words they see in code, error messages and search results.

When a Bengali suffix is needed, attach it to the English term with a hyphen, for example: "request-এর", "FastAPI-তে", "Python-এ", "parameter-গুলো", "dependency-টি". Do not add an English plural "s" to make a Bengali plural; use "-গুলো" instead (but never change identifiers in code).

For the following terms, use these specific choices:

* path / path parameter / path operation / path operation function: keep in English (do not transliterate as "পাথ")
* query / query parameter: keep in English (do not transliterate as "কোয়েরি")
* parameter / argument: keep in English (do not transliterate as "প্যারামিটার", do not translate as "পরামিতি")
* header / headers (HTTP): keep in English (do not transliterate as "হেডার")
* cookie / cookies: keep in English (do not transliterate as "কুকি")
* form / form data: keep in English (do not transliterate as "ফর্ম")
* body / request body / response body: keep in English (do not transliterate as "বডি")
* request / response: keep in English (do not transliterate as "রিকোয়েস্ট" / "রেসপন্স", do not translate as "অনুরোধ" / "প্রতিক্রিয়া")
* status code: keep in English
* route / router / endpoint: keep in English (do not transliterate as "রাউটার")
* middleware: keep in English (do not transliterate as "মিডলওয়্যার")
* server / client: keep in English (do not transliterate as "সার্ভার")
* function: keep in English (do not transliterate as "ফাংশন")
* variable: keep in English (do not transliterate as "ভেরিয়েবল", do not translate as "চলক")
* type / type hint / type annotation: keep in English (do not transliterate as "টাইপ", do not translate as "প্রকার")
* class / instance / attribute / method: keep in English
* model / Pydantic model / response model: keep in English (do not transliterate as "মডেল")
* field / fields: keep in English (do not transliterate as "ফিল্ড", do not translate as "ক্ষেত্র")
* Enum / enumeration: keep in English
* dependency / dependency injection / sub-dependency: keep in English (do not transliterate as "ডিপেন্ডেন্সি", do not translate as "নির্ভরতা")
* security / authentication / authorization / scope / token: keep in English (do not translate as "নিরাপত্তা" / "প্রমাণীকরণ")
* lifespan / startup / shutdown / event: keep in English
* background task / WebSocket / streaming / upload: keep in English
* data: keep in English (do not transliterate as "ডেটা" / "ডাটা", do not translate as "উপাত্ত")
* value: keep in English (do not translate as "মান")
* default: keep in English (do not transliterate as "ডিফল্ট")
* required / optional: keep in English (do not translate as "আবশ্যক" / "ঐচ্ছিক")
* validation / validate: keep in English (do not translate as "যাচাই")
* serialization / parsing / conversion: keep in English (do not translate as "রূপান্তর")
* schema / JSON / alias: keep in English
* install / installation: keep in English (do not transliterate as "ইনস্টল"); write the verb as "install করুন"
* package / library / framework / tool: keep in English (do not transliterate as "প্যাকেজ" / "ফ্রেমওয়ার্ক")
* editor / editor support / autocomplete: keep in English (do not transliterate as "এডিটর")
* virtual environment / environment variable: keep in English (do not transliterate as "এনভায়রনমেন্ট")
* directory / file / project / terminal / command: keep in English (do not transliterate as "ডিরেক্টরি" / "ফাইল")
* deploy / deployment / production / development: keep in English
* worker / process / proxy / container: keep in English
* async / await / asynchronous / concurrency / parallelism / thread / event loop / coroutine: keep in English (do not transliterate as "অ্যাসিঙ্ক্রোনাস")
* tutorial / feature: keep in English
* Recap (section heading): keep in English

Never half-translate an English technical phrase. If a phrase has a modifier, keep the whole phrase in English. Do not translate the adjective and keep only the noun in English. For example: write "high performance", not "উচ্চ performance"; write "deeply nested JSON objects", not "গভীরভাবে nested JSON objects"; write "open source", "production-ready", "type hints", "auto-reload", "developer experience". Bengali words may surround the phrase (for example "খুবই high performance", "deeply nested JSON objects-এর জন্যও").

Ordinary, non-technical words are written in Bengali, for example: "উদাহরণস্বরূপ" (for example), "ধাপ" (step), "দেখুন" (see), "ব্যবহার করুন" (use), "তৈরি করুন" (create), "আরও পড়ুন" (read more). If a word could be read as a technical term in context, keep it in English.

### Quotes

Use typographic double quotes (“ ”) and single quotes (‘ ’) in prose. Do not change quotes inside code snippets, code blocks or inline code.

### Abbreviations

In `<abbr title="...">`, translate the title text into Bengali and keep the abbreviation itself unchanged.
