# 🖥 📋

👆 💪 🔬 🖥 📋 🏃 *⏮️* 🛬 📨.

👉 ⚠ 🛠️ 👈 💪 🔨 ⏮️ 📨, ✋️ 👈 👩‍💻 🚫 🤙 ✔️ ⌛ 🛠️ 🏁 ⏭ 📨 📨.

👉 🔌, 🖼:

* 📧 📨 📨 ⏮️ 🎭 🎯:
    * 🔗 📧 💽 &amp; 📨 📧 😑 "🐌" (📚 🥈), 👆 💪 📨 📨 ▶️️ ↖️ &amp; 📨 📧 📨 🖥.
* 🏭 💽:
    * 🖼, ➡️ 💬 👆 📨 📁 👈 🔜 🚶 🔘 🐌 🛠️, 👆 💪 📨 📨 "🚫" (🇺🇸🔍 2️⃣0️⃣2️⃣) &amp; 🛠️ ⚫️ 🖥.

## ⚙️ `BackgroundTasks`

🥇, 🗄 `BackgroundTasks` &amp; 🔬 🔢 👆 *➡ 🛠️ 🔢* ⏮️ 🆎 📄 `BackgroundTasks`:

```Python hl_lines="1  13"
{!../../../docs_src/background_tasks/tutorial001.py!}
```

**FastAPI** 🔜 ✍ 🎚 🆎 `BackgroundTasks` 👆 &amp; 🚶‍♀️ ⚫️ 👈 🔢.

## ✍ 📋 🔢

✍ 🔢 🏃 🖥 📋.

⚫️ 🐩 🔢 👈 💪 📨 🔢.

⚫️ 💪 `async def` ⚖️ 😐 `def` 🔢, **FastAPI** 🔜 💭 ❔ 🍵 ⚫️ ☑.

👉 💼, 📋 🔢 🔜 ✍ 📁 (⚖ 📨 📧).

&amp; ✍ 🛠️ 🚫 ⚙️ `async` &amp; `await`, 👥 🔬 🔢 ⏮️ 😐 `def`:

```Python hl_lines="6-9"
{!../../../docs_src/background_tasks/tutorial001.py!}
```

## 🚮 🖥 📋

🔘 👆 *➡ 🛠️ 🔢*, 🚶‍♀️ 👆 📋 🔢 *🖥 📋* 🎚 ⏮️ 👩‍🔬 `.add_task()`:

```Python hl_lines="14"
{!../../../docs_src/background_tasks/tutorial001.py!}
```

`.add_task()` 📨 ❌:

* 📋 🔢 🏃 🖥 (`write_notification`).
* 🙆 🔁 ❌ 👈 🔜 🚶‍♀️ 📋 🔢 ✔ (`email`).
* 🙆 🇨🇻 ❌ 👈 🔜 🚶‍♀️ 📋 🔢 (`message="some notification"`).

## 🔗 💉

⚙️ `BackgroundTasks` 👷 ⏮️ 🔗 💉 ⚙️, 👆 💪 📣 🔢 🆎 `BackgroundTasks` 💗 🎚: *➡ 🛠️ 🔢*, 🔗 (☑), 🎧-🔗, ♒️.

**FastAPI** 💭 ⚫️❔ 🔠 💼 &amp; ❔ 🏤-⚙️ 🎏 🎚, 👈 🌐 🖥 📋 🔗 👯‍♂️ &amp; 🏃 🖥 ⏮️:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="13  15  22  25"
    {!> ../../../docs_src/background_tasks/tutorial002.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="11  13  20  23"
    {!> ../../../docs_src/background_tasks/tutorial002_py310.py!}
    ```

👉 🖼, 📧 🔜 ✍ `log.txt` 📁 *⏮️* 📨 📨.

🚥 📤 🔢 📨, ⚫️ 🔜 ✍ 🕹 🖥 📋.

&amp; ⤴️ ➕1️⃣ 🖥 📋 🏗 *➡ 🛠️ 🔢* 🔜 ✍ 📧 ⚙️ `email` ➡ 🔢.

## 📡 ℹ

🎓 `BackgroundTasks` 👟 🔗 ⚪️➡️ <a href="https://www.starlette.io/background/" class="external-link" target="_blank">`starlette.background`</a>.

⚫️ 🗄/🔌 🔗 🔘 FastAPI 👈 👆 💪 🗄 ⚫️ ⚪️➡️ `fastapi` &amp; ❎ 😫 🗄 🎛 `BackgroundTask` (🍵 `s` 🔚) ⚪️➡️ `starlette.background`.

🕴 ⚙️ `BackgroundTasks` (&amp; 🚫 `BackgroundTask`), ⚫️ ⤴️ 💪 ⚙️ ⚫️ *➡ 🛠️ 🔢* 🔢 &amp; ✔️ **FastAPI** 🍵 🎂 👆, 💖 🕐❔ ⚙️ `Request` 🎚 🔗.

⚫️ 💪 ⚙️ `BackgroundTask` 😞 FastAPI, ✋️ 👆 ✔️ ✍ 🎚 👆 📟 &amp; 📨 💃 `Response` 🔌 ⚫️.

👆 💪 👀 🌖 ℹ <a href="https://www.starlette.io/background/" class="external-link" target="_blank">💃 🛂 🩺 🖥 📋</a>.

## ⚠

🚥 👆 💪 🎭 🏋️ 🖥 📊 &amp; 👆 🚫 🎯 💪 ⚫️ 🏃 🎏 🛠️ (🖼, 👆 🚫 💪 💰 💾, 🔢, ♒️), 👆 💪 💰 ⚪️➡️ ⚙️ 🎏 🦏 🧰 💖 <a href="https://docs.celeryq.dev" class="external-link" target="_blank">🥒</a>.

👫 😑 🚚 🌖 🏗 📳, 📧/👨‍🏭 📤 👨‍💼, 💖 ✳ ⚖️ ✳, ✋️ 👫 ✔ 👆 🏃 🖥 📋 💗 🛠️, &amp; ✴️, 💗 💽.

👀 🖼, ✅ [🏗 🚂](../project-generation.md){.internal-link target=_blank}, 👫 🌐 🔌 🥒 ⏪ 📶.

✋️ 🚥 👆 💪 🔐 🔢 &amp; 🎚 ⚪️➡️ 🎏 **FastAPI** 📱, ⚖️ 👆 💪 🎭 🤪 🖥 📋 (💖 📨 📧 📨), 👆 💪 🎯 ⚙️ `BackgroundTasks`.

## 🌃

🗄 &amp; ⚙️ `BackgroundTasks` ⏮️ 🔢 *➡ 🛠️ 🔢* &amp; 🔗 🚮 🖥 📋.
