# 📨 💪

🕐❔ 👆 💪 📨 📊 ⚪️➡️ 👩‍💻 (➡️ 💬, 🖥) 👆 🛠️, 👆 📨 ⚫️ **📨 💪**.

**📨** 💪 📊 📨 👩‍💻 👆 🛠️. **📨** 💪 💽 👆 🛠️ 📨 👩‍💻.

👆 🛠️ 🌖 🕧 ✔️ 📨 **📨** 💪. ✋️ 👩‍💻 🚫 🎯 💪 📨 **📨** 💪 🌐 🕰.

📣 **📨** 💪, 👆 ⚙️ <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> 🏷 ⏮️ 🌐 👫 🏋️ &amp; 💰.

/// info

📨 💽, 👆 🔜 ⚙️ 1️⃣: `POST` (🌅 ⚠), `PUT`, `DELETE` ⚖️ `PATCH`.

📨 💪 ⏮️ `GET` 📨 ✔️ ⚠ 🎭 🔧, 👐, ⚫️ 🐕‍🦺 FastAPI, 🕴 📶 🏗/😕 ⚙️ 💼.

⚫️ 🚫, 🎓 🩺 ⏮️ 🦁 🎚 🏆 🚫 🎦 🧾 💪 🕐❔ ⚙️ `GET`, &amp; 🗳 🖕 💪 🚫 🐕‍🦺 ⚫️.

///

## 🗄 Pydantic `BaseModel`

🥇, 👆 💪 🗄 `BaseModel` ⚪️➡️ `pydantic`:

{* ../../docs_src/body/tutorial001.py hl[4] *}

## ✍ 👆 💽 🏷

⤴️ 👆 📣 👆 💽 🏷 🎓 👈 😖 ⚪️➡️ `BaseModel`.

⚙️ 🐩 🐍 🆎 🌐 🔢:

{* ../../docs_src/body/tutorial001.py hl[7:11] *}

🎏 🕐❔ 📣 🔢 🔢, 🕐❔ 🏷 🔢 ✔️ 🔢 💲, ⚫️ 🚫 ✔. ⏪, ⚫️ ✔. ⚙️ `None` ⚒ ⚫️ 📦.

🖼, 👉 🏷 🔛 📣 🎻 "`object`" (⚖️ 🐍 `dict`) 💖:

