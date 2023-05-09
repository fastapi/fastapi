# 🗄 ⏲

👆 💪 ✍ 🛠️ ⏮️ *➡ 🛠️* 👈 💪 ⏲ 📨 *🔢 🛠️* ✍ 👱 🙆 (🎲 🎏 👩‍💻 👈 🔜 *⚙️* 👆 🛠️).

🛠️ 👈 🔨 🕐❔ 👆 🛠️ 📱 🤙 *🔢 🛠️* 📛 "⏲". ↩️ 🖥 👈 🔢 👩‍💻 ✍ 📨 📨 👆 🛠️ &amp; ⤴️ 👆 🛠️ *🤙 🔙*, 📨 📨 *🔢 🛠️* (👈 🎲 ✍ 🎏 👩‍💻).

👉 💼, 👆 💪 💚 📄 ❔ 👈 🔢 🛠️ *🔜* 👀 💖. ⚫️❔ *➡ 🛠️* ⚫️ 🔜 ✔️, ⚫️❔ 💪 ⚫️ 🔜 ⌛, ⚫️❔ 📨 ⚫️ 🔜 📨, ♒️.

## 📱 ⏮️ ⏲

➡️ 👀 🌐 👉 ⏮️ 🖼.

🌈 👆 🛠️ 📱 👈 ✔ 🏗 🧾.

👉 🧾 🔜 ✔️ `id`, `title` (📦), `customer`, &amp; `total`.

👩‍💻 👆 🛠️ (🔢 👩‍💻) 🔜 ✍ 🧾 👆 🛠️ ⏮️ 🏤 📨.

⤴️ 👆 🛠️ 🔜 (➡️ 🌈):

* 📨 🧾 🕴 🔢 👩‍💻.
* 📈 💸.
* 📨 📨 🔙 🛠️ 👩‍💻 (🔢 👩‍💻).
    * 👉 🔜 🔨 📨 🏤 📨 (⚪️➡️ *👆 🛠️*) *🔢 🛠️* 🚚 👈 🔢 👩‍💻 (👉 "⏲").

## 😐 **FastAPI** 📱

➡️ 🥇 👀 ❔ 😐 🛠️ 📱 🔜 👀 💖 ⏭ ❎ ⏲.

⚫️ 🔜 ✔️ *➡ 🛠️* 👈 🔜 📨 `Invoice` 💪, &amp; 🔢 🔢 `callback_url` 👈 🔜 🔌 📛 ⏲.

👉 🍕 📶 😐, 🌅 📟 🎲 ⏪ 😰 👆:

```Python hl_lines="9-13  36-53"
{!../../../docs_src/openapi_callbacks/tutorial001.py!}
```

!!! tip
     `callback_url` 🔢 🔢 ⚙️ Pydantic <a href="https://pydantic-docs.helpmanual.io/usage/types/#urls" class="external-link" target="_blank">📛</a> 🆎.

🕴 🆕 👜 `callbacks=messages_callback_router.routes` ❌ *➡ 🛠️ 👨‍🎨*. 👥 🔜 👀 ⚫️❔ 👈 ⏭.

## 🔬 ⏲

☑ ⏲ 📟 🔜 🪀 🙇 🔛 👆 👍 🛠️ 📱.

&amp; ⚫️ 🔜 🎲 🪀 📚 ⚪️➡️ 1️⃣ 📱 ⏭.

⚫️ 💪 1️⃣ ⚖️ 2️⃣ ⏸ 📟, 💖:

```Python
callback_url = "https://example.com/api/v1/invoices/events/"
httpx.post(callback_url, json={"description": "Invoice paid", "paid": True})
```

✋️ 🎲 🏆 ⚠ 🍕 ⏲ ⚒ 💭 👈 👆 🛠️ 👩‍💻 (🔢 👩‍💻) 🛠️ *🔢 🛠️* ☑, 🛄 💽 👈 *👆 🛠️* 🔜 📨 📨 💪 ⏲, ♒️.

, ⚫️❔ 👥 🔜 ⏭ 🚮 📟 📄 ❔ 👈 *🔢 🛠️* 🔜 👀 💖 📨 ⏲ ⚪️➡️ *👆 🛠️*.

👈 🧾 🔜 🎦 🆙 🦁 🎚 `/docs` 👆 🛠️, &amp; ⚫️ 🔜 ➡️ 🔢 👩‍💻 💭 ❔ 🏗 *🔢 🛠️*.

👉 🖼 🚫 🛠️ ⏲ ⚫️ (👈 💪 ⏸ 📟), 🕴 🧾 🍕.

!!! tip
    ☑ ⏲ 🇺🇸🔍 📨.

    🕐❔ 🛠️ ⏲ 👆, 👆 💪 ⚙️ 🕳 💖 <a href="https://www.python-httpx.org" class="external-link" target="_blank">🇸🇲</a> ⚖️ <a href="https://requests.readthedocs.io/" class="external-link" target="_blank">📨</a>.

## ✍ ⏲ 🧾 📟

👉 📟 🏆 🚫 🛠️ 👆 📱, 👥 🕴 💪 ⚫️ *📄* ❔ 👈 *🔢 🛠️* 🔜 👀 💖.

✋️, 👆 ⏪ 💭 ❔ 💪 ✍ 🏧 🧾 🛠️ ⏮️ **FastAPI**.

👥 🔜 ⚙️ 👈 🎏 💡 📄 ❔ *🔢 🛠️* 🔜 👀 💖... 🏗 *➡ 🛠️(Ⓜ)* 👈 🔢 🛠️ 🔜 🛠️ (🕐 👆 🛠️ 🔜 🤙).

