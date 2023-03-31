# 💽 👨‍🏭 - 🐁 ⏮️ Uvicorn

➡️ ✅ 🔙 👈 🛠️ 🔧 ⚪️➡️ ⏭:

* 💂‍♂ - 🇺🇸🔍
* 🏃‍♂ 🔛 🕴
* ⏏
* **🧬 (🔢 🛠️ 🏃)**
* 💾
* ⏮️ 🔁 ⏭ ▶️

🆙 👉 ☝, ⏮️ 🌐 🔰 🩺, 👆 ✔️ 🎲 🏃‍♂ **💽 📋** 💖 Uvicorn, 🏃‍♂ **👁 🛠️**.

🕐❔ 🛠️ 🈸 👆 🔜 🎲 💚 ✔️ **🧬 🛠️** ✊ 📈 **💗 🐚** &amp; 💪 🍵 🌅 📨.

👆 👀 ⏮️ 📃 🔃 [🛠️ 🔧](./concepts.md){.internal-link target=_blank}, 📤 💗 🎛 👆 💪 ⚙️.

📥 👤 🔜 🎦 👆 ❔ ⚙️ <a href="https://gunicorn.org/" class="external-link" target="_blank">**🐁**</a> ⏮️ **Uvicorn 👨‍🏭 🛠️**.

!!! info
    🚥 👆 ⚙️ 📦, 🖼 ⏮️ ☁ ⚖️ Kubernete, 👤 🔜 💬 👆 🌅 🔃 👈 ⏭ 📃: [FastAPI 📦 - ☁](./docker.md){.internal-link target=_blank}.

    🎯, 🕐❔ 🏃 🔛 **Kubernete** 👆 🔜 🎲 **🚫** 💚 ⚙️ 🐁 &amp; ↩️ 🏃 **👁 Uvicorn 🛠️ 📍 📦**, ✋️ 👤 🔜 💬 👆 🔃 ⚫️ ⏪ 👈 📃.

## 🐁 ⏮️ Uvicorn 👨‍🏭

**🐁** ✴️ 🈸 💽 ⚙️ **🇨🇻 🐩**. 👈 ⛓ 👈 🐁 💪 🍦 🈸 💖 🏺 &amp; ✳. 🐁 ⚫️ 🚫 🔗 ⏮️ **FastAPI**, FastAPI ⚙️ 🆕 **<a href="https://asgi.readthedocs.io/en/latest/" class="external-link" target="_blank">🔫 🐩</a>**.

✋️ 🐁 🐕‍🦺 👷 **🛠️ 👨‍💼** &amp; 🤝 👩‍💻 💬 ⚫️ ❔ 🎯 **👨‍🏭 🛠️ 🎓** ⚙️. ⤴️ 🐁 🔜 ▶️ 1️⃣ ⚖️ 🌖 **👨‍🏭 🛠️** ⚙️ 👈 🎓.

&amp; **Uvicorn** ✔️ **🐁-🔗 👨‍🏭 🎓**.

⚙️ 👈 🌀, 🐁 🔜 🚫 **🛠️ 👨‍💼**, 👂 🔛 **⛴** &amp; **📢**. &amp; ⚫️ 🔜 **📶** 📻 👨‍🏭 🛠️ 🏃 **Uvicorn 🎓**.

&amp; ⤴️ 🐁-🔗 **Uvicorn 👨‍🏭** 🎓 🔜 🈚 🏭 📊 📨 🐁 🔫 🐩 FastAPI ⚙️ ⚫️.

## ❎ 🐁 &amp; Uvicorn

<div class="termy">

```console
$ pip install "uvicorn[standard]" gunicorn

---> 100%
```

</div>

👈 🔜 ❎ 👯‍♂️ Uvicorn ⏮️ `standard` ➕ 📦 (🤚 ↕ 🎭) &amp; 🐁.

## 🏃 🐁 ⏮️ Uvicorn 👨‍🏭

⤴️ 👆 💪 🏃 🐁 ⏮️:

<div class="termy">

