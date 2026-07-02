Translate to Russian (русский язык).

Language code: ru.

---

### Grammar and tone

Use a neutral tone (not overly formal or informal).

Use correct Russian grammar — appropriate cases, suffixes, and endings depending on context.

Address the reader as «вы». Never capitalize «вы», «ваш», «вам» mid-sentence: write «если вы сравниваете», not «если Вы сравниваете».

Write natural Russian, not word-for-word calques of English syntax. In particular:

* Put the generic Russian noun before the Latin name: «приложение FastAPI» (not «FastAPI приложение»), «события lifespan» (not «lifespan события»), «эндпоинты FastAPI» (not «FastAPI эндпоинты»).
* Hyphenate compounds where a Latin term modifies a Russian noun: «SQL-база данных», «JSON-схема», «бэкенд-API» (not «SQL база данных», «JSON схема», «бэкенд API»).
* Never mix Latin and Cyrillic letters inside one word: every letter of a Russian word must be Cyrillic (a Latin «a» in «полезнa» or a Latin «e» in «созданиe» corrupts the text and breaks search).
* Never leave stray English words in a Russian sentence: «…где именно и что было некорректно», not «…где именно and что было некорректно».
* Do not attach Cyrillic case endings directly to Latin words. Rephrase so the Latin name stays unchanged: «Python придётся сравнить…», not «Pythonу придётся сравнить…».
* A деепричастный оборот must share its subject with the main clause. Do not translate English "By doing X, …" as a dangling participle: «Если вы добавите звезду, другим пользователям будет проще найти проект», not «Добавив звезду, другим пользователям будет проще его найти».
* Watch case government and agreement across coordinated parts: «быстрее вашего предыдущего фреймворка (или как минимум сопоставим с ним)», not «быстрее (или сопоставим) с вашим предыдущим фреймворком»; «Он перестал быть веб-фреймворком для API», not «Это перестал быть веб-фреймворк для API»; «объявленные в текущих зависимостях `Security` и во всех зависящих», not «…и всеми зависящими».
* Use the correct prepositional forms: «об этих» (not «о этих»), «во внешний API» (not «в внешний API»).
* Use «который», not colloquial «что», as the relative pronoun: «часть модуля `functools`, входящего в стандартную библиотеку Python», not «часть `functools`, что входит в стандартную библиотеку».
* English singular "they" refers back to a singular noun — translate it with «тот»/«он»/«она», not plural «они»: «говорит повару, чтобы тот знал», not «чтобы они знали».
* Do not stack infinitives literally: "to tell it to use base64" → «чтобы указать, что нужно использовать base64», not «указать использовать base64».
* Preserve modality and hedging: "could trigger" → «может инициировать» (not «будет инициировать»); "could be less stable" → «может работать менее стабильно» (not «делает систему менее стабильной»); "probably" must not be dropped.
* Do not translate "shared (among requests)" as «разделяются между» (ambiguous — reads as "divided among"); use «общие для всех запросов» / «используются совместно всеми запросами».

Use the letter «ё» consistently everywhere it belongs: «начнёт», «своём», «ещё», «придётся», «развёртывание», «за счёт». Do not mix «ё» and «е» spellings of the same word within the documentation.

### Headings

Use noun-style headings, consistent with the rest of the Russian docs: "## Use a `Response` parameter" → «## Использование параметра `Response`», "### Simulate a File" → «### Имитация файла». Do not use the bare infinitive («## Использовать параметр `Response`», «### Симулировать файл»). Translate identical English headings identically on every page; different English headings on the same page must stay different in Russian (en "Requirements" and "Dependencies" must not both become «Зависимости»). Never change the anchor hash.

### Typography