!!! tip
    🕐❔ ✍ 📟 📄 ⏲, ⚫️ 💪 ⚠ 🌈 👈 👆 👈 *🔢 👩‍💻*. &amp; 👈 👆 ⏳ 🛠️ *🔢 🛠️*, 🚫 *👆 🛠️*.

    🍕 🛠️ 👉 ☝ 🎑 ( *🔢 👩‍💻*) 💪 ℹ 👆 💭 💖 ⚫️ 🌅 ⭐ 🌐❔ 🚮 🔢, Pydantic 🏷 💪, 📨, ♒️. 👈 *🔢 🛠️*.

### ✍ ⏲ `APIRouter`

🥇 ✍ 🆕 `APIRouter` 👈 🔜 🔌 1️⃣ ⚖️ 🌅 ⏲.

```Python hl_lines="3  25"
{!../../../docs_src/openapi_callbacks/tutorial001.py!}
```

### ✍ ⏲ *➡ 🛠️*

✍ ⏲ *➡ 🛠️* ⚙️ 🎏 `APIRouter` 👆 ✍ 🔛.

⚫️ 🔜 👀 💖 😐 FastAPI *➡ 🛠️*:

* ⚫️ 🔜 🎲 ✔️ 📄 💪 ⚫️ 🔜 📨, ✅ `body: InvoiceEvent`.
*  &amp; ⚫️ 💪 ✔️ 📄 📨 ⚫️ 🔜 📨, ✅ `response_model=InvoiceEventReceived`.

```Python hl_lines="16-18  21-22  28-32"
{!../../../docs_src/openapi_callbacks/tutorial001.py!}
```

📤 2️⃣ 👑 🔺 ⚪️➡️ 😐 *➡ 🛠️*:

* ⚫️ 🚫 💪 ✔️ 🙆 ☑ 📟, ↩️ 👆 📱 🔜 🙅 🤙 👉 📟. ⚫️ 🕴 ⚙️ 📄 *🔢 🛠️*. , 🔢 💪 ✔️ `pass`.
*  *➡* 💪 🔌 <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#key-expression" class="external-link" target="_blank">🗄 3️⃣ 🧬</a> (👀 🌖 🔛) 🌐❔ ⚫️ 💪 ⚙️ 🔢 ⏮️ 🔢 &amp; 🍕 ⏮️ 📨 📨 *👆 🛠️*.

### ⏲ ➡ 🧬

⏲ *➡* 💪 ✔️ <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#key-expression" class="external-link" target="_blank">🗄 3️⃣ 🧬</a> 👈 💪 🔌 🍕 ⏮️ 📨 📨 *👆 🛠️*.

👉 💼, ⚫️ `str`:

```Python
"{$callback_url}/invoices/{$request.body.id}"
```

, 🚥 👆 🛠️ 👩‍💻 (🔢 👩‍💻) 📨 📨 *👆 🛠️* :

```
https://yourapi.com/invoices/?callback_url=https://www.external.org/events
```

⏮️ 🎻 💪:

```JSON
{
    "id": "2expen51ve",
    "customer": "Mr. Richie Rich",
    "total": "9999"
}
```

⤴️ *👆 🛠️* 🔜 🛠️ 🧾, &amp; ☝ ⏪, 📨 ⏲ 📨 `callback_url` ( *🔢 🛠️*):

```
https://www.external.org/events/invoices/2expen51ve
```

⏮️ 🎻 💪 ⚗ 🕳 💖:

```JSON
{
    "description": "Payment celebration",
    "paid": true
}
```

&amp; ⚫️ 🔜 ⌛ 📨 ⚪️➡️ 👈 *🔢 🛠️* ⏮️ 🎻 💪 💖:

```JSON
{
    "ok": true
}
```

!!! tip
    👀 ❔ ⏲ 📛 ⚙️ 🔌 📛 📨 🔢 🔢 `callback_url` (`https://www.external.org/events`) &amp; 🧾 `id` ⚪️➡️ 🔘 🎻 💪 (`2expen51ve`).

### 🚮 ⏲ 📻

👉 ☝ 👆 ✔️ *⏲ ➡ 🛠️(Ⓜ)* 💪 (1️⃣(Ⓜ) 👈 *🔢 👩‍💻* 🔜 🛠️ *🔢 🛠️*) ⏲ 📻 👆 ✍ 🔛.

🔜 ⚙️ 🔢 `callbacks` *👆 🛠️ ➡ 🛠️ 👨‍🎨* 🚶‍♀️ 🔢 `.routes` (👈 🤙 `list` 🛣/*➡ 🛠️*) ⚪️➡️ 👈 ⏲ 📻:

```Python hl_lines="35"
{!../../../docs_src/openapi_callbacks/tutorial001.py!}
```

!!! tip
    👀 👈 👆 🚫 🚶‍♀️ 📻 ⚫️ (`invoices_callback_router`) `callback=`, ✋️ 🔢 `.routes`, `invoices_callback_router.routes`.

### ✅ 🩺

🔜 👆 💪 ▶️ 👆 📱 ⏮️ Uvicorn &amp; 🚶 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

👆 🔜 👀 👆 🩺 ✅ "⏲" 📄 👆 *➡ 🛠️* 👈 🎦 ❔ *🔢 🛠️* 🔜 👀 💖:

<img src="/img/tutorial/openapi-callbacks/image01.png">
