# 🏧 🛠

👑 🔰 👆 ✍ ❔ 🚮 [🛃 🛠](../tutorial/middleware.md){.internal-link target=_blank} 👆 🈸.

&amp; ⤴ 👆 ✍ ❔ 🍵 [⚜ ⏮ `CORSMiddleware`](../tutorial/cors.md){.internal-link target=_blank}.

👉 📄 👥 🔜 👀 ❔ ⚙️ 🎏 🛠.

## ❎ 🔫 🛠

**FastAPI** ⚓️ 🔛 💃 &amp; 🛠 <abbr title="Asynchronous Server Gateway Interface">🔫</abbr> 🔧, 👆 💪 ⚙️ 🙆 🔫 🛠.

🛠 🚫 ✔️ ⚒ FastAPI ⚖️ 💃 👷, 📏 ⚫️ ⏩ 🔫 🔌.

🏢, 🔫 🛠 🎓 👈 ⌛ 📨 🔫 📱 🥇 ❌.

, 🧾 🥉-🥳 🔫 🛠 👫 🔜 🎲 💬 👆 🕳 💖:

```Python
from unicorn import UnicornMiddleware

app = SomeASGIApp()

new_app = UnicornMiddleware(app, some_config="rainbow")
```

✋️ FastAPI (🤙 💃) 🚚 🙅 🌌 ⚫️ 👈 ⚒ 💭 👈 🔗 🛠 🍵 💽 ❌ &amp; 🛃 ⚠ 🐕‍🦺 👷 ☑.

👈, 👆 ⚙️ `app.add_middleware()` (🖼 ⚜).

```Python
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()

app.add_middleware(UnicornMiddleware, some_config="rainbow")
```

`app.add_middleware()` 📨 🛠 🎓 🥇 ❌ &amp; 🙆 🌖 ❌ 🚶‍♀️ 🛠.

## 🛠 🛠

**FastAPI** 🔌 📚 🛠 ⚠ ⚙️ 💼, 👥 🔜 👀 ⏭ ❔ ⚙️ 👫.

!!! note "📡 ℹ"
    ⏭ 🖼, 👆 💪 ⚙️ `from starlette.middleware.something import SomethingMiddleware`.

    **FastAPI** 🚚 📚 🛠 `fastapi.middleware` 🏪 👆, 👩‍💻. ✋️ 🌅 💪 🛠 👟 🔗 ⚪️➡️ 💃.

## `HTTPSRedirectMiddleware`

🛠 👈 🌐 📨 📨 🔜 👯‍♂️ `https` ⚖️ `wss`.

🙆 📨 📨 `http` ⚖️ `ws` 🔜 ❎ 🔐 ⚖ ↩️.

```Python hl_lines="2  6"
{!../../../docs_src/advanced_middleware/tutorial001.py!}
```

## `TrustedHostMiddleware`

🛠 👈 🌐 📨 📨 ✔️ ☑ ⚒ `Host` 🎚, ✔ 💂‍♂ 🛡 🇺🇸🔍 🦠 🎚 👊.

```Python hl_lines="2  6-8"
{!../../../docs_src/advanced_middleware/tutorial002.py!}
```

📄 ❌ 🐕‍🦺:

* `allowed_hosts` - 📇 🆔 📛 👈 🔜 ✔ 📛. 🃏 🆔 ✅ `*.example.com` 🐕‍🦺 🎀 📁. ✔ 🙆 📛 👯‍♂️ ⚙️ `allowed_hosts=["*"]` ⚖️ 🚫 🛠.

🚥 📨 📨 🔨 🚫 ✔ ☑ ⤴ `400` 📨 🔜 📨.

## `GZipMiddleware`

🍵 🗜 📨 🙆 📨 👈 🔌 `"gzip"` `Accept-Encoding` 🎚.

🛠 🔜 🍵 👯‍♂️ 🐩 &amp; 🎥 📨.

```Python hl_lines="2  6"
{!../../../docs_src/advanced_middleware/tutorial003.py!}
```

📄 ❌ 🐕‍🦺:

* `minimum_size` - 🚫 🗜 📨 👈 🤪 🌘 👉 💯 📐 🔢. 🔢 `500`.

## 🎏 🛠

📤 📚 🎏 🔫 🛠.

🖼:

* <a href="https://docs.sentry.io/platforms/python/asgi/" class="external-link" target="_blank">🔫</a>
* <a href="https://github.com/encode/uvicorn/blob/master/uvicorn/middleware/proxy_headers.py" class="external-link" target="_blank">Uvicorn `ProxyHeadersMiddleware`</a>
* <a href="https://github.com/florimondmanca/msgpack-asgi" class="external-link" target="_blank">🇸🇲</a>

👀 🎏 💪 🛠 ✅ <a href="https://www.starlette.io/middleware/" class="external-link" target="_blank">💃 🛠 🩺</a> &amp; <a href="https://github.com/florimondmanca/awesome-asgi" class="external-link" target="_blank">🔫 👌 📇</a>.