```JSON
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

... `description` &amp; `tax` 📦 (⏮️ 🔢 💲 `None`), 👉 🎻 "`object`" 🔜 ☑:

```JSON
{
    "name": "Foo",
    "price": 45.2
}
```

## 📣 ⚫️ 🔢

🚮 ⚫️ 👆 *➡ 🛠️*, 📣 ⚫️ 🎏 🌌 👆 📣 ➡ &amp; 🔢 🔢:

{* ../../docs_src/body/tutorial001.py hl[18] *}

...&amp; 📣 🚮 🆎 🏷 👆 ✍, `Item`.

## 🏁

⏮️ 👈 🐍 🆎 📄, **FastAPI** 🔜:

* ✍ 💪 📨 🎻.
* 🗜 🔗 🆎 (🚥 💪).
* ✔ 💽.
    * 🚥 💽 ❌, ⚫️ 🔜 📨 👌 &amp; 🆑 ❌, ☠️ ⚫️❔ 🌐❔ &amp; ⚫️❔ ❌ 📊.
* 🤝 👆 📨 📊 🔢 `item`.
    * 👆 📣 ⚫️ 🔢 🆎 `Item`, 👆 🔜 ✔️ 🌐 👨‍🎨 🐕‍🦺 (🛠️, ♒️) 🌐 🔢 &amp; 👫 🆎.
* 🏗 <a href="https://json-schema.org" class="external-link" target="_blank">🎻 🔗</a> 🔑 👆 🏷, 👆 💪 ⚙️ 👫 🙆 🙆 👆 💖 🚥 ⚫️ ⚒ 🔑 👆 🏗.
* 👈 🔗 🔜 🍕 🏗 🗄 🔗, &amp; ⚙️ 🏧 🧾 <abbr title="User Interfaces">⚜</abbr>.

## 🏧 🩺

🎻 🔗 👆 🏷 🔜 🍕 👆 🗄 🏗 🔗, &amp; 🔜 🎦 🎓 🛠️ 🩺:

<img src="/img/tutorial/body/image01.png">

&amp; 🔜 ⚙️ 🛠️ 🩺 🔘 🔠 *➡ 🛠️* 👈 💪 👫:

<img src="/img/tutorial/body/image02.png">

## 👨‍🎨 🐕‍🦺

👆 👨‍🎨, 🔘 👆 🔢 👆 🔜 🤚 🆎 🔑 &amp; 🛠️ 🌐 (👉 🚫🔜 🔨 🚥 👆 📨 `dict` ↩️ Pydantic 🏷):

<img src="/img/tutorial/body/image03.png">

👆 🤚 ❌ ✅ ❌ 🆎 🛠️:

<img src="/img/tutorial/body/image04.png">

👉 🚫 🤞, 🎂 🛠️ 🏗 🤭 👈 🔧.

&amp; ⚫️ 🙇 💯 🔧 🌓, ⏭ 🙆 🛠️, 🚚 ⚫️ 🔜 👷 ⏮️ 🌐 👨‍🎨.

📤 🔀 Pydantic ⚫️ 🐕‍🦺 👉.

⏮️ 🖼 ✊ ⏮️ <a href="https://code.visualstudio.com" class="external-link" target="_blank">🎙 🎙 📟</a>.

✋️ 👆 🔜 🤚 🎏 👨‍🎨 🐕‍🦺 ⏮️ <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">🗒</a> &amp; 🌅 🎏 🐍 👨‍🎨:

<img src="/img/tutorial/body/image05.png">

/// tip

🚥 👆 ⚙️ <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">🗒</a> 👆 👨‍🎨, 👆 💪 ⚙️ <a href="https://github.com/koxudaxi/pydantic-pycharm-plugin/" class="external-link" target="_blank">Pydantic 🗒 📁</a>.

⚫️ 📉 👨‍🎨 🐕‍🦺 Pydantic 🏷, ⏮️:

* 🚘-🛠️
* 🆎 ✅
* 🛠️
* 🔎
* 🔬

///

## ⚙️ 🏷

🔘 🔢, 👆 💪 🔐 🌐 🔢 🏷 🎚 🔗:

{* ../../docs_src/body/tutorial002.py hl[21] *}

## 📨 💪 ➕ ➡ 🔢

👆 💪 📣 ➡ 🔢 &amp; 📨 💪 🎏 🕰.

**FastAPI** 🔜 🤔 👈 🔢 🔢 👈 🏏 ➡ 🔢 🔜 **✊ ⚪️➡️ ➡**, &amp; 👈 🔢 🔢 👈 📣 Pydantic 🏷 🔜 **✊ ⚪️➡️ 📨 💪**.

{* ../../docs_src/body/tutorial003.py hl[17:18] *}

## 📨 💪 ➕ ➡ ➕ 🔢 🔢

👆 💪 📣 **💪**, **➡** &amp; **🔢** 🔢, 🌐 🎏 🕰.

**FastAPI** 🔜 🤔 🔠 👫 &amp; ✊ 📊 ⚪️➡️ ☑ 🥉.

{* ../../docs_src/body/tutorial004.py hl[18] *}

🔢 🔢 🔜 🤔 ⏩:

* 🚥 🔢 📣 **➡**, ⚫️ 🔜 ⚙️ ➡ 🔢.
* 🚥 🔢 **⭐ 🆎** (💖 `int`, `float`, `str`, `bool`, ♒️) ⚫️ 🔜 🔬 **🔢** 🔢.
* 🚥 🔢 📣 🆎 **Pydantic 🏷**, ⚫️ 🔜 🔬 📨 **💪**.

/// note

FastAPI 🔜 💭 👈 💲 `q` 🚫 ✔ ↩️ 🔢 💲 `= None`.

 `Union` `Union[str, None]` 🚫 ⚙️ FastAPI, ✋️ 🔜 ✔ 👆 👨‍🎨 🤝 👆 👍 🐕‍🦺 &amp; 🔍 ❌.

///

## 🍵 Pydantic

🚥 👆 🚫 💚 ⚙️ Pydantic 🏷, 👆 💪 ⚙️ **💪** 🔢. 👀 🩺 [💪 - 💗 🔢: ⭐ 💲 💪](body-multiple-params.md#_2){.internal-link target=_blank}.
