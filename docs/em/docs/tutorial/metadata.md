# 🗃 &amp; 🩺 📛

👆 💪 🛃 📚 🗃 📳 👆 **FastAPI** 🈸.

## 🗃 🛠️

👆 💪 ⚒ 📄 🏑 👈 ⚙️ 🗄 🔧 &amp; 🏧 🛠️ 🩺 ⚜:

| 🔢 | 🆎 | 📛 |
|------------|------|-------------|
| `title` | `str` | 📛 🛠️. |
| `description` | `str` | 📏 📛 🛠️. ⚫️ 💪 ⚙️ ✍. |
| `version` | `string` | ⏬ 🛠️. 👉 ⏬ 👆 👍 🈸, 🚫 🗄. 🖼 `2.5.0`. |
| `terms_of_service` | `str` | 📛 ⚖ 🐕‍🦺 🛠️. 🚥 🚚, 👉 ✔️ 📛. |
| `contact` | `dict` | 📧 ℹ 🎦 🛠️. ⚫️ 💪 🔌 📚 🏑. <details><summary><code>contact</code> 🏑</summary><table><thead><tr><th>🔢</th><th>🆎</th><th>📛</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td>⚖ 📛 📧 👨‍💼/🏢.</td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>📛 ☝ 📧 ℹ. 🔜 📁 📛.</td></tr><tr><td><code>email</code></td><td><code>str</code></td><td>📧 📢 📧 👨‍💼/🏢. 🔜 📁 📧 📢. </td></tr></tbody></table></details> |
| `license_info` | `dict` | 🛂 ℹ 🎦 🛠️. ⚫️ 💪 🔌 📚 🏑. <details><summary><code>license_info</code> 🏑</summary><table><thead><tr><th>🔢</th><th>🆎</th><th>📛</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td><strong>🚚</strong> (🚥 <code>license_info</code> ⚒). 🛂 📛 ⚙️ 🛠️.</td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>📛 🛂 ⚙️ 🛠️. 🔜 📁 📛. </td></tr></tbody></table></details> |

👆 💪 ⚒ 👫 ⏩:

{* ../../docs_src/metadata/tutorial001.py hl[3:16,19:31] *}

/// tip

👆 💪 ✍ ✍ `description` 🏑 &amp; ⚫️ 🔜 ✍ 🔢.

///

⏮️ 👉 📳, 🏧 🛠️ 🩺 🔜 👀 💖:

<img src="/img/tutorial/metadata/image01.png">

## 🗃 🔖

👆 💪 🚮 🌖 🗃 🎏 🔖 ⚙️ 👪 👆 ➡ 🛠️ ⏮️ 🔢 `openapi_tags`.

⚫️ ✊ 📇 ⚗ 1️⃣ 📖 🔠 🔖.

🔠 📖 💪 🔌:

* `name` (**✔**): `str` ⏮️ 🎏 📛 👆 ⚙️ `tags` 🔢 👆 *➡ 🛠️* &amp; `APIRouter`Ⓜ.
* `description`: `str` ⏮️ 📏 📛 🔖. ⚫️ 💪 ✔️ ✍ &amp; 🔜 🎦 🩺 🎚.
* `externalDocs`: `dict` 🔬 🔢 🧾 ⏮️:
    * `description`: `str` ⏮️ 📏 📛 🔢 🩺.
    * `url` (**✔**): `str` ⏮️ 📛 🔢 🧾.

### ✍ 🗃 🔖

➡️ 🔄 👈 🖼 ⏮️ 🔖 `users` &amp; `items`.

✍ 🗃 👆 🔖 &amp; 🚶‍♀️ ⚫️ `openapi_tags` 🔢:

{* ../../docs_src/metadata/tutorial004.py hl[3:16,18] *}

👀 👈 👆 💪 ⚙️ ✍ 🔘 📛, 🖼 "💳" 🔜 🎦 🦁 (**💳**) &amp; "🎀" 🔜 🎦 ❕ (_🎀_).

/// tip

👆 🚫 ✔️ 🚮 🗃 🌐 🔖 👈 👆 ⚙️.

///

### ⚙️ 👆 🔖

⚙️ `tags` 🔢 ⏮️ 👆 *➡ 🛠️* (&amp; `APIRouter`Ⓜ) 🛠️ 👫 🎏 🔖:

{* ../../docs_src/metadata/tutorial004.py hl[21,26] *}

/// info

✍ 🌅 🔃 🔖 [➡ 🛠️ 📳](path-operation-configuration.md#_3){.internal-link target=_blank}.

///

### ✅ 🩺

🔜, 🚥 👆 ✅ 🩺, 👫 🔜 🎦 🌐 🌖 🗃:

<img src="/img/tutorial/metadata/image02.png">

### ✔ 🔖

✔ 🔠 🔖 🗃 📖 🔬 ✔ 🎦 🩺 🎚.

🖼, ✋️ `users` 🔜 🚶 ⏮️ `items` 🔤 ✔, ⚫️ 🎦 ⏭ 👫, ↩️ 👥 🚮 👫 🗃 🥇 📖 📇.

## 🗄 📛

🔢, 🗄 🔗 🍦 `/openapi.json`.

✋️ 👆 💪 🔗 ⚫️ ⏮️ 🔢 `openapi_url`.

🖼, ⚒ ⚫️ 🍦 `/api/v1/openapi.json`:

{* ../../docs_src/metadata/tutorial002.py hl[3] *}

🚥 👆 💚 ❎ 🗄 🔗 🍕 👆 💪 ⚒ `openapi_url=None`, 👈 🔜 ❎ 🧾 👩‍💻 🔢 👈 ⚙️ ⚫️.

## 🩺 📛

👆 💪 🔗 2️⃣ 🧾 👩‍💻 🔢 🔌:

* **🦁 🎚**: 🍦 `/docs`.
    * 👆 💪 ⚒ 🚮 📛 ⏮️ 🔢 `docs_url`.
    * 👆 💪 ❎ ⚫️ ⚒ `docs_url=None`.
* **📄**: 🍦 `/redoc`.
    * 👆 💪 ⚒ 🚮 📛 ⏮️ 🔢 `redoc_url`.
    * 👆 💪 ❎ ⚫️ ⚒ `redoc_url=None`.

🖼, ⚒ 🦁 🎚 🍦 `/documentation` &amp; ❎ 📄:

{* ../../docs_src/metadata/tutorial003.py hl[3] *}
