# 🎲 🗄

🚥 👆 💪, 👆 💪 ⚙️ ⚒ &amp; 🌐 🔢 🔗 🗄 ✔ ⚓️ 🔛 🌐, &amp; ❎ ⚫️ 🍕.

## 🔃 💂‍♂, 🔗, &amp; 🩺

🕵‍♂ 👆 🧾 👩‍💻 🔢 🏭 *🚫🔜 🚫* 🌌 🛡 👆 🛠️.

👈 🚫 🚮 🙆 ➕ 💂‍♂ 👆 🛠️, *➡ 🛠️* 🔜 💪 🌐❔ 👫.

🚥 📤 💂‍♂ ⚠ 👆 📟, ⚫️ 🔜 🔀.

🕵‍♂ 🧾 ⚒ ⚫️ 🌅 ⚠ 🤔 ❔ 🔗 ⏮️ 👆 🛠️, &amp; 💪 ⚒ ⚫️ 🌅 ⚠ 👆 ℹ ⚫️ 🏭. ⚫️ 💪 🤔 🎯 📨 <a href="https://en.wikipedia.org/wiki/Security_through_obscurity" class="external-link" target="_blank">💂‍♂ 🔘 🌌</a>.

🚥 👆 💚 🔐 👆 🛠️, 📤 📚 👍 👜 👆 💪, 🖼:

* ⚒ 💭 👆 ✔️ 👍 🔬 Pydantic 🏷 👆 📨 💪 &amp; 📨.
* 🔗 🙆 ✔ ✔ &amp; 🔑 ⚙️ 🔗.
* 🙅 🏪 🔢 🔐, 🕴 🔐#️⃣.
* 🛠️ &amp; ⚙️ 👍-💭 🔐 🧰, 💖 🇸🇲 &amp; 🥙 🤝, ♒️.
* 🚮 🌅 🧽 ✔ 🎛 ⏮️ Oauth2️⃣ ↔ 🌐❔ 💪.
* ...♒️.

👐, 👆 5️⃣📆 ✔️ 📶 🎯 ⚙️ 💼 🌐❔ 👆 🤙 💪 ❎ 🛠️ 🩺 🌐 (✅ 🏭) ⚖️ ⚓️ 🔛 📳 ⚪️➡️ 🌐 🔢.

## 🎲 🗄 ⚪️➡️ ⚒ &amp; 🇨🇻 {

👆 💪 💪 ⚙️ 🎏 Pydantic ⚒ 🔗 👆 🏗 🗄 &amp; 🩺 ⚜.

🖼:

```Python hl_lines="6  11"
{!../../../docs_src/conditional_openapi/tutorial001.py!}
```

📥 👥 📣 ⚒ `openapi_url` ⏮️ 🎏 🔢 `"/openapi.json"`.

&amp; ⤴️ 👥 ⚙️ ⚫️ 🕐❔ 🏗 `FastAPI` 📱.

⤴️ 👆 💪 ❎ 🗄 (✅ 🎚 🩺) ⚒ 🌐 🔢 `OPENAPI_URL` 🛁 🎻, 💖:

<div class="termy">

```console
$ OPENAPI_URL= uvicorn main:app

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

⤴️ 🚥 👆 🚶 📛 `/openapi.json`, `/docs`, ⚖️ `/redoc` 👆 🔜 🤚 `404 Not Found` ❌ 💖:

```JSON
{
    "detail": "Not Found"
}
```
