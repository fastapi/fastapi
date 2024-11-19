# 📨 🏷 - 📨 🆎

👆 💪 📣 🆎 ⚙️ 📨 ✍ *➡ 🛠️ 🔢* **📨 🆎**.

👆 💪 ⚙️ **🆎 ✍** 🎏 🌌 👆 🔜 🔢 💽 🔢 **🔢**, 👆 💪 ⚙️ Pydantic 🏷, 📇, 📖, 📊 💲 💖 🔢, 🎻, ♒️.

{* ../../docs_src/response_model/tutorial001_01.py hl[18,23] *}

FastAPI 🔜 ⚙️ 👉 📨 🆎:

* **✔** 📨 💽.
    * 🚥 💽 ❌ (✅ 👆 ❌ 🏑), ⚫️ ⛓ 👈 *👆* 📱 📟 💔, 🚫 🛬 ⚫️❔ ⚫️ 🔜, &amp; ⚫️ 🔜 📨 💽 ❌ ↩️ 🛬 ❌ 💽. 👉 🌌 👆 &amp; 👆 👩‍💻 💪 🎯 👈 👫 🔜 📨 💽 &amp; 💽 💠 📈.
* 🚮 **🎻 🔗** 📨, 🗄 *➡ 🛠️*.
    * 👉 🔜 ⚙️ **🏧 🩺**.
    * ⚫️ 🔜 ⚙️ 🏧 👩‍💻 📟 ⚡ 🧰.

✋️ 🏆 🥈:

* ⚫️ 🔜 **📉 &amp; ⛽** 🔢 📊 ⚫️❔ 🔬 📨 🆎.
    * 👉 ✴️ ⚠ **💂‍♂**, 👥 🔜 👀 🌅 👈 🔛.

## `response_model` 🔢

📤 💼 🌐❔ 👆 💪 ⚖️ 💚 📨 💽 👈 🚫 ⚫️❔ ⚫️❔ 🆎 📣.

🖼, 👆 💪 💚 **📨 📖** ⚖️ 💽 🎚, ✋️ **📣 ⚫️ Pydantic 🏷**. 👉 🌌 Pydantic 🏷 🔜 🌐 💽 🧾, 🔬, ♒️. 🎚 👈 👆 📨 (✅ 📖 ⚖️ 💽 🎚).

