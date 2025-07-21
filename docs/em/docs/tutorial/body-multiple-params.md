# 💪 - 💗 🔢

🔜 👈 👥 ✔️ 👀 ❔ ⚙️ `Path` &amp; `Query`, ➡️ 👀 🌅 🏧 ⚙️ 📨 💪 📄.

## 🌀 `Path`, `Query` &amp; 💪 🔢

🥇, ↗️, 👆 💪 🌀 `Path`, `Query` &amp; 📨 💪 🔢 📄 ➡ &amp; **FastAPI** 🔜 💭 ⚫️❔.

&amp; 👆 💪 📣 💪 🔢 📦, ⚒ 🔢 `None`:

{* ../../docs_src/body_multiple_params/tutorial001.py hl[19:21] *}

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

{* ../../docs_src/body_multiple_params/tutorial002.py hl[22] *}

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

{* ../../docs_src/body_multiple_params/tutorial003.py hl[22] *}

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

{* ../../docs_src/body_multiple_params/tutorial004.py hl[27] *}

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

{* ../../docs_src/body_multiple_params/tutorial005.py hl[17] *}

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
