# 📄

👆 💪 ⚙️ 🙆 📄 🚒 👆 💚 ⏮ **FastAPI**.

⚠ ⚒ Jinja2⃣, 🎏 1⃣ ⚙️ 🏺 &amp; 🎏 🧰.

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
* 📣 `Request` 🔢 *➡ 🛠* 👈 🔜 📨 📄.
* ⚙️ `templates` 👆 ✍ ✍ &amp; 📨 `TemplateResponse`, 🚶‍♀️ `request` 1⃣ 🔑-💲 👫 Jinja2⃣ "🔑".

```Python hl_lines="4  11  15-16"
{!../../../docs_src/templates/tutorial001.py!}
```

!!! note
    👀 👈 👆 ✔️ 🚶‍♀️ `request` 🍕 🔑-💲 👫 🔑 Jinja2⃣. , 👆 ✔️ 📣 ⚫️ 👆 *➡ 🛠*.

!!! tip
    📣 `response_class=HTMLResponse` 🩺 🎚 🔜 💪 💭 👈 📨 🔜 🕸.

!!! note "📡 ℹ"
    👆 💪 ⚙️ `from starlette.templating import Jinja2Templates`.

    **FastAPI** 🚚 🎏 `starlette.templating` `fastapi.templating` 🏪 👆, 👩‍💻. ✋️ 🌅 💪 📨 👟 🔗 ⚪️➡️ 💃. 🎏 ⏮ `Request` &amp; `StaticFiles`.

## ✍ 📄

⤴ 👆 💪 ✍ 📄 `templates/item.html` ⏮:

```jinja hl_lines="7"
{!../../../docs_src/templates/templates/item.html!}
```

⚫️ 🔜 🎦 `id` ✊ ⚪️➡️ "🔑" `dict` 👆 🚶‍♀️:

```Python
{"request": request, "id": id}
```

## 📄 &amp; 🎻 📁

&amp; 👆 💪 ⚙️ `url_for()` 🔘 📄, &amp; ⚙️ ⚫️, 🖼, ⏮ `StaticFiles` 👆 📌.

```jinja hl_lines="4"
{!../../../docs_src/templates/templates/item.html!}
```

👉 🖼, ⚫️ 🔜 🔗 🎚 📁 `static/styles.css` ⏮:

```CSS hl_lines="4"
{!../../../docs_src/templates/static/styles.css!}
```

&amp; ↩️ 👆 ⚙️ `StaticFiles`, 👈 🎚 📁 🔜 🍦 🔁 👆 **FastAPI** 🈸 📛 `/static/styles.css`.

## 🌅 ℹ

🌅 ℹ, 🔌 ❔ 💯 📄, ✅ <a href="https://www.starlette.io/templates/" class="external-link" target="_blank">💃 🩺 🔛 📄</a>.
