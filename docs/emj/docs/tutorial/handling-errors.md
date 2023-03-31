# 🚚 ❌

📤 📚 ⚠ 🌐❔ 👆 💪 🚨 ❌ 👩‍💻 👈 ⚙️ 👆 🛠️.

👉 👩‍💻 💪 🖥 ⏮️ 🕸, 📟 ⚪️➡️ 👱 🙆, ☁ 📳, ♒️.

👆 💪 💪 💬 👩‍💻 👈:

* 👩‍💻 🚫 ✔️ 🥃 😌 👈 🛠️.
* 👩‍💻 🚫 ✔️ 🔐 👈 ℹ.
* 🏬 👩‍💻 🔄 🔐 🚫 🔀.
* ♒️.

👫 💼, 👆 🔜 🛎 📨 **🇺🇸🔍 👔 📟** ↔ **4️⃣0️⃣0️⃣** (⚪️➡️ 4️⃣0️⃣0️⃣ 4️⃣9️⃣9️⃣).

👉 🎏 2️⃣0️⃣0️⃣ 🇺🇸🔍 👔 📟 (⚪️➡️ 2️⃣0️⃣0️⃣ 2️⃣9️⃣9️⃣). 👈 "2️⃣0️⃣0️⃣" 👔 📟 ⛓ 👈 😫 📤 "🏆" 📨.

👔 📟 4️⃣0️⃣0️⃣ ↔ ⛓ 👈 📤 ❌ ⚪️➡️ 👩‍💻.

💭 🌐 👈 **"4️⃣0️⃣4️⃣ 🚫 🔎"** ❌ (&amp; 🤣) ❓

## ⚙️ `HTTPException`

📨 🇺🇸🔍 📨 ⏮️ ❌ 👩‍💻 👆 ⚙️ `HTTPException`.

### 🗄 `HTTPException`

```Python hl_lines="1"
{!../../../docs_src/handling_errors/tutorial001.py!}
```

### 🤚 `HTTPException` 👆 📟

`HTTPException` 😐 🐍 ⚠ ⏮️ 🌖 📊 🔗 🔗.

↩️ ⚫️ 🐍 ⚠, 👆 🚫 `return` ⚫️, 👆 `raise` ⚫️.

👉 ⛓ 👈 🚥 👆 🔘 🚙 🔢 👈 👆 🤙 🔘 👆 *➡ 🛠️ 🔢*, &amp; 👆 🤚 `HTTPException` ⚪️➡️ 🔘 👈 🚙 🔢, ⚫️ 🏆 🚫 🏃 🎂 📟 *➡ 🛠️ 🔢*, ⚫️ 🔜 ❎ 👈 📨 ▶️️ ↖️ &amp; 📨 🇺🇸🔍 ❌ ⚪️➡️ `HTTPException` 👩‍💻.

💰 🙋‍♀ ⚠ 🤭 `return`😅 💲 🔜 🌖 ⭐ 📄 🔃 🔗 &amp; 💂‍♂.

👉 🖼, 🕐❔ 👩‍💻 📨 🏬 🆔 👈 🚫 🔀, 🤚 ⚠ ⏮️ 👔 📟 `404`:

```Python hl_lines="11"
{!../../../docs_src/handling_errors/tutorial001.py!}
```

### 📉 📨

🚥 👩‍💻 📨 `http://example.com/items/foo` ( `item_id` `"foo"`), 👈 👩‍💻 🔜 📨 🇺🇸🔍 👔 📟 2️⃣0️⃣0️⃣, &amp; 🎻 📨:

```JSON
{
  "item": "The Foo Wrestlers"
}
```

✋️ 🚥 👩‍💻 📨 `http://example.com/items/bar` (🚫-🚫 `item_id` `"bar"`), 👈 👩‍💻 🔜 📨 🇺🇸🔍 👔 📟 4️⃣0️⃣4️⃣ ("🚫 🔎" ❌), &amp; 🎻 📨:

```JSON
{
  "detail": "Item not found"
}
```

!!! tip
    🕐❔ 🙋‍♀ `HTTPException`, 👆 💪 🚶‍♀️ 🙆 💲 👈 💪 🗜 🎻 🔢 `detail`, 🚫 🕴 `str`.

    👆 💪 🚶‍♀️ `dict`, `list`, ♒️.

    👫 🍵 🔁 **FastAPI** &amp; 🗜 🎻.

## 🚮 🛃 🎚

