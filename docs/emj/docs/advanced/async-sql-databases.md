# 🔁 🗄 (🔗) 💽

👆 💪 ⚙️ <a href="https://github.com/encode/databases" class="external-link" target="_blank">`encode/databases`</a> ⏮ **FastAPI** 🔗 💽 ⚙️ `async` &amp; `await`.

⚫️ 🔗 ⏮:

* ✳
* ✳
* 🗄

👉 🖼, 👥 🔜 ⚙️ **🗄**, ↩️ ⚫️ ⚙️ 👁 📁 &amp; 🐆 ✔️ 🛠 🐕‍🦺. , 👆 💪 📁 👉 🖼 &amp; 🏃 ⚫️.

⏪, 👆 🏭 🈸, 👆 💪 💚 ⚙️ 💽 💽 💖 **✳**.

!!! tip
    👆 💪 🛠 💭 ⚪️➡️ 📄 🔃 🇸🇲 🐜 ([🗄 (🔗) 💽](../tutorial/sql-databases.md){.internal-link target=_blank}), 💖 ⚙️ 🚙 🔢 🎭 🛠 💽, 🔬 👆 **FastAPI** 📟.

    👉 📄 🚫 ✔ 📚 💭, 🌓 😑 <a href="https://www.starlette.io/database/" class="external-link" target="_blank">💃</a>.

## 🗄 &amp; ⚒ 🆙 `SQLAlchemy`

* 🗄 `SQLAlchemy`.
* ✍ `metadata` 🎚.
* ✍ 🏓 `notes` ⚙️ `metadata` 🎚.

```Python hl_lines="4  14  16-22"
{!../../../docs_src/async_sql_databases/tutorial001.py!}
```

!!! tip
    👀 👈 🌐 👉 📟 😁 🇸🇲 🐚.

    `databases` 🚫 🔨 🕳 📥.

## 🗄 &amp; ⚒ 🆙 `databases`

* 🗄 `databases`.
* ✍ `DATABASE_URL`.
* ✍ `database` 🎚.

```Python hl_lines="3  9  12"
{!../../../docs_src/async_sql_databases/tutorial001.py!}
```

!!! tip
    🚥 👆 🔗 🎏 💽 (✅ ✳), 👆 🔜 💪 🔀 `DATABASE_URL`.

## ✍ 🏓

👉 💼, 👥 🏗 🏓 🎏 🐆 📁, ✋️ 🏭, 👆 🔜 🎲 💚 ✍ 👫 ⏮ ⚗, 🛠 ⏮ 🛠, ♒️.

📥, 👉 📄 🔜 🏃 🔗, ▶️ ⏭ ▶ 👆 **FastAPI** 🈸.

* ✍ `engine`.
* ✍ 🌐 🏓 ⚪️➡️ `metadata` 🎚.

```Python hl_lines="25-28"
{!../../../docs_src/async_sql_databases/tutorial001.py!}
```

## ✍ 🏷

✍ Pydantic 🏷:

* 🗒 ✍ (`NoteIn`).
* 🗒 📨 (`Note`).

```Python hl_lines="31-33  36-39"
{!../../../docs_src/async_sql_databases/tutorial001.py!}
```

🏗 👫 Pydantic 🏷, 🔢 💽 🔜 ✔, 🎻 (🗜), &amp; ✍ (📄).

, 👆 🔜 💪 👀 ⚫️ 🌐 🎓 🛠 🩺.

## 🔗 &amp; 🔌

* ✍ 👆 `FastAPI` 🈸.
* ✍ 🎉 🐕‍🦺 🔗 &amp; 🔌 ⚪️➡️ 💽.

```Python hl_lines="42  45-47  50-52"
{!../../../docs_src/async_sql_databases/tutorial001.py!}
```

## ✍ 🗒

✍ *➡ 🛠 🔢* ✍ 🗒:

```Python hl_lines="55-58"
{!../../../docs_src/async_sql_databases/tutorial001.py!}
```

!!! Note
    👀 👈 👥 🔗 ⏮ 💽 ⚙️ `await`, *➡ 🛠 🔢* 📣 ⏮ `async`.

### 👀 `response_model=List[Note]`

⚫️ ⚙️ `typing.List`.

👈 📄 (&amp; ✔, 🎻, ⛽) 🔢 💽, `list` `Note`Ⓜ.

## ✍ 🗒

✍ *➡ 🛠 🔢* ✍ 🗒:

```Python hl_lines="61-65"
{!../../../docs_src/async_sql_databases/tutorial001.py!}
```

!!! Note
    👀 👈 👥 🔗 ⏮ 💽 ⚙️ `await`, *➡ 🛠 🔢* 📣 ⏮ `async`.

### 🔃 `{**note.dict(), "id": last_record_id}`

`note` Pydantic `Note` 🎚.

`note.dict()` 📨 `dict` ⏮ 🚮 💽, 🕳 💖:

```Python
{
    "text": "Some note",
    "completed": False,
}
```

✋️ ⚫️ 🚫 ✔️ `id` 🏑.

👥 ✍ 🆕 `dict`, 👈 🔌 🔑-💲 👫 ⚪️➡️ `note.dict()` ⏮:

```Python
{**note.dict()}
```

`**🗒.#⃣ ()` "unpacks" the key value pairs directly, so, `{**🗒.#⃣ ()}` would be, more or less, a copy of `🗒.#⃣ ()`.

&amp; ⤴, 👥 ↔ 👈 📁 `dict`, ❎ ➕1️⃣ 🔑-💲 👫: `"id": last_record_id`:

```Python
{**note.dict(), "id": last_record_id}
```

, 🏁 🏁 📨 🔜 🕳 💖:

```Python
{
    "id": 1,
    "text": "Some note",
    "completed": False,
}
```

## ✅ ⚫️

👆 💪 📁 👉 📟, &amp; 👀 🩺 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">Http://127.0.0.1:8000/docs</a>.

📤 👆 💪 👀 🌐 👆 🛠 📄 &amp; 🔗 ⏮ ⚫️:

<img src="/img/tutorial/async-sql-databases/image01.png">

## 🌅 ℹ

👆 💪 ✍ 🌅 🔃 <a href="https://github.com/encode/databases" class="external-link" target="_blank">`encode/databases` 🚮 📂 📃</a>.
