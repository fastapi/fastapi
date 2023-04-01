# 🛃 📨 - 🕸, 🎏, 📁, 🎏

🔢, **FastAPI** 🔜 📨 📨 ⚙️ `JSONResponse`.

👆 💪 🔐 ⚫️ 🛬 `Response` 🔗 👀 [📨 📨 🔗](response-directly.md){.internal-link target=_blank}.

✋️ 🚥 👆 📨 `Response` 🔗, 📊 🏆 🚫 🔁 🗜, &amp; 🧾 🏆 🚫 🔁 🏗 (🖼, 🔌 🎯 "📻 🆎", 🇺🇸🔍 🎚 `Content-Type` 🍕 🏗 🗄).

✋️ 👆 💪 📣 `Response` 👈 👆 💚 ⚙️, *➡ 🛠️ 👨‍🎨*.

🎚 👈 👆 📨 ⚪️➡️ 👆 *➡ 🛠️ 🔢* 🔜 🚮 🔘 👈 `Response`.

&amp; 🚥 👈 `Response` ✔️ 🎻 📻 🆎 (`application/json`), 💖 💼 ⏮️ `JSONResponse` &amp; `UJSONResponse`, 💽 👆 📨 🔜 🔁 🗜 (&amp; ⛽) ⏮️ 🙆 Pydantic `response_model` 👈 👆 📣 *➡ 🛠️ 👨‍🎨*.

!!! note
    🚥 👆 ⚙️ 📨 🎓 ⏮️ 🙅‍♂ 📻 🆎, FastAPI 🔜 ⌛ 👆 📨 ✔️ 🙅‍♂ 🎚, ⚫️ 🔜 🚫 📄 📨 📁 🚮 🏗 🗄 🩺.

## ⚙️ `ORJSONResponse`

🖼, 🚥 👆 ✊ 🎭, 👆 💪 ❎ &amp; ⚙️ <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a> &amp; ⚒ 📨 `ORJSONResponse`.

🗄 `Response` 🎓 (🎧-🎓) 👆 💚 ⚙️ &amp; 📣 ⚫️ *➡ 🛠️ 👨‍🎨*.

⭕ 📨, 📨 `Response` 🔗 🌅 ⏩ 🌘 🛬 📖.

👉 ↩️ 🔢, FastAPI 🔜 ✔ 🔠 🏬 🔘 &amp; ⚒ 💭 ⚫️ 🎻 ⏮️ 🎻, ⚙️ 🎏 [🎻 🔗 🔢](../tutorial/encoder.md){.internal-link target=_blank} 🔬 🔰. 👉 ⚫️❔ ✔ 👆 📨 **❌ 🎚**, 🖼 💽 🏷.

✋️ 🚥 👆 🎯 👈 🎚 👈 👆 🛬 **🎻 ⏮️ 🎻**, 👆 💪 🚶‍♀️ ⚫️ 🔗 📨 🎓 &amp; ❎ ➕ 🌥 👈 FastAPI 🔜 ✔️ 🚶‍♀️ 👆 📨 🎚 🔘 `jsonable_encoder` ⏭ 🚶‍♀️ ⚫️ 📨 🎓.

```Python hl_lines="2  7"
{!../../../docs_src/custom_response/tutorial001b.py!}
```

!!! info
    🔢 `response_class` 🔜 ⚙️ 🔬 "📻 🆎" 📨.

    👉 💼, 🇺🇸🔍 🎚 `Content-Type` 🔜 ⚒ `application/json`.

     &amp; ⚫️ 🔜 📄 ✅ 🗄.

!!! tip
     `ORJSONResponse` ⏳ 🕴 💪 FastAPI, 🚫 💃.

## 🕸 📨

📨 📨 ⏮️ 🕸 🔗 ⚪️➡️ **FastAPI**, ⚙️ `HTMLResponse`.

* 🗄 `HTMLResponse`.
* 🚶‍♀️ `HTMLResponse` 🔢 `response_class` 👆 *➡ 🛠️ 👨‍🎨*.