📤 ⚠ 🌐❔ ⚫️ ⚠ 💪 🚮 🛃 🎚 🇺🇸🔍 ❌. 🖼, 🆎 💂‍♂.

👆 🎲 🏆 🚫 💪 ⚙️ ⚫️ 🔗 👆 📟.

✋️ 💼 👆 💪 ⚫️ 🏧 😐, 👆 💪 🚮 🛃 🎚:

```Python hl_lines="14"
{!../../../docs_src/handling_errors/tutorial002.py!}
```

## ❎ 🛃 ⚠ 🐕‍🦺

👆 💪 🚮 🛃 ⚠ 🐕‍🦺 ⏮️ <a href="https://www.starlette.io/exceptions/" class="external-link" target="_blank">🎏 ⚠ 🚙 ⚪️➡️ 💃</a>.

➡️ 💬 👆 ✔️ 🛃 ⚠ `UnicornException` 👈 👆 (⚖️ 🗃 👆 ⚙️) 💪 `raise`.

&amp; 👆 💚 🍵 👉 ⚠ 🌐 ⏮️ FastAPI.

👆 💪 🚮 🛃 ⚠ 🐕‍🦺 ⏮️ `@app.exception_handler()`:

```Python hl_lines="5-7  13-18  24"
{!../../../docs_src/handling_errors/tutorial003.py!}
```

📥, 🚥 👆 📨 `/unicorns/yolo`, *➡ 🛠️* 🔜 `raise` `UnicornException`.

✋️ ⚫️ 🔜 🍵 `unicorn_exception_handler`.

, 👆 🔜 📨 🧹 ❌, ⏮️ 🇺🇸🔍 👔 📟 `418` &amp; 🎻 🎚:

```JSON
{"message": "Oops! yolo did something. There goes a rainbow..."}
```

!!! note "📡 ℹ"
    👆 💪 ⚙️ `from starlette.requests import Request` &amp; `from starlette.responses import JSONResponse`.

    **FastAPI** 🚚 🎏 `starlette.responses` `fastapi.responses` 🏪 👆, 👩‍💻. ✋️ 🌅 💪 📨 👟 🔗 ⚪️➡️ 💃. 🎏 ⏮️ `Request`.

## 🔐 🔢 ⚠ 🐕‍🦺

**FastAPI** ✔️ 🔢 ⚠ 🐕‍🦺.

👫 🐕‍🦺 🈚 🛬 🔢 🎻 📨 🕐❔ 👆 `raise` `HTTPException` &amp; 🕐❔ 📨 ✔️ ❌ 💽.

👆 💪 🔐 👫 ⚠ 🐕‍🦺 ⏮️ 👆 👍.

### 🔐 📨 🔬 ⚠

🕐❔ 📨 🔌 ❌ 📊, **FastAPI** 🔘 🤚 `RequestValidationError`.

&amp; ⚫️ 🔌 🔢 ⚠ 🐕‍🦺 ⚫️.

🔐 ⚫️, 🗄 `RequestValidationError` &amp; ⚙️ ⚫️ ⏮️ `@app.exception_handler(RequestValidationError)` 🎀 ⚠ 🐕‍🦺.

⚠ 🐕‍🦺 🔜 📨 `Request` &amp; ⚠.

```Python hl_lines="2  14-16"
{!../../../docs_src/handling_errors/tutorial004.py!}
```

🔜, 🚥 👆 🚶 `/items/foo`, ↩️ 💆‍♂ 🔢 🎻 ❌ ⏮️:

```JSON
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```

👆 🔜 🤚 ✍ ⏬, ⏮️:

```
1 validation error
path -> item_id
  value is not a valid integer (type=type_error.integer)
```

#### `RequestValidationError` 🆚 `ValidationError`

!!! warning
    👫 📡 ℹ 👈 👆 💪 🚶 🚥 ⚫️ 🚫 ⚠ 👆 🔜.

`RequestValidationError` 🎧-🎓 Pydantic <a href="https://pydantic-docs.helpmanual.io/usage/models/#error-handling" class="external-link" target="_blank">`ValidationError`</a>.

**FastAPI** ⚙️ ⚫️ 👈, 🚥 👆 ⚙️ Pydantic 🏷 `response_model`, &amp; 👆 💽 ✔️ ❌, 👆 🔜 👀 ❌ 👆 🕹.

✋️ 👩‍💻/👩‍💻 🔜 🚫 👀 ⚫️. ↩️, 👩‍💻 🔜 📨 "🔗 💽 ❌" ⏮️ 🇺🇸🔍 👔 📟 `500`.

