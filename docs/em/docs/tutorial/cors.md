# ⚜ (✖️-🇨🇳 ℹ 🤝)

<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" class="external-link" target="_blank">⚜ ⚖️ "✖️-🇨🇳 ℹ 🤝"</a> 🔗 ⚠ 🕐❔ 🕸 🏃‍♂ 🖥 ✔️ 🕸 📟 👈 🔗 ⏮️ 👩‍💻, &amp; 👩‍💻 🎏 "🇨🇳" 🌘 🕸.

## 🇨🇳

🇨🇳 🌀 🛠️ (`http`, `https`), 🆔 (`myapp.com`, `localhost`, `localhost.tiangolo.com`), &amp; ⛴ (`80`, `443`, `8080`).

, 🌐 👫 🎏 🇨🇳:

* `http://localhost`
* `https://localhost`
* `http://localhost:8080`

🚥 👫 🌐 `localhost`, 👫 ⚙️ 🎏 🛠️ ⚖️ ⛴,, 👫 🎏 "🇨🇳".

## 🔁

, ➡️ 💬 👆 ✔️ 🕸 🏃 👆 🖥 `http://localhost:8080`, &amp; 🚮 🕸 🔄 🔗 ⏮️ 👩‍💻 🏃 `http://localhost` (↩️ 👥 🚫 ✔ ⛴, 🖥 🔜 🤔 🔢 ⛴ `80`).

⤴️, 🖥 🔜 📨 🇺🇸🔍 `OPTIONS` 📨 👩‍💻, &amp; 🚥 👩‍💻 📨 ☑ 🎚 ✔ 📻 ⚪️➡️ 👉 🎏 🇨🇳 (`http://localhost:8080`) ⤴️ 🖥 🔜 ➡️ 🕸 🕸 📨 🚮 📨 👩‍💻.

🏆 👉, 👩‍💻 🔜 ✔️ 📇 "✔ 🇨🇳".

👉 💼, ⚫️ 🔜 ✔️ 🔌 `http://localhost:8080` 🕸 👷 ☑.

## 🃏

⚫️ 💪 📣 📇 `"*"` ("🃏") 💬 👈 🌐 ✔.

✋️ 👈 🔜 🕴 ✔ 🎯 🆎 📻, 🚫 🌐 👈 🔌 🎓: 🍪, ✔ 🎚 💖 📚 ⚙️ ⏮️ 📨 🤝, ♒️.

, 🌐 👷 ☑, ⚫️ 👻 ✔ 🎯 ✔ 🇨🇳.

## ⚙️ `CORSMiddleware`

👆 💪 🔗 ⚫️ 👆 **FastAPI** 🈸 ⚙️ `CORSMiddleware`.

* 🗄 `CORSMiddleware`.
* ✍ 📇 ✔ 🇨🇳 (🎻).
* 🚮 ⚫️ "🛠️" 👆 **FastAPI** 🈸.

👆 💪 ✔ 🚥 👆 👩‍💻 ✔:

* 🎓 (✔ 🎚, 🍪, ♒️).
* 🎯 🇺🇸🔍 👩‍🔬 (`POST`, `PUT`) ⚖️ 🌐 👫 ⏮️ 🃏 `"*"`.
* 🎯 🇺🇸🔍 🎚 ⚖️ 🌐 👫 ⏮️ 🃏 `"*"`.

{* ../../docs_src/cors/tutorial001.py hl[2,6:11,13:19] *}

🔢 🔢 ⚙️ `CORSMiddleware` 🛠️ 🚫 🔢, 👆 🔜 💪 🎯 🛠️ 🎯 🇨🇳, 👩‍🔬, ⚖️ 🎚, ✔ 🖥 ✔ ⚙️ 👫 ✖️-🆔 🔑.

📄 ❌ 🐕‍🦺:

* `allow_origins` - 📇 🇨🇳 👈 🔜 ✔ ⚒ ✖️-🇨🇳 📨. 🤶 Ⓜ. `['https://example.org', 'https://www.example.org']`. 👆 💪 ⚙️ `['*']` ✔ 🙆 🇨🇳.
* `allow_origin_regex` - 🎻 🎻 🏏 🛡 🇨🇳 👈 🔜 ✔ ⚒ ✖️-🇨🇳 📨. ✅ `'https://.*\.example\.org'`.
* `allow_methods` - 📇 🇺🇸🔍 👩‍🔬 👈 🔜 ✔ ✖️-🇨🇳 📨. 🔢 `['GET']`. 👆 💪 ⚙️ `['*']` ✔ 🌐 🐩 👩‍🔬.
* `allow_headers` - 📇 🇺🇸🔍 📨 🎚 👈 🔜 🐕‍🦺 ✖️-🇨🇳 📨. 🔢 `[]`. 👆 💪 ⚙️ `['*']` ✔ 🌐 🎚. `Accept`, `Accept-Language`, `Content-Language` &amp; `Content-Type` 🎚 🕧 ✔ <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#simple_requests" class="external-link" rel="noopener" target="_blank">🙅 ⚜ 📨</a>.
* `allow_credentials` - 🎦 👈 🍪 🔜 🐕‍🦺 ✖️-🇨🇳 📨. 🔢 `False`. , `allow_origins` 🚫🔜 ⚒ `['*']` 🎓 ✔, 🇨🇳 🔜 ✔.
* `expose_headers` - 🎦 🙆 📨 🎚 👈 🔜 ⚒ ♿ 🖥. 🔢 `[]`.
* `max_age` - ⚒ 🔆 🕰 🥈 🖥 💾 ⚜ 📨. 🔢 `600`.

🛠️ 📨 2️⃣ 🎯 🆎 🇺🇸🔍 📨...

### ⚜ 🛫 📨

👉 🙆 `OPTIONS` 📨 ⏮️ `Origin` &amp; `Access-Control-Request-Method` 🎚.

👉 💼 🛠️ 🔜 🆘 📨 📨 &amp; 📨 ⏮️ ☑ ⚜ 🎚, &amp; 👯‍♂️ `200` ⚖️ `400` 📨 🎓 🎯.

### 🙅 📨

🙆 📨 ⏮️ `Origin` 🎚. 👉 💼 🛠️ 🔜 🚶‍♀️ 📨 🔘 😐, ✋️ 🔜 🔌 ☑ ⚜ 🎚 🔛 📨.

## 🌅 ℹ

🌖 ℹ 🔃 <abbr title="Cross-Origin Resource Sharing">⚜</abbr>, ✅ <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" class="external-link" target="_blank">🦎 ⚜ 🧾</a>.

/// note | 📡 ℹ

👆 💪 ⚙️ `from starlette.middleware.cors import CORSMiddleware`.

**FastAPI** 🚚 📚 🛠️ `fastapi.middleware` 🏪 👆, 👩‍💻. ✋️ 🌅 💪 🛠️ 👟 🔗 ⚪️➡️ 💃.

///