```Python hl_lines="2  7"
{!../../../docs_src/custom_response/tutorial002.py!}
```

!!! info
    🔢 `response_class` 🔜 ⚙️ 🔬 "📻 🆎" 📨.

    👉 💼, 🇺🇸🔍 🎚 `Content-Type` 🔜 ⚒ `text/html`.

     &amp; ⚫️ 🔜 📄 ✅ 🗄.

### 📨 `Response`

👀 [📨 📨 🔗](response-directly.md){.internal-link target=_blank}, 👆 💪 🔐 📨 🔗 👆 *➡ 🛠️*, 🛬 ⚫️.

🎏 🖼 ⚪️➡️ 🔛, 🛬 `HTMLResponse`, 💪 👀 💖:

```Python hl_lines="2  7  19"
{!../../../docs_src/custom_response/tutorial003.py!}
```

!!! warning
     `Response` 📨 🔗 👆 *➡ 🛠️ 🔢* 🏆 🚫 📄 🗄 (🖼, `Content-Type` 🏆 🚫 📄) &amp; 🏆 🚫 ⭐ 🏧 🎓 🩺.

!!! info
    ↗️, ☑ `Content-Type` 🎚, 👔 📟, ♒️, 🔜 👟 ⚪️➡️ `Response` 🎚 👆 📨.

### 📄 🗄 &amp; 🔐 `Response`

🚥 👆 💚 🔐 📨 ⚪️➡️ 🔘 🔢 ✋️ 🎏 🕰 📄 "📻 🆎" 🗄, 👆 💪 ⚙️ `response_class` 🔢 &amp; 📨 `Response` 🎚.

`response_class` 🔜 ⤴️ ⚙️ 🕴 📄 🗄 *➡ 🛠️*, ✋️ 👆 `Response` 🔜 ⚙️.

#### 📨 `HTMLResponse` 🔗

🖼, ⚫️ 💪 🕳 💖:

```Python hl_lines="7  21  23"
{!../../../docs_src/custom_response/tutorial004.py!}
```

👉 🖼, 🔢 `generate_html_response()` ⏪ 🏗 &amp; 📨 `Response` ↩️ 🛬 🕸 `str`.

🛬 🏁 🤙 `generate_html_response()`, 👆 ⏪ 🛬 `Response` 👈 🔜 🔐 🔢 **FastAPI** 🎭.

✋️ 👆 🚶‍♀️ `HTMLResponse` `response_class` 💁‍♂️, **FastAPI** 🔜 💭 ❔ 📄 ⚫️ 🗄 &amp; 🎓 🩺 🕸 ⏮️ `text/html`:

<img src="/img/tutorial/custom-response/image01.png">

## 💪 📨

📥 💪 📨.

✔️ 🤯 👈 👆 💪 ⚙️ `Response` 📨 🕳 🙆, ⚖️ ✍ 🛃 🎧-🎓.

!!! note "📡 ℹ"
    👆 💪 ⚙️ `from starlette.responses import HTMLResponse`.

    **FastAPI** 🚚 🎏 `starlette.responses` `fastapi.responses` 🏪 👆, 👩‍💻. ✋️ 🌅 💪 📨 👟 🔗 ⚪️➡️ 💃.

### `Response`

👑 `Response` 🎓, 🌐 🎏 📨 😖 ⚪️➡️ ⚫️.

👆 💪 📨 ⚫️ 🔗.

⚫️ 🚫 📄 🔢:

* `content` - `str` ⚖️ `bytes`.
* `status_code` - `int` 🇺🇸🔍 👔 📟.
* `headers` - `dict` 🎻.
* `media_type` - `str` 🤝 📻 🆎. 🤶 Ⓜ. `"text/html"`.

FastAPI (🤙 💃) 🔜 🔁 🔌 🎚-📐 🎚. ⚫️ 🔜 🔌 🎚-🆎 🎚, ⚓️ 🔛 = &amp; 🔁 = ✍ 🆎.

