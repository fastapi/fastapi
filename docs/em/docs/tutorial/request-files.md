# 📨 📁

👆 💪 🔬 📁 📂 👩‍💻 ⚙️ `File`.

!!! info
    📨 📂 📁, 🥇 ❎ <a href="https://andrew-d.github.io/python-multipart/" class="external-link" target="_blank">`python-multipart`</a>.

    🤶 Ⓜ. `pip install python-multipart`.

    👉 ↩️ 📂 📁 📨 "📨 💽".

## 🗄 `File`

🗄 `File` &amp; `UploadFile` ⚪️➡️ `fastapi`:

```Python hl_lines="1"
{!../../../docs_src/request_files/tutorial001.py!}
```

## 🔬 `File` 🔢

✍ 📁 🔢 🎏 🌌 👆 🔜 `Body` ⚖️ `Form`:

```Python hl_lines="7"
{!../../../docs_src/request_files/tutorial001.py!}
```

!!! info
    `File` 🎓 👈 😖 🔗 ⚪️➡️ `Form`.

    ✋️ 💭 👈 🕐❔ 👆 🗄 `Query`, `Path`, `File` &amp; 🎏 ⚪️➡️ `fastapi`, 👈 🤙 🔢 👈 📨 🎁 🎓.

!!! tip
    📣 📁 💪, 👆 💪 ⚙️ `File`, ↩️ ⏪ 🔢 🔜 🔬 🔢 🔢 ⚖️ 💪 (🎻) 🔢.

📁 🔜 📂 "📨 💽".

🚥 👆 📣 🆎 👆 *➡ 🛠️ 🔢* 🔢 `bytes`, **FastAPI** 🔜 ✍ 📁 👆 &amp; 👆 🔜 📨 🎚 `bytes`.

✔️ 🤯 👈 👉 ⛓ 👈 🎂 🎚 🔜 🏪 💾. 👉 🔜 👷 👍 🤪 📁.

✋️ 📤 📚 💼 ❔ 👆 💪 💰 ⚪️➡️ ⚙️ `UploadFile`.

## 📁 🔢 ⏮️ `UploadFile`

🔬 📁 🔢 ⏮️ 🆎 `UploadFile`:

```Python hl_lines="12"
{!../../../docs_src/request_files/tutorial001.py!}
```

⚙️ `UploadFile` ✔️ 📚 📈 🤭 `bytes`:

* 👆 🚫 ✔️ ⚙️ `File()` 🔢 💲 🔢.
* ⚫️ ⚙️ "🧵" 📁:
    * 📁 🏪 💾 🆙 🔆 📐 📉, &amp; ⏮️ 🚶‍♀️ 👉 📉 ⚫️ 🔜 🏪 💾.
* 👉 ⛓ 👈 ⚫️ 🔜 👷 👍 ⭕ 📁 💖 🖼, 📹, ⭕ 💱, ♒️. 🍵 😩 🌐 💾.
* 👆 💪 🤚 🗃 ⚪️➡️ 📂 📁.
* ⚫️ ✔️ <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">📁-💖</a> `async` 🔢.
* ⚫️ 🎦 ☑ 🐍 <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a> 🎚 👈 👆 💪 🚶‍♀️ 🔗 🎏 🗃 👈 ⌛ 📁-💖 🎚.

### `UploadFile`

`UploadFile` ✔️ 📄 🔢:

* `filename`: `str` ⏮️ ⏮️ 📁 📛 👈 📂 (✅ `myimage.jpg`).
* `content_type`: `str` ⏮️ 🎚 🆎 (📁 🆎 / 📻 🆎) (✅ `image/jpeg`).
* `file`: <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a> ( <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">📁-💖</a> 🎚). 👉 ☑ 🐍 📁 👈 👆 💪 🚶‍♀️ 🔗 🎏 🔢 ⚖️ 🗃 👈 ⌛ "📁-💖" 🎚.

`UploadFile` ✔️ 📄 `async` 👩‍🔬. 👫 🌐 🤙 🔗 📁 👩‍🔬 🔘 (⚙️ 🔗 `SpooledTemporaryFile`).

* `write(data)`: ✍ `data` (`str` ⚖️ `bytes`) 📁.
* `read(size)`: ✍ `size` (`int`) 🔢/🦹 📁.
* `seek(offset)`: 🚶 🔢 🧘 `offset` (`int`) 📁.
    * 🤶 Ⓜ., `await myfile.seek(0)` 🔜 🚶 ▶️ 📁.
    * 👉 ✴️ ⚠ 🚥 👆 🏃 `await myfile.read()` 🕐 &amp; ⤴️ 💪 ✍ 🎚 🔄.
* `close()`: 🔐 📁.

🌐 👫 👩‍🔬 `async` 👩‍🔬, 👆 💪 "⌛" 👫.

🖼, 🔘 `async` *➡ 🛠️ 🔢* 👆 💪 🤚 🎚 ⏮️:

```Python
contents = await myfile.read()
```

🚥 👆 🔘 😐 `def` *➡ 🛠️ 🔢*, 👆 💪 🔐 `UploadFile.file` 🔗, 🖼:

```Python
contents = myfile.file.read()
```

!!! note "`async` 📡 ℹ"
    🕐❔ 👆 ⚙️ `async` 👩‍🔬, **FastAPI** 🏃 📁 👩‍🔬 🧵 &amp; ⌛ 👫.

!!! note "💃 📡 ℹ"
    **FastAPI**'Ⓜ `UploadFile` 😖 🔗 ⚪️➡️ **💃**'Ⓜ `UploadFile`, ✋️ 🚮 💪 🍕 ⚒ ⚫️ 🔗 ⏮️ **Pydantic** &amp; 🎏 🍕 FastAPI.

## ⚫️❔ "📨 💽"

🌌 🕸 📨 (`<form></form>`) 📨 💽 💽 🛎 ⚙️ "🎁" 🔢 👈 📊, ⚫️ 🎏 ⚪️➡️ 🎻.

**FastAPI** 🔜 ⚒ 💭 ✍ 👈 📊 ⚪️➡️ ▶️️ 🥉 ↩️ 🎻.

!!! note "📡 ℹ"
    📊 ⚪️➡️ 📨 🛎 🗜 ⚙️ "📻 🆎" `application/x-www-form-urlencoded` 🕐❔ ⚫️ 🚫 🔌 📁.

    ✋️ 🕐❔ 📨 🔌 📁, ⚫️ 🗜 `multipart/form-data`. 🚥 👆 ⚙️ `File`, **FastAPI** 🔜 💭 ⚫️ ✔️ 🤚 📁 ⚪️➡️ ☑ 🍕 💪.

    🚥 👆 💚 ✍ 🌖 🔃 👉 🔢 &amp; 📨 🏑, 👳 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">🏇</abbr> 🕸 🩺 <code>POST</code></a>.

!!! warning
    👆 💪 📣 💗 `File` &amp; `Form` 🔢 *➡ 🛠️*, ✋️ 👆 💪 🚫 📣 `Body` 🏑 👈 👆 ⌛ 📨 🎻, 📨 🔜 ✔️ 💪 🗜 ⚙️ `multipart/form-data` ↩️ `application/json`.

    👉 🚫 🚫 **FastAPI**, ⚫️ 🍕 🇺🇸🔍 🛠️.

## 📦 📁 📂

👆 💪 ⚒ 📁 📦 ⚙️ 🐩 🆎 ✍ &amp; ⚒ 🔢 💲 `None`:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="9  17"
    {!> ../../../docs_src/request_files/tutorial001_02.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="7  14"
    {!> ../../../docs_src/request_files/tutorial001_02_py310.py!}
    ```

## `UploadFile` ⏮️ 🌖 🗃

👆 💪 ⚙️ `File()` ⏮️ `UploadFile`, 🖼, ⚒ 🌖 🗃:

```Python hl_lines="13"
{!../../../docs_src/request_files/tutorial001_03.py!}
```

## 💗 📁 📂

⚫️ 💪 📂 📚 📁 🎏 🕰.

👫 🔜 👨‍💼 🎏 "📨 🏑" 📨 ⚙️ "📨 💽".

⚙️ 👈, 📣 📇 `bytes` ⚖️ `UploadFile`:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="10  15"
    {!> ../../../docs_src/request_files/tutorial002.py!}
    ```

=== "🐍 3️⃣.9️⃣ &amp; 🔛"

    ```Python hl_lines="8  13"
    {!> ../../../docs_src/request_files/tutorial002_py39.py!}
    ```

👆 🔜 📨, 📣, `list` `bytes` ⚖️ `UploadFile`Ⓜ.

!!! note "📡 ℹ"
    👆 💪 ⚙️ `from starlette.responses import HTMLResponse`.

    **FastAPI** 🚚 🎏 `starlette.responses` `fastapi.responses` 🏪 👆, 👩‍💻. ✋️ 🌅 💪 📨 👟 🔗 ⚪️➡️ 💃.

### 💗 📁 📂 ⏮️ 🌖 🗃

&amp; 🎏 🌌 ⏭, 👆 💪 ⚙️ `File()` ⚒ 🌖 🔢, `UploadFile`:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="18"
    {!> ../../../docs_src/request_files/tutorial003.py!}
    ```

=== "🐍 3️⃣.9️⃣ &amp; 🔛"

    ```Python hl_lines="16"
    {!> ../../../docs_src/request_files/tutorial003_py39.py!}
    ```

## 🌃

⚙️ `File`, `bytes`, &amp; `UploadFile` 📣 📁 📂 📨, 📨 📨 💽.
