# 💪 - 🔁 🏷

⏮️ **FastAPI**, 👆 💪 🔬, ✔, 📄, &amp; ⚙️ 🎲 🙇 🐦 🏷 (👏 Pydantic).

## 📇 🏑

👆 💪 🔬 🔢 🏾. 🖼, 🐍 `list`:

{* ../../docs_src/body_nested_models/tutorial001.py hl[14] *}

👉 🔜 ⚒ `tags` 📇, 👐 ⚫️ 🚫 📣 🆎 🔣 📇.

## 📇 🏑 ⏮️ 🆎 🔢

✋️ 🐍 ✔️ 🎯 🌌 📣 📇 ⏮️ 🔗 🆎, ⚖️ "🆎 🔢":

### 🗄 ⌨ `List`

🐍 3️⃣.9️⃣ &amp; 🔛 👆 💪 ⚙️ 🐩 `list` 📣 👫 🆎 ✍ 👥 🔜 👀 🔛. 👶

✋️ 🐍 ⏬ ⏭ 3️⃣.9️⃣ (3️⃣.6️⃣ &amp; 🔛), 👆 🥇 💪 🗄 `List` ⚪️➡️ 🐩 🐍 `typing` 🕹:

{* ../../docs_src/body_nested_models/tutorial002.py hl[1] *}

### 📣 `list` ⏮️ 🆎 🔢

📣 🆎 👈 ✔️ 🆎 🔢 (🔗 🆎), 💖 `list`, `dict`, `tuple`:

* 🚥 👆 🐍 ⏬ 🔅 🌘 3️⃣.9️⃣, 🗄 👫 🌓 ⏬ ⚪️➡️ `typing` 🕹
* 🚶‍♀️ 🔗 🆎(Ⓜ) "🆎 🔢" ⚙️ ⬜ 🗜: `[` &amp; `]`

🐍 3️⃣.9️⃣ ⚫️ 🔜:

```Python
my_list: list[str]
```

⏬ 🐍 ⏭ 3️⃣.9️⃣, ⚫️ 🔜:

```Python
from typing import List

my_list: List[str]
```

👈 🌐 🐩 🐍 ❕ 🆎 📄.

⚙️ 👈 🎏 🐩 ❕ 🏷 🔢 ⏮️ 🔗 🆎.

, 👆 🖼, 👥 💪 ⚒ `tags` 🎯 "📇 🎻":

{* ../../docs_src/body_nested_models/tutorial002.py hl[14] *}

## ⚒ 🆎

✋️ ⤴️ 👥 💭 🔃 ⚫️, &amp; 🤔 👈 🔖 🚫🔜 🚫 🔁, 👫 🔜 🎲 😍 🎻.

&amp; 🐍 ✔️ 🎁 💽 🆎 ⚒ 😍 🏬, `set`.

⤴️ 👥 💪 📣 `tags` ⚒ 🎻:

{* ../../docs_src/body_nested_models/tutorial003.py hl[1,14] *}

⏮️ 👉, 🚥 👆 📨 📨 ⏮️ ❎ 📊, ⚫️ 🔜 🗜 ⚒ 😍 🏬.

&amp; 🕐❔ 👆 🔢 👈 📊, 🚥 ℹ ✔️ ❎, ⚫️ 🔜 🔢 ⚒ 😍 🏬.

&amp; ⚫️ 🔜 ✍ / 📄 ➡️ 💁‍♂️.

## 🐦 🏷

🔠 🔢 Pydantic 🏷 ✔️ 🆎.

✋️ 👈 🆎 💪 ⚫️ ➕1️⃣ Pydantic 🏷.

, 👆 💪 📣 🙇 🐦 🎻 "🎚" ⏮️ 🎯 🔢 📛, 🆎 &amp; 🔬.

🌐 👈, 🎲 🐦.

### 🔬 📊

🖼, 👥 💪 🔬 `Image` 🏷:

{* ../../docs_src/body_nested_models/tutorial004.py hl[9:11] *}

### ⚙️ 📊 🆎

&amp; ⤴️ 👥 💪 ⚙️ ⚫️ 🆎 🔢:

{* ../../docs_src/body_nested_models/tutorial004.py hl[20] *}

