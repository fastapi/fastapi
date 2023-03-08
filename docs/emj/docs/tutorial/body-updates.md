# 💪 - ℹ

## ℹ ❎ ⏮ `PUT`

ℹ 🏬 👆 💪 ⚙️ <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT" class="external-link" target="_blank">🇺🇸🔍 `PUT`</a> 🛠.

👆 💪 ⚙️ `jsonable_encoder` 🗜 🔢 💽 📊 👈 💪 🏪 🎻 (✅ ⏮ ☁ 💽). 🖼, 🏭 `datetime` `str`.

=== "🐆 3⃣.6⃣ &amp; 🔛"

    ```Python hl_lines="30-35"
    {!> ../../../docs_src/body_updates/tutorial001.py!}
    ```

=== "🐆 3⃣.9⃣ &amp; 🔛"

    ```Python hl_lines="30-35"
    {!> ../../../docs_src/body_updates/tutorial001_py39.py!}
    ```

=== "🐆 3⃣.1⃣0⃣ &amp; 🔛"

    ```Python hl_lines="28-33"
    {!> ../../../docs_src/body_updates/tutorial001_py310.py!}
    ```

`PUT` ⚙️ 📨 💽 👈 🔜 ❎ ♻ 💽.

### ⚠ 🔃 ❎

👈 ⛓ 👈 🚥 👆 💚 ℹ 🏬 `bar` ⚙️ `PUT` ⏮ 💪 ⚗:

```Python
{
    "name": "Barz",
    "price": 3,
    "description": None,
}
```

↩️ ⚫️ 🚫 🔌 ⏪ 🏪 🔢 `"tax": 20.2`, 🔢 🏷 🔜 ✊ 🔢 💲 `"tax": 10.5`.

&amp; 📊 🔜 🖊 ⏮ 👈 "🆕" `tax` `10.5`.

## 🍕 ℹ ⏮ `PATCH`

👆 💪 ⚙️ <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH" class="external-link" target="_blank">🇺🇸🔍 `PATCH`</a> 🛠 *🍕* ℹ 💽.

👉 ⛓ 👈 👆 💪 📨 🕴 💽 👈 👆 💚 ℹ, 🍂 🎂 🐣.

!!! Note
    `PATCH` 🌘 🛎 ⚙️ &amp; 💭 🌘 `PUT`.

     &amp; 📚 🏉 ⚙️ 🕴 `PUT`, 🍕 ℹ.

    👆 **🆓** ⚙️ 👫 👐 👆 💚, **FastAPI** 🚫 🚫 🙆 🚫.

    ✋️ 👉 🦮 🎦 👆, 🌖 ⚖️ 🌘, ❔ 👫 🎯 ⚙️.

### ⚙️ Pydantic `exclude_unset` 🔢

🚥 👆 💚 📨 🍕 ℹ, ⚫️ 📶 ⚠ ⚙️ 🔢 `exclude_unset` Pydantic 🏷 `.dict()`.

💖 `item.dict(exclude_unset=True)`.

👈 🔜 🏗 `dict` ⏮ 🕴 💽 👈 ⚒ 🕐❔ 🏗 `item` 🏷, 🚫 🔢 💲.

⤴ 👆 💪 ⚙️ 👉 🏗 `dict` ⏮ 🕴 💽 👈 ⚒ (📨 📨), 🚫 🔢 💲:

=== "🐆 3⃣.6⃣ &amp; 🔛"

    ```Python hl_lines="34"
    {!> ../../../docs_src/body_updates/tutorial002.py!}
    ```

=== "🐆 3⃣.9⃣ &amp; 🔛"

    ```Python hl_lines="34"
    {!> ../../../docs_src/body_updates/tutorial002_py39.py!}
    ```

=== "🐆 3⃣.1⃣0⃣ &amp; 🔛"

    ```Python hl_lines="32"
    {!> ../../../docs_src/body_updates/tutorial002_py310.py!}
    ```

### ⚙️ Pydantic `update` 🔢

🔜, 👆 💪 ✍ 📁 ♻ 🏷 ⚙️ `.copy()`, &amp; 🚶‍♀️ `update` 🔢 ⏮ `dict` ⚗ 💽 ℹ.

💖 `stored_item_model.copy(update=update_data)`:

=== "🐆 3⃣.6⃣ &amp; 🔛"

    ```Python hl_lines="35"
    {!> ../../../docs_src/body_updates/tutorial002.py!}
    ```

=== "🐆 3⃣.9⃣ &amp; 🔛"

    ```Python hl_lines="35"
    {!> ../../../docs_src/body_updates/tutorial002_py39.py!}
    ```

=== "🐆 3⃣.1⃣0⃣ &amp; 🔛"

    ```Python hl_lines="33"
    {!> ../../../docs_src/body_updates/tutorial002_py310.py!}
    ```

### 🍕 ℹ 🌃

📄, ✔ 🍕 ℹ 👆 🔜:

* (⚗) ⚙️ `PATCH` ↩️ `PUT`.
* 🗃 🏪 💽.
* 🚮 👈 💽 Pydantic 🏷.
* 🏗 `dict` 🍵 🔢 💲 ⚪️➡️ 🔢 🏷 (⚙️ `exclude_unset`).
    * 👉 🌌 👆 💪 ℹ 🕴 💲 🤙 ⚒ 👩‍💻, ↩️ 🔐 💲 ⏪ 🏪 ⏮ 🔢 💲 👆 🏷.
* ✍ 📁 🏪 🏷, 🛠 ⚫️ 🔢 ⏮ 📨 🍕 ℹ (⚙️ `update` 🔢).
* 🗜 📁 🏷 🕳 👈 💪 🏪 👆 💽 (🖼, ⚙️ `jsonable_encoder`).
    * 👉 ⭐ ⚙️ 🏷 `.dict()` 👩‍🔬 🔄, ✋️ ⚫️ ⚒ 💭 (&amp; 🗜) 💲 💽 🆎 👈 💪 🗜 🎻, 🖼, `datetime` `str`.
* 🖊 💽 👆 💽.
* 📨 ℹ 🏷.

=== "🐆 3⃣.6⃣ &amp; 🔛"

    ```Python hl_lines="30-37"
    {!> ../../../docs_src/body_updates/tutorial002.py!}
    ```

=== "🐆 3⃣.9⃣ &amp; 🔛"

    ```Python hl_lines="30-37"
    {!> ../../../docs_src/body_updates/tutorial002_py39.py!}
    ```

=== "🐆 3⃣.1⃣0⃣ &amp; 🔛"

    ```Python hl_lines="28-35"
    {!> ../../../docs_src/body_updates/tutorial002_py310.py!}
    ```

!!! tip
    👆 💪 🤙 ⚙️ 👉 🎏 ⚒ ⏮ 🇺🇸🔍 `PUT` 🛠.

    ✋️ 🖼 📥 ⚙️ `PATCH` ↩️ ⚫️ ✍ 👫 ⚙️ 💼.

!!! note
    👀 👈 🔢 🏷 ✔.

    , 🚥 👆 💚 📨 🍕 ℹ 👈 💪 🚫 🌐 🔢, 👆 💪 ✔️ 🏷 ⏮ 🌐 🔢 ™ 📦 (⏮ 🔢 💲 ⚖️ `None`).

    🔬 ⚪️➡️ 🏷 ⏮ 🌐 📦 💲 **ℹ** &amp; 🏷 ⏮ ✔ 💲 **🏗**, 👆 💪 ⚙️ 💭 🔬 [➕ 🏷](extra-models.md){.internal-link target=_blank}.
