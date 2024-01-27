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
