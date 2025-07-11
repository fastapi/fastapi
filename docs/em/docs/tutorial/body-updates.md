# 💪 - ℹ

## ℹ ❎ ⏮️ `PUT`

ℹ 🏬 👆 💪 ⚙️ <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT" class="external-link" target="_blank">🇺🇸🔍 `PUT`</a> 🛠️.

👆 💪 ⚙️ `jsonable_encoder` 🗜 🔢 💽 📊 👈 💪 🏪 🎻 (✅ ⏮️ ☁ 💽). 🖼, 🏭 `datetime` `str`.

{* ../../docs_src/body_updates/tutorial001.py hl[30:35] *}

`PUT` ⚙️ 📨 💽 👈 🔜 ❎ ♻ 💽.

### ⚠ 🔃 ❎

👈 ⛓ 👈 🚥 👆 💚 ℹ 🏬 `bar` ⚙️ `PUT` ⏮️ 💪 ⚗:

```Python
{
    "name": "Barz",
    "price": 3,
    "description": None,
}
```

↩️ ⚫️ 🚫 🔌 ⏪ 🏪 🔢 `"tax": 20.2`, 🔢 🏷 🔜 ✊ 🔢 💲 `"tax": 10.5`.

&amp; 📊 🔜 🖊 ⏮️ 👈 "🆕" `tax` `10.5`.

## 🍕 ℹ ⏮️ `PATCH`

👆 💪 ⚙️ <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH" class="external-link" target="_blank">🇺🇸🔍 `PATCH`</a> 🛠️ *🍕* ℹ 💽.

👉 ⛓ 👈 👆 💪 📨 🕴 💽 👈 👆 💚 ℹ, 🍂 🎂 🐣.

/// note

`PATCH` 🌘 🛎 ⚙️ &amp; 💭 🌘 `PUT`.

 &amp; 📚 🏉 ⚙️ 🕴 `PUT`, 🍕 ℹ.

👆 **🆓** ⚙️ 👫 👐 👆 💚, **FastAPI** 🚫 🚫 🙆 🚫.

✋️ 👉 🦮 🎦 👆, 🌖 ⚖️ 🌘, ❔ 👫 🎯 ⚙️.

///

### ⚙️ Pydantic `exclude_unset` 🔢

🚥 👆 💚 📨 🍕 ℹ, ⚫️ 📶 ⚠ ⚙️ 🔢 `exclude_unset` Pydantic 🏷 `.dict()`.

💖 `item.dict(exclude_unset=True)`.

👈 🔜 🏗 `dict` ⏮️ 🕴 💽 👈 ⚒ 🕐❔ 🏗 `item` 🏷, 🚫 🔢 💲.

⤴️ 👆 💪 ⚙️ 👉 🏗 `dict` ⏮️ 🕴 💽 👈 ⚒ (📨 📨), 🚫 🔢 💲:

{* ../../docs_src/body_updates/tutorial002.py hl[34] *}

### ⚙️ Pydantic `update` 🔢

🔜, 👆 💪 ✍ 📁 ♻ 🏷 ⚙️ `.copy()`, &amp; 🚶‍♀️ `update` 🔢 ⏮️ `dict` ⚗ 💽 ℹ.

💖 `stored_item_model.copy(update=update_data)`:

{* ../../docs_src/body_updates/tutorial002.py hl[35] *}

### 🍕 ℹ 🌃

📄, ✔ 🍕 ℹ 👆 🔜:

* (⚗) ⚙️ `PATCH` ↩️ `PUT`.
* 🗃 🏪 💽.
* 🚮 👈 💽 Pydantic 🏷.
* 🏗 `dict` 🍵 🔢 💲 ⚪️➡️ 🔢 🏷 (⚙️ `exclude_unset`).
    * 👉 🌌 👆 💪 ℹ 🕴 💲 🤙 ⚒ 👩‍💻, ↩️ 🔐 💲 ⏪ 🏪 ⏮️ 🔢 💲 👆 🏷.
* ✍ 📁 🏪 🏷, 🛠️ ⚫️ 🔢 ⏮️ 📨 🍕 ℹ (⚙️ `update` 🔢).
* 🗜 📁 🏷 🕳 👈 💪 🏪 👆 💽 (🖼, ⚙️ `jsonable_encoder`).
    * 👉 ⭐ ⚙️ 🏷 `.dict()` 👩‍🔬 🔄, ✋️ ⚫️ ⚒ 💭 (&amp; 🗜) 💲 💽 🆎 👈 💪 🗜 🎻, 🖼, `datetime` `str`.
* 🖊 💽 👆 💽.
* 📨 ℹ 🏷.

{* ../../docs_src/body_updates/tutorial002.py hl[30:37] *}

/// tip

👆 💪 🤙 ⚙️ 👉 🎏 ⚒ ⏮️ 🇺🇸🔍 `PUT` 🛠️.

✋️ 🖼 📥 ⚙️ `PATCH` ↩️ ⚫️ ✍ 👫 ⚙️ 💼.

///

/// note

👀 👈 🔢 🏷 ✔.

, 🚥 👆 💚 📨 🍕 ℹ 👈 💪 🚫 🌐 🔢, 👆 💪 ✔️ 🏷 ⏮️ 🌐 🔢 ™ 📦 (⏮️ 🔢 💲 ⚖️ `None`).

🔬 ⚪️➡️ 🏷 ⏮️ 🌐 📦 💲 **ℹ** &amp; 🏷 ⏮️ ✔ 💲 **🏗**, 👆 💪 ⚙️ 💭 🔬 [➕ 🏷](extra-models.md){.internal-link target=_blank}.

///