🚥 👆 🚮 📨 🆎 ✍, 🧰 &amp; 👨‍🎨 🔜 😭 ⏮️ (☑) ❌ 💬 👆 👈 👆 🔢 🛬 🆎 (✅#️⃣) 👈 🎏 ⚪️➡️ ⚫️❔ 👆 📣 (✅ Pydantic 🏷).

📚 💼, 👆 💪 ⚙️ *➡ 🛠️ 👨‍🎨* 🔢 `response_model` ↩️ 📨 🆎.

👆 💪 ⚙️ `response_model` 🔢 🙆 *➡ 🛠️*:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* ♒️.

{* ../../docs_src/response_model/tutorial001.py hl[17,22,24:27] *}

/// note

👀 👈 `response_model` 🔢 "👨‍🎨" 👩‍🔬 (`get`, `post`, ♒️). 🚫 👆 *➡ 🛠️ 🔢*, 💖 🌐 🔢 &amp; 💪.

///

`response_model` 📨 🎏 🆎 👆 🔜 📣 Pydantic 🏷 🏑,, ⚫️ 💪 Pydantic 🏷, ✋️ ⚫️ 💪, ✅ `list` Pydantic 🏷, 💖 `List[Item]`.

FastAPI 🔜 ⚙️ 👉 `response_model` 🌐 💽 🧾, 🔬, ♒️. &amp; **🗜 &amp; ⛽ 🔢 📊** 🚮 🆎 📄.

/// tip

🚥 👆 ✔️ ⚠ 🆎 ✅ 👆 👨‍🎨, ✍, ♒️, 👆 💪 📣 🔢 📨 🆎 `Any`.

👈 🌌 👆 💬 👨‍🎨 👈 👆 😫 🛬 🕳. ✋️ FastAPI 🔜 💽 🧾, 🔬, 🖥, ♒️. ⏮️ `response_model`.

///

### `response_model` 📫

🚥 👆 📣 👯‍♂️ 📨 🆎 &amp; `response_model`, `response_model` 🔜 ✊ 📫 &amp; ⚙️ FastAPI.

👉 🌌 👆 💪 🚮 ☑ 🆎 ✍ 👆 🔢 🕐❔ 👆 🛬 🆎 🎏 🌘 📨 🏷, ⚙️ 👨‍🎨 &amp; 🧰 💖 ✍. &amp; 👆 💪 ✔️ FastAPI 💽 🔬, 🧾, ♒️. ⚙️ `response_model`.

👆 💪 ⚙️ `response_model=None` ❎ 🏗 📨 🏷 👈 *➡ 🛠️*, 👆 5️⃣📆 💪 ⚫️ 🚥 👆 ❎ 🆎 ✍ 👜 👈 🚫 ☑ Pydantic 🏑, 👆 🔜 👀 🖼 👈 1️⃣ 📄 🔛.

## 📨 🎏 🔢 💽

📥 👥 📣 `UserIn` 🏷, ⚫️ 🔜 🔌 🔢 🔐:

{* ../../docs_src/response_model/tutorial002.py hl[9,11] *}

/// info

⚙️ `EmailStr`, 🥇 ❎ <a href="https://github.com/JoshData/python-email-validator" class="external-link" target="_blank">`email-validator`</a>.

🤶 Ⓜ. `pip install email-validator`
⚖️ `pip install pydantic[email]`.

///

&amp; 👥 ⚙️ 👉 🏷 📣 👆 🔢 &amp; 🎏 🏷 📣 👆 🔢:

{* ../../docs_src/response_model/tutorial002.py hl[18] *}

🔜, 🕐❔ 🖥 🏗 👩‍💻 ⏮️ 🔐, 🛠️ 🔜 📨 🎏 🔐 📨.

👉 💼, ⚫️ 💪 🚫 ⚠, ↩️ ⚫️ 🎏 👩‍💻 📨 🔐.

✋️ 🚥 👥 ⚙️ 🎏 🏷 ➕1️⃣ *➡ 🛠️*, 👥 💪 📨 👆 👩‍💻 🔐 🔠 👩‍💻.

/// danger

🙅 🏪 ✅ 🔐 👩‍💻 ⚖️ 📨 ⚫️ 📨 💖 👉, 🚥 👆 💭 🌐 ⚠ &amp; 👆 💭 ⚫️❔ 👆 🔨.

///

## 🚮 🔢 🏷

👥 💪 ↩️ ✍ 🔢 🏷 ⏮️ 🔢 🔐 &amp; 🔢 🏷 🍵 ⚫️:

{* ../../docs_src/response_model/tutorial003.py hl[9,11,16] *}

📥, ✋️ 👆 *➡ 🛠️ 🔢* 🛬 🎏 🔢 👩‍💻 👈 🔌 🔐:

{* ../../docs_src/response_model/tutorial003.py hl[24] *}

...👥 📣 `response_model` 👆 🏷 `UserOut`, 👈 🚫 🔌 🔐:

{* ../../docs_src/response_model/tutorial003.py hl[22] *}

, **FastAPI** 🔜 ✊ 💅 🖥 👅 🌐 💽 👈 🚫 📣 🔢 🏷 (⚙️ Pydantic).

### `response_model` ⚖️ 📨 🆎

👉 💼, ↩️ 2️⃣ 🏷 🎏, 🚥 👥 ✍ 🔢 📨 🆎 `UserOut`, 👨‍🎨 &amp; 🧰 🔜 😭 👈 👥 🛬 ❌ 🆎, 📚 🎏 🎓.

👈 ⚫️❔ 👉 🖼 👥 ✔️ 📣 ⚫️ `response_model` 🔢.

...✋️ 😣 👂 🔛 👀 ❔ ❎ 👈.

## 📨 🆎 &amp; 💽 🖥

➡️ 😣 ⚪️➡️ ⏮️ 🖼. 👥 💚 **✍ 🔢 ⏮️ 1️⃣ 🆎** ✋️ 📨 🕳 👈 🔌 **🌅 💽**.

👥 💚 FastAPI 🚧 **🖥** 📊 ⚙️ 📨 🏷.

⏮️ 🖼, ↩️ 🎓 🎏, 👥 ✔️ ⚙️ `response_model` 🔢. ✋️ 👈 ⛓ 👈 👥 🚫 🤚 🐕‍🦺 ⚪️➡️ 👨‍🎨 &amp; 🧰 ✅ 🔢 📨 🆎.

✋️ 🌅 💼 🌐❔ 👥 💪 🕳 💖 👉, 👥 💚 🏷 **⛽/❎** 📊 👉 🖼.

&amp; 👈 💼, 👥 💪 ⚙️ 🎓 &amp; 🧬 ✊ 📈 🔢 **🆎 ✍** 🤚 👍 🐕‍🦺 👨‍🎨 &amp; 🧰, &amp; 🤚 FastAPI **💽 🖥**.

{* ../../docs_src/response_model/tutorial003_01.py hl[9:13,15:16,20] *}

⏮️ 👉, 👥 🤚 🏭 🐕‍🦺, ⚪️➡️ 👨‍🎨 &amp; ✍ 👉 📟 ☑ ⚖ 🆎, ✋️ 👥 🤚 💽 🖥 ⚪️➡️ FastAPI.

❔ 🔨 👉 👷 ❓ ➡️ ✅ 👈 👅. 👶

### 🆎 ✍ &amp; 🏭

🥇 ➡️ 👀 ❔ 👨‍🎨, ✍ &amp; 🎏 🧰 🔜 👀 👉.

`BaseUser` ✔️ 🧢 🏑. ⤴️ `UserIn` 😖 ⚪️➡️ `BaseUser` &amp; 🚮 `password` 🏑,, ⚫️ 🔜 🔌 🌐 🏑 ⚪️➡️ 👯‍♂️ 🏷.

👥 ✍ 🔢 📨 🆎 `BaseUser`, ✋️ 👥 🤙 🛬 `UserIn` 👐.

👨‍🎨, ✍, &amp; 🎏 🧰 🏆 🚫 😭 🔃 👉 ↩️, ⌨ ⚖, `UserIn` 🏿 `BaseUser`, ❔ ⛓ ⚫️ *☑* 🆎 🕐❔ ⚫️❔ ⌛ 🕳 👈 `BaseUser`.

### FastAPI 💽 🖥

🔜, FastAPI, ⚫️ 🔜 👀 📨 🆎 &amp; ⚒ 💭 👈 ⚫️❔ 👆 📨 🔌 **🕴** 🏑 👈 📣 🆎.

FastAPI 🔨 📚 👜 🔘 ⏮️ Pydantic ⚒ 💭 👈 📚 🎏 🚫 🎓 🧬 🚫 ⚙️ 📨 💽 🖥, ⏪ 👆 💪 🔚 🆙 🛬 🌅 🌅 💽 🌘 ⚫️❔ 👆 📈.

👉 🌌, 👆 💪 🤚 🏆 👯‍♂️ 🌏: 🆎 ✍ ⏮️ **🏭 🐕‍🦺** &amp; **💽 🖥**.

## 👀 ⚫️ 🩺

🕐❔ 👆 👀 🏧 🩺, 👆 💪 ✅ 👈 🔢 🏷 &amp; 🔢 🏷 🔜 👯‍♂️ ✔️ 👫 👍 🎻 🔗:

<img src="/img/tutorial/response-model/image01.png">

&amp; 👯‍♂️ 🏷 🔜 ⚙️ 🎓 🛠️ 🧾:

<img src="/img/tutorial/response-model/image02.png">

## 🎏 📨 🆎 ✍

📤 5️⃣📆 💼 🌐❔ 👆 📨 🕳 👈 🚫 ☑ Pydantic 🏑 &amp; 👆 ✍ ⚫️ 🔢, 🕴 🤚 🐕‍🦺 🚚 🏭 (👨‍🎨, ✍, ♒️).

### 📨 📨 🔗

🏆 ⚠ 💼 🔜 [🛬 📨 🔗 🔬 ⏪ 🏧 🩺](../advanced/response-directly.md){.internal-link target=_blank}.

{* ../../docs_src/response_model/tutorial003_02.py hl[8,10:11] *}

👉 🙅 💼 🍵 🔁 FastAPI ↩️ 📨 🆎 ✍ 🎓 (⚖️ 🏿) `Response`.

&amp; 🧰 🔜 😄 ↩️ 👯‍♂️ `RedirectResponse` &amp; `JSONResponse` 🏿 `Response`, 🆎 ✍ ☑.

### ✍ 📨 🏿

👆 💪 ⚙️ 🏿 `Response` 🆎 ✍:

{* ../../docs_src/response_model/tutorial003_03.py hl[8:9] *}

👉 🔜 👷 ↩️ `RedirectResponse` 🏿 `Response`, &amp; FastAPI 🔜 🔁 🍵 👉 🙅 💼.

### ❌ 📨 🆎 ✍

✋️ 🕐❔ 👆 📨 🎏 ❌ 🎚 👈 🚫 ☑ Pydantic 🆎 (✅ 💽 🎚) &amp; 👆 ✍ ⚫️ 💖 👈 🔢, FastAPI 🔜 🔄 ✍ Pydantic 📨 🏷 ⚪️➡️ 👈 🆎 ✍, &amp; 🔜 ❌.

🎏 🔜 🔨 🚥 👆 ✔️ 🕳 💖 <abbr title='A union between multiple types means "any of these types".'>🇪🇺</abbr> 🖖 🎏 🆎 🌐❔ 1️⃣ ⚖️ 🌅 👫 🚫 ☑ Pydantic 🆎, 🖼 👉 🔜 ❌ 👶:

{* ../../docs_src/response_model/tutorial003_04.py hl[10] *}

...👉 ❌ ↩️ 🆎 ✍ 🚫 Pydantic 🆎 &amp; 🚫 👁 `Response` 🎓 ⚖️ 🏿, ⚫️ 🇪🇺 (🙆 2️⃣) 🖖 `Response` &amp; `dict`.

### ❎ 📨 🏷

▶️ ⚪️➡️ 🖼 🔛, 👆 5️⃣📆 🚫 💚 ✔️ 🔢 💽 🔬, 🧾, 🖥, ♒️. 👈 🎭 FastAPI.

✋️ 👆 💪 💚 🚧 📨 🆎 ✍ 🔢 🤚 🐕‍🦺 ⚪️➡️ 🧰 💖 👨‍🎨 &amp; 🆎 ☑ (✅ ✍).

👉 💼, 👆 💪 ❎ 📨 🏷 ⚡ ⚒ `response_model=None`:

{* ../../docs_src/response_model/tutorial003_05.py hl[9] *}

👉 🔜 ⚒ FastAPI 🚶 📨 🏷 ⚡ &amp; 👈 🌌 👆 💪 ✔️ 🙆 📨 🆎 ✍ 👆 💪 🍵 ⚫️ 🤕 👆 FastAPI 🈸. 👶

## 📨 🏷 🔢 🔢

👆 📨 🏷 💪 ✔️ 🔢 💲, 💖:

{* ../../docs_src/response_model/tutorial004.py hl[11,13:14] *}

* `description: Union[str, None] = None` (⚖️ `str | None = None` 🐍 3️⃣.1️⃣0️⃣) ✔️ 🔢 `None`.
* `tax: float = 10.5` ✔️ 🔢 `10.5`.
* `tags: List[str] = []` 🔢 🛁 📇: `[]`.

✋️ 👆 💪 💚 🚫 👫 ⚪️➡️ 🏁 🚥 👫 🚫 🤙 🏪.

🖼, 🚥 👆 ✔️ 🏷 ⏮️ 📚 📦 🔢 ☁ 💽, ✋️ 👆 🚫 💚 📨 📶 📏 🎻 📨 🌕 🔢 💲.

### ⚙️ `response_model_exclude_unset` 🔢

👆 💪 ⚒ *➡ 🛠️ 👨‍🎨* 🔢 `response_model_exclude_unset=True`:

{* ../../docs_src/response_model/tutorial004.py hl[24] *}

&amp; 👈 🔢 💲 🏆 🚫 🔌 📨, 🕴 💲 🤙 ⚒.

, 🚥 👆 📨 📨 👈 *➡ 🛠️* 🏬 ⏮️ 🆔 `foo`, 📨 (🚫 ✅ 🔢 💲) 🔜:

```JSON
{
    "name": "Foo",
    "price": 50.2
}
```

/// info

FastAPI ⚙️ Pydantic 🏷 `.dict()` ⏮️ <a href="https://docs.pydantic.dev/latest/concepts/serialization/#modeldict" class="external-link" target="_blank">🚮 `exclude_unset` 🔢</a> 🏆 👉.

///

/// info

👆 💪 ⚙️:

* `response_model_exclude_defaults=True`
* `response_model_exclude_none=True`

🔬 <a href="https://docs.pydantic.dev/latest/concepts/serialization/#modeldict" class="external-link" target="_blank">Pydantic 🩺</a> `exclude_defaults` &amp; `exclude_none`.

///

#### 📊 ⏮️ 💲 🏑 ⏮️ 🔢

✋️ 🚥 👆 📊 ✔️ 💲 🏷 🏑 ⏮️ 🔢 💲, 💖 🏬 ⏮️ 🆔 `bar`:

```Python hl_lines="3  5"
{
    "name": "Bar",
    "description": "The bartenders",
    "price": 62,
    "tax": 20.2
}
```

👫 🔜 🔌 📨.

#### 📊 ⏮️ 🎏 💲 🔢

🚥 📊 ✔️ 🎏 💲 🔢 🕐, 💖 🏬 ⏮️ 🆔 `baz`:

```Python hl_lines="3  5-6"
{
    "name": "Baz",
    "description": None,
    "price": 50.2,
    "tax": 10.5,
    "tags": []
}
```

FastAPI 🙃 🥃 (🤙, Pydantic 🙃 🥃) 🤔 👈, ✋️ `description`, `tax`, &amp; `tags` ✔️ 🎏 💲 🔢, 👫 ⚒ 🎯 (↩️ ✊ ⚪️➡️ 🔢).

, 👫 🔜 🔌 🎻 📨.

/// tip

👀 👈 🔢 💲 💪 🕳, 🚫 🕴 `None`.

👫 💪 📇 (`[]`), `float` `10.5`, ♒️.

///

### `response_model_include` &amp; `response_model_exclude`

👆 💪 ⚙️ *➡ 🛠️ 👨‍🎨* 🔢 `response_model_include` &amp; `response_model_exclude`.

👫 ✊ `set` `str` ⏮️ 📛 🔢 🔌 (❎ 🎂) ⚖️ 🚫 (✅ 🎂).

👉 💪 ⚙️ ⏩ ⌨ 🚥 👆 ✔️ 🕴 1️⃣ Pydantic 🏷 &amp; 💚 ❎ 💽 ⚪️➡️ 🔢.

/// tip

✋️ ⚫️ 👍 ⚙️ 💭 🔛, ⚙️ 💗 🎓, ↩️ 👫 🔢.

👉 ↩️ 🎻 🔗 🏗 👆 📱 🗄 (&amp; 🩺) 🔜 1️⃣ 🏁 🏷, 🚥 👆 ⚙️ `response_model_include` ⚖️ `response_model_exclude` 🚫 🔢.

👉 ✔ `response_model_by_alias` 👈 👷 ➡.

///

{* ../../docs_src/response_model/tutorial005.py hl[31,37] *}

/// tip

❕ `{"name", "description"}` ✍ `set` ⏮️ 📚 2️⃣ 💲.

⚫️ 🌓 `set(["name", "description"])`.

///

#### ⚙️ `list`Ⓜ ↩️ `set`Ⓜ

🚥 👆 💭 ⚙️ `set` &amp; ⚙️ `list` ⚖️ `tuple` ↩️, FastAPI 🔜 🗜 ⚫️ `set` &amp; ⚫️ 🔜 👷 ☑:

{* ../../docs_src/response_model/tutorial006.py hl[31,37] *}

## 🌃

⚙️ *➡ 🛠️ 👨‍🎨* 🔢 `response_model` 🔬 📨 🏷 &amp; ✴️ 🚚 📢 💽 ⛽ 👅.

⚙️ `response_model_exclude_unset` 📨 🕴 💲 🎯 ⚒.
