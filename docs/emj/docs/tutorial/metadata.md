# 🗃 &amp; 🩺 📛

👆 💪 🛃 📚 🗃 📳 👆 **FastAPI** 🈸.

## 🗃 🛠

👆 💪 ⚒ 📄 🏑 👈 ⚙️ 🗄 🔧 &amp; 🏧 🛠 🩺 ⚜:

| 🔢 | 🆎 | 📛 |
|------------|------|-------------|
| `title` | `str` | 📛 🛠. |
| `description` | `str` | 📏 📛 🛠. ⚫️ 💪 ⚙️ ✍. |
| `version` | `string` | ⏬ 🛠. 👉 ⏬ 👆 👍 🈸, 🚫 🗄. 🖼 `2.5.0`. |
| `terms_of_service` | `str` | 📛 ⚖ 🐕‍🦺 🛠. 🚥 🚚, 👉 ✔️ 📛. |
| `contact` | `dict` | 📧 ℹ 🎦 🛠. ⚫️ 💪 🔌 📚 🏑. <details><summary><code>contact</code> 🏑</summary><table><thead><tr><th>🔢</th><th>🆎</th><th>📛</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td>⚖ 📛 📧 👨‍💼/🏢.</td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>📛 ☝ 📧 ℹ. 🔜 📁 📛.</td></tr><tr><td><code>email</code></td><td><code>str</code></td><td>📧 📢 📧 👨‍💼/🏢. 🔜 📁 📧 📢. </td></tr></tbody></table></details> |
| `license_info` | `dict` | 🛂 ℹ 🎦 🛠. ⚫️ 💪 🔌 📚 🏑. <details><summary><code>license_info</code> 🏑</summary><table><thead><tr><th>🔢</th><th>🆎</th><th>📛</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td><strong>🚚</strong> (🚥 <code>license_info</code> ⚒). 🛂 📛 ⚙️ 🛠.</td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>📛 🛂 ⚙️ 🛠. 🔜 📁 📛. </td></tr></tbody></table></details> |

👆 💪 ⚒ 👫 ⏩:

```Python hl_lines="3-16  19-31"
{!../../../docs_src/metadata/tutorial001.py!}
```

!!! tip
    👆 💪 ✍ ✍ `description` 🏑 &amp; ⚫️ 🔜 ✍ 🔢.

⏮ 👉 📳, 🏧 🛠 🩺 🔜 👀 💖:

<img src="/img/tutorial/metadata/image01.png">

## 🗃 🔖

👆 💪 🚮 🌖 🗃 🎏 🔖 ⚙️ 👪 👆 ➡ 🛠 ⏮ 🔢 `openapi_tags`.

⚫️ ✊ 📇 ⚗ 1⃣ 📖 🔠 🔖.

🔠 📖 💪 🔌:

* `name` (**✔**): `str` ⏮ 🎏 📛 👆 ⚙️ `tags` 🔢 👆 *➡ 🛠* &amp; `APIRouter`Ⓜ.
* `description`: `str` ⏮ 📏 📛 🔖. ⚫️ 💪 ✔️ ✍ &amp; 🔜 🎦 🩺 🎚.
* `externalDocs`: `dict` 🔬 🔢 🧾 ⏮:
    * `description`: `str` ⏮ 📏 📛 🔢 🩺.
    * `url` (**✔**): `str` ⏮ 📛 🔢 🧾.

### ✍ 🗃 🔖

➡️ 🔄 👈 🖼 ⏮ 🔖 `users` &amp; `items`.

✍ 🗃 👆 🔖 &amp; 🚶‍♀️ ⚫️ `openapi_tags` 🔢:

```Python hl_lines="3-16  18"
{!../../../docs_src/metadata/tutorial004.py!}
```

👀 👈 👆 💪 ⚙️ ✍ 🔘 📛, 🖼 "💳" 🔜 🎦 🦁 (**💳**) &amp; "🎀" 🔜 🎦 ❕ (_🎀_).

!!! tip
    👆 🚫 ✔️ 🚮 🗃 🌐 🔖 👈 👆 ⚙️.

### ⚙️ 👆 🔖

⚙️ `tags` 🔢 ⏮ 👆 *➡ 🛠* (&amp; `APIRouter`Ⓜ) 🛠 👫 🎏 🔖:

```Python hl_lines="21  26"
{!../../../docs_src/metadata/tutorial004.py!}
```

!!! info
    ✍ 🌅 🔃 🔖 [➡ 🛠 📳](../path-operation-configuration/#tags){.internal-link target=_blank}.

### ✅ 🩺

🔜, 🚥 👆 ✅ 🩺, 👫 🔜 🎦 🌐 🌖 🗃:

<img src="/img/tutorial/metadata/image02.png">

### ✔ 🔖

✔ 🔠 🔖 🗃 📖 🔬 ✔ 🎦 🩺 🎚.

🖼, ✋️ `users` 🔜 🚶 ⏮ `items` 🔤 ✔, ⚫️ 🎦 ⏭ 👫, ↩️ 👥 🚮 👫 🗃 🥇 📖 📇.

## 🗄 📛

🔢, 🗄 🔗 🍦 `/openapi.json`.

✋️ 👆 💪 🔗 ⚫️ ⏮ 🔢 `openapi_url`.

🖼, ⚒ ⚫️ 🍦 `/api/v1/openapi.json`:

```Python hl_lines="3"
{!../../../docs_src/metadata/tutorial002.py!}
```

🚥 👆 💚 ❎ 🗄 🔗 🍕 👆 💪 ⚒ `openapi_url=None`, 👈 🔜 ❎ 🧾 👩‍💻 🔢 👈 ⚙️ ⚫️.

## 🩺 📛

👆 💪 🔗 2⃣ 🧾 👩‍💻 🔢 🔌:

* **🦁 🎚**: 🍦 `/docs`.
    * 👆 💪 ⚒ 🚮 📛 ⏮ 🔢 `docs_url`.
    * 👆 💪 ❎ ⚫️ ⚒ `docs_url=None`.
* **📄**: 🍦 `/redoc`.
    * 👆 💪 ⚒ 🚮 📛 ⏮ 🔢 `redoc_url`.
    * 👆 💪 ❎ ⚫️ ⚒ `redoc_url=None`.

🖼, ⚒ 🦁 🎚 🍦 `/documentation` &amp; ❎ 📄:

```Python hl_lines="3"
{!../../../docs_src/metadata/tutorial003.py!}
```
