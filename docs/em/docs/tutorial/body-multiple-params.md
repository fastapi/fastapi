# 💪 - 💗 🔢

🔜 👈 👥 ✔️ 👀 ❔ ⚙️ `Path` &amp; `Query`, ➡️ 👀 🌅 🏧 ⚙️ 📨 💪 📄.

## 🌀 `Path`, `Query` &amp; 💪 🔢

🥇, ↗️, 👆 💪 🌀 `Path`, `Query` &amp; 📨 💪 🔢 📄 ➡ &amp; **FastAPI** 🔜 💭 ⚫️❔.

&amp; 👆 💪 📣 💪 🔢 📦, ⚒ 🔢 `None`:

//// tab | 🐍 3️⃣.6️⃣ &amp; 🔛

```Python hl_lines="19-21"
{!> ../../../docs_src/body_multiple_params/tutorial001.py!}
```

////

//// tab | 🐍 3️⃣.1️⃣0️⃣ &amp; 🔛

```Python hl_lines="17-19"
{!> ../../../docs_src/body_multiple_params/tutorial001_py310.py!}
```

////

/// note

👀 👈, 👉 💼, `item` 👈 🔜 ✊ ⚪️➡️ 💪 📦. ⚫️ ✔️ `None` 🔢 💲.

///

## 💗 💪 🔢

⏮️ 🖼, *➡ 🛠️* 🔜 ⌛ 🎻 💪 ⏮️ 🔢 `Item`, 💖:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

✋️ 👆 💪 📣 💗 💪 🔢, ✅ `item` &amp; `user`:

//// tab | 🐍 3️⃣.6️⃣ &amp; 🔛

```Python hl_lines="22"
{!> ../../../docs_src/body_multiple_params/tutorial002.py!}
```

////

//// tab | 🐍 3️⃣.1️⃣0️⃣ &amp; 🔛

```Python hl_lines="20"
{!> ../../../docs_src/body_multiple_params/tutorial002_py310.py!}
```

////

👉 💼, **FastAPI** 🔜 👀 👈 📤 🌅 🌘 1️⃣ 💪 🔢 🔢 (2️⃣ 🔢 👈 Pydantic 🏷).

, ⚫️ 🔜 ⤴️ ⚙️ 🔢 📛 🔑 (🏑 📛) 💪, &amp; ⌛ 💪 💖:

```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    }
}
```

/// note

👀 👈 ✋️ `item` 📣 🎏 🌌 ⏭, ⚫️ 🔜 ⌛ 🔘 💪 ⏮️ 🔑 `item`.

///

**FastAPI** 🔜 🏧 🛠️ ⚪️➡️ 📨, 👈 🔢 `item` 📨 ⚫️ 🎯 🎚 &amp; 🎏 `user`.

⚫️ 🔜 🎭 🔬 ⚗ 💽, &amp; 🔜 📄 ⚫️ 💖 👈 🗄 🔗 &amp; 🏧 🩺.

## ⭐ 💲 💪

🎏 🌌 📤 `Query` &amp; `Path` 🔬 ➕ 💽 🔢 &amp; ➡ 🔢, **FastAPI** 🚚 🌓 `Body`.

🖼, ↔ ⏮️ 🏷, 👆 💪 💭 👈 👆 💚 ✔️ ➕1️⃣ 🔑 `importance` 🎏 💪, 🥈 `item` &amp; `user`.

🚥 👆 📣 ⚫️, ↩️ ⚫️ ⭐ 💲, **FastAPI** 🔜 🤔 👈 ⚫️ 🔢 🔢.

✋️ 👆 💪 💡 **FastAPI** 😥 ⚫️ ➕1️⃣ 💪 🔑 ⚙️ `Body`:

//// tab | 🐍 3️⃣.6️⃣ &amp; 🔛

```Python hl_lines="22"
{!> ../../../docs_src/body_multiple_params/tutorial003.py!}
```

////

//// tab | 🐍 3️⃣.1️⃣0️⃣ &amp; 🔛

```Python hl_lines="20"
{!> ../../../docs_src/body_multiple_params/tutorial003_py310.py!}
```

////

👉 💼, **FastAPI** 🔜 ⌛ 💪 💖:

```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    },
    "importance": 5
}
```

🔄, ⚫️ 🔜 🗜 📊 🆎, ✔, 📄, ♒️.

## 💗 💪 = &amp; 🔢

↗️, 👆 💪 📣 🌖 🔢 🔢 🕐❔ 👆 💪, 🌖 🙆 💪 🔢.

, 🔢, ⭐ 💲 🔬 🔢 🔢, 👆 🚫 ✔️ 🎯 🚮 `Query`, 👆 💪:

```Python
q: Union[str, None] = None
```

⚖️ 🐍 3️⃣.1️⃣0️⃣ &amp; 🔛:

```Python
q: str | None = None
```

🖼:

//// tab | 🐍 3️⃣.6️⃣ &amp; 🔛

```Python hl_lines="27"
{!> ../../../docs_src/body_multiple_params/tutorial004.py!}
```

////

//// tab | 🐍 3️⃣.1️⃣0️⃣ &amp; 🔛

```Python hl_lines="26"
{!> ../../../docs_src/body_multiple_params/tutorial004_py310.py!}
```

////

/// info

`Body` ✔️ 🌐 🎏 ➕ 🔬 &amp; 🗃 🔢 `Query`,`Path` &amp; 🎏 👆 🔜 👀 ⏪.

///

## ⏯ 👁 💪 🔢

➡️ 💬 👆 🕴 ✔️ 👁 `item` 💪 🔢 ⚪️➡️ Pydantic 🏷 `Item`.

🔢, **FastAPI** 🔜 ⤴️ ⌛ 🚮 💪 🔗.

✋️ 🚥 👆 💚 ⚫️ ⌛ 🎻 ⏮️ 🔑 `item` &amp; 🔘 ⚫️ 🏷 🎚, ⚫️ 🔨 🕐❔ 👆 📣 ➕ 💪 🔢, 👆 💪 ⚙️ 🎁 `Body` 🔢 `embed`:

```Python
item: Item = Body(embed=True)
```

:

//// tab | 🐍 3️⃣.6️⃣ &amp; 🔛

```Python hl_lines="17"
{!> ../../../docs_src/body_multiple_params/tutorial005.py!}
```

////

//// tab | 🐍 3️⃣.1️⃣0️⃣ &amp; 🔛

```Python hl_lines="15"
{!> ../../../docs_src/body_multiple_params/tutorial005_py310.py!}
```

////

👉 💼 **FastAPI** 🔜 ⌛ 💪 💖:

```JSON hl_lines="2"
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
}
```

↩️:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

## 🌃

👆 💪 🚮 💗 💪 🔢 👆 *➡ 🛠️ 🔢*, ✋️ 📨 💪 🕴 ✔️ 👁 💪.

✋️ **FastAPI** 🔜 🍵 ⚫️, 🤝 👆 ☑ 📊 👆 🔢, &amp; ✔ &amp; 📄 ☑ 🔗 *➡ 🛠️*.

👆 💪 📣 ⭐ 💲 📨 🍕 💪.

&amp; 👆 💪 💡 **FastAPI** ⏯ 💪 🔑 🕐❔ 📤 🕴 👁 🔢 📣.
