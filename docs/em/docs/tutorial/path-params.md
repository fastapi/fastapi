# ➡ 🔢

👆 💪 📣 ➡ "🔢" ⚖️ "🔢" ⏮️ 🎏 ❕ ⚙️ 🐍 📁 🎻:

```Python hl_lines="6-7"
{!../../../docs_src/path_params/tutorial001.py!}
```

💲 ➡ 🔢 `item_id` 🔜 🚶‍♀️ 👆 🔢 ❌ `item_id`.

, 🚥 👆 🏃 👉 🖼 &amp; 🚶 <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a>, 👆 🔜 👀 📨:

```JSON
{"item_id":"foo"}
```

## ➡ 🔢 ⏮️ 🆎

👆 💪 📣 🆎 ➡ 🔢 🔢, ⚙️ 🐩 🐍 🆎 ✍:

```Python hl_lines="7"
{!../../../docs_src/path_params/tutorial002.py!}
```

👉 💼, `item_id` 📣 `int`.

!!! check
    👉 🔜 🤝 👆 👨‍🎨 🐕‍🦺 🔘 👆 🔢, ⏮️ ❌ ✅, 🛠️, ♒️.

## 💽 <abbr title="also known as: serialization, parsing, marshalling">🛠️</abbr>

🚥 👆 🏃 👉 🖼 &amp; 📂 👆 🖥 <a href="http://127.0.0.1:8000/items/3" class="external-link" target="_blank">http://127.0.0.1:8000/items/3</a>, 👆 🔜 👀 📨:

```JSON
{"item_id":3}
```

!!! check
    👀 👈 💲 👆 🔢 📨 (&amp; 📨) `3`, 🐍 `int`, 🚫 🎻 `"3"`.

    , ⏮️ 👈 🆎 📄, **FastAPI** 🤝 👆 🏧 📨 <abbr title="converting the string that comes from an HTTP request into Python data">"✍"</abbr>.

## 💽 🔬

✋️ 🚥 👆 🚶 🖥 <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a>, 👆 🔜 👀 👌 🇺🇸🔍 ❌:

```JSON
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```

↩️ ➡ 🔢 `item_id` ✔️ 💲 `"foo"`, ❔ 🚫 `int`.

🎏 ❌ 🔜 😑 🚥 👆 🚚 `float` ↩️ `int`,: <a href="http://127.0.0.1:8000/items/4.2" class="external-link" target="_blank">http://127.0.0.1:8000/items/4.2</a>

!!! check
    , ⏮️ 🎏 🐍 🆎 📄, **FastAPI** 🤝 👆 💽 🔬.

    👀 👈 ❌ 🎯 🇵🇸 ⚫️❔ ☝ 🌐❔ 🔬 🚫 🚶‍♀️.

    👉 🙃 👍 ⏪ 🛠️ &amp; 🛠️ 📟 👈 🔗 ⏮️ 👆 🛠️.

## 🧾

&amp; 🕐❔ 👆 📂 👆 🖥 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>, 👆 🔜 👀 🏧, 🎓, 🛠️ 🧾 💖:

<img src="/img/tutorial/path-params/image01.png">

!!! check
    🔄, ⏮️ 👈 🎏 🐍 🆎 📄, **FastAPI** 🤝 👆 🏧, 🎓 🧾 (🛠️ 🦁 🎚).

    👀 👈 ➡ 🔢 📣 🔢.

## 🐩-⚓️ 💰, 🎛 🧾

&amp; ↩️ 🏗 🔗 ⚪️➡️ <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md" class="external-link" target="_blank">🗄</a> 🐩, 📤 📚 🔗 🧰.

↩️ 👉, **FastAPI** ⚫️ 🚚 🎛 🛠️ 🧾 (⚙️ 📄), ❔ 👆 💪 🔐 <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>:

<img src="/img/tutorial/path-params/image02.png">

🎏 🌌, 📤 📚 🔗 🧰. ✅ 📟 ⚡ 🧰 📚 🇪🇸.

## Pydantic

🌐 💽 🔬 🎭 🔽 🚘 <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a>, 👆 🤚 🌐 💰 ⚪️➡️ ⚫️. &amp; 👆 💭 👆 👍 ✋.

👆 💪 ⚙️ 🎏 🆎 📄 ⏮️ `str`, `float`, `bool` &amp; 📚 🎏 🏗 📊 🆎.

📚 👫 🔬 ⏭ 📃 🔰.

## ✔ 🤔

🕐❔ 🏗 *➡ 🛠️*, 👆 💪 🔎 ⚠ 🌐❔ 👆 ✔️ 🔧 ➡.

💖 `/users/me`, ➡️ 💬 👈 ⚫️ 🤚 📊 🔃 ⏮️ 👩‍💻.

&amp; ⤴️ 👆 💪 ✔️ ➡ `/users/{user_id}` 🤚 💽 🔃 🎯 👩‍💻 👩‍💻 🆔.

↩️ *➡ 🛠️* 🔬 ✔, 👆 💪 ⚒ 💭 👈 ➡ `/users/me` 📣 ⏭ 1️⃣ `/users/{user_id}`:

```Python hl_lines="6  11"
{!../../../docs_src/path_params/tutorial003.py!}
```

⏪, ➡ `/users/{user_id}` 🔜 🏏 `/users/me`, "💭" 👈 ⚫️ 📨 🔢 `user_id` ⏮️ 💲 `"me"`.

➡, 👆 🚫🔜 ↔ ➡ 🛠️:

```Python hl_lines="6  11"
{!../../../docs_src/path_params/tutorial003b.py!}
```

🥇 🕐 🔜 🕧 ⚙️ ↩️ ➡ 🏏 🥇.

## 🔁 💲