```Python hl_lines="1  18"
{!../../../docs_src/response_directly/tutorial002.py!}
```

### `HTMLResponse`

✊ ✍ ⚖️ 🔢 &amp; 📨 🕸 📨, 👆 ✍ 🔛.

### `PlainTextResponse`

✊ ✍ ⚖️ 🔢 &amp; 📨 ✅ ✍ 📨.

```Python hl_lines="2  7  9"
{!../../../docs_src/custom_response/tutorial005.py!}
```

### `JSONResponse`

✊ 💽 &amp; 📨 `application/json` 🗜 📨.

👉 🔢 📨 ⚙️ **FastAPI**, 👆 ✍ 🔛.

### `ORJSONResponse`

⏩ 🎛 🎻 📨 ⚙️ <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a>, 👆 ✍ 🔛.

### `UJSONResponse`

🎛 🎻 📨 ⚙️ <a href="https://github.com/ultrajson/ultrajson" class="external-link" target="_blank">`ujson`</a>.

!!! warning
    `ujson` 🌘 💛 🌘 🐍 🏗-🛠️ ❔ ⚫️ 🍵 📐-💼.

```Python hl_lines="2  7"
{!../../../docs_src/custom_response/tutorial001.py!}
```

!!! tip
    ⚫️ 💪 👈 `ORJSONResponse` 💪 ⏩ 🎛.

### `RedirectResponse`

📨 🇺🇸🔍 ❎. ⚙️ 3️⃣0️⃣7️⃣ 👔 📟 (🍕 ❎) 🔢.

👆 💪 📨 `RedirectResponse` 🔗:

```Python hl_lines="2  9"
{!../../../docs_src/custom_response/tutorial006.py!}
```

---

⚖️ 👆 💪 ⚙️ ⚫️ `response_class` 🔢:


```Python hl_lines="2  7  9"
{!../../../docs_src/custom_response/tutorial006b.py!}
```

🚥 👆 👈, ⤴️ 👆 💪 📨 📛 🔗 ⚪️➡️ 👆 *➡ 🛠️* 🔢.

👉 💼, `status_code` ⚙️ 🔜 🔢 1️⃣ `RedirectResponse`, ❔ `307`.

---

👆 💪 ⚙️ `status_code` 🔢 🌀 ⏮️ `response_class` 🔢:

```Python hl_lines="2  7  9"
{!../../../docs_src/custom_response/tutorial006c.py!}
```

### `StreamingResponse`

✊ 🔁 🚂 ⚖️ 😐 🚂/🎻 &amp; 🎏 📨 💪.

```Python hl_lines="2  14"
{!../../../docs_src/custom_response/tutorial007.py!}
```

#### ⚙️ `StreamingResponse` ⏮️ 📁-💖 🎚

🚥 👆 ✔️ 📁-💖 🎚 (✅ 🎚 📨 `open()`), 👆 💪 ✍ 🚂 🔢 🔁 🤭 👈 📁-💖 🎚.

👈 🌌, 👆 🚫 ✔️ ✍ ⚫️ 🌐 🥇 💾, &amp; 👆 💪 🚶‍♀️ 👈 🚂 🔢 `StreamingResponse`, &amp; 📨 ⚫️.

👉 🔌 📚 🗃 🔗 ⏮️ ☁ 💾, 📹 🏭, &amp; 🎏.

```{ .python .annotate hl_lines="2  10-12  14" }
{!../../../docs_src/custom_response/tutorial008.py!}
```

