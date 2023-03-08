# 🥇 🔁

🙅 FastAPI 📁 💪 👀 💖 👉:

```Python
{!../../../docs_src/first_steps/tutorial001.py!}
```

📁 👈 📁 `main.py`.

🏃 🖖 💽:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
<span style="color: green;">INFO</span>:     Started reloader process [28720]
<span style="color: green;">INFO</span>:     Started server process [28722]
<span style="color: green;">INFO</span>:     Waiting for application startup.
<span style="color: green;">INFO</span>:     Application startup complete.
```

</div>

!!! note
    📋 `uvicorn main:app` 🔗:

    * `main`: 📁 `main.py` (🐆 "🕹").
    * `app`: 🎚 ✍ 🔘 `main.py` ⏮ ⏸ `app = FastAPI()`.
    * `--reload`: ⚒ 💽 ⏏ ⏮ 📟 🔀. 🕴 ⚙️ 🛠.

🔢, 📤 ⏸ ⏮ 🕳 💖:

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

👈 ⏸ 🎦 📛 🌐❔ 👆 📱 ➖ 🍦, 👆 🇧🇿 🎰.

### ✅ ⚫️

📂 👆 🖥 <a href="http://127.0.0.1:8000" class="external-link" target="_blank">Http://127.0.0.1:8000</a>.

👆 🔜 👀 🎻 📨:

```JSON
{"message": "Hello World"}
```

### 🎓 🛠 🩺

🔜 🚶 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">Http://127.0.0.1:8000/docs</a>.

👆 🔜 👀 🏧 🎓 🛠 🧾 (🚚 <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">🦁 🎚</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### 🎛 🛠 🩺

&amp; 🔜, 🚶 <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">Http://127.0.0.1:8000/redoc</a>.

👆 🔜 👀 🎛 🏧 🧾 (🚚 <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">📄</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### 🗄

**FastAPI** 🏗 "🔗" ⏮ 🌐 👆 🛠 ⚙️ **🗄** 🐩 ⚖ 🔗.

#### "🔗"

"🔗" 🔑 ⚖️ 📛 🕳. 🚫 📟 👈 🛠 ⚫️, ✋️ 📝 📛.

#### 🛠 "🔗"

👉 💼, <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">🗄</a> 🔧 👈 🤔 ❔ 🔬 🔗 👆 🛠.

👉 🔗 🔑 🔌 👆 🛠 ➡, 💪 🔢 👫 ✊, ♒️.

#### 💽 "🔗"

⚖ "🔗" 💪 🔗 💠 💽, 💖 🎻 🎚.

👈 💼, ⚫️ 🔜 ⛓ 🎻 🔢, &amp; 📊 🆎 👫 ✔️, ♒️.

#### 🗄 &amp; 🎻 🔗

🗄 🔬 🛠 🔗 👆 🛠. &amp; 👈 🔗 🔌 🔑 (⚖️ "🔗") 📊 📨 &amp; 📨 👆 🛠 ⚙️ **🎻 🔗**, 🐩 🎻 📊 🔗.

#### ✅ `openapi.json`

🚥 👆 😟 🔃 ❔ 🍣 🗄 🔗 👀 💖, FastAPI 🔁 🏗 🎻 (🔗) ⏮ 📛 🌐 👆 🛠.

👆 💪 👀 ⚫️ 🔗: <a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">Http://127.0.0.1:8000/openapi.json</a>.

⚫️ 🔜 🎦 🎻 ▶ ⏮ 🕳 💖:

```JSON
{
    "openapi": "3.0.2",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {



...
```

#### ⚫️❔ 🗄 

🗄 🔗 ⚫️❔ 🏋️ 2⃣ 🎓 🧾 ⚙️ 🔌.

&amp; 📤 💯 🎛, 🌐 ⚓️ 🔛 🗄. 👆 💪 💪 🚮 🙆 📚 🎛 👆 🈸 🏗 ⏮ **FastAPI**.

👆 💪 ⚙️ ⚫️ 🏗 📟 🔁, 👩‍💻 👈 🔗 ⏮ 👆 🛠. 🖼, 🕸, 📱 ⚖️ ☁ 🈸.

## 🌃, 🔁 🔁

### 🔁 1⃣: 🗄 `FastAPI`

```Python hl_lines="1"
{!../../../docs_src/first_steps/tutorial001.py!}
```

`FastAPI` 🐆 🎓 👈 🚚 🌐 🛠 👆 🛠.

!!! note "📡 ℹ"
    `FastAPI` 🎓 👈 😖 🔗 ⚪️➡️ `Starlette`.

    👆 💪 ⚙️ 🌐 <a href="https://www.starlette.io/" class="external-link" target="_blank">💃</a> 🛠 ⏮ `FastAPI` 💁‍♂️.

### 🔁 2⃣: ✍ `FastAPI` "👐"

```Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial001.py!}
```

📥 `app` 🔢 🔜 "👐" 🎓 `FastAPI`.

👉 🔜 👑 ☝ 🔗 ✍ 🌐 👆 🛠.

👉 `app` 🎏 1⃣ 🔗 `uvicorn` 📋:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

🚥 👆 ✍ 👆 📱 💖:

```Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial002.py!}
```

&amp; 🚮 ⚫️ 📁 `main.py`, ⤴ 👆 🔜 🤙 `uvicorn` 💖:

<div class="termy">

```console
$ uvicorn main:my_awesome_api --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

