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

```Python hl_lines="2  6-38  41-43"
{!../../../docs_src/websockets/tutorial001.py!}
```

## ✍ `websocket`

👆 **FastAPI** 🈸, ✍ `websocket`:

```Python hl_lines="1  46-47"
{!../../../docs_src/websockets/tutorial001.py!}
```

!!! note "📡 ℹ"
    👆 💪 ⚙️ `from starlette.websockets import WebSocket`.

    **FastAPI** 🚚 🎏 `WebSocket` 🔗 🏪 👆, 👩‍💻. ✋️ ⚫️ 👟 🔗 ⚪️➡️ 💃.

## ⌛ 📧 &amp; 📨 📧

👆 *️⃣ 🛣 👆 💪 `await` 📧 &amp; 📨 📧.

```Python hl_lines="48-52"
{!../../../docs_src/websockets/tutorial001.py!}
```

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

```Python hl_lines="66-77  76-91"
{!../../../docs_src/websockets/tutorial002.py!}
```

!!! info
    👉 *️⃣ ⚫️ 🚫 🤙 ⚒ 🔑 🤚 `HTTPException`, ↩️ 👥 🤚 `WebSocketException`.

    👆 💪 ⚙️ 📪 📟 ⚪️➡️ <a href="https://tools.ietf.org/html/rfc6455#section-7.4.1" class="external-link" target="_blank">☑ 📟 🔬 🔧</a>.

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

!!! tip
    👀 👈 🔢 `token` 🔜 🍵 🔗.

⏮️ 👈 👆 💪 🔗 *️⃣ &amp; ⤴️ 📨 &amp; 📨 📧:

<img src="/img/tutorial/websockets/image05.png">

## 🚚 🔀 &amp; 💗 👩‍💻

🕐❔ *️⃣ 🔗 📪, `await websocket.receive_text()` 🔜 🤚 `WebSocketDisconnect` ⚠, ❔ 👆 💪 ⤴️ ✊ &amp; 🍵 💖 👉 🖼.

```Python hl_lines="81-83"
{!../../../docs_src/websockets/tutorial003.py!}
```

🔄 ⚫️ 👅:

* 📂 📱 ⏮️ 📚 🖥 📑.
* ✍ 📧 ⚪️➡️ 👫.
* ⤴️ 🔐 1️⃣ 📑.

👈 🔜 🤚 `WebSocketDisconnect` ⚠, &amp; 🌐 🎏 👩‍💻 🔜 📨 📧 💖:

```
Client #1596980209979 left the chat
```

!!! tip
    📱 🔛 ⭐ &amp; 🙅 🖼 🎦 ❔ 🍵 &amp; 📻 📧 📚 *️⃣ 🔗.

    ✋️ ✔️ 🤯 👈, 🌐 🍵 💾, 👁 📇, ⚫️ 🔜 🕴 👷 ⏪ 🛠️ 🏃, &amp; 🔜 🕴 👷 ⏮️ 👁 🛠️.

    🚥 👆 💪 🕳 ⏩ 🛠️ ⏮️ FastAPI ✋️ 👈 🌖 🏋️, 🐕‍🦺 ✳, ✳ ⚖️ 🎏, ✅ <a href="https://github.com/encode/broadcaster" class="external-link" target="_blank">🗜/📻</a>.

## 🌅 ℹ

💡 🌅 🔃 🎛, ✅ 💃 🧾:

* <a href="https://www.starlette.io/websockets/" class="external-link" target="_blank"> `WebSocket` 🎓</a>.
* <a href="https://www.starlette.io/endpoints/#websocketendpoint" class="external-link" target="_blank">🎓-⚓️ *️⃣ 🚚</a>.