🚥 👆 ✔️ *➡ 🛠️* 👈 📨 *➡ 🔢*, ✋️ 👆 💚 💪 ☑ *➡ 🔢* 💲 🔁, 👆 💪 ⚙️ 🐩 🐍 <abbr title="Enumeration">`Enum`</abbr>.

### ✍ `Enum` 🎓

🗄 `Enum` &amp; ✍ 🎧-🎓 👈 😖 ⚪️➡️ `str` &amp; ⚪️➡️ `Enum`.

😖 ⚪️➡️ `str` 🛠️ 🩺 🔜 💪 💭 👈 💲 🔜 🆎 `string` &amp; 🔜 💪 ✍ ☑.

⤴️ ✍ 🎓 🔢 ⏮️ 🔧 💲, ❔ 🔜 💪 ☑ 💲:

```Python hl_lines="1  6-9"
{!../../../docs_src/path_params/tutorial005.py!}
```

!!! info
    <a href="https://docs.python.org/3/library/enum.html" class="external-link" target="_blank">🔢 (⚖️ 🔢) 💪 🐍</a> ↩️ ⏬ 3️⃣.4️⃣.

!!! tip
    🚥 👆 💭, "📊", "🎓", &amp; "🍏" 📛 🎰 🏫 <abbr title="Technically, Deep Learning model architectures">🏷</abbr>.

### 📣 *➡ 🔢*

⤴️ ✍ *➡ 🔢* ⏮️ 🆎 ✍ ⚙️ 🔢 🎓 👆 ✍ (`ModelName`):

```Python hl_lines="16"
{!../../../docs_src/path_params/tutorial005.py!}
```

### ✅ 🩺

↩️ 💪 💲 *➡ 🔢* 🔢, 🎓 🩺 💪 🎦 👫 🎆:

<img src="/img/tutorial/path-params/image03.png">

### 👷 ⏮️ 🐍 *🔢*

💲 *➡ 🔢* 🔜 *🔢 👨‍🎓*.

#### 🔬 *🔢 👨‍🎓*

👆 💪 🔬 ⚫️ ⏮️ *🔢 👨‍🎓* 👆 ✍ 🔢 `ModelName`:

```Python hl_lines="17"
{!../../../docs_src/path_params/tutorial005.py!}
```

#### 🤚 *🔢 💲*

👆 💪 🤚 ☑ 💲 ( `str` 👉 💼) ⚙️ `model_name.value`, ⚖️ 🏢, `your_enum_member.value`:

```Python hl_lines="20"
{!../../../docs_src/path_params/tutorial005.py!}
```

!!! tip
    👆 💪 🔐 💲 `"lenet"` ⏮️ `ModelName.lenet.value`.

#### 📨 *🔢 👨‍🎓*

👆 💪 📨 *🔢 👨‍🎓* ⚪️➡️ 👆 *➡ 🛠️*, 🐦 🎻 💪 (✅ `dict`).

👫 🔜 🗜 👫 🔗 💲 (🎻 👉 💼) ⏭ 🛬 👫 👩‍💻:

```Python hl_lines="18  21  23"
{!../../../docs_src/path_params/tutorial005.py!}
```

👆 👩‍💻 👆 🔜 🤚 🎻 📨 💖:

```JSON
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

## ➡ 🔢 ⚗ ➡

➡️ 💬 👆 ✔️ *➡ 🛠️* ⏮️ ➡ `/files/{file_path}`.

✋️ 👆 💪 `file_path` ⚫️ 🔌 *➡*, 💖 `home/johndoe/myfile.txt`.

, 📛 👈 📁 🔜 🕳 💖: `/files/home/johndoe/myfile.txt`.

### 🗄 🐕‍🦺

🗄 🚫 🐕‍🦺 🌌 📣 *➡ 🔢* 🔌 *➡* 🔘, 👈 💪 ↘️ 😐 👈 ⚠ 💯 &amp; 🔬.

👐, 👆 💪 ⚫️ **FastAPI**, ⚙️ 1️⃣ 🔗 🧰 ⚪️➡️ 💃.

&amp; 🩺 🔜 👷, 👐 🚫 ❎ 🙆 🧾 💬 👈 🔢 🔜 🔌 ➡.

### ➡ 🔌

⚙️ 🎛 🔗 ⚪️➡️ 💃 👆 💪 📣 *➡ 🔢* ⚗ *➡* ⚙️ 📛 💖:

```
/files/{file_path:path}
```

👉 💼, 📛 🔢 `file_path`, &amp; 🏁 🍕, `:path`, 💬 ⚫️ 👈 🔢 🔜 🏏 🙆 *➡*.

, 👆 💪 ⚙️ ⚫️ ⏮️:

```Python hl_lines="6"
{!../../../docs_src/path_params/tutorial004.py!}
```

!!! tip
    👆 💪 💪 🔢 🔌 `/home/johndoe/myfile.txt`, ⏮️ 🏁 🔪 (`/`).

    👈 💼, 📛 🔜: `/files//home/johndoe/myfile.txt`, ⏮️ 2️⃣✖️ 🔪 (`//`) 🖖 `files` &amp; `home`.

## 🌃

⏮️ **FastAPI**, ⚙️ 📏, 🏋️ &amp; 🐩 🐍 🆎 📄, 👆 🤚:

* 👨‍🎨 🐕‍🦺: ❌ ✅, ✍, ♒️.
* 💽 "<abbr title="converting the string that comes from an HTTP request into Python data">✍</abbr>"
* 💽 🔬
* 🛠️ ✍ &amp; 🏧 🧾

&amp; 👆 🕴 ✔️ 📣 👫 🕐.

👈 🎲 👑 ⭐ 📈 **FastAPI** 🔬 🎛 🛠️ (↖️ ⚪️➡️ 🍣 🎭).