```console
$ gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80

[19499] [INFO] Starting gunicorn 20.1.0
[19499] [INFO] Listening at: http://0.0.0.0:80 (19499)
[19499] [INFO] Using worker: uvicorn.workers.UvicornWorker
[19511] [INFO] Booting worker with pid: 19511
[19513] [INFO] Booting worker with pid: 19513
[19514] [INFO] Booting worker with pid: 19514
[19515] [INFO] Booting worker with pid: 19515
[19511] [INFO] Started server process [19511]
[19511] [INFO] Waiting for application startup.
[19511] [INFO] Application startup complete.
[19513] [INFO] Started server process [19513]
[19513] [INFO] Waiting for application startup.
[19513] [INFO] Application startup complete.
[19514] [INFO] Started server process [19514]
[19514] [INFO] Waiting for application startup.
[19514] [INFO] Application startup complete.
[19515] [INFO] Started server process [19515]
[19515] [INFO] Waiting for application startup.
[19515] [INFO] Application startup complete.
```

</div>

➡️ 👀 ⚫️❔ 🔠 👈 🎛 ⛓:

* `main:app`: 👉 🎏 ❕ ⚙️ Uvicorn, `main` ⛓ 🐍 🕹 📛 "`main`",, 📁 `main.py`. &amp; `app` 📛 🔢 👈 **FastAPI** 🈸.
    * 👆 💪 🌈 👈 `main:app` 🌓 🐍 `import` 📄 💖:

        ```Python
        from main import app
        ```

    * , ❤ `main:app` 🔜 🌓 🐍 `import` 🍕 `from main import app`.
* `--workers`: 🔢 👨‍🏭 🛠️ ⚙️, 🔠 🔜 🏃 Uvicorn 👨‍🏭, 👉 💼, 4️⃣ 👨‍🏭.
* `--worker-class`: 🐁-🔗 👨‍🏭 🎓 ⚙️ 👨‍🏭 🛠️.
    * 📥 👥 🚶‍♀️ 🎓 👈 🐁 💪 🗄 &amp; ⚙️ ⏮️:

        ```Python
        import uvicorn.workers.UvicornWorker
        ```

* `--bind`: 👉 💬 🐁 📢 &amp; ⛴ 👂, ⚙️ ❤ (`:`) 🎏 📢 &amp; ⛴.
    * 🚥 👆 🏃‍♂ Uvicorn 🔗, ↩️ `--bind 0.0.0.0:80` (🐁 🎛) 👆 🔜 ⚙️ `--host 0.0.0.0` &amp; `--port 80`.

🔢, 👆 💪 👀 👈 ⚫️ 🎦 **🕹** (🛠️ 🆔) 🔠 🛠️ (⚫️ 🔢).

👆 💪 👀 👈:

* 🐁 **🛠️ 👨‍💼** ▶️ ⏮️ 🕹 `19499` (👆 💼 ⚫️ 🔜 🎏 🔢).
* ⤴️ ⚫️ ▶️ `Listening at: http://0.0.0.0:80`.
* ⤴️ ⚫️ 🔍 👈 ⚫️ ✔️ ⚙️ 👨‍🏭 🎓 `uvicorn.workers.UvicornWorker`.
*  &amp; ⤴️ ⚫️ ▶️ **4️⃣ 👨‍🏭**, 🔠 ⏮️ 🚮 👍 🕹: `19511`, `19513`, `19514`, &amp; `19515`.

🐁 🔜 ✊ 💅 🛠️ **☠️ 🛠️** &amp; **🔁** 🆕 🕐 🚥 💚 🚧 🔢 👨‍🏭. 👈 ℹ 🍕 ⏮️ **⏏** 🔧 ⚪️➡️ 📇 🔛.

👐, 👆 🔜 🎲 💚 ✔️ 🕳 🏞 ⚒ 💭 **⏏ 🐁** 🚥 💪, &amp; **🏃 ⚫️ 🔛 🕴**, ♒️.

## Uvicorn ⏮️ 👨‍🏭

