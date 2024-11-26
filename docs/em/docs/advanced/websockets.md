#  *️⃣

👆 💪 ⚙️ <a href="https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API" class="external-link" target="_blank"> *️⃣ </a> ⏮️ **FastAPI**.

## ❎ `WebSockets`

🥇 👆 💪 ❎ `WebSockets`:

<div class="termy">

```console
$ pip install websockets

---> 100%
```

</div>

##  *️⃣ 👩‍💻

### 🏭

👆 🏭 ⚙️, 👆 🎲 ✔️ 🕸 ✍ ⏮️ 🏛 🛠️ 💖 😥, Vue.js ⚖️ 📐.

&amp; 🔗 ⚙️ *️⃣ ⏮️ 👆 👩‍💻 👆 🔜 🎲 ⚙️ 👆 🕸 🚙.

⚖️ 👆 💪 ✔️ 🇦🇸 📱 🈸 👈 🔗 ⏮️ 👆 *️⃣ 👩‍💻 🔗, 🇦🇸 📟.

⚖️ 👆 5️⃣📆 ✔️ 🙆 🎏 🌌 🔗 ⏮️ *️⃣ 🔗.

---

✋️ 👉 🖼, 👥 🔜 ⚙️ 📶 🙅 🕸 📄 ⏮️ 🕸, 🌐 🔘 📏 🎻.

👉, ↗️, 🚫 ⚖ &amp; 👆 🚫🔜 ⚙️ ⚫️ 🏭.

🏭 👆 🔜 ✔️ 1️⃣ 🎛 🔛.

✋️ ⚫️ 🙅 🌌 🎯 🔛 💽-🚄 *️⃣ &amp; ✔️ 👷 🖼:

{* ../../docs_src/websockets/tutorial001.py hl[2,6:38,41:43] *}

## ✍ `websocket`

👆 **FastAPI** 🈸, ✍ `websocket`:

{* ../../docs_src/websockets/tutorial001.py hl[1,46:47] *}

/// note | 📡 ℹ

👆 💪 ⚙️ `from starlette.websockets import WebSocket`.

**FastAPI** 🚚 🎏 `WebSocket` 🔗 🏪 👆, 👩‍💻. ✋️ ⚫️ 👟 🔗 ⚪️➡️ 💃.

///

## ⌛ 📧 &amp; 📨 📧

👆 *️⃣ 🛣 👆 💪 `await` 📧 &amp; 📨 📧.

{* ../../docs_src/websockets/tutorial001.py hl[48:52] *}

👆 💪 📨 &amp; 📨 💱, ✍, &amp; 🎻 💽.

## 🔄 ⚫️

🚥 👆 📁 📛 `main.py`, 🏃 👆 🈸 ⏮️:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

📂 👆 🖥 <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

👆 🔜 👀 🙅 📃 💖:

<img src="/img/tutorial/websockets/image01.png">

👆 💪 🆎 📧 🔢 📦, &amp; 📨 👫:

<img src="/img/tutorial/websockets/image02.png">

&amp; 👆 **FastAPI** 🈸 ⏮️ *️⃣ 🔜 📨 🔙:

<img src="/img/tutorial/websockets/image03.png">

👆 💪 📨 (&amp; 📨) 📚 📧:

<img src="/img/tutorial/websockets/image04.png">

&amp; 🌐 👫 🔜 ⚙️ 🎏 *️⃣ 🔗.

## ⚙️ `Depends` &amp; 🎏

*️⃣ 🔗 👆 💪 🗄 ⚪️➡️ `fastapi` &amp; ⚙️:

* `Depends`
* `Security`
* `Cookie`
* `Header`
* `Path`
* `Query`

👫 👷 🎏 🌌 🎏 FastAPI 🔗/*➡ 🛠️*:

{* ../../docs_src/websockets/tutorial002.py hl[66:77,76:91] *}

/// info

👉 *️⃣ ⚫️ 🚫 🤙 ⚒ 🔑 🤚 `HTTPException`, ↩️ 👥 🤚 `WebSocketException`.

👆 💪 ⚙️ 📪 📟 ⚪️➡️ <a href="https://tools.ietf.org/html/rfc6455#section-7.4.1" class="external-link" target="_blank">☑ 📟 🔬 🔧</a>.

///

### 🔄 *️⃣ ⏮️ 🔗

🚥 👆 📁 📛 `main.py`, 🏃 👆 🈸 ⏮️:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

📂 👆 🖥 <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

📤 👆 💪 ⚒:

*  "🏬 🆔", ⚙️ ➡.
*  "🤝" ⚙️ 🔢 🔢.

/// tip

👀 👈 🔢 `token` 🔜 🍵 🔗.

///

⏮️ 👈 👆 💪 🔗 *️⃣ &amp; ⤴️ 📨 &amp; 📨 📧:

<img src="/img/tutorial/websockets/image05.png">

## 🚚 🔀 &amp; 💗 👩‍💻

🕐❔ *️⃣ 🔗 📪, `await websocket.receive_text()` 🔜 🤚 `WebSocketDisconnect` ⚠, ❔ 👆 💪 ⤴️ ✊ &amp; 🍵 💖 👉 🖼.

{* ../../docs_src/websockets/tutorial003.py hl[81:83] *}

🔄 ⚫️ 👅:

* 📂 📱 ⏮️ 📚 🖥 📑.
* ✍ 📧 ⚪️➡️ 👫.
* ⤴️ 🔐 1️⃣ 📑.

👈 🔜 🤚 `WebSocketDisconnect` ⚠, &amp; 🌐 🎏 👩‍💻 🔜 📨 📧 💖:

```
Client #1596980209979 left the chat
```

/// tip

📱 🔛 ⭐ &amp; 🙅 🖼 🎦 ❔ 🍵 &amp; 📻 📧 📚 *️⃣ 🔗.

✋️ ✔️ 🤯 👈, 🌐 🍵 💾, 👁 📇, ⚫️ 🔜 🕴 👷 ⏪ 🛠️ 🏃, &amp; 🔜 🕴 👷 ⏮️ 👁 🛠️.

🚥 👆 💪 🕳 ⏩ 🛠️ ⏮️ FastAPI ✋️ 👈 🌖 🏋️, 🐕‍🦺 ✳, ✳ ⚖️ 🎏, ✅ <a href="https://github.com/encode/broadcaster" class="external-link" target="_blank">🗜/📻</a>.

///

## 🌅 ℹ

💡 🌅 🔃 🎛, ✅ 💃 🧾:

* <a href="https://www.starlette.io/websockets/" class="external-link" target="_blank"> `WebSocket` 🎓</a>.
* <a href="https://www.starlette.io/endpoints/#websocketendpoint" class="external-link" target="_blank">🎓-⚓️ *️⃣ 🚚</a>.
