# 🗄 (🔗) 💽 ⏮️ 🏒

!!! warning
    🚥 👆 ▶️, 🔰 [🗄 (🔗) 💽](../tutorial/sql-databases.md){.internal-link target=_blank} 👈 ⚙️ 🇸🇲 🔜 🥃.

    💭 🆓 🚶 👉.

🚥 👆 ▶️ 🏗 ⚪️➡️ 🖌, 👆 🎲 👻 📆 ⏮️ 🇸🇲 🐜 ([🗄 (🔗) 💽](../tutorial/sql-databases.md){.internal-link target=_blank}), ⚖️ 🙆 🎏 🔁 🐜.

🚥 👆 ⏪ ✔️ 📟 🧢 👈 ⚙️ <a href="https://docs.peewee-orm.com/en/latest/" class="external-link" target="_blank">🏒 🐜</a>, 👆 💪 ✅ 📥 ❔ ⚙️ ⚫️ ⏮️ **FastAPI**.

!!! warning "🐍 3️⃣.7️⃣ ➕ ✔"
    👆 🔜 💪 🐍 3️⃣.7️⃣ ⚖️ 🔛 🔒 ⚙️ 🏒 ⏮️ FastAPI.

## 🏒 🔁

🏒 🚫 🔧 🔁 🛠️, ⚖️ ⏮️ 👫 🤯.

🏒 ✔️ 🏋️ 🔑 🔃 🚮 🔢 &amp; 🔃 ❔ ⚫️ 🔜 ⚙️.

🚥 👆 🛠️ 🈸 ⏮️ 🗝 🚫-🔁 🛠️, &amp; 💪 👷 ⏮️ 🌐 🚮 🔢, **⚫️ 💪 👑 🧰**.

✋️ 🚥 👆 💪 🔀 🔢, 🐕‍🦺 🌖 🌘 1️⃣ 🔁 💽, 👷 ⏮️ 🔁 🛠️ (💖 FastAPI), ♒️, 👆 🔜 💪 🚮 🏗 ➕ 📟 🔐 👈 🔢.

👐, ⚫️ 💪 ⚫️, &amp; 📥 👆 🔜 👀 ⚫️❔ ⚫️❔ 📟 👆 ✔️ 🚮 💪 ⚙️ 🏒 ⏮️ FastAPI.

!!! note "📡 ℹ"
    👆 💪 ✍ 🌅 🔃 🏒 🧍 🔃 🔁 🐍 <a href="https://docs.peewee-orm.com/en/latest/peewee/database.html#async-with-gevent" class="external-link" target="_blank">🩺</a>, <a href="https://github.com/coleifer/peewee/issues/263#issuecomment-517347032" class="external-link" target="_blank">❔</a>, <a href="https://github.com/coleifer/peewee/pull/2072#issuecomment-563215132" class="external-link" target="_blank">🇵🇷</a>.

## 🎏 📱

👥 🔜 ✍ 🎏 🈸 🇸🇲 🔰 ([🗄 (🔗) 💽](../tutorial/sql-databases.md){.internal-link target=_blank}).

🌅 📟 🤙 🎏.

, 👥 🔜 🎯 🕴 🔛 🔺.

## 📁 📊

➡️ 💬 👆 ✔️ 📁 📛 `my_super_project` 👈 🔌 🎧-📁 🤙 `sql_app` ⏮️ 📊 💖 👉:

```
.
└── sql_app
    ├── __init__.py
    ├── crud.py
    ├── database.py
    ├── main.py
    └── schemas.py
```

👉 🌖 🎏 📊 👥 ✔️ 🇸🇲 🔰.

🔜 ➡️ 👀 ⚫️❔ 🔠 📁/🕹 🔨.

## ✍ 🏒 🍕

➡️ 🔗 📁 `sql_app/database.py`.

### 🐩 🏒 📟

➡️ 🥇 ✅ 🌐 😐 🏒 📟, ✍ 🏒 💽:

```Python hl_lines="3  5  22"
{!../../../docs_src/sql_databases_peewee/sql_app/database.py!}
```

