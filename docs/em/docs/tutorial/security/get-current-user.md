# 🤚 ⏮️ 👩‍💻

⏮️ 📃 💂‍♂ ⚙️ (❔ 🧢 🔛 🔗 💉 ⚙️) 🤝 *➡ 🛠️ 🔢* `token` `str`:

{* ../../docs_src/security/tutorial001.py hl[10] *}

✋️ 👈 🚫 👈 ⚠.

➡️ ⚒ ⚫️ 🤝 👥 ⏮️ 👩‍💻.

## ✍ 👩‍💻 🏷

🥇, ➡️ ✍ Pydantic 👩‍💻 🏷.

🎏 🌌 👥 ⚙️ Pydantic 📣 💪, 👥 💪 ⚙️ ⚫️ 🙆 🙆:

{* ../../docs_src/security/tutorial002.py hl[5,12:16] *}

## ✍ `get_current_user` 🔗

➡️ ✍ 🔗 `get_current_user`.

💭 👈 🔗 💪 ✔️ 🎧-🔗 ❓

`get_current_user` 🔜 ✔️ 🔗 ⏮️ 🎏 `oauth2_scheme` 👥 ✍ ⏭.

🎏 👥 🔨 ⏭ *➡ 🛠️* 🔗, 👆 🆕 🔗 `get_current_user` 🔜 📨 `token` `str` ⚪️➡️ 🎧-🔗 `oauth2_scheme`:

{* ../../docs_src/security/tutorial002.py hl[25] *}

## 🤚 👩‍💻

`get_current_user` 🔜 ⚙️ (❌) 🚙 🔢 👥 ✍, 👈 ✊ 🤝 `str` &amp; 📨 👆 Pydantic `User` 🏷:

{* ../../docs_src/security/tutorial002.py hl[19:22,26:27] *}

## 💉 ⏮️ 👩‍💻

🔜 👥 💪 ⚙️ 🎏 `Depends` ⏮️ 👆 `get_current_user` *➡ 🛠️*:

{* ../../docs_src/security/tutorial002.py hl[31] *}

👀 👈 👥 📣 🆎 `current_user` Pydantic 🏷 `User`.

👉 🔜 ℹ 🇺🇲 🔘 🔢 ⏮️ 🌐 🛠️ &amp; 🆎 ✅.

/// tip

👆 5️⃣📆 💭 👈 📨 💪 📣 ⏮️ Pydantic 🏷.

📥 **FastAPI** 🏆 🚫 🤚 😨 ↩️ 👆 ⚙️ `Depends`.

///

/// check

🌌 👉 🔗 ⚙️ 🏗 ✔ 👥 ✔️ 🎏 🔗 (🎏 "☑") 👈 🌐 📨 `User` 🏷.

👥 🚫 🚫 ✔️ 🕴 1️⃣ 🔗 👈 💪 📨 👈 🆎 💽.

///

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

{* ../../docs_src/security/tutorial002.py hl[30:32] *}

## 🌃

👆 💪 🔜 🤚 ⏮️ 👩‍💻 🔗 👆 *➡ 🛠️ 🔢*.

👥 ⏪ 😬 📤.

👥 💪 🚮 *➡ 🛠️* 👩‍💻/👩‍💻 🤙 📨 `username` &amp; `password`.

👈 👟 ⏭.
