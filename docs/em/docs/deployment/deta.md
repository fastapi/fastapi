# 🛠️ FastAPI 🔛 🪔

👉 📄 👆 🔜 💡 ❔ 💪 🛠️ **FastAPI** 🈸 🔛 <a href="https://www.deta.sh/?ref=fastapi" class="external-link" target="_blank">🪔</a> ⚙️ 🆓 📄. 👶

⚫️ 🔜 ✊ 👆 🔃 **1️⃣0️⃣ ⏲**.

!!! info
    <a href="https://www.deta.sh/?ref=fastapi" class="external-link" target="_blank">🪔</a> **FastAPI** 💰. 👶

## 🔰 **FastAPI** 📱

* ✍ 📁 👆 📱, 🖼, `./fastapideta/` &amp; ⛔ 🔘 ⚫️.

### FastAPI 📟

* ✍ `main.py` 📁 ⏮️:

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

### 📄

🔜, 🎏 📁 ✍ 📁 `requirements.txt` ⏮️:

```text
fastapi
```

!!! tip
    👆 🚫 💪 ❎ Uvicorn 🛠️ 🔛 🪔, 👐 👆 🔜 🎲 💚 ❎ ⚫️ 🌐 💯 👆 📱.

### 📁 📊

👆 🔜 🔜 ✔️ 1️⃣ 📁 `./fastapideta/` ⏮️ 2️⃣ 📁:

```
.
└── main.py
└── requirements.txt
```

## ✍ 🆓 🪔 🏧

🔜 ✍ <a href="https://www.deta.sh/?ref=fastapi" class="external-link" target="_blank">🆓 🏧 🔛 🪔</a>, 👆 💪 📧 &amp; 🔐.

👆 🚫 💪 💳.

## ❎ ✳

🕐 👆 ✔️ 👆 🏧, ❎ 🪔 <abbr title="Command Line Interface application">✳</abbr>:

=== "💾, 🇸🇻"

    <div class="termy">

    ```console
    $ curl -fsSL https://get.deta.dev/cli.sh | sh
    ```

    </div>

=== "🚪 📋"

    <div class="termy">

    ```console
    $ iwr https://get.deta.dev/cli.ps1 -useb | iex
    ```

    </div>

⏮️ ❎ ⚫️, 📂 🆕 📶 👈 ❎ ✳ 🔍.

🆕 📶, ✔ 👈 ⚫️ ☑ ❎ ⏮️:

<div class="termy">

```console
$ deta --help

Deta command line interface for managing deta micros.
Complete documentation available at https://docs.deta.sh

Usage:
  deta [flags]
  deta [command]

Available Commands:
  auth        Change auth settings for a deta micro

...
```

</div>

!!! tip
    🚥 👆 ✔️ ⚠ ❎ ✳, ✅ <a href="https://docs.deta.sh/docs/micros/getting_started?ref=fastapi" class="external-link" target="_blank">🛂 🪔 🩺</a>.

## 💳 ⏮️ ✳

🔜 💳 🪔 ⚪️➡️ ✳ ⏮️:

<div class="termy">

```console
$ deta login

Please, log in from the web page. Waiting..
Logged in successfully.
```

</div>

👉 🔜 📂 🕸 🖥 &amp; 🔓 🔁.

## 🛠️ ⏮️ 🪔

⏭, 🛠️ 👆 🈸 ⏮️ 🪔 ✳:

<div class="termy">

```console
$ deta new

Successfully created a new micro

// Notice the "endpoint" 🔍

{
    "name": "fastapideta",
    "runtime": "python3.7",
    "endpoint": "https://qltnci.deta.dev",
    "visor": "enabled",
    "http_auth": "enabled"
}

Adding dependencies...


---> 100%


Successfully installed fastapi-0.61.1 pydantic-1.7.2 starlette-0.13.6
```

</div>

👆 🔜 👀 🎻 📧 🎏:

```JSON hl_lines="4"
{
        "name": "fastapideta",
        "runtime": "python3.7",
        "endpoint": "https://qltnci.deta.dev",
        "visor": "enabled",
        "http_auth": "enabled"
}
```

!!! tip
    👆 🛠️ 🔜 ✔️ 🎏 `"endpoint"` 📛.

## ✅ ⚫️

🔜 📂 👆 🖥 👆 `endpoint` 📛. 🖼 🔛 ⚫️ `https://qltnci.deta.dev`, ✋️ 👆 🔜 🎏.

👆 🔜 👀 🎻 📨 ⚪️➡️ 👆 FastAPI 📱:

