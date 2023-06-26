# ☁ (📎 / 🦏 💽) 💽

**FastAPI** 💪 🛠️ ⏮️ 🙆 <abbr title="Distributed database (Big Data), also 'Not Only SQL'">☁</abbr>.

📥 👥 🔜 👀 🖼 ⚙️ **<a href="https://www.couchbase.com/" class="external-link" target="_blank">🗄</a>**, <abbr title="Document here refers to a JSON object (a dict), with keys and values, and those values can also be other JSON objects, arrays (lists), numbers, strings, booleans, etc.">📄</abbr> 🧢 ☁ 💽.

👆 💪 🛠️ ⚫️ 🙆 🎏 ☁ 💽 💖:

* **✳**
* **👸**
* **✳**
* **🇸🇲**
* **✳**, ♒️.

!!! tip
    📤 🛂 🏗 🚂 ⏮️ **FastAPI** &amp; **🗄**, 🌐 ⚓️ 🔛 **☁**, 🔌 🕸 &amp; 🌖 🧰: <a href="https://github.com/tiangolo/full-stack-fastapi-couchbase" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-fastapi-couchbase</a>

## 🗄 🗄 🦲

🔜, 🚫 💸 🙋 🎂, 🕴 🗄:

```Python hl_lines="3-5"
{!../../../docs_src/nosql_databases/tutorial001.py!}
```

## 🔬 📉 ⚙️ "📄 🆎"

👥 🔜 ⚙️ ⚫️ ⏪ 🔧 🏑 `type` 👆 📄.

👉 🚫 ✔ 🗄, ✋️ 👍 💡 👈 🔜 ℹ 👆 ⏮️.

```Python hl_lines="9"
{!../../../docs_src/nosql_databases/tutorial001.py!}
```

## 🚮 🔢 🤚 `Bucket`

**🗄**, 🥡 ⚒ 📄, 👈 💪 🎏 🆎.

👫 🛎 🌐 🔗 🎏 🈸.

🔑 🔗 💽 🌏 🔜 "💽" (🎯 💽, 🚫 💽 💽).

🔑 **✳** 🔜 "🗃".

📟, `Bucket` 🎨 👑 🇨🇻 📻 ⏮️ 💽.

👉 🚙 🔢 🔜:

* 🔗 **🗄** 🌑 (👈 💪 👁 🎰).
    * ⚒ 🔢 ⏲.
* 🔓 🌑.
* 🤚 `Bucket` 👐.
    * ⚒ 🔢 ⏲.
* 📨 ⚫️.

```Python hl_lines="12-21"
{!../../../docs_src/nosql_databases/tutorial001.py!}
```

## ✍ Pydantic 🏷

**🗄** "📄" 🤙 "🎻 🎚", 👥 💪 🏷 👫 ⏮️ Pydantic.

### `User` 🏷

🥇, ➡️ ✍ `User` 🏷:

```Python hl_lines="24-28"
{!../../../docs_src/nosql_databases/tutorial001.py!}
```

👥 🔜 ⚙️ 👉 🏷 👆 *➡ 🛠️ 🔢*,, 👥 🚫 🔌 ⚫️ `hashed_password`.

### `UserInDB` 🏷

🔜, ➡️ ✍ `UserInDB` 🏷.

👉 🔜 ✔️ 💽 👈 🤙 🏪 💽.

👥 🚫 ✍ ⚫️ 🏿 Pydantic `BaseModel` ✋️ 🏿 👆 👍 `User`, ↩️ ⚫️ 🔜 ✔️ 🌐 🔢 `User` ➕ 👩‍❤‍👨 🌅:

```Python hl_lines="31-33"
{!../../../docs_src/nosql_databases/tutorial001.py!}
```

!!! note
    👀 👈 👥 ✔️ `hashed_password` &amp; `type` 🏑 👈 🔜 🏪 💽.

    ✋️ ⚫️ 🚫 🍕 🏢 `User` 🏷 (1️⃣ 👥 🔜 📨 *➡ 🛠️*).

## 🤚 👩‍💻

🔜 ✍ 🔢 👈 🔜:

* ✊ 🆔.
* 🏗 📄 🆔 ⚪️➡️ ⚫️.
* 🤚 📄 ⏮️ 👈 🆔.
* 🚮 🎚 📄 `UserInDB` 🏷.

🏗 🔢 👈 🕴 💡 🤚 👆 👩‍💻 ⚪️➡️ `username` (⚖️ 🙆 🎏 🔢) 🔬 👆 *➡ 🛠️ 🔢*, 👆 💪 🌖 💪 🏤-⚙️ ⚫️ 💗 🍕 &amp; 🚮 <abbr title="Automated test, written in code, that checks if another piece of code is working correctly.">⚒ 💯</abbr> ⚫️:

```Python hl_lines="36-42"
{!../../../docs_src/nosql_databases/tutorial001.py!}
```

### Ⓜ-🎻

🚥 👆 🚫 😰 ⏮️ `f"userprofile::{username}"`, ⚫️ 🐍 "<a href="https://docs.python.org/3/glossary.html#term-f-string" class="external-link" target="_blank">Ⓜ-🎻</a>".

🙆 🔢 👈 🚮 🔘 `{}` Ⓜ-🎻 🔜 ↔ / 💉 🎻.

### `dict` 🏗

🚥 👆 🚫 😰 ⏮️ `UserInDB(**result.value)`, <a href="https://docs.python.org/3/glossary.html#term-argument" class="external-link" target="_blank">⚫️ ⚙️ `dict` "🏗"</a>.

⚫️ 🔜 ✊ `dict` `result.value`, &amp; ✊ 🔠 🚮 🔑 &amp; 💲 &amp; 🚶‍♀️ 👫 🔑-💲 `UserInDB` 🇨🇻 ❌.

, 🚥 `dict` 🔌:

```Python
{
    "username": "johndoe",
    "hashed_password": "some_hash",
}
```

⚫️ 🔜 🚶‍♀️ `UserInDB` :

```Python
UserInDB(username="johndoe", hashed_password="some_hash")
```

## ✍ 👆 **FastAPI** 📟

### ✍ `FastAPI` 📱

```Python hl_lines="46"
{!../../../docs_src/nosql_databases/tutorial001.py!}
```

### ✍ *➡ 🛠️ 🔢*

👆 📟 🤙 🗄 &amp; 👥 🚫 ⚙️ <a href="https://docs.couchbase.com/python-sdk/2.5/async-programming.html#asyncio-python-3-5" class="external-link" target="_blank">🥼 🐍 <code>await</code> 🐕‍🦺</a>, 👥 🔜 📣 👆 🔢 ⏮️ 😐 `def` ↩️ `async def`.

, 🗄 👍 🚫 ⚙️ 👁 `Bucket` 🎚 💗 "<abbr title="A sequence of code being executed by the program, while at the same time, or at intervals, there can be others being executed too.">🧵</abbr>Ⓜ",, 👥 💪 🤚 🥡 🔗 &amp; 🚶‍♀️ ⚫️ 👆 🚙 🔢:

```Python hl_lines="49-53"
{!../../../docs_src/nosql_databases/tutorial001.py!}
```

## 🌃

👆 💪 🛠️ 🙆 🥉 🥳 ☁ 💽, ⚙️ 👫 🐩 📦.

🎏 ✔ 🙆 🎏 🔢 🧰, ⚙️ ⚖️ 🛠️.
