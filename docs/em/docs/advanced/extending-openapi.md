# ↔ 🗄

!!! warning
    👉 👍 🏧 ⚒. 👆 🎲 💪 🚶 ⚫️.

    🚥 👆 📄 🔰 - 👩‍💻 🦮, 👆 💪 🎲 🚶 👉 📄.

    🚥 👆 ⏪ 💭 👈 👆 💪 🔀 🏗 🗄 🔗, 😣 👂.

📤 💼 🌐❔ 👆 💪 💪 🔀 🏗 🗄 🔗.

👉 📄 👆 🔜 👀 ❔.

## 😐 🛠️

😐 (🔢) 🛠️, ⏩.

`FastAPI` 🈸 (👐) ✔️ `.openapi()` 👩‍🔬 👈 📈 📨 🗄 🔗.

🍕 🈸 🎚 🏗, *➡ 🛠️* `/openapi.json` (⚖️ ⚫️❔ 👆 ⚒ 👆 `openapi_url`) ®.

⚫️ 📨 🎻 📨 ⏮️ 🏁 🈸 `.openapi()` 👩‍🔬.

🔢, ⚫️❔ 👩‍🔬 `.openapi()` 🔨 ✅ 🏠 `.openapi_schema` 👀 🚥 ⚫️ ✔️ 🎚 &amp; 📨 👫.

🚥 ⚫️ 🚫, ⚫️ 🏗 👫 ⚙️ 🚙 🔢 `fastapi.openapi.utils.get_openapi`.

&amp; 👈 🔢 `get_openapi()` 📨 🔢:

* `title`: 🗄 📛, 🎦 🩺.
* `version`: ⏬ 👆 🛠️, ✅ `2.5.0`.
* `openapi_version`: ⏬ 🗄 🔧 ⚙️. 🔢, ⏪: `3.0.2`.
* `description`: 📛 👆 🛠️.
* `routes`: 📇 🛣, 👫 🔠 ® *➡ 🛠️*. 👫 ✊ ⚪️➡️ `app.routes`.

## 🔑 🔢

⚙️ ℹ 🔛, 👆 💪 ⚙️ 🎏 🚙 🔢 🏗 🗄 🔗 &amp; 🔐 🔠 🍕 👈 👆 💪.

🖼, ➡️ 🚮 <a href="https://github.com/Rebilly/ReDoc/blob/master/docs/redoc-vendor-extensions.md#x-logo" class="external-link" target="_blank">📄 🗄 ↔ 🔌 🛃 🔱</a>.

### 😐 **FastAPI**

🥇, ✍ 🌐 👆 **FastAPI** 🈸 🛎:

```Python hl_lines="1  4  7-9"
{!../../../docs_src/extending_openapi/tutorial001.py!}
```

### 🏗 🗄 🔗

⤴️, ⚙️ 🎏 🚙 🔢 🏗 🗄 🔗, 🔘 `custom_openapi()` 🔢:

```Python hl_lines="2  15-20"
{!../../../docs_src/extending_openapi/tutorial001.py!}
```

### 🔀 🗄 🔗

🔜 👆 💪 🚮 📄 ↔, ❎ 🛃 `x-logo` `info` "🎚" 🗄 🔗:

```Python hl_lines="21-23"
{!../../../docs_src/extending_openapi/tutorial001.py!}
```

### 💾 🗄 🔗

👆 💪 ⚙️ 🏠 `.openapi_schema` "💾", 🏪 👆 🏗 🔗.

👈 🌌, 👆 🈸 🏆 🚫 ✔️ 🏗 🔗 🔠 🕰 👩‍💻 📂 👆 🛠️ 🩺.

⚫️ 🔜 🏗 🕴 🕐, &amp; ⤴️ 🎏 💾 🔗 🔜 ⚙️ ⏭ 📨.

```Python hl_lines="13-14  24-25"
{!../../../docs_src/extending_openapi/tutorial001.py!}
```

### 🔐 👩‍🔬

🔜 👆 💪 ❎ `.openapi()` 👩‍🔬 ⏮️ 👆 🆕 🔢.

```Python hl_lines="28"
{!../../../docs_src/extending_openapi/tutorial001.py!}
```

### ✅ ⚫️

