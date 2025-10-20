# 📄

👆 💪 ⚙️ 🙆 📄 🚒 👆 💚 ⏮️ **FastAPI**.

⚠ ⚒ Jinja2️⃣, 🎏 1️⃣ ⚙️ 🏺 &amp; 🎏 🧰.

📤 🚙 🔗 ⚫️ 💪 👈 👆 💪 ⚙️ 🔗 👆 **FastAPI** 🈸 (🚚 💃).

## ❎ 🔗

❎ `jinja2`:

<div class="termy">

```console
$ pip install jinja2

---> 100%
```

</div>

## ⚙️ `Jinja2Templates`

* 🗄 `Jinja2Templates`.
* ✍ `templates` 🎚 👈 👆 💪 🏤-⚙️ ⏪.
* 📣 `Request` 🔢 *➡ 🛠️* 👈 🔜 📨 📄.
* ⚙️ `templates` 👆 ✍ ✍ &amp; 📨 `TemplateResponse`, 🚶‍♀️ `request` 1️⃣ 🔑-💲 👫 Jinja2️⃣ "🔑".

{* ../../docs_src/templates/tutorial001.py hl[4,11,15:18] *}

/// note

👀 👈 👆 ✔️ 🚶‍♀️ `request` 🍕 🔑-💲 👫 🔑 Jinja2️⃣. , 👆 ✔️ 📣 ⚫️ 👆 *➡ 🛠️*.

///

/// tip

📣 `response_class=HTMLResponse` 🩺 🎚 🔜 💪 💭 👈 📨 🔜 🕸.

///

/// note | 📡 ℹ

👆 💪 ⚙️ `from starlette.templating import Jinja2Templates`.

**FastAPI** 🚚 🎏 `starlette.templating` `fastapi.templating` 🏪 👆, 👩‍💻. ✋️ 🌅 💪 📨 👟 🔗 ⚪️➡️ 💃. 🎏 ⏮️ `Request` &amp; `StaticFiles`.

///

## ✍ 📄

⤴️ 👆 💪 ✍ 📄 `templates/item.html` ⏮️:

```jinja hl_lines="7"
{!../../docs_src/templates/templates/item.html!}
```

⚫️ 🔜 🎦 `id` ✊ ⚪️➡️ "🔑" `dict` 👆 🚶‍♀️:

```Python
{"request": request, "id": id}
```

## 📄 &amp; 🎻 📁

&amp; 👆 💪 ⚙️ `url_for()` 🔘 📄, &amp; ⚙️ ⚫️, 🖼, ⏮️ `StaticFiles` 👆 📌.

```jinja hl_lines="4"
{!../../docs_src/templates/templates/item.html!}
```

👉 🖼, ⚫️ 🔜 🔗 🎚 📁 `static/styles.css` ⏮️:

```CSS hl_lines="4"
{!../../docs_src/templates/static/styles.css!}
```

&amp; ↩️ 👆 ⚙️ `StaticFiles`, 👈 🎚 📁 🔜 🍦 🔁 👆 **FastAPI** 🈸 📛 `/static/styles.css`.

## 🌅 ℹ

🌅 ℹ, 🔌 ❔ 💯 📄, ✅ <a href="https://www.starlette.dev/templates/" class="external-link" target="_blank">💃 🩺 🔛 📄</a>.