* Use Russian guillemets «…» for quotes in prose, not straight quotes "…" or '…': «под капотом», «закрепить», «продвинутыми». Never change quotes inside inline code, code blocks, URLs, or file paths.
* Use the em dash « — » in prose, including as the copula where English uses "is": «**FastAPI CLI** — это программа…», not «**FastAPI CLI** - это программа…». Use the hyphen «-» only inside compound words (sole exception: the fixed title «Учебник - Руководство пользователя» keeps its spaced hyphen — see the glossary).
* The only hyphen character allowed is the ASCII hyphen-minus «-» (U+002D). Never use the non-breaking hyphen (U+2011): write «что-то», «HTTP-заголовок», «из-за», not «что‑то», «HTTP‑заголовок», «из‑за» — U+2011 breaks in-page text search.
* Follow standard Russian comma rules: «Вы уже видели, как тестировать…»; «Чтобы обеспечить их срабатывание, используйте…»; no spurious comma between a fronted object and the subject that follows it («Так что выбор версии Starlette можно просто оставить за FastAPI», not «Так что решение об используемой версии Starlette, вы можете оставить FastAPI»).
* Do not produce double periods or double spaces: «…и т.д. Эти изменения», not «…и т.д.. Эти изменения».
* Do not copy English Title Case capitalization mid-sentence: «модель машинного обучения», «семантическое версионирование» (capitalize glossary terms only at the start of a sentence or in a heading).

### Markdown structure

* Preserve every **bold** and *italic* of the original — translate the emphasized words and keep the markers: "from my very **subjective** point of view" → «с моей очень **субъективной** точки зрения». Do not drop emphasis, and do not add emphasis, quotes, or code formatting that the original does not have (no «…» around headings).
* Keep inline code in backticks exactly as in the original: `fastapi.status` must stay in backticks; never alter code blocks, URLs, or file paths.
* Keep list markers and indentation exactly as in the original: `*` stays `*`, `-` stays `-`, and nested list items keep 4 spaces of indentation per level (with 2 spaces python-markdown renders the hierarchy flat).
* Keep blank lines exactly as in the original, including the blank line after code-include macros like `{* ... *}`.

### Links

Never change link targets. When the link text is the title of another documentation page or section, use the exact Russian title of that target as it appears on that page: a link to `tutorial/encoder.md` reads «JSON-совместимый кодировщик», a link to `tutorial/bigger-applications.md` reads «Большие приложения — несколько файлов». Translate identical link texts identically on every page.

### /// admonitions

Keep the admonition keyword in English. When the English admonition has no title of its own, use exactly these Russian titles on every page (no variants):

* `/// note` → `/// note | Примечание`
* `/// tip` → `/// tip | Совет`
* `/// warning` → `/// warning | Предупреждение`
* `/// info` → `/// info | Информация`
* `/// danger` → `/// danger | Осторожно`
* `/// check` → `/// check | Проверка`

When the English admonition already has its own title, translate that title instead of using the generic one, and translate identical titles identically on every page. Translate "Technical Details" in any casing or variant as «Технические детали»: `/// note | Technical Details` and `/// note | Technical details` → `/// note | Технические детали`, `/// note | Very Technical Details` → `/// note | Очень технические детали`, `/// note | Starlette Technical Details` → `/// note | Технические детали Starlette`. Other examples: `/// tip | Inspired **FastAPI** to` → `/// tip | Вдохновило **FastAPI** на`, `/// tip | Authorize button!` → `/// tip | Кнопка авторизации!`.

Do not use «Подсказка», «Внимание», «Заметка», «Технические подробности».

### Mermaid diagrams

Translate all human-readable display text inside mermaid diagrams completely and consistently — notes, messages, and display labels (the text after a colon or introduced with `as`): "Note over Server: Server interprets headers" → «Note over Server: Сервер интерпретирует заголовки». Never translate the identifiers themselves — participant and node names like `Server` in `Note over Server:` must stay exactly as in the original, or the diagram stops rendering. Do not leave a diagram half-translated or mix languages in one label («с корректными HTTPS-URL», not «с верными HTTPS URLs»).

### Terms