1️⃣. 👉 🚂 🔢. ⚫️ "🚂 🔢" ↩️ ⚫️ 🔌 `yield` 📄 🔘.
2️⃣. ⚙️ `with` 🍫, 👥 ⚒ 💭 👈 📁-💖 🎚 📪 ⏮️ 🚂 🔢 🔨. , ⏮️ ⚫️ 🏁 📨 📨.
3️⃣. 👉 `yield from` 💬 🔢 🔁 🤭 👈 👜 🌟 `file_like`. &amp; ⤴️, 🔠 🍕 🔁, 🌾 👈 🍕 👟 ⚪️➡️ 👉 🚂 🔢.

    , ⚫️ 🚂 🔢 👈 📨 "🏭" 👷 🕳 🙆 🔘.

    🔨 ⚫️ 👉 🌌, 👥 💪 🚮 ⚫️ `with` 🍫, &amp; 👈 🌌, 🚚 👈 ⚫️ 📪 ⏮️ 🏁.

!!! tip
    👀 👈 📥 👥 ⚙️ 🐩 `open()` 👈 🚫 🐕‍🦺 `async` &amp; `await`, 👥 📣 ➡ 🛠️ ⏮️ 😐 `def`.

### `FileResponse`

🔁 🎏 📁 📨.

✊ 🎏 ⚒ ❌ 🔗 🌘 🎏 📨 🆎:

* `path` - 📁 📁 🎏.
* `headers` - 🙆 🛃 🎚 🔌, 📖.
* `media_type` - 🎻 🤝 📻 🆎. 🚥 🔢, 📁 ⚖️ ➡ 🔜 ⚙️ 🔑 📻 🆎.
* `filename` - 🚥 ⚒, 👉 🔜 🔌 📨 `Content-Disposition`.

📁 📨 🔜 🔌 ☑ `Content-Length`, `Last-Modified` &amp; `ETag` 🎚.

```Python hl_lines="2  10"
{!../../../docs_src/custom_response/tutorial009.py!}
```

👆 💪 ⚙️ `response_class` 🔢:

```Python hl_lines="2  8  10"
{!../../../docs_src/custom_response/tutorial009b.py!}
```

👉 💼, 👆 💪 📨 📁 ➡ 🔗 ⚪️➡️ 👆 *➡ 🛠️* 🔢.

## 🛃 📨 🎓

👆 💪 ✍ 👆 👍 🛃 📨 🎓, 😖 ⚪️➡️ `Response` &amp; ⚙️ ⚫️.

🖼, ➡️ 💬 👈 👆 💚 ⚙️ <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a>, ✋️ ⏮️ 🛃 ⚒ 🚫 ⚙️ 🔌 `ORJSONResponse` 🎓.

➡️ 💬 👆 💚 ⚫️ 📨 🔂 &amp; 📁 🎻, 👆 💚 ⚙️ Orjson 🎛 `orjson.OPT_INDENT_2`.

👆 💪 ✍ `CustomORJSONResponse`. 👑 👜 👆 ✔️ ✍ `Response.render(content)` 👩‍🔬 👈 📨 🎚 `bytes`:

```Python hl_lines="9-14  17"
{!../../../docs_src/custom_response/tutorial009c.py!}
```

🔜 ↩️ 🛬:

```json
{"message": "Hello World"}
```

...👉 📨 🔜 📨:

```json
{
  "message": "Hello World"
}
```

↗️, 👆 🔜 🎲 🔎 🌅 👍 🌌 ✊ 📈 👉 🌘 ❕ 🎻. 👶

## 🔢 📨 🎓

🕐❔ 🏗 **FastAPI** 🎓 👐 ⚖️ `APIRouter` 👆 💪 ✔ ❔ 📨 🎓 ⚙️ 🔢.

🔢 👈 🔬 👉 `default_response_class`.

🖼 🔛, **FastAPI** 🔜 ⚙️ `ORJSONResponse` 🔢, 🌐 *➡ 🛠️*, ↩️ `JSONResponse`.

```Python hl_lines="2  4"
{!../../../docs_src/custom_response/tutorial010.py!}
```

!!! tip
    👆 💪 🔐 `response_class` *➡ 🛠️* ⏭.

## 🌖 🧾

👆 💪 📣 📻 🆎 &amp; 📚 🎏 ℹ 🗄 ⚙️ `responses`: [🌖 📨 🗄](additional-responses.md){.internal-link target=_blank}.
