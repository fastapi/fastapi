# 📨 📁

👆 💪 🔬 📁 📂 👩‍💻 ⚙️ `File`.

/// info

📨 📂 📁, 🥇 ❎ <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>.

🤶 Ⓜ. `pip install python-multipart`.

👉 ↩️ 📂 📁 📨 "📨 💽".

///

## 🗄 `File`

🗄 `File` &amp; `UploadFile` ⚪️➡️ `fastapi`:

{* ../../docs_src/request_files/tutorial001.py hl[1] *}


## 🔬 `File` 🔢

✍ 📁 🔢 🎏 🌌 👆 🔜 `Body` ⚖️ `Form`:

{* ../../docs_src/request_files/tutorial001.py hl[7] *}


/// info

`File` 🎓 👈 😖 🔗 ⚪️➡️ `Form`.

✋️ 💭 👈 🕐❔ 👆 🗄 `Query`, `Path`, `File` &amp; 🎏 ⚪️➡️ `fastapi`, 👈 🤙 🔢 👈 📨 🎁 🎓.

///

/// tip

📣 📁 💪, 👆 💪 ⚙️ `File`, ↩️ ⏪ 🔢 🔜 🔬 🔢 🔢 ⚖️ 💪 (🎻) 🔢.

///

📁 🔜 📂 "📨 💽".

🚥 👆 📣 🆎 👆 *➡ 🛠️ 🔢* 🔢 `bytes`, **FastAPI** 🔜 ✍ 📁 👆 &amp; 👆 🔜 📨 🎚 `bytes`.

✔️ 🤯 👈 👉 ⛓ 👈 🎂 🎚 🔜 🏪 💾. 👉 🔜 👷 👍 🤪 📁.

✋️ 📤 📚 💼 ❔ 👆 💪 💰 ⚪️➡️ ⚙️ `UploadFile`.

## 📁 🔢 ⏮️ `UploadFile`

🔬 📁 🔢 ⏮️ 🆎 `UploadFile`:

{* ../../docs_src/request_files/tutorial001.py hl[12] *}


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

/// note | `async` 📡 ℹ

🕐❔ 👆 ⚙️ `async` 👩‍🔬, **FastAPI** 🏃 📁 👩‍🔬 🧵 &amp; ⌛ 👫.

///

/// note | 💃 📡 ℹ

**FastAPI**'Ⓜ `UploadFile` 😖 🔗 ⚪️➡️ **💃**'Ⓜ `UploadFile`, ✋️ 🚮 💪 🍕 ⚒ ⚫️ 🔗 ⏮️ **Pydantic** &amp; 🎏 🍕 FastAPI.

///

## ⚫️❔ "📨 💽"

🌌 🕸 📨 (`<form></form>`) 📨 💽 💽 🛎 ⚙️ "🎁" 🔢 👈 📊, ⚫️ 🎏 ⚪️➡️ 🎻.

**FastAPI** 🔜 ⚒ 💭 ✍ 👈 📊 ⚪️➡️ ▶️️ 🥉 ↩️ 🎻.

/// note | 📡 ℹ

📊 ⚪️➡️ 📨 🛎 🗜 ⚙️ "📻 🆎" `application/x-www-form-urlencoded` 🕐❔ ⚫️ 🚫 🔌 📁.

✋️ 🕐❔ 📨 🔌 📁, ⚫️ 🗜 `multipart/form-data`. 🚥 👆 ⚙️ `File`, **FastAPI** 🔜 💭 ⚫️ ✔️ 🤚 📁 ⚪️➡️ ☑ 🍕 💪.

🚥 👆 💚 ✍ 🌖 🔃 👉 🔢 &amp; 📨 🏑, 👳 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">🏇</abbr> 🕸 🩺 <code>POST</code></a>.

///

/// warning

👆 💪 📣 💗 `File` &amp; `Form` 🔢 *➡ 🛠️*, ✋️ 👆 💪 🚫 📣 `Body` 🏑 👈 👆 ⌛ 📨 🎻, 📨 🔜 ✔️ 💪 🗜 ⚙️ `multipart/form-data` ↩️ `application/json`.

👉 🚫 🚫 **FastAPI**, ⚫️ 🍕 🇺🇸🔍 🛠️.

///

## 📦 📁 📂

👆 💪 ⚒ 📁 📦 ⚙️ 🐩 🆎 ✍ &amp; ⚒ 🔢 💲 `None`:

//// tab | 🐍 3️⃣.6️⃣ &amp; 🔛

{* ../../docs_src/request_files/tutorial001_02.py hl[9,17] *}


////

//// tab | 🐍 3️⃣.1️⃣0️⃣ &amp; 🔛

{* ../../docs_src/request_files/tutorial001_02_py310.py hl[7,14] *}


////

## `UploadFile` ⏮️ 🌖 🗃

👆 💪 ⚙️ `File()` ⏮️ `UploadFile`, 🖼, ⚒ 🌖 🗃:

{* ../../docs_src/request_files/tutorial001_03.py hl[13] *}


## 💗 📁 📂

⚫️ 💪 📂 📚 📁 🎏 🕰.

👫 🔜 👨‍💼 🎏 "📨 🏑" 📨 ⚙️ "📨 💽".

⚙️ 👈, 📣 📇 `bytes` ⚖️ `UploadFile`:

//// tab | 🐍 3️⃣.6️⃣ &amp; 🔛

{* ../../docs_src/request_files/tutorial002.py hl[10,15] *}


////

//// tab | 🐍 3️⃣.9️⃣ &amp; 🔛

{* ../../docs_src/request_files/tutorial002_py39.py hl[8,13] *}


////

👆 🔜 📨, 📣, `list` `bytes` ⚖️ `UploadFile`Ⓜ.

/// note | 📡 ℹ

👆 💪 ⚙️ `from starlette.responses import HTMLResponse`.

**FastAPI** 🚚 🎏 `starlette.responses` `fastapi.responses` 🏪 👆, 👩‍💻. ✋️ 🌅 💪 📨 👟 🔗 ⚪️➡️ 💃.

///

### 💗 📁 📂 ⏮️ 🌖 🗃

&amp; 🎏 🌌 ⏭, 👆 💪 ⚙️ `File()` ⚒ 🌖 🔢, `UploadFile`:

//// tab | 🐍 3️⃣.6️⃣ &amp; 🔛

{* ../../docs_src/request_files/tutorial003.py hl[18] *}


////

//// tab | 🐍 3️⃣.9️⃣ &amp; 🔛

{* ../../docs_src/request_files/tutorial003_py39.py hl[16] *}


////

## 🌃

⚙️ `File`, `bytes`, &amp; `UploadFile` 📣 📁 📂 📨, 📨 📨 💽.
