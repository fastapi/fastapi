# 📣 📨 🖼 💽

👆 💪 📣 🖼 💽 👆 📱 💪 📨.

📥 📚 🌌 ⚫️.

## Pydantic `schema_extra`

👆 💪 📣 `example` Pydantic 🏷 ⚙️ `Config` &amp; `schema_extra`, 🔬 <a href="https://docs.pydantic.dev/latest/concepts/json_schema/#customizing-json-schema" class="external-link" target="_blank">Pydantic 🩺: 🔗 🛃</a>:

{* ../../docs_src/schema_extra_example/tutorial001.py hl[15:23] *}

👈 ➕ ℹ 🔜 🚮-🔢 **🎻 🔗** 👈 🏷, &amp; ⚫️ 🔜 ⚙️ 🛠️ 🩺.

/// tip

👆 💪 ⚙️ 🎏 ⚒ ↔ 🎻 🔗 &amp; 🚮 👆 👍 🛃 ➕ ℹ.

🖼 👆 💪 ⚙️ ⚫️ 🚮 🗃 🕸 👩‍💻 🔢, ♒️.

///

## `Field` 🌖 ❌

🕐❔ ⚙️ `Field()` ⏮️ Pydantic 🏷, 👆 💪 📣 ➕ ℹ **🎻 🔗** 🚶‍♀️ 🙆 🎏 ❌ ❌ 🔢.

👆 💪 ⚙️ 👉 🚮 `example` 🔠 🏑:

{* ../../docs_src/schema_extra_example/tutorial002.py hl[4,10:13] *}

/// warning

🚧 🤯 👈 📚 ➕ ❌ 🚶‍♀️ 🏆 🚫 🚮 🙆 🔬, 🕴 ➕ ℹ, 🧾 🎯.

///

## `example` &amp; `examples` 🗄

🕐❔ ⚙️ 🙆:

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

👆 💪 📣 💽 `example` ⚖️ 👪 `examples` ⏮️ 🌖 ℹ 👈 🔜 🚮 **🗄**.

### `Body` ⏮️ `example`

📥 👥 🚶‍♀️ `example` 📊 ⌛ `Body()`:

{* ../../docs_src/schema_extra_example/tutorial003.py hl[20:25] *}

### 🖼 🩺 🎚

⏮️ 🙆 👩‍🔬 🔛 ⚫️ 🔜 👀 💖 👉 `/docs`:

<img src="/img/tutorial/body-fields/image01.png">

### `Body` ⏮️ 💗 `examples`

👐 👁 `example`, 👆 💪 🚶‍♀️ `examples` ⚙️ `dict` ⏮️ **💗 🖼**, 🔠 ⏮️ ➕ ℹ 👈 🔜 🚮 **🗄** 💁‍♂️.

🔑 `dict` 🔬 🔠 🖼, &amp; 🔠 💲 ➕1️⃣ `dict`.

🔠 🎯 🖼 `dict` `examples` 💪 🔌:

* `summary`: 📏 📛 🖼.
* `description`: 📏 📛 👈 💪 🔌 ✍ ✍.
* `value`: 👉 ☑ 🖼 🎦, ✅ `dict`.
* `externalValue`: 🎛 `value`, 📛 ☝ 🖼. 👐 👉 5️⃣📆 🚫 🐕‍🦺 📚 🧰 `value`.

{* ../../docs_src/schema_extra_example/tutorial004.py hl[21:47] *}

### 🖼 🩺 🎚

⏮️ `examples` 🚮 `Body()` `/docs` 🔜 👀 💖:

<img src="/img/tutorial/body-fields/image02.png">

## 📡 ℹ

/// warning

👉 📶 📡 ℹ 🔃 🐩 **🎻 🔗** &amp; **🗄**.

🚥 💭 🔛 ⏪ 👷 👆, 👈 💪 🥃, &amp; 👆 🎲 🚫 💪 👉 ℹ, 💭 🆓 🚶 👫.

///

🕐❔ 👆 🚮 🖼 🔘 Pydantic 🏷, ⚙️ `schema_extra` ⚖️ `Field(example="something")` 👈 🖼 🚮 **🎻 🔗** 👈 Pydantic 🏷.

&amp; 👈 **🎻 🔗** Pydantic 🏷 🔌 **🗄** 👆 🛠️, &amp; ⤴️ ⚫️ ⚙️ 🩺 🎚.

**🎻 🔗** 🚫 🤙 ✔️ 🏑 `example` 🐩. ⏮️ ⏬ 🎻 🔗 🔬 🏑 <a href="https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.9.5" class="external-link" target="_blank">`examples`</a>, ✋️ 🗄 3️⃣.0️⃣.3️⃣ ⚓️ 🔛 🗝 ⏬ 🎻 🔗 👈 🚫 ✔️ `examples`.

, 🗄 3️⃣.0️⃣.3️⃣ 🔬 🚮 👍 <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#fixed-fields-20" class="external-link" target="_blank">`example`</a> 🔀 ⏬ **🎻 🔗** ⚫️ ⚙️, 🎏 🎯 (✋️ ⚫️ 👁 `example`, 🚫 `examples`), &amp; 👈 ⚫️❔ ⚙️ 🛠️ 🩺 🎚 (⚙️ 🦁 🎚).

, 👐 `example` 🚫 🍕 🎻 🔗, ⚫️ 🍕 🗄 🛃 ⏬ 🎻 🔗, &amp; 👈 ⚫️❔ 🔜 ⚙️ 🩺 🎚.

✋️ 🕐❔ 👆 ⚙️ `example` ⚖️ `examples` ⏮️ 🙆 🎏 🚙 (`Query()`, `Body()`, ♒️.) 📚 🖼 🚫 🚮 🎻 🔗 👈 🔬 👈 💽 (🚫 🗄 👍 ⏬ 🎻 🔗), 👫 🚮 🔗 *➡ 🛠️* 📄 🗄 (🏞 🍕 🗄 👈 ⚙️ 🎻 🔗).

`Path()`, `Query()`, `Header()`, &amp; `Cookie()`, `example` ⚖️ `examples` 🚮 <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#parameter-object" class="external-link" target="_blank">🗄 🔑, `Parameter Object` (🔧)</a>.

&amp; `Body()`, `File()`, &amp; `Form()`, `example` ⚖️ `examples` 📊 🚮 <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#mediaTypeObject" class="external-link" target="_blank">🗄 🔑, `Request Body Object`, 🏑 `content`, 🔛 `Media Type Object` (🔧)</a>.

🔛 🎏 ✋, 📤 🆕 ⏬ 🗄: **3️⃣.1️⃣.0️⃣**, ⏳ 🚀. ⚫️ ⚓️ 🔛 ⏪ 🎻 🔗 &amp; 🏆 🛠️ ⚪️➡️ 🗄 🛃 ⏬ 🎻 🔗 ❎, 💱 ⚒ ⚪️➡️ ⏮️ ⏬ 🎻 🔗, 🌐 👫 🤪 🔺 📉. 👐, 🦁 🎚 ⏳ 🚫 🐕‍🦺 🗄 3️⃣.1️⃣.0️⃣,, 🔜, ⚫️ 👍 😣 ⚙️ 💭 🔛.
