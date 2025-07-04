# 🛃 📨 - 🕸, 🎏, 📁, 🎏

🔢, **FastAPI** 🔜 📨 📨 ⚙️ `JSONResponse`.

👆 💪 🔐 ⚫️ 🛬 `Response` 🔗 👀 [📨 📨 🔗](response-directly.md){.internal-link target=_blank}.

✋️ 🚥 👆 📨 `Response` 🔗, 📊 🏆 🚫 🔁 🗜, &amp; 🧾 🏆 🚫 🔁 🏗 (🖼, 🔌 🎯 "📻 🆎", 🇺🇸🔍 🎚 `Content-Type` 🍕 🏗 🗄).

✋️ 👆 💪 📣 `Response` 👈 👆 💚 ⚙️, *➡ 🛠️ 👨‍🎨*.

🎚 👈 👆 📨 ⚪️➡️ 👆 *➡ 🛠️ 🔢* 🔜 🚮 🔘 👈 `Response`.

&amp; 🚥 👈 `Response` ✔️ 🎻 📻 🆎 (`application/json`), 💖 💼 ⏮️ `JSONResponse` &amp; `UJSONResponse`, 💽 👆 📨 🔜 🔁 🗜 (&amp; ⛽) ⏮️ 🙆 Pydantic `response_model` 👈 👆 📣 *➡ 🛠️ 👨‍🎨*.

/// note

🚥 👆 ⚙️ 📨 🎓 ⏮️ 🙅‍♂ 📻 🆎, FastAPI 🔜 ⌛ 👆 📨 ✔️ 🙅‍♂ 🎚, ⚫️ 🔜 🚫 📄 📨 📁 🚮 🏗 🗄 🩺.

///

## ⚙️ `ORJSONResponse`

🖼, 🚥 👆 ✊ 🎭, 👆 💪 ❎ &amp; ⚙️ <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a> &amp; ⚒ 📨 `ORJSONResponse`.

🗄 `Response` 🎓 (🎧-🎓) 👆 💚 ⚙️ &amp; 📣 ⚫️ *➡ 🛠️ 👨‍🎨*.

⭕ 📨, 📨 `Response` 🔗 🌅 ⏩ 🌘 🛬 📖.

👉 ↩️ 🔢, FastAPI 🔜 ✔ 🔠 🏬 🔘 &amp; ⚒ 💭 ⚫️ 🎻 ⏮️ 🎻, ⚙️ 🎏 [🎻 🔗 🔢](../tutorial/encoder.md){.internal-link target=_blank} 🔬 🔰. 👉 ⚫️❔ ✔ 👆 📨 **❌ 🎚**, 🖼 💽 🏷.

✋️ 🚥 👆 🎯 👈 🎚 👈 👆 🛬 **🎻 ⏮️ 🎻**, 👆 💪 🚶‍♀️ ⚫️ 🔗 📨 🎓 &amp; ❎ ➕ 🌥 👈 FastAPI 🔜 ✔️ 🚶‍♀️ 👆 📨 🎚 🔘 `jsonable_encoder` ⏭ 🚶‍♀️ ⚫️ 📨 🎓.

{* ../../docs_src/custom_response/tutorial001b.py hl[2,7] *}

/// info

🔢 `response_class` 🔜 ⚙️ 🔬 "📻 🆎" 📨.

👉 💼, 🇺🇸🔍 🎚 `Content-Type` 🔜 ⚒ `application/json`.

 &amp; ⚫️ 🔜 📄 ✅ 🗄.

///

/// tip

`ORJSONResponse` ⏳ 🕴 💪 FastAPI, 🚫 💃.

///

## 🕸 📨

📨 📨 ⏮️ 🕸 🔗 ⚪️➡️ **FastAPI**, ⚙️ `HTMLResponse`.

* 🗄 `HTMLResponse`.
* 🚶‍♀️ `HTMLResponse` 🔢 `response_class` 👆 *➡ 🛠️ 👨‍🎨*.

{* ../../docs_src/custom_response/tutorial002.py hl[2,7] *}

/// info

🔢 `response_class` 🔜 ⚙️ 🔬 "📻 🆎" 📨.

👉 💼, 🇺🇸🔍 🎚 `Content-Type` 🔜 ⚒ `text/html`.

 &amp; ⚫️ 🔜 📄 ✅ 🗄.

///

### 📨 `Response`

👀 [📨 📨 🔗](response-directly.md){.internal-link target=_blank}, 👆 💪 🔐 📨 🔗 👆 *➡ 🛠️*, 🛬 ⚫️.

🎏 🖼 ⚪️➡️ 🔛, 🛬 `HTMLResponse`, 💪 👀 💖:

{* ../../docs_src/custom_response/tutorial003.py hl[2,7,19] *}

/// warning

