# 🌖 📨 🗄

!!! warning
    👉 👍 🏧 ❔.

    🚥 👆 ▶️ ⏮️ **FastAPI**, 👆 💪 🚫 💪 👉.

👆 💪 📣 🌖 📨, ⏮️ 🌖 👔 📟, 🔉 🆎, 📛, ♒️.

👈 🌖 📨 🔜 🔌 🗄 🔗, 👫 🔜 😑 🛠️ 🩺.

✋️ 👈 🌖 📨 👆 ✔️ ⚒ 💭 👆 📨 `Response` 💖 `JSONResponse` 🔗, ⏮️ 👆 👔 📟 &amp; 🎚.

## 🌖 📨 ⏮️ `model`

👆 💪 🚶‍♀️ 👆 *➡ 🛠️ 👨‍🎨* 🔢 `responses`.

⚫️ 📨 `dict`, 🔑 👔 📟 🔠 📨, 💖 `200`, &amp; 💲 🎏 `dict`Ⓜ ⏮️ ℹ 🔠 👫.

🔠 👈 📨 `dict`Ⓜ 💪 ✔️ 🔑 `model`, ⚗ Pydantic 🏷, 💖 `response_model`.

**FastAPI** 🔜 ✊ 👈 🏷, 🏗 🚮 🎻 🔗 &amp; 🔌 ⚫️ ☑ 🥉 🗄.

🖼, 📣 ➕1️⃣ 📨 ⏮️ 👔 📟 `404` &amp; Pydantic 🏷 `Message`, 👆 💪 ✍:

```Python hl_lines="18  22"
{!../../../docs_src/additional_responses/tutorial001.py!}
```

!!! note
    ✔️ 🤯 👈 👆 ✔️ 📨 `JSONResponse` 🔗.

!!! info
     `model` 🔑 🚫 🍕 🗄.

    **FastAPI** 🔜 ✊ Pydantic 🏷 ⚪️➡️ 📤, 🏗 `JSON Schema`, &amp; 🚮 ⚫️ ☑ 🥉.

    ☑ 🥉:

    * 🔑 `content`, 👈 ✔️ 💲 ➕1️⃣ 🎻 🎚 (`dict`) 👈 🔌:
        * 🔑 ⏮️ 📻 🆎, ✅ `application/json`, 👈 🔌 💲 ➕1️⃣ 🎻 🎚, 👈 🔌:
            * 🔑 `schema`, 👈 ✔️ 💲 🎻 🔗 ⚪️➡️ 🏷, 📥 ☑ 🥉.
                * **FastAPI** 🚮 🔗 📥 🌐 🎻 🔗 ➕1️⃣ 🥉 👆 🗄 ↩️ ✅ ⚫️ 🔗. 👉 🌌, 🎏 🈸 &amp; 👩‍💻 💪 ⚙️ 👈 🎻 🔗 🔗, 🚚 👻 📟 ⚡ 🧰, ♒️.

🏗 📨 🗄 👉 *➡ 🛠️* 🔜:

```JSON hl_lines="3-12"
{
    "responses": {
        "404": {
            "description": "Additional Response",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/Message"
                    }
                }
            }
        },
        "200": {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/Item"
                    }
                }
            }
        },
        "422": {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/HTTPValidationError"
                    }
                }
            }
        }
    }
}
```

🔗 🔗 ➕1️⃣ 🥉 🔘 🗄 🔗:

```JSON hl_lines="4-16"
{
    "components": {
        "schemas": {
            "Message": {
                "title": "Message",
                "required": [
                    "message"
                ],
                "type": "object",
                "properties": {
                    "message": {
                        "title": "Message",
                        "type": "string"
                    }
                }
            },
            "Item": {
                "title": "Item",
                "required": [
                    "id",
                    "value"
                ],
                "type": "object",
                "properties": {
                    "id": {
                        "title": "Id",
                        "type": "string"
                    },
                    "value": {
                        "title": "Value",
                        "type": "string"
                    }
                }
            },
            "ValidationError": {
                "title": "ValidationError",
                "required": [
                    "loc",
                    "msg",
                    "type"
                ],
                "type": "object",
                "properties": {
                    "loc": {
                        "title": "Location",
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "msg": {
                        "title": "Message",
                        "type": "string"
                    },
                    "type": {
                        "title": "Error Type",
                        "type": "string"
                    }
                }
            },
            "HTTPValidationError": {
                "title": "HTTPValidationError",
                "type": "object",
                "properties": {
                    "detail": {
                        "title": "Detail",
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/ValidationError"
                        }
                    }
                }
            }
        }
    }
}
```