```JSON
{
    "Hello": "World"
}
```

&amp; 🔜 🚶 `/docs` 👆 🛠️, 🖼 🔛 ⚫️ 🔜 `https://qltnci.deta.dev/docs`.

⚫️ 🔜 🎦 👆 🩺 💖:

<img src="/img/deployment/deta/image01.png">

## 🛠️ 📢 🔐

🔢, 🪔 🔜 🍵 🤝 ⚙️ 🍪 👆 🏧.

✋️ 🕐 👆 🔜, 👆 💪 ⚒ ⚫️ 📢 ⏮️:

<div class="termy">

```console
$ deta auth disable

Successfully disabled http auth
```

</div>

🔜 👆 💪 💰 👈 📛 ⏮️ 🙆 &amp; 👫 🔜 💪 🔐 👆 🛠️. 👶

## 🇺🇸🔍

㊗ ❗ 👆 🛠️ 👆 FastAPI 📱 🪔 ❗ 👶 👶

, 👀 👈 🪔 ☑ 🍵 🇺🇸🔍 👆, 👆 🚫 ✔️ ✊ 💅 👈 &amp; 💪 💭 👈 👆 👩‍💻 🔜 ✔️ 🔐 🗜 🔗. 👶 👶

## ✅ 🕶

⚪️➡️ 👆 🩺 🎚 (👫 🔜 📛 💖 `https://qltnci.deta.dev/docs`) 📨 📨 👆 *➡ 🛠️* `/items/{item_id}`.

🖼 ⏮️ 🆔 `5`.

🔜 🚶 <a href="https://web.deta.sh/" class="external-link" target="_blank">https://web.deta.sh</a>.

👆 🔜 👀 📤 📄 ◀️ 🤙 <abbr title="it comes from Micro(server)">"◾"</abbr> ⏮️ 🔠 👆 📱.

👆 🔜 👀 📑 ⏮️ "ℹ", &amp; 📑 "🕶", 🚶 📑 "🕶".

📤 👆 💪 ✔ ⏮️ 📨 📨 👆 📱.

👆 💪 ✍ 👫 &amp; 🏤-🤾 👫.

<img src="/img/deployment/deta/image02.png">

## 💡 🌅

☝, 👆 🔜 🎲 💚 🏪 💽 👆 📱 🌌 👈 😣 🔘 🕰. 👈 👆 💪 ⚙️ <a href="https://docs.deta.sh/docs/base/py_tutorial?ref=fastapi" class="external-link" target="_blank">🪔 🧢</a>, ⚫️ ✔️ 👍 **🆓 🎚**.

👆 💪 ✍ 🌅 <a href="https://docs.deta.sh?ref=fastapi" class="external-link" target="_blank">🪔 🩺</a>.

## 🛠️ 🔧

👟 🔙 🔧 👥 🔬 [🛠️ 🔧](./concepts.md){.internal-link target=_blank}, 📥 ❔ 🔠 👫 🔜 🍵 ⏮️ 🪔:

* **🇺🇸🔍**: 🍵 🪔, 👫 🔜 🤝 👆 📁 &amp; 🍵 🇺🇸🔍 🔁.
* **🏃‍♂ 🔛 🕴**: 🍵 🪔, 🍕 👫 🐕‍🦺.
* **⏏**: 🍵 🪔, 🍕 👫 🐕‍🦺.
* **🧬**: 🍵 🪔, 🍕 👫 🐕‍🦺.
* **💾**: 📉 🔁 🪔, 👆 💪 📧 👫 📈 ⚫️.
* **⏮️ 🔁 ⏭ ▶️**: 🚫 🔗 🐕‍🦺, 👆 💪 ⚒ ⚫️ 👷 ⏮️ 👫 💾 ⚙️ ⚖️ 🌖 ✍.

!!! note
    🪔 🔧 ⚒ ⚫️ ⏩ (&amp; 🆓) 🛠️ 🙅 🈸 🔜.

    ⚫️ 💪 📉 📚 ⚙️ 💼, ✋️ 🎏 🕰, ⚫️ 🚫 🐕‍🦺 🎏, 💖 ⚙️ 🔢 💽 (↖️ ⚪️➡️ 🪔 👍 ☁ 💽 ⚙️), 🛃 🕹 🎰, ♒️.

    👆 💪 ✍ 🌅 ℹ <a href="https://docs.deta.sh/docs/micros/about/" class="external-link" target="_blank">🪔 🩺</a> 👀 🚥 ⚫️ ▶️️ ⚒ 👆.
