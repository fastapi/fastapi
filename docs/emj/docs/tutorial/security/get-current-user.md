# 🤚 ⏮️ 👩‍💻

⏮️ 📃 💂‍♂ ⚙️ (❔ 🧢 🔛 🔗 💉 ⚙️) 🤝 *➡ 🛠️ 🔢* `token` `str`:

```Python hl_lines="10"
{!../../../docs_src/security/tutorial001.py!}
```

✋️ 👈 🚫 👈 ⚠.

➡️ ⚒ ⚫️ 🤝 👥 ⏮️ 👩‍💻.

## ✍ 👩‍💻 🏷

🥇, ➡️ ✍ Pydantic 👩‍💻 🏷.

🎏 🌌 👥 ⚙️ Pydantic 📣 💪, 👥 💪 ⚙️ ⚫️ 🙆 🙆:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="5  12-16"
    {!> ../../../docs_src/security/tutorial002.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="3  10-14"
    {!> ../../../docs_src/security/tutorial002_py310.py!}
    ```

## ✍ `get_current_user` 🔗

➡️ ✍ 🔗 `get_current_user`.

💭 👈 🔗 💪 ✔️ 🎧-🔗 ❓

`get_current_user` 🔜 ✔️ 🔗 ⏮️ 🎏 `oauth2_scheme` 👥 ✍ ⏭.

🎏 👥 🔨 ⏭ *➡ 🛠️* 🔗, 👆 🆕 🔗 `get_current_user` 🔜 📨 `token` `str` ⚪️➡️ 🎧-🔗 `oauth2_scheme`:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="25"
    {!> ../../../docs_src/security/tutorial002.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="23"
    {!> ../../../docs_src/security/tutorial002_py310.py!}
    ```

## 🤚 👩‍💻

`get_current_user` 🔜 ⚙️ (❌) 🚙 🔢 👥 ✍, 👈 ✊ 🤝 `str` &amp; 📨 👆 Pydantic `User` 🏷:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="19-22  26-27"
    {!> ../../../docs_src/security/tutorial002.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="17-20  24-25"
    {!> ../../../docs_src/security/tutorial002_py310.py!}
    ```

## 💉 ⏮️ 👩‍💻

🔜 👥 💪 ⚙️ 🎏 `Depends` ⏮️ 👆 `get_current_user` *➡ 🛠️*:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="31"
    {!> ../../../docs_src/security/tutorial002.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="29"
    {!> ../../../docs_src/security/tutorial002_py310.py!}
    ```

👀 👈 👥 📣 🆎 `current_user` Pydantic 🏷 `User`.

👉 🔜 ℹ 🇺🇲 🔘 🔢 ⏮️ 🌐 🛠️ &amp; 🆎 ✅.

!!! tip
    👆 5️⃣📆 💭 👈 📨 💪 📣 ⏮️ Pydantic 🏷.

    📥 **FastAPI** 🏆 🚫 🤚 😨 ↩️ 👆 ⚙️ `Depends`.

!!! check
    🌌 👉 🔗 ⚙️ 🏗 ✔ 👥 ✔️ 🎏 🔗 (🎏 "☑") 👈 🌐 📨 `User` 🏷.

    👥 🚫 🚫 ✔️ 🕴 1️⃣ 🔗 👈 💪 📨 👈 🆎 💽.

## 🎏 🏷

👆 💪 🔜 🤚 ⏮️ 👩‍💻 🔗 *➡ 🛠️ 🔢* &amp; 🙅 ⏮️ 💂‍♂ 🛠️ **🔗 💉** 🎚, ⚙️ `Depends`.

&amp; 👆 💪 ⚙️ 🙆 🏷 ⚖️ 💽 💂‍♂ 📄 (👉 💼, Pydantic 🏷 `User`).

✋️ 👆 🚫 🚫 ⚙️ 🎯 💽 🏷, 🎓 ⚖️ 🆎.

👆 💚 ✔️ `id` &amp; `email` &amp; 🚫 ✔️ 🙆 `username` 👆 🏷 ❓ 💭. 👆 💪 ⚙️ 👉 🎏 🧰.

👆 💚 ✔️ `str`❓ ⚖️ `dict`❓ ⚖️ 💽 🎓 🏷 👐 🔗 ❓ ⚫️ 🌐 👷 🎏 🌌.

👆 🤙 🚫 ✔️ 👩‍💻 👈 🕹 👆 🈸 ✋️ 🤖, 🤖, ⚖️ 🎏 ⚙️, 👈 ✔️ 🔐 🤝 ❓ 🔄, ⚫️ 🌐 👷 🎏.

⚙️ 🙆 😇 🏷, 🙆 😇 🎓, 🙆 😇 💽 👈 👆 💪 👆 🈸. **FastAPI** ✔️ 👆 📔 ⏮️ 🔗 💉 ⚙️.

## 📟 📐

👉 🖼 5️⃣📆 😑 🔁. ✔️ 🤯 👈 👥 🌀 💂‍♂, 📊 🏷, 🚙 🔢 &amp; *➡ 🛠️* 🎏 📁.

✋️ 📥 🔑 ☝.

💂‍♂ &amp; 🔗 💉 💩 ✍ 🕐.

&amp; 👆 💪 ⚒ ⚫️ 🏗 👆 💚. &amp; , ✔️ ⚫️ ✍ 🕴 🕐, 👁 🥉. ⏮️ 🌐 💪.

✋️ 👆 💪 ✔️ 💯 🔗 (*➡ 🛠️*) ⚙️ 🎏 💂‍♂ ⚙️.

&amp; 🌐 👫 (⚖️ 🙆 ↔ 👫 👈 👆 💚) 💪 ✊ 📈 🏤-⚙️ 👫 🔗 ⚖️ 🙆 🎏 🔗 👆 ✍.

&amp; 🌐 👉 💯 *➡ 🛠️* 💪 🤪 3️⃣ ⏸:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="30-32"
    {!> ../../../docs_src/security/tutorial002.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="28-30"
    {!> ../../../docs_src/security/tutorial002_py310.py!}
    ```

## 🌃

👆 💪 🔜 🤚 ⏮️ 👩‍💻 🔗 👆 *➡ 🛠️ 🔢*.

👥 ⏪ 😬 📤.

👥 💪 🚮 *➡ 🛠️* 👩‍💻/👩‍💻 🤙 📨 `username` &amp; `password`.

👈 👟 ⏭.
