# 🏃 💽 ❎ - Uvicorn

👑 👜 👆 💪 🏃 **FastAPI** 🈸 🛰 💽 🎰 🔫 💽 📋 💖 **Uvicorn**.

📤 3️⃣ 👑 🎛:

* <a href="https://www.uvicorn.dev/" class="external-link" target="_blank">Uvicorn</a>: ↕ 🎭 🔫 💽.
* <a href="https://hypercorn.readthedocs.io/" class="external-link" target="_blank">Hypercorn</a>: 🔫 💽 🔗 ⏮️ 🇺🇸🔍/2️⃣ &amp; 🎻 👪 🎏 ⚒.
* <a href="https://github.com/django/daphne" class="external-link" target="_blank">👸</a>: 🔫 💽 🏗 ✳ 📻.

## 💽 🎰 &amp; 💽 📋

📤 🤪 ℹ 🔃 📛 ✔️ 🤯. 👶

🔤 "**💽**" 🛎 ⚙️ 🔗 👯‍♂️ 🛰/☁ 💻 (⚛ ⚖️ 🕹 🎰) &amp; 📋 👈 🏃‍♂ 🔛 👈 🎰 (✅ Uvicorn).

✔️ 👈 🤯 🕐❔ 👆 ✍ "💽" 🏢, ⚫️ 💪 🔗 1️⃣ 📚 2️⃣ 👜.

🕐❔ 🔗 🛰 🎰, ⚫️ ⚠ 🤙 ⚫️ **💽**, ✋️ **🎰**, **💾** (🕹 🎰), **🕸**. 👈 🌐 🔗 🆎 🛰 🎰, 🛎 🏃‍♂ 💾, 🌐❔ 👆 🏃 📋.

## ❎ 💽 📋

👆 💪 ❎ 🔫 🔗 💽 ⏮️:

//// tab | Uvicorn

* <a href="https://www.uvicorn.dev/" class="external-link" target="_blank">Uvicorn</a>, 🌩-⏩ 🔫 💽, 🏗 🔛 uvloop &amp; httptool.

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

/// tip

❎ `standard`, Uvicorn 🔜 ❎ &amp; ⚙️ 👍 ➕ 🔗.

👈 ✅ `uvloop`, ↕-🎭 💧-♻ `asyncio`, 👈 🚚 🦏 🛠️ 🎭 📈.

///

////

//// tab | Hypercorn

* <a href="https://github.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>, 🔫 💽 🔗 ⏮️ 🇺🇸🔍/2️⃣.

<div class="termy">

```console
$ pip install hypercorn

---> 100%
```

</div>

...⚖️ 🙆 🎏 🔫 💽.

////

## 🏃 💽 📋

👆 💪 ⤴️ 🏃 👆 🈸 🎏 🌌 👆 ✔️ ⌛ 🔰, ✋️ 🍵 `--reload` 🎛, ✅:

//// tab | Uvicorn

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 80

<span style="color: green;">INFO</span>:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

</div>

////

//// tab | Hypercorn

<div class="termy">

```console
$ hypercorn main:app --bind 0.0.0.0:80

Running on 0.0.0.0:8080 over http (CTRL + C to quit)
```

</div>

////

/// warning

💭 ❎ `--reload` 🎛 🚥 👆 ⚙️ ⚫️.

 `--reload` 🎛 🍴 🌅 🌅 ℹ, 🌅 ⚠, ♒️.

⚫️ ℹ 📚 ⏮️ **🛠️**, ✋️ 👆 **🚫🔜 🚫** ⚙️ ⚫️ **🏭**.

///

## Hypercorn ⏮️ 🎻

💃 &amp; **FastAPI** ⚓️ 🔛 <a href="https://anyio.readthedocs.io/en/stable/" class="external-link" target="_blank">AnyIO</a>, ❔ ⚒ 👫 🔗 ⏮️ 👯‍♂️ 🐍 🐩 🗃 <a href="https://docs.python.org/3/library/asyncio-task.html" class="external-link" target="_blank">✳</a> &amp; <a href="https://trio.readthedocs.io/en/stable/" class="external-link" target="_blank">🎻</a>.

👐, Uvicorn ⏳ 🕴 🔗 ⏮️ ✳, &amp; ⚫️ 🛎 ⚙️ <a href="https://github.com/MagicStack/uvloop" class="external-link" target="_blank">`uvloop`</a>, ↕-🎭 💧-♻ `asyncio`.

✋️ 🚥 👆 💚 🔗 ⚙️ **🎻**, ⤴️ 👆 💪 ⚙️ **Hypercorn** ⚫️ 🐕‍🦺 ⚫️. 👶

### ❎ Hypercorn ⏮️ 🎻

🥇 👆 💪 ❎ Hypercorn ⏮️ 🎻 🐕‍🦺:

<div class="termy">

```console
$ pip install "hypercorn[trio]"
---> 100%
```

</div>

### 🏃 ⏮️ 🎻

⤴️ 👆 💪 🚶‍♀️ 📋 ⏸ 🎛 `--worker-class` ⏮️ 💲 `trio`:

<div class="termy">

```console
$ hypercorn main:app --worker-class trio
```

</div>

&amp; 👈 🔜 ▶️ Hypercorn ⏮️ 👆 📱 ⚙️ 🎻 👩‍💻.

🔜 👆 💪 ⚙️ 🎻 🔘 👆 📱. ⚖️ 👍, 👆 💪 ⚙️ AnyIO, 🚧 👆 📟 🔗 ⏮️ 👯‍♂️ 🎻 &amp; ✳. 👶

## 🛠️ 🔧

👫 🖼 🏃 💽 📋 (📧.Ⓜ Uvicorn), ▶️ **👁 🛠️**, 👂 🔛 🌐 📢 (`0.0.0.0`) 🔛 🔁 ⛴ (✅ `80`).

👉 🔰 💭. ✋️ 👆 🔜 🎲 💚 ✊ 💅 🌖 👜, 💖:

* 💂‍♂ - 🇺🇸🔍
* 🏃‍♂ 🔛 🕴
* ⏏
* 🧬 (🔢 🛠️ 🏃)
* 💾
* ⏮️ 🔁 ⏭ ▶️

👤 🔜 💬 👆 🌅 🔃 🔠 👫 🔧, ❔ 💭 🔃 👫, &amp; 🧱 🖼 ⏮️ 🎛 🍵 👫 ⏭ 📃. 👶
