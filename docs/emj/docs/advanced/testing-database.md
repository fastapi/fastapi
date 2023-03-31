# 🔬 💽

👆 💪 ⚙️ 🎏 🔗 🔐 ⚪️➡️ [🔬 🔗 ⏮️ 🔐](testing-dependencies.md){.internal-link target=_blank} 📉 💽 🔬.

👆 💪 💚 ⚒ 🆙 🎏 💽 🔬, 💾 💽 ⏮️ 💯, 🏤-🥧 ⚫️ ⏮️ 🔬 💽, ♒️.

👑 💭 ⚫️❔ 🎏 👆 👀 👈 ⏮️ 📃.

## 🚮 💯 🗄 📱

➡️ ℹ 🖼 ⚪️➡️ [🗄 (🔗) 💽](../tutorial/sql-databases.md){.internal-link target=_blank} ⚙️ 🔬 💽.

🌐 📱 📟 🎏, 👆 💪 🚶 🔙 👈 📃 ✅ ❔ ⚫️.

🕴 🔀 📥 🆕 🔬 📁.

👆 😐 🔗 `get_db()` 🔜 📨 💽 🎉.

💯, 👆 💪 ⚙️ 🔗 🔐 📨 👆 *🛃* 💽 🎉 ↩️ 1️⃣ 👈 🔜 ⚙️ 🛎.

👉 🖼 👥 🔜 ✍ 🍕 💽 🕴 💯.

## 📁 📊

👥 ✍ 🆕 📁 `sql_app/tests/test_sql_app.py`.

🆕 📁 📊 👀 💖:

``` hl_lines="9-11"
.
└── sql_app
    ├── __init__.py
    ├── crud.py
    ├── database.py
    ├── main.py
    ├── models.py
    ├── schemas.py
    └── tests
        ├── __init__.py
        └── test_sql_app.py
```

## ✍ 🆕 💽 🎉

🥇, 👥 ✍ 🆕 💽 🎉 ⏮️ 🆕 💽.

💯 👥 🔜 ⚙️ 📁 `test.db` ↩️ `sql_app.db`.

✋️ 🎂 🎉 📟 🌅 ⚖️ 🌘 🎏, 👥 📁 ⚫️.

```Python hl_lines="8-13"
{!../../../docs_src/sql_databases/sql_app/tests/test_sql_app.py!}
```

!!! tip
    👆 💪 📉 ❎ 👈 📟 🚮 ⚫️ 🔢 &amp; ⚙️ ⚫️ ⚪️➡️ 👯‍♂️ `database.py` &amp; `tests/test_sql_app.py`.

    🦁 &amp; 🎯 🔛 🎯 🔬 📟, 👥 🖨 ⚫️.

## ✍ 💽

↩️ 🔜 👥 🔜 ⚙️ 🆕 💽 🆕 📁, 👥 💪 ⚒ 💭 👥 ✍ 💽 ⏮️:

```Python
Base.metadata.create_all(bind=engine)
```

👈 🛎 🤙 `main.py`, ✋️ ⏸ `main.py` ⚙️ 💽 📁 `sql_app.db`, &amp; 👥 💪 ⚒ 💭 👥 ✍ `test.db` 💯.

👥 🚮 👈 ⏸ 📥, ⏮️ 🆕 📁.

```Python hl_lines="16"
{!../../../docs_src/sql_databases/sql_app/tests/test_sql_app.py!}
```

## 🔗 🔐

🔜 👥 ✍ 🔗 🔐 &amp; 🚮 ⚫️ 🔐 👆 📱.

```Python hl_lines="19-24  27"
{!../../../docs_src/sql_databases/sql_app/tests/test_sql_app.py!}
```

!!! tip
    📟 `override_get_db()` 🌖 ⚫️❔ 🎏 `get_db()`, ✋️ `override_get_db()` 👥 ⚙️ `TestingSessionLocal` 🔬 💽 ↩️.

## 💯 📱

⤴️ 👥 💪 💯 📱 🛎.

```Python hl_lines="32-47"
{!../../../docs_src/sql_databases/sql_app/tests/test_sql_app.py!}
```

&amp; 🌐 🛠️ 👥 ⚒ 💽 ⏮️ 💯 🔜 `test.db` 💽 ↩️ 👑 `sql_app.db`.
