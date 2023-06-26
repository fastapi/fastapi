# 🛠️

👆 💪 🔗 🕹 👆 👨‍🎨, 🖼 ⏮️ 🎙 🎙 📟 ⚖️ 🗒.

## 🤙 `uvicorn`

👆 FastAPI 🈸, 🗄 &amp; 🏃 `uvicorn` 🔗:

```Python hl_lines="1  15"
{!../../../docs_src/debugging/tutorial001.py!}
```

### 🔃 `__name__ == "__main__"`

👑 🎯 `__name__ == "__main__"` ✔️ 📟 👈 🛠️ 🕐❔ 👆 📁 🤙 ⏮️:

<div class="termy">

```console
$ python myapp.py
```

</div>

✋️ 🚫 🤙 🕐❔ ➕1️⃣ 📁 🗄 ⚫️, 💖:

```Python
from myapp import app
```

#### 🌅 ℹ

➡️ 💬 👆 📁 🌟 `myapp.py`.

🚥 👆 🏃 ⚫️ ⏮️:

<div class="termy">

```console
$ python myapp.py
```

</div>

⤴️ 🔗 🔢 `__name__` 👆 📁, ✍ 🔁 🐍, 🔜 ✔️ 💲 🎻 `"__main__"`.

, 📄:

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

🔜 🏃.

---

👉 🏆 🚫 🔨 🚥 👆 🗄 👈 🕹 (📁).

, 🚥 👆 ✔️ ➕1️⃣ 📁 `importer.py` ⏮️:

```Python
from myapp import app

# Some more code
```

👈 💼, 🏧 🔢 🔘 `myapp.py` 🔜 🚫 ✔️ 🔢 `__name__` ⏮️ 💲 `"__main__"`.

, ⏸:

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

🔜 🚫 🛠️.

!!! info
    🌅 ℹ, ✅ <a href="https://docs.python.org/3/library/__main__.html" class="external-link" target="_blank">🛂 🐍 🩺</a>.

## 🏃 👆 📟 ⏮️ 👆 🕹

↩️ 👆 🏃 Uvicorn 💽 🔗 ⚪️➡️ 👆 📟, 👆 💪 🤙 👆 🐍 📋 (👆 FastAPI 🈸) 🔗 ⚪️➡️ 🕹.

---

🖼, 🎙 🎙 📟, 👆 💪:

* 🚶 "ℹ" 🎛.
* "🚮 📳...".
* 🖊 "🐍"
* 🏃 🕹 ⏮️ 🎛 "`Python: Current File (Integrated Terminal)`".

⚫️ 🔜 ⤴️ ▶️ 💽 ⏮️ 👆 **FastAPI** 📟, ⛔️ 👆 0️⃣, ♒️.

📥 ❔ ⚫️ 💪 👀:

<img src="/img/tutorial/debugging/image01.png">

---

🚥 👆 ⚙️ 🗒, 👆 💪:

* 📂 "🏃" 🍣.
* 🖊 🎛 "ℹ...".
* ⤴️ 🔑 🍣 🎦 🆙.
* 🖊 📁 ℹ (👉 💼, `main.py`).

⚫️ 🔜 ⤴️ ▶️ 💽 ⏮️ 👆 **FastAPI** 📟, ⛔️ 👆 0️⃣, ♒️.

📥 ❔ ⚫️ 💪 👀:

<img src="/img/tutorial/debugging/image02.png">
