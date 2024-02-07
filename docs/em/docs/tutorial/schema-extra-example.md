# 📣 📨 🖼 💽

👆 💪 📣 🖼 💽 👆 📱 💪 📨.

📥 📚 🌌 ⚫️.

## Pydantic `schema_extra`

👆 💪 📣 `example` Pydantic 🏷 ⚙️ `Config` &amp; `schema_extra`, 🔬 <a href="https://pydantic-docs.helpmanual.io/usage/schema/#schema-customization" class="external-link" target="_blank">Pydantic 🩺: 🔗 🛃</a>:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="15-23"
    {!> ../../../docs_src/schema_extra_example/tutorial001.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="13-21"
    {!> ../../../docs_src/schema_extra_example/tutorial001_py310.py!}
    ```

👈 ➕ ℹ 🔜 🚮-🔢 **🎻 🔗** 👈 🏷, &amp; ⚫️ 🔜 ⚙️ 🛠️ 🩺.

!!! tip
    👆 💪 ⚙️ 🎏 ⚒ ↔ 🎻 🔗 &amp; 🚮 👆 👍 🛃 ➕ ℹ.

    🖼 👆 💪 ⚙️ ⚫️ 🚮 🗃 🕸 👩‍💻 🔢, ♒️.

## `Field` 🌖 ❌

🕐❔ ⚙️ `Field()` ⏮️ Pydantic 🏷, 👆 💪 📣 ➕ ℹ **🎻 🔗** 🚶‍♀️ 🙆 🎏 ❌ ❌ 🔢.

👆 💪 ⚙️ 👉 🚮 `example` 🔠 🏑:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="4  10-13"
    {!> ../../../docs_src/schema_extra_example/tutorial002.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="2  8-11"
    {!> ../../../docs_src/schema_extra_example/tutorial002_py310.py!}
    ```

!!! warning
    🚧 🤯 👈 📚 ➕ ❌ 🚶‍♀️ 🏆 🚫 🚮 🙆 🔬, 🕴 ➕ ℹ, 🧾 🎯.

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

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="20-25"
    {!> ../../../docs_src/schema_extra_example/tutorial003.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="18-23"
    {!> ../../../docs_src/schema_extra_example/tutorial003_py310.py!}
    ```

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

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="21-47"
    {!> ../../../docs_src/schema_extra_example/tutorial004.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="19-45"
    {!> ../../../docs_src/schema_extra_example/tutorial004_py310.py!}
    ```

### 🖼 🩺 🎚

⏮️ `examples` 🚮 `Body()` `/docs` 🔜 👀 💖:

<img src="/img/tutorial/body-fields/image02.png">

## 📡 ℹ

!!! warning
    👉 📶 📡 ℹ 🔃 🐩 **🎻 🔗** &amp; **🗄**.

    🚥 💭 🔛 ⏪ 👷 👆, 👈 💪 🥃, &amp; 👆 🎲 🚫 💪 👉 ℹ, 💭 🆓 🚶 👫.

🕐❔ 👆 🚮 🖼 🔘 Pydantic 🏷, ⚙️ `schema_extra` ⚖️ `Field(example="something")` 👈 🖼 🚮 **🎻 🔗** 👈 Pydantic 🏷.

&amp; 👈 **🎻 🔗** Pydantic 🏷 🔌 **🗄** 👆 🛠️, &amp; ⤴️ ⚫️ ⚙️ 🩺 🎚.

**🎻 🔗** 🚫 🤙 ✔️ 🏑 `example` 🐩. ⏮️ ⏬ 🎻 🔗 🔬 🏑 <a href="https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.9.5" class="external-link" target="_blank">`examples`</a>, ✋️ 🗄 3️⃣.0️⃣.3️⃣ ⚓️ 🔛 🗝 ⏬ 🎻 🔗 👈 🚫 ✔️ `examples`.

, 🗄 3️⃣.0️⃣.3️⃣ 🔬 🚮 👍 <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#fixed-fields-20" class="external-link" target="_blank">`example`</a> 🔀 ⏬ **🎻 🔗** ⚫️ ⚙️, 🎏 🎯 (✋️ ⚫️ 👁 `example`, 🚫 `examples`), &amp; 👈 ⚫️❔ ⚙️ 🛠️ 🩺 🎚 (⚙️ 🦁 🎚).

, 👐 `example` 🚫 🍕 🎻 🔗, ⚫️ 🍕 🗄 🛃 ⏬ 🎻 🔗, &amp; 👈 ⚫️❔ 🔜 ⚙️ 🩺 🎚.

✋️ 🕐❔ 👆 ⚙️ `example` ⚖️ `examples` ⏮️ 🙆 🎏 🚙 (`Query()`, `Body()`, ♒️.) 📚 🖼 🚫 🚮 🎻 🔗 👈 🔬 👈 💽 (🚫 🗄 👍 ⏬ 🎻 🔗), 👫 🚮 🔗 *➡ 🛠️* 📄 🗄 (🏞 🍕 🗄 👈 ⚙️ 🎻 🔗).

`Path()`, `Query()`, `Header()`, &amp; `Cookie()`, `example` ⚖️ `examples` 🚮 <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#parameter-object" class="external-link" target="_blank">🗄 🔑, `Parameter Object` (🔧)</a>.

&amp; `Body()`, `File()`, &amp; `Form()`, `example` ⚖️ `examples` 📊 🚮 <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#mediaTypeObject" class="external-link" target="_blank">🗄 🔑, `Request Body Object`, 🏑 `content`, 🔛 `Media Type Object` (🔧)</a>.

🔛 🎏 ✋, 📤 🆕 ⏬ 🗄: **3️⃣.1️⃣.0️⃣**, ⏳ 🚀. ⚫️ ⚓️ 🔛 ⏪ 🎻 🔗 &amp; 🏆 🛠️ ⚪️➡️ 🗄 🛃 ⏬ 🎻 🔗 ❎, 💱 ⚒ ⚪️➡️ ⏮️ ⏬ 🎻 🔗, 🌐 👫 🤪 🔺 📉. 👐, 🦁 🎚 ⏳ 🚫 🐕‍🦺 🗄 3️⃣.1️⃣.0️⃣,, 🔜, ⚫️ 👍 😣 ⚙️ 💭 🔛.