⚫️ 🔜 👉 🌌 ↩️ 🚥 👆 ✔️ Pydantic `ValidationError` 👆 *📨* ⚖️ 🙆 👆 📟 (🚫 👩‍💻 *📨*), ⚫️ 🤙 🐛 👆 📟.

&amp; ⏪ 👆 🔧 ⚫️, 👆 👩‍💻/👩‍💻 🚫🔜 🚫 ✔️ 🔐 🔗 ℹ 🔃 ❌, 👈 💪 🎦 💂‍♂ ⚠.

### 🔐 `HTTPException` ❌ 🐕‍🦺

🎏 🌌, 👆 💪 🔐 `HTTPException` 🐕‍🦺.

🖼, 👆 💪 💚 📨 ✅ ✍ 📨 ↩️ 🎻 👫 ❌:

```Python hl_lines="3-4  9-11  22"
{!../../../docs_src/handling_errors/tutorial004.py!}
```

!!! note "📡 ℹ"
    👆 💪 ⚙️ `from starlette.responses import PlainTextResponse`.

    **FastAPI** 🚚 🎏 `starlette.responses` `fastapi.responses` 🏪 👆, 👩‍💻. ✋️ 🌅 💪 📨 👟 🔗 ⚪️➡️ 💃.

### ⚙️ `RequestValidationError` 💪

`RequestValidationError` 🔌 `body` ⚫️ 📨 ⏮️ ❌ 💽.

👆 💪 ⚙️ ⚫️ ⏪ 🛠️ 👆 📱 🕹 💪 &amp; ℹ ⚫️, 📨 ⚫️ 👩‍💻, ♒️.

```Python hl_lines="14"
{!../../../docs_src/handling_errors/tutorial005.py!}
```

🔜 🔄 📨 ❌ 🏬 💖:

```JSON
{
  "title": "towel",
  "size": "XL"
}
```

👆 🔜 📨 📨 💬 👆 👈 💽 ❌ ⚗ 📨 💪:

```JSON hl_lines="12-15"
{
  "detail": [
    {
      "loc": [
        "body",
        "size"
      ],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ],
  "body": {
    "title": "towel",
    "size": "XL"
  }
}
```

#### FastAPI `HTTPException` 🆚 💃 `HTTPException`

**FastAPI** ✔️ 🚮 👍 `HTTPException`.

&amp; **FastAPI**'Ⓜ `HTTPException` ❌ 🎓 😖 ⚪️➡️ 💃 `HTTPException` ❌ 🎓.

🕴 🔺, 👈 **FastAPI**'Ⓜ `HTTPException` ✔ 👆 🚮 🎚 🔌 📨.

👉 💪/⚙️ 🔘 ✳ 2️⃣.0️⃣ &amp; 💂‍♂ 🚙.

, 👆 💪 🚧 🙋‍♀ **FastAPI**'Ⓜ `HTTPException` 🛎 👆 📟.

✋️ 🕐❔ 👆 ® ⚠ 🐕‍🦺, 👆 🔜 ® ⚫️ 💃 `HTTPException`.

👉 🌌, 🚥 🙆 🍕 💃 🔗 📟, ⚖️ 💃 ↔ ⚖️ 🔌 -, 🤚 💃 `HTTPException`, 👆 🐕‍🦺 🔜 💪 ✊ &amp; 🍵 ⚫️.

👉 🖼, 💪 ✔️ 👯‍♂️ `HTTPException`Ⓜ 🎏 📟, 💃 ⚠ 📁 `StarletteHTTPException`:

```Python
from starlette.exceptions import HTTPException as StarletteHTTPException
```

### 🏤-⚙️ **FastAPI**'Ⓜ ⚠ 🐕‍🦺

🚥 👆 💚 ⚙️ ⚠ ⤴️ ⏮️ 🎏 🔢 ⚠ 🐕‍🦺 ⚪️➡️ **FastAPI**, 👆 💪 🗄 &amp; 🏤-⚙️ 🔢 ⚠ 🐕‍🦺 ⚪️➡️ `fastapi.exception_handlers`:

```Python hl_lines="2-5  15  21"
{!../../../docs_src/handling_errors/tutorial006.py!}
```

👉 🖼 👆 `print`😅 ❌ ⏮️ 📶 🎨 📧, ✋️ 👆 🤚 💭. 👆 💪 ⚙️ ⚠ &amp; ⤴️ 🏤-⚙️ 🔢 ⚠ 🐕‍🦺.