### 🔁 3⃣: ✍ *➡ 🛠*

#### ➡

"➡" 📥 🔗 🏁 🍕 📛 ▶ ⚪️➡️ 🥇 `/`.

, 📛 💖:

```
https://example.com/items/foo
```

...➡ 🔜:

```
/items/foo
```

!!! info
     "➡" 🛎 🤙 "🔗" ⚖️ "🛣".

⏪ 🏗 🛠, "➡" 👑 🌌 🎏 "⚠" &amp; "ℹ".

#### 🛠

"🛠" 📥 🔗 1⃣ 🇺🇸🔍 "👩‍🔬".

1⃣:

* `POST`
* `GET`
* `PUT`
* `DELETE`

...&amp; 🌅 😍 🕐:

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

🇺🇸🔍 🛠, 👆 💪 🔗 🔠 ➡ ⚙️ 1⃣ (⚖️ 🌅) 👫 "👩‍🔬".

---

🕐❔ 🏗 🔗, 👆 🛎 ⚙️ 👫 🎯 🇺🇸🔍 👩‍🔬 🎭 🎯 🎯.

🛎 👆 ⚙️:

* `POST`: ✍ 💽.
* `GET`: ✍ 💽.
* `PUT`: ℹ 💽.
* `DELETE`: ❎ 💽.

, 🗄, 🔠 🇺🇸🔍 👩‍🔬 🤙 "🛠".

👥 🔜 🤙 👫 "**🛠**" 💁‍♂️.

#### 🔬 *➡ 🛠 👨‍🎨*

```Python hl_lines="6"
{!../../../docs_src/first_steps/tutorial001.py!}
```

`@app.get("/")` 💬 **FastAPI** 👈 🔢 ▶️ 🔛 🈚 🚚 📨 👈 🚶:

* ➡ `/`
* ⚙️ <abbr title="an HTTP GET method"><code>get</code> 🛠</abbr>

!!! info "`@decorator` ℹ"
    👈 `@something` ❕ 🐆 🤙 "👨‍🎨".

    👆 🚮 ⚫️ 🔛 🔝 🔢. 💖 📶 📔 👒 (👤 💭 👈 🌐❔ ⚖ 👟 ⚪️➡️).

     "👨‍🎨" ✊ 🔢 🔛 &amp; 🔨 🕳 ⏮ ⚫️.

    👆 💼, 👉 👨‍🎨 💬 **FastAPI** 👈 🔢 🔛 🔗 **➡** `/` ⏮ **🛠** `get`.

    ⚫️ "**➡ 🛠 👨‍🎨**".

👆 💪 ⚙️ 🎏 🛠:

* `@app.post()`
* `@app.put()`
* `@app.delete()`

&amp; 🌅 😍 🕐:

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

!!! tip
    👆 🆓 ⚙️ 🔠 🛠 (🇺🇸🔍 👩‍🔬) 👆 🎋.

    **FastAPI** 🚫 🛠 🙆 🎯 🔑.

    ℹ 📥 🎁 📄, 🚫 📄.

    🖼, 🕐❔ ⚙️ 🕹 👆 🛎 🎭 🌐 🎯 ⚙️ 🕴 `POST` 🛠.

### 🔁 4⃣: 🔬 **➡ 🛠 🔢**

👉 👆 "**➡ 🛠 🔢**":

* **➡**: `/`.
* **🛠**: `get`.
* **🔢**: 🔢 🔛 "👨‍🎨" (🔛 `@app.get("/")`).

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial001.py!}
```

👉 🐆 🔢.

⚫️ 🔜 🤙 **FastAPI** 🕐❔ ⚫️ 📨 📨 📛 "`/`" ⚙️ `GET` 🛠.

👉 💼, ⚫️ `async` 🔢.

---

👆 💪 🔬 ⚫️ 😐 🔢 ↩️ `async def`:

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial003.py!}
```

!!! note
    🚥 👆 🚫 💭 🔺, ✅ [🔁: *"🏃 ❓"*](../async.md#in-a-hurry){.internal-link target=_blank}.

### 🔁 5⃣: 📨 🎚

```Python hl_lines="8"
{!../../../docs_src/first_steps/tutorial001.py!}
```

👆 💪 📨 `dict`, `list`, ⭐ 💲 `str`, `int`, ♒️.

👆 💪 📨 Pydantic 🏷 (👆 🔜 👀 🌅 🔃 👈 ⏪).

📤 📚 🎏 🎚 &amp; 🏷 👈 🔜 🔁 🗜 🎻 (🔌 🐜, ♒️). 🔄 ⚙️ 👆 💕 🕐, ⚫️ 🏆 🎲 👈 👫 ⏪ 🐕‍🦺.

## 🌃

* 🗄 `FastAPI`.
* ✍ `app` 👐.
* ✍ **➡ 🛠 👨‍🎨** (💖 `@app.get("/")`).
* ✍ **➡ 🛠 🔢** (💖 `def root(): ...` 🔛).
* 🏃 🛠 💽 (💖 `uvicorn main:app --reload`).