🕐 👆 🚶 <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> 👆 🔜 👀 👈 👆 ⚙️ 👆 🛃 🔱 (👉 🖼, **FastAPI**'Ⓜ 🔱):

<img src="/img/tutorial/extending-openapi/image01.png">

## 👤-🕸 🕸 &amp; 🎚 🩺

🛠️ 🩺 ⚙️ **🦁 🎚** &amp; **📄**, &amp; 🔠 👈 💪 🕸 &amp; 🎚 📁.

🔢, 👈 📁 🍦 ⚪️➡️ <abbr title="Content Delivery Network: A service, normally composed of several servers, that provides static files, like JavaScript and CSS. It's commonly used to serve those files from the server closer to the client, improving performance.">💲</abbr>.

✋️ ⚫️ 💪 🛃 ⚫️, 👆 💪 ⚒ 🎯 💲, ⚖️ 🍦 📁 👆.

👈 ⚠, 🖼, 🚥 👆 💪 👆 📱 🚧 👷 ⏪ 📱, 🍵 📂 🕸 🔐, ⚖️ 🇧🇿 🕸.

📥 👆 🔜 👀 ❔ 🍦 👈 📁 👆, 🎏 FastAPI 📱, &amp; 🔗 🩺 ⚙️ 👫.

### 🏗 📁 📊

➡️ 💬 👆 🏗 📁 📊 👀 💖 👉:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
```

🔜 ✍ 📁 🏪 📚 🎻 📁.

👆 🆕 📁 📊 💪 👀 💖 👉:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static/
```

### ⏬ 📁

⏬ 🎻 📁 💪 🩺 &amp; 🚮 👫 🔛 👈 `static/` 📁.

👆 💪 🎲 ▶️️-🖊 🔠 🔗 &amp; 🖊 🎛 🎏 `Save link as...`.

**🦁 🎚** ⚙️ 📁:

* <a href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui-bundle.js" class="external-link" target="_blank">`swagger-ui-bundle.js`</a>
* <a href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui.css" class="external-link" target="_blank">`swagger-ui.css`</a>

&amp; **📄** ⚙️ 📁:

* <a href="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js" class="external-link" target="_blank">`redoc.standalone.js`</a>

⏮️ 👈, 👆 📁 📊 💪 👀 💖:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static
    ├── redoc.standalone.js
    ├── swagger-ui-bundle.js
    └── swagger-ui.css
```

### 🍦 🎻 📁

* 🗄 `StaticFiles`.
* "🗻" `StaticFiles()` 👐 🎯 ➡.

```Python hl_lines="7  11"
{!../../../docs_src/extending_openapi/tutorial002.py!}
```

### 💯 🎻 📁

▶️ 👆 🈸 &amp; 🚶 <a href="http://127.0.0.1:8000/static/redoc.standalone.js" class="external-link" target="_blank">http://127.0.0.1:8000/static/redoc.standalone.js</a>.

👆 🔜 👀 📶 📏 🕸 📁 **📄**.

⚫️ 💪 ▶️ ⏮️ 🕳 💖:

```JavaScript
/*!
 * ReDoc - OpenAPI/Swagger-generated API Reference Documentation
 * -------------------------------------------------------------
 *   Version: "2.0.0-rc.18"
 *   Repo: https://github.com/Redocly/redoc
 */
!function(e,t){"object"==typeof exports&&"object"==typeof m

...
```

👈 ✔ 👈 👆 💆‍♂ 💪 🍦 🎻 📁 ⚪️➡️ 👆 📱, &amp; 👈 👆 🥉 🎻 📁 🩺 ☑ 🥉.

🔜 👥 💪 🔗 📱 ⚙️ 📚 🎻 📁 🩺.

### ❎ 🏧 🩺

🥇 🔁 ❎ 🏧 🩺, 📚 ⚙️ 💲 🔢.

❎ 👫, ⚒ 👫 📛 `None` 🕐❔ 🏗 👆 `FastAPI` 📱:

```Python hl_lines="9"
{!../../../docs_src/extending_openapi/tutorial002.py!}
```

### 🔌 🛃 🩺

🔜 👆 💪 ✍ *➡ 🛠️* 🛃 🩺.

👆 💪 🏤-⚙️ FastAPI 🔗 🔢 ✍ 🕸 📃 🩺, &amp; 🚶‍♀️ 👫 💪 ❌:

* `openapi_url`: 📛 🌐❔ 🕸 📃 🩺 💪 🤚 🗄 🔗 👆 🛠️. 👆 💪 ⚙️ 📥 🔢 `app.openapi_url`.
* `title`: 📛 👆 🛠️.
* `oauth2_redirect_url`: 👆 💪 ⚙️ `app.swagger_ui_oauth2_redirect_url` 📥 ⚙️ 🔢.
* `swagger_js_url`: 📛 🌐❔ 🕸 👆 🦁 🎚 🩺 💪 🤚 **🕸** 📁. 👉 1️⃣ 👈 👆 👍 📱 🔜 🍦.
* `swagger_css_url`: 📛 🌐❔ 🕸 👆 🦁 🎚 🩺 💪 🤚 **🎚** 📁. 👉 1️⃣ 👈 👆 👍 📱 🔜 🍦.

&amp; ➡ 📄...

```Python hl_lines="2-6  14-22  25-27  30-36"
{!../../../docs_src/extending_openapi/tutorial002.py!}
```

!!! tip
     *➡ 🛠️* `swagger_ui_redirect` 👩‍🎓 🕐❔ 👆 ⚙️ Oauth2️⃣.

    🚥 👆 🛠️ 👆 🛠️ ⏮️ Oauth2️⃣ 🐕‍🦺, 👆 🔜 💪 🔓 &amp; 👟 🔙 🛠️ 🩺 ⏮️ 📎 🎓. &amp; 🔗 ⏮️ ⚫️ ⚙️ 🎰 Oauth2️⃣ 🤝.

    🦁 🎚 🔜 🍵 ⚫️ ⛅ 🎑 👆, ✋️ ⚫️ 💪 👉 "❎" 👩‍🎓.

### ✍ *➡ 🛠️* 💯 ⚫️

🔜, 💪 💯 👈 🌐 👷, ✍ *➡ 🛠️*:

```Python hl_lines="39-41"
{!../../../docs_src/extending_openapi/tutorial002.py!}
```

### 💯 ⚫️

🔜, 👆 🔜 💪 🔌 👆 📻, 🚶 👆 🩺 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>, &amp; 🔃 📃.

&amp; 🍵 🕸, 👆 🔜 💪 👀 🩺 👆 🛠️ &amp; 🔗 ⏮️ ⚫️.

## 🛠️ 🦁 🎚

👆 💪 🔗 ➕ <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration" class="external-link" target="_blank">🦁 🎚 🔢</a>.

🔗 👫, 🚶‍♀️ `swagger_ui_parameters` ❌ 🕐❔ 🏗 `FastAPI()` 📱 🎚 ⚖️ `get_swagger_ui_html()` 🔢.

`swagger_ui_parameters` 📨 📖 ⏮️ 📳 🚶‍♀️ 🦁 🎚 🔗.

FastAPI 🗜 📳 **🎻** ⚒ 👫 🔗 ⏮️ 🕸, 👈 ⚫️❔ 🦁 🎚 💪.

### ❎ ❕ 🎦

🖼, 👆 💪 ❎ ❕ 🎦 🦁 🎚.

🍵 🔀 ⚒, ❕ 🎦 🛠️ 🔢:

<img src="/img/tutorial/extending-openapi/image02.png">

✋️ 👆 💪 ❎ ⚫️ ⚒ `syntaxHighlight` `False`:

```Python hl_lines="3"
{!../../../docs_src/extending_openapi/tutorial003.py!}
```

...&amp; ⤴️ 🦁 🎚 🏆 🚫 🎦 ❕ 🎦 🚫🔜:

<img src="/img/tutorial/extending-openapi/image03.png">

### 🔀 🎢

🎏 🌌 👆 💪 ⚒ ❕ 🎦 🎢 ⏮️ 🔑 `"syntaxHighlight.theme"` (👀 👈 ⚫️ ✔️ ❣ 🖕):

```Python hl_lines="3"
{!../../../docs_src/extending_openapi/tutorial004.py!}
```

👈 📳 🔜 🔀 ❕ 🎦 🎨 🎢:

<img src="/img/tutorial/extending-openapi/image04.png">

### 🔀 🔢 🦁 🎚 🔢

FastAPI 🔌 🔢 📳 🔢 ☑ 🌅 ⚙️ 💼.

⚫️ 🔌 👫 🔢 📳:

```Python
{!../../../fastapi/openapi/docs.py[ln:7-13]!}
```

👆 💪 🔐 🙆 👫 ⚒ 🎏 💲 ❌ `swagger_ui_parameters`.

🖼, ❎ `deepLinking` 👆 💪 🚶‍♀️ 👉 ⚒ `swagger_ui_parameters`:

```Python hl_lines="3"
{!../../../docs_src/extending_openapi/tutorial005.py!}
```

### 🎏 🦁 🎚 🔢

👀 🌐 🎏 💪 📳 👆 💪 ⚙️, ✍ 🛂 <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration" class="external-link" target="_blank">🩺 🦁 🎚 🔢</a>.

### 🕸-🕴 ⚒

🦁 🎚 ✔ 🎏 📳 **🕸-🕴** 🎚 (🖼, 🕸 🔢).

FastAPI 🔌 👫 🕸-🕴 `presets` ⚒:

```JavaScript
presets: [
    SwaggerUIBundle.presets.apis,
    SwaggerUIBundle.SwaggerUIStandalonePreset
]
```

👫 **🕸** 🎚, 🚫 🎻, 👆 💪 🚫 🚶‍♀️ 👫 ⚪️➡️ 🐍 📟 🔗.

🚥 👆 💪 ⚙️ 🕸-🕴 📳 💖 📚, 👆 💪 ⚙️ 1️⃣ 👩‍🔬 🔛. 🔐 🌐 🦁 🎚 *➡ 🛠️* &amp; ❎ ✍ 🙆 🕸 👆 💪.
