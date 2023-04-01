# 🎚 🔢

👆 💪 🔬 🎚 🔢 🎏 🌌 👆 🔬 `Query`, `Path` &amp; `Cookie` 🔢.

## 🗄 `Header`

🥇 🗄 `Header`:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="3"
    {!> ../../../docs_src/header_params/tutorial001.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="1"
    {!> ../../../docs_src/header_params/tutorial001_py310.py!}
    ```

## 📣 `Header` 🔢

⤴️ 📣 🎚 🔢 ⚙️ 🎏 📊 ⏮️ `Path`, `Query` &amp; `Cookie`.

🥇 💲 🔢 💲, 👆 💪 🚶‍♀️ 🌐 ➕ 🔬 ⚖️ ✍ 🔢:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="9"
    {!> ../../../docs_src/header_params/tutorial001.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="7"
    {!> ../../../docs_src/header_params/tutorial001_py310.py!}
    ```

!!! note "📡 ℹ"
    `Header` "👭" 🎓 `Path`, `Query` &amp; `Cookie`. ⚫️ 😖 ⚪️➡️ 🎏 ⚠ `Param` 🎓.

    ✋️ 💭 👈 🕐❔ 👆 🗄 `Query`, `Path`, `Header`, &amp; 🎏 ⚪️➡️ `fastapi`, 👈 🤙 🔢 👈 📨 🎁 🎓.

!!! info
    📣 🎚, 👆 💪 ⚙️ `Header`, ↩️ ⏪ 🔢 🔜 🔬 🔢 🔢.

## 🏧 🛠️

`Header` ✔️ 🐥 ➕ 🛠️ 🔛 🔝 ⚫️❔ `Path`, `Query` &amp; `Cookie` 🚚.

🌅 🐩 🎚 🎏 "🔠" 🦹, 💭 "➖ 🔣" (`-`).

✋️ 🔢 💖 `user-agent` ❌ 🐍.

, 🔢, `Header` 🔜 🗜 🔢 📛 🦹 ⚪️➡️ 🎦 (`_`) 🔠 (`-`) ⚗ &amp; 📄 🎚.

, 🇺🇸🔍 🎚 💼-😛,, 👆 💪 📣 👫 ⏮️ 🐩 🐍 👗 (💭 "🔡").

, 👆 💪 ⚙️ `user_agent` 👆 🛎 🔜 🐍 📟, ↩️ 💆‍♂ 🎯 🥇 🔤 `User_Agent` ⚖️ 🕳 🎏.

🚥 🤔 👆 💪 ❎ 🏧 🛠️ 🎦 🔠, ⚒ 🔢 `convert_underscores` `Header` `False`:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="10"
    {!> ../../../docs_src/header_params/tutorial002.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="8"
    {!> ../../../docs_src/header_params/tutorial002_py310.py!}
    ```

!!! warning
    ⏭ ⚒ `convert_underscores` `False`, 🐻 🤯 👈 🇺🇸🔍 🗳 &amp; 💽 / ⚙️ 🎚 ⏮️ 🎦.

## ❎ 🎚

⚫️ 💪 📨 ❎ 🎚. 👈 ⛓, 🎏 🎚 ⏮️ 💗 💲.

👆 💪 🔬 👈 💼 ⚙️ 📇 🆎 📄.

👆 🔜 📨 🌐 💲 ⚪️➡️ ❎ 🎚 🐍 `list`.

🖼, 📣 🎚 `X-Token` 👈 💪 😑 🌅 🌘 🕐, 👆 💪 ✍:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="9"
    {!> ../../../docs_src/header_params/tutorial003.py!}
    ```

=== "🐍 3️⃣.9️⃣ &amp; 🔛"

    ```Python hl_lines="9"
    {!> ../../../docs_src/header_params/tutorial003_py39.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="7"
    {!> ../../../docs_src/header_params/tutorial003_py310.py!}
    ```

🚥 👆 🔗 ⏮️ 👈 *➡ 🛠️* 📨 2️⃣ 🇺🇸🔍 🎚 💖:

```
X-Token: foo
X-Token: bar
```

📨 🔜 💖:

```JSON
{
    "X-Token values": [
        "bar",
        "foo"
    ]
}
```

## 🌃

📣 🎚 ⏮️ `Header`, ⚙️ 🎏 ⚠ ⚓ `Query`, `Path` &amp; `Cookie`.

&amp; 🚫 😟 🔃 🎦 👆 🔢, **FastAPI** 🔜 ✊ 💅 🏭 👫.