For the following technical terms, use these specific translations to ensure consistency and clarity across the documentation. Use these translations, do not invent your own. The rules above and this glossary are both binding; if a general rule and a specific glossary entry conflict, the glossary entry wins. Both take precedence over an existing translation: if an existing translation uses a different term, spelling, quote style, or admonition title, update it to match this prompt. Translate the same English term with the same Russian term throughout a page and across pages — do not alternate synonyms («пользовательский» in one paragraph and «кастомный» in the next). When an entry lists an alternative translation, the first one is the default; use the alternative only in the context the entry states.

* production (meaning production software or environment): продакшен (spelled with «е», like «ресепшен», «промоушен»; not «продакшн»; decline normally: «в продакшене»; translate "production applications" as «продакшен-приложения», not «приложения в продакшн»)
* completion (meaning code auto-completion): автозавершение
* editor (meaning component of IDE): редактор кода
* adopt (meaning start to use): использовать (or `начать использовать`)
* headers (meaning HTTP-headers): HTTP-заголовки
* cookie sessions: сессии с использованием cookie
* tested (adjective): протестированный
* middleware: middleware (don't translate, but add `промежуточный слой` if clarification is needed)
* path operation: операция пути (plural: «операции пути», not «операций путей»; optionally clarify as `обработчик пути`)
* path operation function: функция-обработчик пути (or `функция обработки пути`)
* proprietary: проприетарный
* benchmark: бенчмарк (add (`тест производительности`) if clarification is needed or use just `тест производительности`)
* ASGI server: ASGI-сервер
* In a hurry? : Нет времени?
* response status code: статус-код ответа
* HTTP status code: HTTP-статус-код (hyphenated throughout, per the compound rule above; existing pages write «HTTP статус-код» — update it)
* issue (meaning GitHub issue): Issue (add `тикет/обращение` if clarification is needed — with a slash, not a backslash)
* PR (meaning GitHub pull request): пулл-реквест (add `запрос на изменение` if clarification is needed)
* run (meaning run the code): запустить (or `прогнать` if it's about testing the program)
* to reach users: донести до пользователей (or `привлечь внимание пользователей` in the promotion context)
* body (meaning HTTP request body): тело запроса
* body (meaning HTTP response body): тело ответа
* body parameter : body-параметр (or `параметр тела запроса`)
* validate: валидировать (or `выполнить валидацию`)
* requirements (meaning dependencies): зависимости (but translate a "Requirements" heading as «Требования» when the same page also has a "Dependencies" heading, so the two stay distinct)
* auto-reload: авто-перезагрузка (or `перезагрузить автоматически` if used as a verb)
* show (meaning show on the screen): отобразить
* parsing (noun): парсинг
* origin (in web development): origin (add `источник` if clarification is needed)
* include: включать (add `в себя` if it's appropriate, or use `содержать` as an alternative)
* virtual environment: виртуальное окружение
* framework: фреймворк
* path parameter: path-параметр
* path (as in URL path): путь
* form (as in HTML form): форма
* media type: тип содержимого
* request: HTTP-запрос
* response: HTTP-ответ
* type hints: аннотации типов
* type annotations: аннотации типов
* context manager: менеджер контекста
* code base: кодовая база
* instantiate: создать экземпляр (avoid "инстанцировать")
* load balancer: балансировщик нагрузки
* load balance: балансировка нагрузки
* worker process: воркер-процесс (or `процесс воркера`)
* worker: воркер
* lifespan: lifespan (do not translate when it's about lifespan events, but translate as `жизненный цикл` or `срок жизни` in other cases)
* mount (verb): монтировать
* mount (noun): точка монтирования / mount (keep in English if it's a FastAPI keyword)
* plugin: плагин
* plug-in: плагин
* full stack: full stack (do not translate)
* full-stack: full-stack (do not translate)
* loop (as in async loop): цикл событий
* Machine Learning: машинное обучение (capitalize only at the start of a sentence or in a heading: «модель машинного обучения» mid-sentence)
* Deep Learning: глубокое обучение (same capitalization rule)
* callback hell: callback hell (clarify as `ад обратных вызовов`)
* on the fly: на лету
* scratch the surface: поверхностно ознакомиться
* tip: совет (never «подсказка»)
* Pydantic model: Pydantic-модель (use `модель Pydantic` only where the declined form reads more naturally; never «Pydantic модель» — see the word-order rule)
* declare: объявить
* have the next best performance, after: быть на следующем месте по производительности после
* timing attack: тайминговая атака (clarify `атака по времени` if needed)
* OAuth2 scope: OAuth2 scope (clarify `область` if needed)
* TLS Termination Proxy: прокси-сервер TLS-терминации
* utilize (resources): использовать
* content: содержимое (not «контент»)
* raise exception: выбросить исключение (do not use «вызвать» next to «возвращать»/«вызывать функцию», where it reads as "call")
* password flow: password flow (clarify as `аутентификация по паролю` if needed)
* tutorial: руководство (use `учебник` only in the fixed title «Учебник - Руководство пользователя»)
* too long; didn't read: слишком длинно; не читал
* proxy with a stripped path prefix: прокси с функцией удаления префикса пути
* nerd: умник
* sub application: подприложение
* webhook request: вебхук-запрос
* serve (meaning providing access to something): «отдавать» (or `предоставлять доступ к`)
* recap (noun): резюме
* utility function: вспомогательная функция
* fast to code: позволяет быстро писать код
* Tutorial - User Guide: Учебник - Руководство пользователя (use exactly this form with a hyphen; do not replace the hyphen with an em dash)
* submodule: подмодуль
* subpackage: подпакет
* router: роутер
* building, deploying, accessing (when describing features of FastAPI Cloud): создание, развёртывание и доступ
* type checker tool: инструмент проверки типов
* backend: бэкенд (not «бекэнд»)
* custom (as in custom response, custom class): пользовательский (not «кастомный»)
* deployment: развёртывание (with «ё»; not «деплой», not «развертывание»)
* WebSocket: веб-сокет (not «вебсокет»); WebSocket connection: WebSocket-соединение (or `соединение по веб-сокету`; not «веб-сокет соединение» — in hyphenated compounds the protocol name keeps its Latin spelling)
* `with` statement: оператор `with` (not «менеджер контекста `with`» — a `with` statement is not a context manager)
* parse (e.g. a request body): распарсить / разобрать (e.g. «тело запроса распарсено как JSON»; not «обработано» — that blurs parse vs. process)
* cookies (plural, in prose): cookies (use this plural form consistently, not invariant «cookie»)
* stream (verb, about sending a file/response): передавать потоком (e.g. "Asynchronously streams a file as the response" → «Асинхронно передаёт файл потоком в качестве ответа»; not simply «отправляет»)
* testing or automation workflows: рабочие процессы тестирования и автоматизации (not «воркфлоу»)
* as you normally would: как обычно (not «как и раньше»)
* Semantic Versioning: семантическое версионирование (lowercase mid-sentence)
* input location (e.g. the path passed to a generator's `-i`): путь к входному файлу (not «входное расположение»)
* Global view (section heading): Общий обзор (not «Взгляд издалека»)
* query parameter: query-параметр (not «параметр запроса», which reads as "request parameter")
* Dependency Injection: внедрение зависимостей (not «встраивание зависимостей»; lowercase mid-sentence)
* keyword arguments: именованные аргументы (not «ключевые аргументы»)
* hash / hashed / hashing: хеш / хешированный / хеширование (never «хэш»)
* directory: директория (use consistently; do not alternate with «каталог» and «папка»)
* open source (adjective): с открытым исходным кодом ("the first open-source release" → «первый релиз с открытым исходным кодом», not «открытый релиз»)
* Blueprints (Flask): Blueprints (do not translate as «шаблоны» — those are Flask templates, a different mechanism)
* Advanced User Guide: Расширенное руководство пользователя (exactly the RU title of advanced/index.md; not «Продвинутое руководство пользователя»)

Do not add whitespace in `т.д.`, `т.п.`.