👉 🔜 ⛓ 👈 **FastAPI** 🔜 ⌛ 💪 🎏:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://example.com/baz.jpg",
        "name": "The Foo live"
    }
}
```

🔄, 🤸 👈 📄, ⏮️ **FastAPI** 👆 🤚:

* 👨‍🎨 🐕‍🦺 (🛠️, ♒️), 🐦 🏷
* 💽 🛠️
* 💽 🔬
* 🏧 🧾

## 🎁 🆎 &amp; 🔬

↖️ ⚪️➡️ 😐 ⭐ 🆎 💖 `str`, `int`, `float`, ♒️. 👆 💪 ⚙️ 🌅 🏗 ⭐ 🆎 👈 😖 ⚪️➡️ `str`.

👀 🌐 🎛 👆 ✔️, 🛒 🩺 <a href="https://docs.pydantic.dev/latest/concepts/types/" class="external-link" target="_blank">Pydantic 😍 🆎</a>. 👆 🔜 👀 🖼 ⏭ 📃.

🖼, `Image` 🏷 👥 ✔️ `url` 🏑, 👥 💪 📣 ⚫️ ↩️ `str`, Pydantic `HttpUrl`:

{* ../../docs_src/body_nested_models/tutorial005.py hl[4,10] *}

🎻 🔜 ✅ ☑ 📛, &amp; 📄 🎻 🔗 / 🗄 ✅.

## 🔢 ⏮️ 📇 📊

👆 💪 ⚙️ Pydantic 🏷 🏾 `list`, `set`, ♒️:

{* ../../docs_src/body_nested_models/tutorial006.py hl[20] *}

👉 🔜 ⌛ (🗜, ✔, 📄, ♒️) 🎻 💪 💖:

```JSON hl_lines="11"
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": [
        "rock",
        "metal",
        "bar"
    ],
    "images": [
        {
            "url": "http://example.com/baz.jpg",
            "name": "The Foo live"
        },
        {
            "url": "http://example.com/dave.jpg",
            "name": "The Baz"
        }
    ]
}
```

/// info

👀 ❔ `images` 🔑 🔜 ✔️ 📇 🖼 🎚.

///

## 🙇 🐦 🏷

👆 💪 🔬 🎲 🙇 🐦 🏷:

{* ../../docs_src/body_nested_models/tutorial007.py hl[9,14,20,23,27] *}

/// info

👀 ❔ `Offer` ✔️ 📇 `Item`Ⓜ, ❔ 🔄 ✔️ 📦 📇 `Image`Ⓜ

///

## 💪 😁 📇

🚥 🔝 🎚 💲 🎻 💪 👆 ⌛ 🎻 `array` (🐍 `list`), 👆 💪 📣 🆎 🔢 🔢, 🎏 Pydantic 🏷:

```Python
images: List[Image]
```

⚖️ 🐍 3️⃣.9️⃣ &amp; 🔛:

```Python
images: list[Image]
```

:

{* ../../docs_src/body_nested_models/tutorial008.py hl[15] *}

## 👨‍🎨 🐕‍🦺 🌐

&amp; 👆 🤚 👨‍🎨 🐕‍🦺 🌐.

🏬 🔘 📇:

<img src="/img/tutorial/body-nested-models/image01.png">

👆 🚫 🚫 🤚 👉 😇 👨‍🎨 🐕‍🦺 🚥 👆 👷 🔗 ⏮️ `dict` ↩️ Pydantic 🏷.

✋️ 👆 🚫 ✔️ 😟 🔃 👫 👯‍♂️, 📨 #️⃣ 🗜 🔁 &amp; 👆 🔢 🗜 🔁 🎻 💁‍♂️.

## 💪 ❌ `dict`Ⓜ

👆 💪 📣 💪 `dict` ⏮️ 🔑 🆎 &amp; 💲 🎏 🆎.

🍵 ✔️ 💭 ⏪ ⚫️❔ ☑ 🏑/🔢 📛 (🔜 💼 ⏮️ Pydantic 🏷).

👉 🔜 ⚠ 🚥 👆 💚 📨 🔑 👈 👆 🚫 ⏪ 💭.

---

🎏 ⚠ 💼 🕐❔ 👆 💚 ✔️ 🔑 🎏 🆎, ✅ `int`.

👈 ⚫️❔ 👥 🔜 👀 📥.

👉 💼, 👆 🔜 🚫 🙆 `dict` 📏 ⚫️ ✔️ `int` 🔑 ⏮️ `float` 💲:

{* ../../docs_src/body_nested_models/tutorial009.py hl[9] *}

/// tip

✔️ 🤯 👈 🎻 🕴 🐕‍🦺 `str` 🔑.

✋️ Pydantic ✔️ 🏧 💽 🛠️.

👉 ⛓ 👈, ✋️ 👆 🛠️ 👩‍💻 💪 🕴 📨 🎻 🔑, 📏 👈 🎻 🔌 😁 🔢, Pydantic 🔜 🗜 👫 &amp; ✔ 👫.

 &amp; `dict` 👆 📨 `weights` 🔜 🤙 ✔️ `int` 🔑 &amp; `float` 💲.

///

## 🌃

⏮️ **FastAPI** 👆 ✔️ 🔆 💪 🚚 Pydantic 🏷, ⏪ 🚧 👆 📟 🙅, 📏 &amp; 😍.

✋️ ⏮️ 🌐 💰:

* 👨‍🎨 🐕‍🦺 (🛠️ 🌐 ❗)
* 💽 🛠️ (.Ⓜ.. ✍ / 🛠️)
* 💽 🔬
* 🔗 🧾
* 🏧 🩺