Uvicorn ✔️ 🎛 ▶️ &amp; 🏃 📚 **👨‍🏭 🛠️**.

👐, 🔜, Uvicorn 🛠️ 🚚 👨‍🏭 🛠️ 🌅 📉 🌘 🐁. , 🚥 👆 💚 ✔️ 🛠️ 👨‍💼 👉 🎚 (🐍 🎚), ⤴️ ⚫️ 💪 👍 🔄 ⏮️ 🐁 🛠️ 👨‍💼.

🙆 💼, 👆 🔜 🏃 ⚫️ 💖 👉:

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
<font color="#A6E22E">INFO</font>:     Uvicorn running on <b>http://0.0.0.0:8080</b> (Press CTRL+C to quit)
<font color="#A6E22E">INFO</font>:     Started parent process [<font color="#A1EFE4"><b>27365</b></font>]
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27368</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27369</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27370</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27367</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
```

</div>

🕴 🆕 🎛 📥 `--workers` 💬 Uvicorn ▶️ 4️⃣ 👨‍🏭 🛠️.

👆 💪 👀 👈 ⚫️ 🎦 **🕹** 🔠 🛠️, `27365` 👪 🛠️ (👉 **🛠️ 👨‍💼**) &amp; 1️⃣ 🔠 👨‍🏭 🛠️: `27368`, `27369`, `27370`, &amp; `27367`.

## 🛠️ 🔧

📥 👆 👀 ❔ ⚙️ **🐁** (⚖️ Uvicorn) 🛠️ **Uvicorn 👨‍🏭 🛠️** **🔁** 🛠️ 🈸, ✊ 📈 **💗 🐚** 💽, &amp; 💪 🍦 **🌅 📨**.

⚪️➡️ 📇 🛠️ 🔧 ⚪️➡️ 🔛, ⚙️ 👨‍🏭 🔜 ✴️ ℹ ⏮️ **🧬** 🍕, &amp; 🐥 🍖 ⏮️ **⏏**, ✋️ 👆 💪 ✊ 💅 🎏:

* **💂‍♂ - 🇺🇸🔍**
* **🏃‍♂ 🔛 🕴**
* ***⏏***
* 🧬 (🔢 🛠️ 🏃)
* **💾**
* **⏮️ 🔁 ⏭ ▶️**

## 📦 &amp; ☁

⏭ 📃 🔃 [FastAPI 📦 - ☁](./docker.md){.internal-link target=_blank} 👤 🔜 💬 🎛 👆 💪 ⚙️ 🍵 🎏 **🛠️ 🔧**.

👤 🔜 🎦 👆 **🛂 ☁ 🖼** 👈 🔌 **🐁 ⏮️ Uvicorn 👨‍🏭** &amp; 🔢 📳 👈 💪 ⚠ 🙅 💼.

📤 👤 🔜 🎦 👆 ❔ **🏗 👆 👍 🖼 ⚪️➡️ 🖌** 🏃 👁 Uvicorn 🛠️ (🍵 🐁). ⚫️ 🙅 🛠️ &amp; 🎲 ⚫️❔ 👆 🔜 💚 🕐❔ ⚙️ 📎 📦 🧾 ⚙️ 💖 **Kubernete**.

## 🌃

👆 💪 ⚙️ **🐁** (⚖️ Uvicorn) 🛠️ 👨‍💼 ⏮️ Uvicorn 👨‍🏭 ✊ 📈 **👁-🐚 💽**, 🏃 **💗 🛠️ 🔗**.

👆 💪 ⚙️ 👉 🧰 &amp; 💭 🚥 👆 ⚒ 🆙 **👆 👍 🛠️ ⚙️** ⏪ ✊ 💅 🎏 🛠️ 🔧 👆.

✅ 👅 ⏭ 📃 💡 🔃 **FastAPI** ⏮️ 📦 (✅ ☁ &amp; Kubernete). 👆 🔜 👀 👈 👈 🧰 ✔️ 🙅 🌌 ❎ 🎏 **🛠️ 🔧** 👍. 👶