`Response` 📨 🔗 👆 *➡ 🛠️ 🔢* 🏆 🚫 📄 🗄 (🖼, `Content-Type` 🏆 🚫 📄) &amp; 🏆 🚫 ⭐ 🏧 🎓 🩺.

///

/// info

↗️, ☑ `Content-Type` 🎚, 👔 📟, ♒️, 🔜 👟 ⚪️➡️ `Response` 🎚 👆 📨.

///

### 📄 🗄 &amp; 🔐 `Response`

🚥 👆 💚 🔐 📨 ⚪️➡️ 🔘 🔢 ✋️ 🎏 🕰 📄 "📻 🆎" 🗄, 👆 💪 ⚙️ `response_class` 🔢 &amp; 📨 `Response` 🎚.

`response_class` 🔜 ⤴️ ⚙️ 🕴 📄 🗄 *➡ 🛠️*, ✋️ 👆 `Response` 🔜 ⚙️.

#### 📨 `HTMLResponse` 🔗

🖼, ⚫️ 💪 🕳 💖:

{* ../../docs_src/custom_response/tutorial004.py hl[7,21,23] *}

👉 🖼, 🔢 `generate_html_response()` ⏪ 🏗 &amp; 📨 `Response` ↩️ 🛬 🕸 `str`.

🛬 🏁 🤙 `generate_html_response()`, 👆 ⏪ 🛬 `Response` 👈 🔜 🔐 🔢 **FastAPI** 🎭.

✋️ 👆 🚶‍♀️ `HTMLResponse` `response_class` 💁‍♂️, **FastAPI** 🔜 💭 ❔ 📄 ⚫️ 🗄 &amp; 🎓 🩺 🕸 ⏮️ `text/html`:

<img src="/img/tutorial/custom-response/image01.png">

## 💪 📨

📥 💪 📨.

✔️ 🤯 👈 👆 💪 ⚙️ `Response` 📨 🕳 🙆, ⚖️ ✍ 🛃 🎧-🎓.

/// note | 📡 ℹ

👆 💪 ⚙️ `from starlette.responses import HTMLResponse`.

**FastAPI** 🚚 🎏 `starlette.responses` `fastapi.responses` 🏪 👆, 👩‍💻. ✋️ 🌅 💪 📨 👟 🔗 ⚪️➡️ 💃.

///

### `Response`

👑 `Response` 🎓, 🌐 🎏 📨 😖 ⚪️➡️ ⚫️.

👆 💪 📨 ⚫️ 🔗.

⚫️ 🚫 📄 🔢:

* `content` - `str` ⚖️ `bytes`.
* `status_code` - `int` 🇺🇸🔍 👔 📟.
* `headers` - `dict` 🎻.
* `media_type` - `str` 🤝 📻 🆎. 🤶 Ⓜ. `"text/html"`.

FastAPI (🤙 💃) 🔜 🔁 🔌 🎚-📐 🎚. ⚫️ 🔜 🔌 🎚-🆎 🎚, ⚓️ 🔛 = &amp; 🔁 = ✍ 🆎.

{* ../../docs_src/response_directly/tutorial002.py hl[1,18] *}

### `HTMLResponse`

✊ ✍ ⚖️ 🔢 &amp; 📨 🕸 📨, 👆 ✍ 🔛.

### `PlainTextResponse`

✊ ✍ ⚖️ 🔢 &amp; 📨 ✅ ✍ 📨.

{* ../../docs_src/custom_response/tutorial005.py hl[2,7,9] *}

### `JSONResponse`

✊ 💽 &amp; 📨 `application/json` 🗜 📨.

👉 🔢 📨 ⚙️ **FastAPI**, 👆 ✍ 🔛.

### `ORJSONResponse`

⏩ 🎛 🎻 📨 ⚙️ <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a>, 👆 ✍ 🔛.

### `UJSONResponse`

🎛 🎻 📨 ⚙️ <a href="https://github.com/ultrajson/ultrajson" class="external-link" target="_blank">`ujson`</a>.

/// warning

`ujson` 🌘 💛 🌘 🐍 🏗-🛠️ ❔ ⚫️ 🍵 📐-💼.

///

{* ../../docs_src/custom_response/tutorial001.py hl[2,7] *}

/// tip

⚫️ 💪 👈 `ORJSONResponse` 💪 ⏩ 🎛.

///

### `RedirectResponse`

📨 🇺🇸🔍 ❎. ⚙️ 3️⃣0️⃣7️⃣ 👔 📟 (🍕 ❎) 🔢.

👆 💪 📨 `RedirectResponse` 🔗:

{* ../../docs_src/custom_response/tutorial006.py hl[2,9] *}

---

⚖️ 👆 💪 ⚙️ ⚫️ `response_class` 🔢:


{* ../../docs_src/custom_response/tutorial006b.py hl[2,7,9] *}

🚥 👆 👈, ⤴️ 👆 💪 📨 📛 🔗 ⚪️➡️ 👆 *➡ 🛠️* 🔢.

