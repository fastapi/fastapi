# ➡ 🛠️ 🏧 📳

## 🗄 {

/// warning

🚥 👆 🚫 "🕴" 🗄, 👆 🎲 🚫 💪 👉.

///

👆 💪 ⚒ 🗄 `operationId` ⚙️ 👆 *➡ 🛠️* ⏮️ 🔢 `operation_id`.

👆 🔜 ✔️ ⚒ 💭 👈 ⚫️ 😍 🔠 🛠️.

{* ../../docs_src/path_operation_advanced_configuration/tutorial001.py hl[6] *}

### ⚙️ *➡ 🛠️ 🔢* 📛 {

🚥 👆 💚 ⚙️ 👆 🔗' 🔢 📛 `operationId`Ⓜ, 👆 💪 🔁 🤭 🌐 👫 &amp; 🔐 🔠 *➡ 🛠️* `operation_id` ⚙️ 👫 `APIRoute.name`.

👆 🔜 ⚫️ ⏮️ ❎ 🌐 👆 *➡ 🛠️*.

{* ../../docs_src/path_operation_advanced_configuration/tutorial002.py hl[2,12:21,24] *}

/// tip

🚥 👆 ❎ 🤙 `app.openapi()`, 👆 🔜 ℹ `operationId`Ⓜ ⏭ 👈.

///

/// warning

🚥 👆 👉, 👆 ✔️ ⚒ 💭 🔠 1️⃣ 👆 *➡ 🛠️ 🔢* ✔️ 😍 📛.

🚥 👫 🎏 🕹 (🐍 📁).

///

## 🚫 ⚪️➡️ 🗄

🚫 *➡ 🛠️* ⚪️➡️ 🏗 🗄 🔗 (&amp; ➡️, ⚪️➡️ 🏧 🧾 ⚙️), ⚙️ 🔢 `include_in_schema` &amp; ⚒ ⚫️ `False`:

{* ../../docs_src/path_operation_advanced_configuration/tutorial003.py hl[6] *}

## 🏧 📛 ⚪️➡️ #️⃣

👆 💪 📉 ⏸ ⚙️ ⚪️➡️ #️⃣ *➡ 🛠️ 🔢* 🗄.

❎ `\f` (😖 "📨 🍼" 🦹) 🤕 **FastAPI** 🔁 🔢 ⚙️ 🗄 👉 ☝.

⚫️ 🏆 🚫 🎦 🆙 🧾, ✋️ 🎏 🧰 (✅ 🐉) 🔜 💪 ⚙️ 🎂.

{* ../../docs_src/path_operation_advanced_configuration/tutorial004.py hl[19:29] *}

## 🌖 📨

👆 🎲 ✔️ 👀 ❔ 📣 `response_model` &amp; `status_code` *➡ 🛠️*.

👈 🔬 🗃 🔃 👑 📨 *➡ 🛠️*.

👆 💪 📣 🌖 📨 ⏮️ 👫 🏷, 👔 📟, ♒️.

📤 🎂 📃 📥 🧾 🔃 ⚫️, 👆 💪 ✍ ⚫️ [🌖 📨 🗄](additional-responses.md){.internal-link target=_blank}.

## 🗄 ➕

🕐❔ 👆 📣 *➡ 🛠️* 👆 🈸, **FastAPI** 🔁 🏗 🔗 🗃 🔃 👈 *➡ 🛠️* 🔌 🗄 🔗.

/// note | 📡 ℹ

🗄 🔧 ⚫️ 🤙 <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#operation-object" class="external-link" target="_blank">🛠️ 🎚</a>.

///

⚫️ ✔️ 🌐 ℹ 🔃 *➡ 🛠️* &amp; ⚙️ 🏗 🏧 🧾.

⚫️ 🔌 `tags`, `parameters`, `requestBody`, `responses`, ♒️.

👉 *➡ 🛠️*-🎯 🗄 🔗 🛎 🏗 🔁 **FastAPI**, ✋️ 👆 💪 ↔ ⚫️.

/// tip

👉 🔅 🎚 ↔ ☝.

