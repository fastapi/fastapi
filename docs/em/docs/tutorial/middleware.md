# 🛠️

👆 💪 🚮 🛠️ **FastAPI** 🈸.

"🛠️" 🔢 👈 👷 ⏮️ 🔠 **📨** ⏭ ⚫️ 🛠️ 🙆 🎯 *➡ 🛠️*. &amp; ⏮️ 🔠 **📨** ⏭ 🛬 ⚫️.

* ⚫️ ✊ 🔠 **📨** 👈 👟 👆 🈸.
* ⚫️ 💪 ⤴️ 🕳 👈 **📨** ⚖️ 🏃 🙆 💪 📟.
* ⤴️ ⚫️ 🚶‍♀️ **📨** 🛠️ 🎂 🈸 ( *➡ 🛠️*).
* ⚫️ ⤴️ ✊ **📨** 🏗 🈸 ( *➡ 🛠️*).
* ⚫️ 💪 🕳 👈 **📨** ⚖️ 🏃 🙆 💪 📟.
* ⤴️ ⚫️ 📨 **📨**.

!!! note "📡 ℹ"
    🚥 👆 ✔️ 🔗 ⏮️ `yield`, 🚪 📟 🔜 🏃 *⏮️* 🛠️.

    🚥 📤 🙆 🖥 📋 (📄 ⏪), 👫 🔜 🏃 *⏮️* 🌐 🛠️.

## ✍ 🛠️

✍ 🛠️ 👆 ⚙️ 👨‍🎨 `@app.middleware("http")` 🔛 🔝 🔢.

🛠️ 🔢 📨:

*  `request`.
* 🔢 `call_next` 👈 🔜 📨 `request` 🔢.
    * 👉 🔢 🔜 🚶‍♀️ `request` 🔗 *➡ 🛠️*.
    * ⤴️ ⚫️ 📨 `response` 🏗 🔗 *➡ 🛠️*.
* 👆 💪 ⤴️ 🔀 🌅 `response` ⏭ 🛬 ⚫️.

```Python hl_lines="8-9  11  14"
{!../../../docs_src/middleware/tutorial001.py!}
```

!!! tip
    ✔️ 🤯 👈 🛃 © 🎚 💪 🚮 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">⚙️ '✖-' 🔡</a>.

    ✋️ 🚥 👆 ✔️ 🛃 🎚 👈 👆 💚 👩‍💻 🖥 💪 👀, 👆 💪 🚮 👫 👆 ⚜ 📳 ([⚜ (✖️-🇨🇳 ℹ 🤝)](cors.md){.internal-link target=_blank}) ⚙️ 🔢 `expose_headers` 📄 <a href="https://www.starlette.io/middleware/#corsmiddleware" class="external-link" target="_blank">💃 ⚜ 🩺</a>.

!!! note "📡 ℹ"
    👆 💪 ⚙️ `from starlette.requests import Request`.

    **FastAPI** 🚚 ⚫️ 🏪 👆, 👩‍💻. ✋️ ⚫️ 👟 🔗 ⚪️➡️ 💃.

### ⏭ &amp; ⏮️ `response`

👆 💪 🚮 📟 🏃 ⏮️ `request`, ⏭ 🙆 *➡ 🛠️* 📨 ⚫️.

&amp; ⏮️ `response` 🏗, ⏭ 🛬 ⚫️.

🖼, 👆 💪 🚮 🛃 🎚 `X-Process-Time` ⚗ 🕰 🥈 👈 ⚫️ ✊ 🛠️ 📨 &amp; 🏗 📨:

```Python hl_lines="10  12-13"
{!../../../docs_src/middleware/tutorial001.py!}
```

## 🎏 🛠️

👆 💪 ⏪ ✍ 🌖 🔃 🎏 🛠️ [🏧 👩‍💻 🦮: 🏧 🛠️](../advanced/middleware.md){.internal-link target=_blank}.

👆 🔜 ✍ 🔃 ❔ 🍵 <abbr title="Cross-Origin Resource Sharing">⚜</abbr> ⏮️ 🛠️ ⏭ 📄.