!!! tip
    ✔️ 🤯 👈 🚥 👆 💚 ⚙️ 🎏 💽, 💖 ✳, 👆 🚫 🚫 🔀 🎻. 👆 🔜 💪 ⚙️ 🎏 🏒 💽 🎓.

#### 🗒

❌:

```Python
check_same_thread=False
```

🌓 1️⃣ 🇸🇲 🔰:

```Python
connect_args={"check_same_thread": False}
```

...⚫️ 💪 🕴 `SQLite`.

!!! info "📡 ℹ"

    ⚫️❔ 🎏 📡 ℹ [🗄 (🔗) 💽](../tutorial/sql-databases.md#note){.internal-link target=_blank} ✔.

### ⚒ 🏒 🔁-🔗 `PeeweeConnectionState`

👑 ❔ ⏮️ 🏒 &amp; FastAPI 👈 🏒 ⚓️ 🙇 🔛 <a href="https://docs.python.org/3/library/threading.html#thread-local-data" class="external-link" target="_blank">🐍 `threading.local`</a>, &amp; ⚫️ 🚫 ✔️ 🎯 🌌 🔐 ⚫️ ⚖️ ➡️ 👆 🍵 🔗/🎉 🔗 (🔨 🇸🇲 🔰).

&amp; `threading.local` 🚫 🔗 ⏮️ 🆕 🔁 ⚒ 🏛 🐍.

!!! note "📡 ℹ"
    `threading.local` ⚙️ ✔️ "🎱" 🔢 👈 ✔️ 🎏 💲 🔠 🧵.

    👉 ⚠ 🗝 🛠️ 🏗 ✔️ 1️⃣ 👁 🧵 📍 📨, 🙅‍♂ 🌖, 🙅‍♂ 🌘.

    ⚙️ 👉, 🔠 📨 🔜 ✔️ 🚮 👍 💽 🔗/🎉, ❔ ☑ 🏁 🥅.

    ✋️ FastAPI, ⚙️ 🆕 🔁 ⚒, 💪 🍵 🌅 🌘 1️⃣ 📨 🔛 🎏 🧵. &amp; 🎏 🕰, 👁 📨, ⚫️ 💪 🏃 💗 👜 🎏 🧵 (🧵), ⚓️ 🔛 🚥 👆 ⚙️ `async def` ⚖️ 😐 `def`. 👉 ⚫️❔ 🤝 🌐 🎭 📈 FastAPI.

✋️ 🐍 3️⃣.7️⃣ &amp; 🔛 🚚 🌖 🏧 🎛 `threading.local`, 👈 💪 ⚙️ 🥉 🌐❔ `threading.local` 🔜 ⚙️, ✋️ 🔗 ⏮️ 🆕 🔁 ⚒.

👥 🔜 ⚙️ 👈. ⚫️ 🤙 <a href="https://docs.python.org/3/library/contextvars.html" class="external-link" target="_blank">`contextvars`</a>.

👥 🔜 🔐 🔗 🍕 🏒 👈 ⚙️ `threading.local` &amp; ❎ 👫 ⏮️ `contextvars`, ⏮️ 🔗 ℹ.

👉 5️⃣📆 😑 🍖 🏗 (&amp; ⚫️ 🤙), 👆 🚫 🤙 💪 🍕 🤔 ❔ ⚫️ 👷 ⚙️ ⚫️.

👥 🔜 ✍ `PeeweeConnectionState`:

```Python hl_lines="10-19"
{!../../../docs_src/sql_databases_peewee/sql_app/database.py!}
```

👉 🎓 😖 ⚪️➡️ 🎁 🔗 🎓 ⚙️ 🏒.

⚫️ ✔️ 🌐 ⚛ ⚒ 🏒 ⚙️ `contextvars` ↩️ `threading.local`.

`contextvars` 👷 🍖 🎏 🌘 `threading.local`. ✋️ 🎂 🏒 🔗 📟 🤔 👈 👉 🎓 👷 ⏮️ `threading.local`.

, 👥 💪 ➕ 🎱 ⚒ ⚫️ 👷 🚥 ⚫️ ⚙️ `threading.local`. `__init__`, `__setattr__`, &amp; `__getattr__` 🛠️ 🌐 ✔ 🎱 👉 ⚙️ 🏒 🍵 🤔 👈 ⚫️ 🔜 🔗 ⏮️ FastAPI.

!!! tip
    👉 🔜 ⚒ 🏒 🎭 ☑ 🕐❔ ⚙️ ⏮️ FastAPI. 🚫 🎲 📂 ⚖️ 📪 🔗 👈 ➖ ⚙️, 🏗 ❌, ♒️.

    ✋️ ⚫️ 🚫 🤝 🏒 🔁 💎-🏋️. 👆 🔜 ⚙️ 😐 `def` 🔢 &amp; 🚫 `async def`.

### ⚙️ 🛃 `PeeweeConnectionState` 🎓

🔜, 📁 `._state` 🔗 🔢 🏒 💽 `db` 🎚 ⚙️ 🆕 `PeeweeConnectionState`:

```Python hl_lines="24"
{!../../../docs_src/sql_databases_peewee/sql_app/database.py!}
```

!!! tip
    ⚒ 💭 👆 📁 `db._state` *⏮️* 🏗 `db`.

!!! tip
    👆 🔜 🎏 🙆 🎏 🏒 💽, 🔌 `PostgresqlDatabase`, `MySQLDatabase`, ♒️.

## ✍ 💽 🏷

➡️ 🔜 👀 📁 `sql_app/models.py`.

### ✍ 🏒 🏷 👆 💽

🔜 ✍ 🏒 🏷 (🎓) `User` &amp; `Item`.

👉 🎏 👆 🔜 🚥 👆 ⏩ 🏒 🔰 &amp; ℹ 🏷 ✔️ 🎏 💽 🇸🇲 🔰.

!!! tip
    🏒 ⚙️ ⚖ "**🏷**" 🔗 👉 🎓 &amp; 👐 👈 🔗 ⏮️ 💽.

    ✋️ Pydantic ⚙️ ⚖ "**🏷**" 🔗 🕳 🎏, 💽 🔬, 🛠️, &amp; 🧾 🎓 &amp; 👐.

🗄 `db` ⚪️➡️ `database` (📁 `database.py` ⚪️➡️ 🔛) &amp; ⚙️ ⚫️ 📥.

```Python hl_lines="3  6-12  15-21"
{!../../../docs_src/sql_databases_peewee/sql_app/models.py!}
```

!!! tip
    🏒 ✍ 📚 🎱 🔢.

    ⚫️ 🔜 🔁 🚮 `id` 🔢 🔢 👑 🔑.

    ⚫️ 🔜 ⚒ 📛 🏓 ⚓️ 🔛 🎓 📛.

     `Item`, ⚫️ 🔜 ✍ 🔢 `owner_id` ⏮️ 🔢 🆔 `User`. ✋️ 👥 🚫 📣 ⚫️ 🙆.

## ✍ Pydantic 🏷

🔜 ➡️ ✅ 📁 `sql_app/schemas.py`.

!!! tip
    ❎ 😨 🖖 🏒 *🏷* &amp; Pydantic *🏷*, 👥 🔜 ✔️ 📁 `models.py` ⏮️ 🏒 🏷, &amp; 📁 `schemas.py` ⏮️ Pydantic 🏷.

    👫 Pydantic 🏷 🔬 🌅 ⚖️ 🌘 "🔗" (☑ 📊 💠).

    👉 🔜 ℹ 👥 ❎ 😨 ⏪ ⚙️ 👯‍♂️.

### ✍ Pydantic *🏷* / 🔗

✍ 🌐 🎏 Pydantic 🏷 🇸🇲 🔰:

```Python hl_lines="16-18  21-22  25-30  34-35  38-39  42-48"
{!../../../docs_src/sql_databases_peewee/sql_app/schemas.py!}
```

!!! tip
    📥 👥 🏗 🏷 ⏮️ `id`.

    👥 🚫 🎯 ✔ `id` 🔢 🏒 🏷, ✋️ 🏒 🚮 1️⃣ 🔁.

    👥 ❎ 🎱 `owner_id` 🔢 `Item`.

### ✍ `PeeweeGetterDict` Pydantic *🏷* / 🔗

🕐❔ 👆 🔐 💛 🏒 🎚, 💖 `some_user.items`, 🏒 🚫 🚚 `list` `Item`.

⚫️ 🚚 🎁 🛃 🎚 🎓 `ModelSelect`.

⚫️ 💪 ✍ `list` 🚮 🏬 ⏮️ `list(some_user.items)`.

✋️ 🎚 ⚫️ 🚫 `list`. &amp; ⚫️ 🚫 ☑ 🐍 <a href="https://docs.python.org/3/glossary.html#term-generator" class="external-link" target="_blank">🚂</a>. ↩️ 👉, Pydantic 🚫 💭 🔢 ❔ 🗜 ⚫️ `list` Pydantic *🏷* / 🔗.

✋️ ⏮️ ⏬ Pydantic ✔ 🚚 🛃 🎓 👈 😖 ⚪️➡️ `pydantic.utils.GetterDict`, 🚚 🛠️ ⚙️ 🕐❔ ⚙️ `orm_mode = True` 🗃 💲 🐜 🏷 🔢.

👥 🔜 ✍ 🛃 `PeeweeGetterDict` 🎓 &amp; ⚙️ ⚫️ 🌐 🎏 Pydantic *🏷* / 🔗 👈 ⚙️ `orm_mode`:

```Python hl_lines="3  8-13  31  49"
{!../../../docs_src/sql_databases_peewee/sql_app/schemas.py!}
```

📥 👥 ✅ 🚥 🔢 👈 ➖ 🔐 (✅ `.items` `some_user.items`) 👐 `peewee.ModelSelect`.

&amp; 🚥 👈 💼, 📨 `list` ⏮️ ⚫️.

&amp; ⤴️ 👥 ⚙️ ⚫️ Pydantic *🏷* / 🔗 👈 ⚙️ `orm_mode = True`, ⏮️ 📳 🔢 `getter_dict = PeeweeGetterDict`.

!!! tip
    👥 🕴 💪 ✍ 1️⃣ `PeeweeGetterDict` 🎓, &amp; 👥 💪 ⚙️ ⚫️ 🌐 Pydantic *🏷* / 🔗.

## 💩 🇨🇻

🔜 ➡️ 👀 📁 `sql_app/crud.py`.

### ✍ 🌐 💩 🇨🇻

✍ 🌐 🎏 💩 🇨🇻 🇸🇲 🔰, 🌐 📟 📶 🎏:

```Python hl_lines="1  4-5  8-9  12-13  16-20  23-24  27-30"
{!../../../docs_src/sql_databases_peewee/sql_app/crud.py!}
```

📤 🔺 ⏮️ 📟 🇸🇲 🔰.

👥 🚫 🚶‍♀️ `db` 🔢 🤭. ↩️ 👥 ⚙️ 🏷 🔗. 👉 ↩️ `db` 🎚 🌐 🎚, 👈 🔌 🌐 🔗 ⚛. 👈 ⚫️❔ 👥 ✔️ 🌐 `contextvars` ℹ 🔛.

🆖, 🕐❔ 🛬 📚 🎚, 💖 `get_users`, 👥 🔗 🤙 `list`, 💖:

```Python
list(models.User.select())
```

👉 🎏 🤔 👈 👥 ✔️ ✍ 🛃 `PeeweeGetterDict`. ✋️ 🛬 🕳 👈 ⏪ `list` ↩️ `peewee.ModelSelect` `response_model` *➡ 🛠️* ⏮️ `List[models.User]` (👈 👥 🔜 👀 ⏪) 🔜 👷 ☑.

## 👑 **FastAPI** 📱

&amp; 🔜 📁 `sql_app/main.py` ➡️ 🛠️ &amp; ⚙️ 🌐 🎏 🍕 👥 ✍ ⏭.

### ✍ 💽 🏓

📶 🙃 🌌 ✍ 💽 🏓:

```Python hl_lines="9-11"
{!../../../docs_src/sql_databases_peewee/sql_app/main.py!}
```

### ✍ 🔗

✍ 🔗 👈 🔜 🔗 💽 ▶️️ ▶️ 📨 &amp; 🔌 ⚫️ 🔚:

```Python hl_lines="23-29"
{!../../../docs_src/sql_databases_peewee/sql_app/main.py!}
```

📥 👥 ✔️ 🛁 `yield` ↩️ 👥 🤙 🚫 ⚙️ 💽 🎚 🔗.

⚫️ 🔗 💽 &amp; ♻ 🔗 💽 🔗 🔢 👈 🔬 🔠 📨 (⚙️ `contextvars` 🎱 ⚪️➡️ 🔛).

↩️ 💽 🔗 ⚠ 👤/🅾 🚧, 👉 🔗 ✍ ⏮️ 😐 `def` 🔢.

&amp; ⤴️, 🔠 *➡ 🛠️ 🔢* 👈 💪 🔐 💽 👥 🚮 ⚫️ 🔗.

✋️ 👥 🚫 ⚙️ 💲 👐 👉 🔗 (⚫️ 🤙 🚫 🤝 🙆 💲, ⚫️ ✔️ 🛁 `yield`). , 👥 🚫 🚮 ⚫️ *➡ 🛠️ 🔢* ✋️ *➡ 🛠️ 👨‍🎨* `dependencies` 🔢:

```Python hl_lines="32  40  47  59  65  72"
{!../../../docs_src/sql_databases_peewee/sql_app/main.py!}
```

### 🔑 🔢 🎧-🔗

🌐 `contextvars` 🍕 👷, 👥 💪 ⚒ 💭 👥 ✔️ 🔬 💲 `ContextVar` 🔠 📨 👈 ⚙️ 💽, &amp; 👈 💲 🔜 ⚙️ 💽 🇵🇸 (🔗, 💵, ♒️) 🎂 📨.

👈, 👥 💪 ✍ ➕1️⃣ `async` 🔗 `reset_db_state()` 👈 ⚙️ 🎧-🔗 `get_db()`. ⚫️ 🔜 ⚒ 💲 🔑 🔢 (⏮️ 🔢 `dict`) 👈 🔜 ⚙️ 💽 🇵🇸 🎂 📨. &amp; ⤴️ 🔗 `get_db()` 🔜 🏪 ⚫️ 💽 🇵🇸 (🔗, 💵, ♒️).

```Python hl_lines="18-20"
{!../../../docs_src/sql_databases_peewee/sql_app/main.py!}
```

**⏭ 📨**, 👥 🔜 ⏲ 👈 🔑 🔢 🔄 `async` 🔗 `reset_db_state()` &amp; ⤴️ ✍ 🆕 🔗 `get_db()` 🔗, 👈 🆕 📨 🔜 ✔️ 🚮 👍 💽 🇵🇸 (🔗, 💵, ♒️).

!!! tip
    FastAPI 🔁 🛠️, 1️⃣ 📨 💪 ▶️ ➖ 🛠️, &amp; ⏭ 🏁, ➕1️⃣ 📨 💪 📨 &amp; ▶️ 🏭 👍, &amp; ⚫️ 🌐 💪 🛠️ 🎏 🧵.

    ✋️ 🔑 🔢 🤔 👫 🔁 ⚒,, 🏒 💽 🇵🇸 ⚒ `async` 🔗 `reset_db_state()` 🔜 🚧 🚮 👍 💽 🎂 🎂 📨.

     &amp; 🎏 🕰, 🎏 🛠️ 📨 🔜 ✔️ 🚮 👍 💽 🇵🇸 👈 🔜 🔬 🎂 📨.

#### 🏒 🗳

🚥 👆 ⚙️ <a href="https://docs.peewee-orm.com/en/latest/peewee/database.html#dynamically-defining-a-database" class="external-link" target="_blank">🏒 🗳</a>, ☑ 💽 `db.obj`.

, 👆 🔜 ⏲ ⚫️ ⏮️:

```Python hl_lines="3-4"
async def reset_db_state():
    database.db.obj._state._state.set(db_state_default.copy())
    database.db.obj._state.reset()
```

### ✍ 👆 **FastAPI** *➡ 🛠️*

🔜, 😒, 📥 🐩 **FastAPI** *➡ 🛠️* 📟.

```Python hl_lines="32-37  40-43  46-53  56-62  65-68  71-79"
{!../../../docs_src/sql_databases_peewee/sql_app/main.py!}
```

### 🔃 `def` 🆚 `async def`

🎏 ⏮️ 🇸🇲, 👥 🚫 🔨 🕳 💖:

```Python
user = await models.User.select().first()
```

...✋️ ↩️ 👥 ⚙️:

```Python
user = models.User.select().first()
```

, 🔄, 👥 🔜 📣 *➡ 🛠️ 🔢* &amp; 🔗 🍵 `async def`, ⏮️ 😐 `def`,:

```Python hl_lines="2"
# Something goes here
def read_users(skip: int = 0, limit: int = 100):
    # Something goes here
```

## 🔬 🏒 ⏮️ 🔁

👉 🖼 🔌 ➕ *➡ 🛠️* 👈 🔬 📏 🏭 📨 ⏮️ `time.sleep(sleep_time)`.

⚫️ 🔜 ✔️ 💽 🔗 📂 ▶️ &amp; 🔜 ⌛ 🥈 ⏭ 🙇 🔙. &amp; 🔠 🆕 📨 🔜 ⌛ 🕐 🥈 🌘.

👉 🔜 💪 ➡️ 👆 💯 👈 👆 📱 ⏮️ 🏒 &amp; FastAPI 🎭 ☑ ⏮️ 🌐 💩 🔃 🧵.

🚥 👆 💚 ✅ ❔ 🏒 🔜 💔 👆 📱 🚥 ⚙️ 🍵 🛠️, 🚶 `sql_app/database.py` 📁 &amp; 🏤 ⏸:

```Python
# db._state = PeeweeConnectionState()
```

&amp; 📁 `sql_app/main.py` 📁, 🏤 💪 `async` 🔗 `reset_db_state()` &amp; ❎ ⚫️ ⏮️ `pass`:

```Python
async def reset_db_state():
#     database.db._state._state.set(db_state_default.copy())
#     database.db._state.reset()
    pass
```

⤴️ 🏃 👆 📱 ⏮️ Uvicorn:

<div class="termy">

```console
$ uvicorn sql_app.main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

📂 👆 🖥 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> &amp; ✍ 👩‍❤‍👨 👩‍💻.

⤴️ 📂 1️⃣0️⃣ 📑 <a href="http://127.0.0.1:8000/docs#/default/read_slow_users_slowusers__get" class="external-link" target="_blank">http://127.0.0.1:8000/docs#/default/read_🐌_👩‍💻_slowusers_ = </a> 🎏 🕰.

🚶 *➡ 🛠️* "🤚 `/slowusers/`" 🌐 📑. ⚙️ "🔄 ⚫️ 👅" 🔼 &amp; 🛠️ 📨 🔠 📑, 1️⃣ ▶️️ ⏮️ 🎏.

📑 🔜 ⌛ 🍖 &amp; ⤴️ 👫 🔜 🎦 `Internal Server Error`.

### ⚫️❔ 🔨

🥇 📑 🔜 ⚒ 👆 📱 ✍ 🔗 💽 &amp; ⌛ 🥈 ⏭ 🙇 🔙 &amp; 📪 💽 🔗.

⤴️, 📨 ⏭ 📑, 👆 📱 🔜 ⌛ 🕐 🥈 🌘, &amp; 🔛.

👉 ⛓ 👈 ⚫️ 🔜 🔚 🆙 🏁 🏁 📑' 📨 ⏪ 🌘 ⏮️ 🕐.

⤴️ 1️⃣ 🏁 📨 👈 ⌛ 🌘 🥈 🔜 🔄 📂 💽 🔗, ✋️ 1️⃣ 📚 ⏮️ 📨 🎏 📑 🔜 🎲 🍵 🎏 🧵 🥇 🕐, ⚫️ 🔜 ✔️ 🎏 💽 🔗 👈 ⏪ 📂, &amp; 🏒 🔜 🚮 ❌ &amp; 👆 🔜 👀 ⚫️ 📶, &amp; 📨 🔜 ✔️ `Internal Server Error`.

👉 🔜 🎲 🔨 🌅 🌘 1️⃣ 📚 📑.

🚥 👆 ✔️ 💗 👩‍💻 💬 👆 📱 ⚫️❔ 🎏 🕰, 👉 ⚫️❔ 💪 🔨.

&amp; 👆 📱 ▶️ 🍵 🌅 &amp; 🌖 👩‍💻 🎏 🕰, ⌛ 🕰 👁 📨 💪 📏 &amp; 📏 ⏲ ❌.

### 🔧 🏒 ⏮️ FastAPI

🔜 🚶 🔙 📁 `sql_app/database.py`, &amp; ✍ ⏸:

```Python
db._state = PeeweeConnectionState()
```

&amp; 📁 `sql_app/main.py` 📁, ✍ 💪 `async` 🔗 `reset_db_state()`:

```Python
async def reset_db_state():
    database.db._state._state.set(db_state_default.copy())
    database.db._state.reset()
```

❎ 👆 🏃‍♂ 📱 &amp; ▶️ ⚫️ 🔄.

🔁 🎏 🛠️ ⏮️ 1️⃣0️⃣ 📑. 👉 🕰 🌐 👫 🔜 ⌛ &amp; 👆 🔜 🤚 🌐 🏁 🍵 ❌.

...👆 🔧 ⚫️ ❗

## 📄 🌐 📁

 💭 👆 🔜 ✔️ 📁 📛 `my_super_project` (⚖️ 👐 👆 💚) 👈 🔌 🎧-📁 🤙 `sql_app`.

`sql_app` 🔜 ✔️ 📄 📁:

* `sql_app/__init__.py`: 🛁 📁.

* `sql_app/database.py`:

```Python
{!../../../docs_src/sql_databases_peewee/sql_app/database.py!}
```

* `sql_app/models.py`:

```Python
{!../../../docs_src/sql_databases_peewee/sql_app/models.py!}
```

* `sql_app/schemas.py`:

```Python
{!../../../docs_src/sql_databases_peewee/sql_app/schemas.py!}
```

* `sql_app/crud.py`:

```Python
{!../../../docs_src/sql_databases_peewee/sql_app/crud.py!}
```

* `sql_app/main.py`:

```Python
{!../../../docs_src/sql_databases_peewee/sql_app/main.py!}
```

## 📡 ℹ

!!! warning
    👉 📶 📡 ℹ 👈 👆 🎲 🚫 💪.

### ⚠

🏒 ⚙️ <a href="https://docs.python.org/3/library/threading.html#thread-local-data" class="external-link" target="_blank">`threading.local`</a> 🔢 🏪 ⚫️ 💽 "🇵🇸" 💽 (🔗, 💵, ♒️).

`threading.local` ✍ 💲 🌟 ⏮️ 🧵, ✋️ 🔁 🛠️ 🔜 🏃 🌐 📟 (✅ 🔠 📨) 🎏 🧵, &amp; 🎲 🚫 ✔.

🔛 🔝 👈, 🔁 🛠️ 💪 🏃 🔁 📟 🧵 (⚙️ `asyncio.run_in_executor`), ✋️ 🔗 🎏 📨.

👉 ⛓ 👈, ⏮️ 🏒 ⏮️ 🛠️, 💗 📋 💪 ⚙️ 🎏 `threading.local` 🔢 &amp; 🔚 🆙 🤝 🎏 🔗 &amp; 💽 (👈 👫 🚫🔜 🚫), &amp; 🎏 🕰, 🚥 👫 🛠️ 🔁 👤/🅾-🚧 📟 🧵 (⏮️ 😐 `def` 🔢 FastAPI, *➡ 🛠️* &amp; 🔗), 👈 📟 🏆 🚫 ✔️ 🔐 💽 🇵🇸 🔢, ⏪ ⚫️ 🍕 🎏 📨 &amp; ⚫️ 🔜 💪 🤚 🔐 🎏 💽 🇵🇸.

### 🔑 🔢

🐍 3️⃣.7️⃣ ✔️ <a href="https://docs.python.org/3/library/contextvars.html" class="external-link" target="_blank">`contextvars`</a> 👈 💪 ✍ 🇧🇿 🔢 📶 🎏 `threading.local`, ✋️ 🔗 👫 🔁 ⚒.

📤 📚 👜 ✔️ 🤯.

`ContextVar` ✔️ ✍ 🔝 🕹, 💖:

```Python
some_var = ContextVar("some_var", default="default value")
```

⚒ 💲 ⚙️ ⏮️ "🔑" (✅ ⏮️ 📨) ⚙️:

```Python
some_var.set("new value")
```

🤚 💲 🙆 🔘 🔑 (✅ 🙆 🍕 🚚 ⏮️ 📨) ⚙️:

```Python
some_var.get()
```

### ⚒ 🔑 🔢 `async` 🔗 `reset_db_state()`

🚥 🍕 🔁 📟 ⚒ 💲 ⏮️ `some_var.set("updated in function")` (✅ 💖 `async` 🔗), 🎂 📟 ⚫️ &amp; 📟 👈 🚶 ⏮️ (✅ 📟 🔘 `async` 🔢 🤙 ⏮️ `await`) 🔜 👀 👈 🆕 💲.

, 👆 💼, 🚥 👥 ⚒ 🏒 🇵🇸 🔢 (⏮️ 🔢 `dict`) `async` 🔗, 🌐 🎂 🔗 📟 👆 📱 🔜 👀 👉 💲 &amp; 🔜 💪 ♻ ⚫️ 🎂 📨.

&amp; 🔑 🔢 🔜 ⚒ 🔄 ⏭ 📨, 🚥 👫 🛠️.

### ⚒ 💽 🇵🇸 🔗 `get_db()`

`get_db()` 😐 `def` 🔢, **FastAPI** 🔜 ⚒ ⚫️ 🏃 🧵, ⏮️ *📁* "🔑", 🧑‍🤝‍🧑 🎏 💲 🔑 🔢 ( `dict` ⏮️ ⏲ 💽 🇵🇸). ⤴️ ⚫️ 💪 🚮 💽 🇵🇸 👈 `dict`, 💖 🔗, ♒️.

✋️ 🚥 💲 🔑 🔢 (🔢 `dict`) ⚒ 👈 😐 `def` 🔢, ⚫️ 🔜 ✍ 🆕 💲 👈 🔜 🚧 🕴 👈 🧵 🧵, &amp; 🎂 📟 (💖 *➡ 🛠️ 🔢*) 🚫🔜 ✔️ 🔐 ⚫️. `get_db()` 👥 💪 🕴 ⚒ 💲 `dict`, ✋️ 🚫 🎂 `dict` ⚫️.

, 👥 💪 ✔️ `async` 🔗 `reset_db_state()` ⚒ `dict` 🔑 🔢. 👈 🌌, 🌐 📟 ✔️ 🔐 🎏 `dict` 💽 🇵🇸 👁 📨.

### 🔗 &amp; 🔌 🔗 `get_db()`

⤴️ ⏭ ❔ 🔜, ⚫️❔ 🚫 🔗 &amp; 🔌 💽 `async` 🔗 ⚫️, ↩️ `get_db()`❓

`async` 🔗 ✔️ `async` 🔑 🔢 🛡 🎂 📨, ✋️ 🏗 &amp; 📪 💽 🔗 ⚠ 🚧, ⚫️ 💪 📉 🎭 🚥 ⚫️ 📤.

👥 💪 😐 `def` 🔗 `get_db()`.