🚥 👆 🕴 💪 📣 🌖 📨, 🌅 🏪 🌌 ⚫️ ⏮️ [🌖 📨 🗄](additional-responses.md){.internal-link target=_blank}.

///

👆 💪 ↔ 🗄 🔗 *➡ 🛠️* ⚙️ 🔢 `openapi_extra`.

### 🗄 ↔

👉 `openapi_extra` 💪 👍, 🖼, 📣 [🗄 ↔](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#specificationExtensions):

{* ../../docs_src/path_operation_advanced_configuration/tutorial005.py hl[6] *}

🚥 👆 📂 🏧 🛠️ 🩺, 👆 ↔ 🔜 🎦 🆙 🔝 🎯 *➡ 🛠️*.

<img src="/img/tutorial/path-operation-advanced-configuration/image01.png">

&amp; 🚥 👆 👀 📉 🗄 ( `/openapi.json` 👆 🛠️), 👆 🔜 👀 👆 ↔ 🍕 🎯 *➡ 🛠️* 💁‍♂️:

```JSON hl_lines="22"
{
    "openapi": "3.0.2",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "summary": "Read Items",
                "operationId": "read_items_items__get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                },
                "x-aperture-labs-portal": "blue"
            }
        }
    }
}
```

### 🛃 🗄 *➡ 🛠️* 🔗

📖 `openapi_extra` 🔜 🙇 🔗 ⏮️ 🔁 🏗 🗄 🔗 *➡ 🛠️*.

, 👆 💪 🚮 🌖 💽 🔁 🏗 🔗.

🖼, 👆 💪 💭 ✍ &amp; ✔ 📨 ⏮️ 👆 👍 📟, 🍵 ⚙️ 🏧 ⚒ FastAPI ⏮️ Pydantic, ✋️ 👆 💪 💚 🔬 📨 🗄 🔗.

👆 💪 👈 ⏮️ `openapi_extra`:

{* ../../docs_src/path_operation_advanced_configuration/tutorial006.py hl[20:37,39:40] *}

👉 🖼, 👥 🚫 📣 🙆 Pydantic 🏷. 👐, 📨 💪 🚫 <abbr title="converted from some plain format, like bytes, into Python objects">🎻</abbr> 🎻, ⚫️ ✍ 🔗 `bytes`, &amp; 🔢 `magic_data_reader()` 🔜 🈚 🎻 ⚫️ 🌌.

👐, 👥 💪 📣 📈 🔗 📨 💪.

### 🛃 🗄 🎚 🆎

⚙️ 👉 🎏 🎱, 👆 💪 ⚙️ Pydantic 🏷 🔬 🎻 🔗 👈 ⤴️ 🔌 🛃 🗄 🔗 📄 *➡ 🛠️*.

&amp; 👆 💪 👉 🚥 💽 🆎 📨 🚫 🎻.

🖼, 👉 🈸 👥 🚫 ⚙️ FastAPI 🛠️ 🛠️ ⚗ 🎻 🔗 ⚪️➡️ Pydantic 🏷 🚫 🏧 🔬 🎻. 👐, 👥 📣 📨 🎚 🆎 📁, 🚫 🎻:

{* ../../docs_src/path_operation_advanced_configuration/tutorial007.py hl[17:22,24] *}

👐, 👐 👥 🚫 ⚙️ 🔢 🛠️ 🛠️, 👥 ⚙️ Pydantic 🏷 ❎ 🏗 🎻 🔗 💽 👈 👥 💚 📨 📁.

⤴️ 👥 ⚙️ 📨 🔗, &amp; ⚗ 💪 `bytes`. 👉 ⛓ 👈 FastAPI 🏆 🚫 🔄 🎻 📨 🚀 🎻.

&amp; ⤴️ 👆 📟, 👥 🎻 👈 📁 🎚 🔗, &amp; ⤴️ 👥 🔄 ⚙️ 🎏 Pydantic 🏷 ✔ 📁 🎚:

{* ../../docs_src/path_operation_advanced_configuration/tutorial007.py hl[26:33] *}

/// tip

📥 👥 🏤-⚙️ 🎏 Pydantic 🏷.

✋️ 🎏 🌌, 👥 💪 ✔️ ✔ ⚫️ 🎏 🌌.

///