## 🌖 🔉 🆎 👑 📨

👆 💪 ⚙️ 👉 🎏 `responses` 🔢 🚮 🎏 🔉 🆎 🎏 👑 📨.

🖼, 👆 💪 🚮 🌖 📻 🆎 `image/png`, 📣 👈 👆 *➡ 🛠️* 💪 📨 🎻 🎚 (⏮️ 📻 🆎 `application/json`) ⚖️ 🇩🇴 🖼:

```Python hl_lines="19-24  28"
{!../../../docs_src/additional_responses/tutorial002.py!}
```

!!! note
    👀 👈 👆 ✔️ 📨 🖼 ⚙️ `FileResponse` 🔗.

!!! info
    🚥 👆 ✔ 🎏 📻 🆎 🎯 👆 `responses` 🔢, FastAPI 🔜 🤔 📨 ✔️ 🎏 📻 🆎 👑 📨 🎓 (🔢 `application/json`).

    ✋️ 🚥 👆 ✔️ ✔ 🛃 📨 🎓 ⏮️ `None` 🚮 📻 🆎, FastAPI 🔜 ⚙️ `application/json` 🙆 🌖 📨 👈 ✔️ 👨‍💼 🏷.

## 🌀 ℹ

👆 💪 🌀 📨 ℹ ⚪️➡️ 💗 🥉, 🔌 `response_model`, `status_code`, &amp; `responses` 🔢.

👆 💪 📣 `response_model`, ⚙️ 🔢 👔 📟 `200` (⚖️ 🛃 1️⃣ 🚥 👆 💪), &amp; ⤴️ 📣 🌖 ℹ 👈 🎏 📨 `responses`, 🔗 🗄 🔗.

**FastAPI** 🔜 🚧 🌖 ℹ ⚪️➡️ `responses`, &amp; 🌀 ⚫️ ⏮️ 🎻 🔗 ⚪️➡️ 👆 🏷.

🖼, 👆 💪 📣 📨 ⏮️ 👔 📟 `404` 👈 ⚙️ Pydantic 🏷 &amp; ✔️ 🛃 `description`.

&amp; 📨 ⏮️ 👔 📟 `200` 👈 ⚙️ 👆 `response_model`, ✋️ 🔌 🛃 `example`:

```Python hl_lines="20-31"
{!../../../docs_src/additional_responses/tutorial003.py!}
```

⚫️ 🔜 🌐 🌀 &amp; 🔌 👆 🗄, &amp; 🎦 🛠️ 🩺:

<img src="/img/tutorial/additional-responses/image01.png">

## 🌀 🔢 📨 &amp; 🛃 🕐

👆 💪 💚 ✔️ 🔁 📨 👈 ✔ 📚 *➡ 🛠️*, ✋️ 👆 💚 🌀 👫 ⏮️ 🛃 📨 💚 🔠 *➡ 🛠️*.

📚 💼, 👆 💪 ⚙️ 🐍 ⚒ "🏗" `dict` ⏮️ `**dict_to_unpack`:

```Python
old_dict = {
    "old key": "old value",
    "second old key": "second old value",
}
new_dict = {**old_dict, "new key": "new value"}
```

📥, `new_dict` 🔜 🔌 🌐 🔑-💲 👫 ⚪️➡️ `old_dict` ➕ 🆕 🔑-💲 👫:

```Python
{
    "old key": "old value",
    "second old key": "second old value",
    "new key": "new value",
}
```

👆 💪 ⚙️ 👈 ⚒ 🏤-⚙️ 🔢 📨 👆 *➡ 🛠️* &amp; 🌀 👫 ⏮️ 🌖 🛃 🕐.

🖼:

```Python hl_lines="13-17  26"
{!../../../docs_src/additional_responses/tutorial004.py!}
```

## 🌖 ℹ 🔃 🗄 📨

👀 ⚫️❔ ⚫️❔ 👆 💪 🔌 📨, 👆 💪 ✅ 👉 📄 🗄 🔧:

* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#responsesObject" class="external-link" target="_blank">🗄 📨 🎚</a>, ⚫️ 🔌 `Response Object`.
* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#responseObject" class="external-link" target="_blank">🗄 📨 🎚</a>, 👆 💪 🔌 🕳 ⚪️➡️ 👉 🔗 🔠 📨 🔘 👆 `responses` 🔢. ✅ `description`, `headers`, `content` (🔘 👉 👈 👆 📣 🎏 🔉 🆎 &amp; 🎻 🔗), &amp; `links`.
