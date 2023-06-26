# 📨 👔 📟

🎏 🌌 👆 💪 ✔ 📨 🏷, 👆 💪 📣 🇺🇸🔍 👔 📟 ⚙️ 📨 ⏮️ 🔢 `status_code` 🙆 *➡ 🛠️*:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* ♒️.

```Python hl_lines="6"
{!../../../docs_src/response_status_code/tutorial001.py!}
```

!!! note
    👀 👈 `status_code` 🔢 "👨‍🎨" 👩‍🔬 (`get`, `post`, ♒️). 🚫 👆 *➡ 🛠️ 🔢*, 💖 🌐 🔢 &amp; 💪.

`status_code` 🔢 📨 🔢 ⏮️ 🇺🇸🔍 👔 📟.

!!! info
    `status_code` 💪 👐 📨 `IntEnum`, ✅ 🐍 <a href="https://docs.python.org/3/library/http.html#http.HTTPStatus" class="external-link" target="_blank">`http.HTTPStatus`</a>.

⚫️ 🔜:

* 📨 👈 👔 📟 📨.
* 📄 ⚫️ ✅ 🗄 🔗 ( &amp; , 👩‍💻 🔢):

<img src="/img/tutorial/response-status-code/image01.png">

!!! note
    📨 📟 (👀 ⏭ 📄) 🎦 👈 📨 🔨 🚫 ✔️ 💪.

    FastAPI 💭 👉, &amp; 🔜 🏭 🗄 🩺 👈 🇵🇸 📤 🙅‍♂ 📨 💪.

## 🔃 🇺🇸🔍 👔 📟

!!! note
    🚥 👆 ⏪ 💭 ⚫️❔ 🇺🇸🔍 👔 📟, 🚶 ⏭ 📄.

🇺🇸🔍, 👆 📨 🔢 👔 📟 3️⃣ 9️⃣ 🍕 📨.

👫 👔 📟 ✔️ 📛 🔗 🤔 👫, ✋️ ⚠ 🍕 🔢.

📏:

* `100` &amp; 🔛 "ℹ". 👆 🛎 ⚙️ 👫 🔗. 📨 ⏮️ 👫 👔 📟 🚫🔜 ✔️ 💪.
* **`200`** &amp; 🔛 "🏆" 📨. 👫 🕐 👆 🔜 ⚙️ 🏆.
    * `200` 🔢 👔 📟, ❔ ⛓ 🌐 "👌".
    * ➕1️⃣ 🖼 🔜 `201`, "✍". ⚫️ 🛎 ⚙️ ⏮️ 🏗 🆕 ⏺ 💽.
    * 🎁 💼 `204`, "🙅‍♂ 🎚". 👉 📨 ⚙️ 🕐❔ 📤 🙅‍♂ 🎚 📨 👩‍💻, &amp; 📨 🔜 🚫 ✔️ 💪.
* **`300`** &amp; 🔛 "❎". 📨 ⏮️ 👫 👔 📟 5️⃣📆 ⚖️ 5️⃣📆 🚫 ✔️ 💪, 🌖 `304`, "🚫 🔀", ❔ 🔜 🚫 ✔️ 1️⃣.
* **`400`** &amp; 🔛 "👩‍💻 ❌" 📨. 👫 🥈 🆎 👆 🔜 🎲 ⚙️ 🏆.
    * 🖼 `404`, "🚫 🔎" 📨.
    * 💊 ❌ ⚪️➡️ 👩‍💻, 👆 💪 ⚙️ `400`.
* `500` &amp; 🔛 💽 ❌. 👆 🌖 🙅 ⚙️ 👫 🔗. 🕐❔ 🕳 🚶 ❌ 🍕 👆 🈸 📟, ⚖️ 💽, ⚫️ 🔜 🔁 📨 1️⃣ 👫 👔 📟.

!!! tip
    💭 🌅 🔃 🔠 👔 📟 &amp; ❔ 📟 ⚫️❔, ✅ <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Status" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">🏇</abbr> 🧾 🔃 🇺🇸🔍 👔 📟</a>.

## ⌨ 💭 📛

➡️ 👀 ⏮️ 🖼 🔄:

```Python hl_lines="6"
{!../../../docs_src/response_status_code/tutorial001.py!}
```

`201` 👔 📟 "✍".

✋️ 👆 🚫 ✔️ ✍ ⚫️❔ 🔠 👉 📟 ⛓.

👆 💪 ⚙️ 🏪 🔢 ⚪️➡️ `fastapi.status`.

```Python hl_lines="1  6"
{!../../../docs_src/response_status_code/tutorial002.py!}
```

👫 🏪, 👫 🧑‍🤝‍🧑 🎏 🔢, ✋️ 👈 🌌 👆 💪 ⚙️ 👨‍🎨 📋 🔎 👫:

<img src="/img/tutorial/response-status-code/image02.png">

!!! note "📡 ℹ"
    👆 💪 ⚙️ `from starlette import status`.

    **FastAPI** 🚚 🎏 `starlette.status` `fastapi.status` 🏪 👆, 👩‍💻. ✋️ ⚫️ 👟 🔗 ⚪️➡️ 💃.

## 🔀 🔢

⏪, [🏧 👩‍💻 🦮](../advanced/response-change-status-code.md){.internal-link target=_blank}, 👆 🔜 👀 ❔ 📨 🎏 👔 📟 🌘 🔢 👆 📣 📥.