👉 💼, `status_code` ⚙️ 🔜 🔢 1️⃣ `RedirectResponse`, ❔ `307`.

---

👆 💪 ⚙️ `status_code` 🔢 🌀 ⏮️ `response_class` 🔢:

{* ../../docs_src/custom_response/tutorial006c.py hl[2,7,9] *}

### `StreamingResponse`

✊ 🔁 🚂 ⚖️ 😐 🚂/🎻 &amp; 🎏 📨 💪.

{* ../../docs_src/custom_response/tutorial007.py hl[2,14] *}

#### ⚙️ `StreamingResponse` ⏮️ 📁-💖 🎚

🚥 👆 ✔️ 📁-💖 🎚 (✅ 🎚 📨 `open()`), 👆 💪 ✍ 🚂 🔢 🔁 🤭 👈 📁-💖 🎚.

👈 🌌, 👆 🚫 ✔️ ✍ ⚫️ 🌐 🥇 💾, &amp; 👆 💪 🚶‍♀️ 👈 🚂 🔢 `StreamingResponse`, &amp; 📨 ⚫️.

👉 🔌 📚 🗃 🔗 ⏮️ ☁ 💾, 📹 🏭, &amp; 🎏.

```{ .python .annotate hl_lines="2  10-12  14" }
{!../../docs_src/custom_response/tutorial008.py!}
```

1️⃣. 👉 🚂 🔢. ⚫️ "🚂 🔢" ↩️ ⚫️ 🔌 `yield` 📄 🔘.
2️⃣. ⚙️ `with` 🍫, 👥 ⚒ 💭 👈 📁-💖 🎚 📪 ⏮️ 🚂 🔢 🔨. , ⏮️ ⚫️ 🏁 📨 📨.
3️⃣. 👉 `yield from` 💬 🔢 🔁 🤭 👈 👜 🌟 `file_like`. &amp; ⤴️, 🔠 🍕 🔁, 🌾 👈 🍕 👟 ⚪️➡️ 👉 🚂 🔢.

    , ⚫️ 🚂 🔢 👈 📨 "🏭" 👷 🕳 🙆 🔘.

    🔨 ⚫️ 👉 🌌, 👥 💪 🚮 ⚫️ `with` 🍫, &amp; 👈 🌌, 🚚 👈 ⚫️ 📪 ⏮️ 🏁.

/// tip

👀 👈 📥 👥 ⚙️ 🐩 `open()` 👈 🚫 🐕‍🦺 `async` &amp; `await`, 👥 📣 ➡ 🛠️ ⏮️ 😐 `def`.

///

### `FileResponse`

🔁 🎏 📁 📨.

✊ 🎏 ⚒ ❌ 🔗 🌘 🎏 📨 🆎:

* `path` - 📁 📁 🎏.
* `headers` - 🙆 🛃 🎚 🔌, 📖.
* `media_type` - 🎻 🤝 📻 🆎. 🚥 🔢, 📁 ⚖️ ➡ 🔜 ⚙️ 🔑 📻 🆎.
* `filename` - 🚥 ⚒, 👉 🔜 🔌 📨 `Content-Disposition`.

📁 📨 🔜 🔌 ☑ `Content-Length`, `Last-Modified` &amp; `ETag` 🎚.

{* ../../docs_src/custom_response/tutorial009.py hl[2,10] *}

👆 💪 ⚙️ `response_class` 🔢:

{* ../../docs_src/custom_response/tutorial009b.py hl[2,8,10] *}

👉 💼, 👆 💪 📨 📁 ➡ 🔗 ⚪️➡️ 👆 *➡ 🛠️* 🔢.

## 🛃 📨 🎓

👆 💪 ✍ 👆 👍 🛃 📨 🎓, 😖 ⚪️➡️ `Response` &amp; ⚙️ ⚫️.

🖼, ➡️ 💬 👈 👆 💚 ⚙️ <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a>, ✋️ ⏮️ 🛃 ⚒ 🚫 ⚙️ 🔌 `ORJSONResponse` 🎓.

➡️ 💬 👆 💚 ⚫️ 📨 🔂 &amp; 📁 🎻, 👆 💚 ⚙️ Orjson 🎛 `orjson.OPT_INDENT_2`.

👆 💪 ✍ `CustomORJSONResponse`. 👑 👜 👆 ✔️ ✍ `Response.render(content)` 👩‍🔬 👈 📨 🎚 `bytes`:

{* ../../docs_src/custom_response/tutorial009c.py hl[9:14,17] *}

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

{* ../../docs_src/custom_response/tutorial010.py hl[2,4] *}

/// tip

👆 💪 🔐 `response_class` *➡ 🛠️* ⏭.

///

## 🌖 🧾

👆 💪 📣 📻 🆎 &amp; 📚 🎏 ℹ 🗄 ⚙️ `responses`: [🌖 📨 🗄](additional-responses.md){.internal-link target=_blank}.
