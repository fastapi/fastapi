# FastAPI 📦 - ☁

🕐❔ 🛠️ FastAPI 🈸 ⚠ 🎯 🏗 **💾 📦 🖼**. ⚫️ 🛎 🔨 ⚙️ <a href="https://www.docker.com/" class="external-link" target="_blank">**☁**</a>. 👆 💪 ⤴️ 🛠️ 👈 📦 🖼 1️⃣ 👩‍❤‍👨 💪 🌌.

⚙️ 💾 📦 ✔️ 📚 📈 ✅ **💂‍♂**, **🔬**, **🦁**, &amp; 🎏.

!!! tip
    🏃 &amp; ⏪ 💭 👉 💩 ❓ 🦘 [`Dockerfile` 🔛 👶](#build-a-docker-image-for-fastapi).

<details>
<summary>📁 🎮 👶</summary>

```Dockerfile
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]
```

</details>

## ⚫️❔ 📦

📦 (✴️ 💾 📦) 📶 **💿** 🌌 📦 🈸 ✅ 🌐 👫 🔗 &amp; 💪 📁 ⏪ 🚧 👫 ❎ ⚪️➡️ 🎏 📦 (🎏 🈸 ⚖️ 🦲) 🎏 ⚙️.

💾 📦 🏃 ⚙️ 🎏 💾 💾 🦠 (🎰, 🕹 🎰, ☁ 💽, ♒️). 👉 ⛓ 👈 👫 📶 💿 (🔬 🌕 🕹 🎰 👍 🎂 🏃‍♂ ⚙️).

👉 🌌, 📦 🍴 **🐥 ℹ**, 💸 ⭐ 🏃‍♂ 🛠️ 🔗 (🕹 🎰 🔜 🍴 🌅 🌅).

📦 ✔️ 👫 👍 **❎** 🏃‍♂ 🛠️ (🛎 1️⃣ 🛠️), 📁 ⚙️, &amp; 🕸, 🔬 🛠️, 💂‍♂, 🛠️, ♒️.

## ⚫️❔ 📦 🖼

**📦** 🏃 ⚪️➡️ **📦 🖼**.

📦 🖼 **🎻** ⏬ 🌐 📁, 🌐 🔢, &amp; 🔢 📋/📋 👈 🔜 🎁 📦. **🎻** 📥 ⛓ 👈 📦 **🖼** 🚫 🏃, ⚫️ 🚫 ➖ 🛠️, ⚫️ 🕴 📦 📁 &amp; 🗃.

🔅 "**📦 🖼**" 👈 🏪 🎻 🎚,"**📦**" 🛎 🔗 🏃‍♂ 👐, 👜 👈 ➖ **🛠️**.

🕐❔ **📦** ▶️ &amp; 🏃‍♂ (▶️ ⚪️➡️ **📦 🖼**) ⚫️ 💪 ✍ ⚖️ 🔀 📁, 🌐 🔢, ♒️. 👈 🔀 🔜 🔀 🕴 👈 📦, ✋️ 🔜 🚫 😣 👽 📦 🖼 (🔜 🚫 🖊 💾).

📦 🖼 ⭐ **📋** 📁 &amp; 🎚, ✅ `python` &amp; 📁 `main.py`.

&amp; **📦** ⚫️ (🔅 **📦 🖼**) ☑ 🏃 👐 🖼, ⭐ **🛠️**. 👐, 📦 🏃 🕴 🕐❔ ⚫️ ✔️ **🛠️ 🏃** (&amp; 🛎 ⚫️ 🕴 👁 🛠️). 📦 ⛔️ 🕐❔ 📤 🙅‍♂ 🛠️ 🏃 ⚫️.

## 📦 🖼

☁ ✔️ 1️⃣ 👑 🧰 ✍ &amp; 🛠️ **📦 🖼** &amp; **📦**.

&amp; 📤 📢 <a href="https://hub.docker.com/" class="external-link" target="_blank">☁ 🎡</a> ⏮️ 🏤-⚒ **🛂 📦 🖼** 📚 🧰, 🌐, 💽, &amp; 🈸.

🖼, 📤 🛂 <a href="https://hub.docker.com/_/python" class="external-link" target="_blank">🐍 🖼</a>.

&amp; 📤 📚 🎏 🖼 🎏 👜 💖 💽, 🖼:

* <a href="https://hub.docker.com/_/postgres" class="external-link" target="_blank">✳</a>
* <a href="https://hub.docker.com/_/mysql" class="external-link" target="_blank">✳</a>
* <a href="https://hub.docker.com/_/mongo" class="external-link" target="_blank">✳</a>
* <a href="https://hub.docker.com/_/redis" class="external-link" target="_blank">✳</a>, ♒️.

⚙️ 🏤-⚒ 📦 🖼 ⚫️ 📶 ⏩ **🌀** &amp; ⚙️ 🎏 🧰. 🖼, 🔄 👅 🆕 💽. 🌅 💼, 👆 💪 ⚙️ **🛂 🖼**, &amp; 🔗 👫 ⏮️ 🌐 🔢.

👈 🌌, 📚 💼 👆 💪 💡 🔃 📦 &amp; ☁ &amp; 🏤-⚙️ 👈 💡 ⏮️ 📚 🎏 🧰 &amp; 🦲.

, 👆 🔜 🏃 **💗 📦** ⏮️ 🎏 👜, 💖 💽, 🐍 🈸, 🕸 💽 ⏮️ 😥 🕸 🈸, &amp; 🔗 👫 👯‍♂️ 📨 👫 🔗 🕸.

🌐 📦 🧾 ⚙️ (💖 ☁ ⚖️ Kubernete) ✔️ 👫 🕸 ⚒ 🛠️ 🔘 👫.

## 📦 &amp; 🛠️

**📦 🖼** 🛎 🔌 🚮 🗃 🔢 📋 ⚖️ 📋 👈 🔜 🏃 🕐❔ **📦** ▶️ &amp; 🔢 🚶‍♀️ 👈 📋. 📶 🎏 ⚫️❔ 🔜 🚥 ⚫️ 📋 ⏸.

🕐❔ **📦** ▶️, ⚫️ 🔜 🏃 👈 📋/📋 (👐 👆 💪 🔐 ⚫️ &amp; ⚒ ⚫️ 🏃 🎏 📋/📋).

📦 🏃 📏 **👑 🛠️** (📋 ⚖️ 📋) 🏃.

📦 🛎 ✔️ **👁 🛠️**, ✋️ ⚫️ 💪 ▶️ ✳ ⚪️➡️ 👑 🛠️, &amp; 👈 🌌 👆 🔜 ✔️ **💗 🛠️** 🎏 📦.

✋️ ⚫️ 🚫 💪 ✔️ 🏃‍♂ 📦 🍵 **🌘 1️⃣ 🏃‍♂ 🛠️**. 🚥 👑 🛠️ ⛔️, 📦 ⛔️.

## 🏗 ☁ 🖼 FastAPI

🆗, ➡️ 🏗 🕳 🔜 ❗ 👶

👤 🔜 🎦 👆 ❔ 🏗 **☁ 🖼** FastAPI **⚪️➡️ 🖌**, ⚓️ 🔛 **🛂 🐍** 🖼.

👉 ⚫️❔ 👆 🔜 💚 **🏆 💼**, 🖼:

* ⚙️ **Kubernete** ⚖️ 🎏 🧰
* 🕐❔ 🏃‍♂ 🔛 **🍓 👲**
* ⚙️ ☁ 🐕‍🦺 👈 🔜 🏃 📦 🖼 👆, ♒️.

### 📦 📄

👆 🔜 🛎 ✔️ **📦 📄** 👆 🈸 📁.

⚫️ 🔜 🪀 ✴️ 🔛 🧰 👆 ⚙️ **❎** 👈 📄.

🌅 ⚠ 🌌 ⚫️ ✔️ 📁 `requirements.txt` ⏮️ 📦 📛 &amp; 👫 ⏬, 1️⃣ 📍 ⏸.

👆 🔜 ↗️ ⚙️ 🎏 💭 👆 ✍ [🔃 FastAPI ⏬](./versions.md){.internal-link target=_blank} ⚒ ↔ ⏬.

🖼, 👆 `requirements.txt` 💪 👀 💖:

```
fastapi>=0.68.0,<0.69.0
pydantic>=1.8.0,<2.0.0
uvicorn>=0.15.0,<0.16.0
```

&amp; 👆 🔜 🛎 ❎ 👈 📦 🔗 ⏮️ `pip`, 🖼:

<div class="termy">

```console
$ pip install -r requirements.txt
---> 100%
Successfully installed fastapi pydantic uvicorn
```

</div>

!!! info
    📤 🎏 📁 &amp; 🧰 🔬 &amp; ❎ 📦 🔗.

    👤 🔜 🎦 👆 🖼 ⚙️ 🎶 ⏪ 📄 🔛. 👶

### ✍ **FastAPI** 📟

* ✍ `app` 📁 &amp; ⛔ ⚫️.
* ✍ 🛁 📁 `__init__.py`.
* ✍ `main.py` 📁 ⏮️:

```Python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

### 📁

🔜 🎏 🏗 📁 ✍ 📁 `Dockerfile` ⏮️:

```{ .dockerfile .annotate }
# (1)
FROM python:3.9

# (2)
WORKDIR /code

# (3)
COPY ./requirements.txt /code/requirements.txt

# (4)
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (5)
COPY ./app /code/app

# (6)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

1️⃣. ▶️ ⚪️➡️ 🛂 🐍 🧢 🖼.

2️⃣. ⚒ ⏮️ 👷 📁 `/code`.

    👉 🌐❔ 👥 🔜 🚮 `requirements.txt` 📁 &amp; `app` 📁.

3️⃣. 📁 📁 ⏮️ 📄 `/code` 📁.

    📁 **🕴** 📁 ⏮️ 📄 🥇, 🚫 🎂 📟.

    👉 📁 **🚫 🔀 🛎**, ☁ 🔜 🔍 ⚫️ &amp; ⚙️ **💾** 👉 🔁, 🛠️ 💾 ⏭ 🔁 💁‍♂️.

4️⃣. ❎ 📦 🔗 📄 📁.

     `--no-cache-dir` 🎛 💬 `pip` 🚫 🖊 ⏬ 📦 🌐, 👈 🕴 🚥 `pip` 🔜 🏃 🔄 ❎ 🎏 📦, ✋️ 👈 🚫 💼 🕐❔ 👷 ⏮️ 📦.

    !!! note
         `--no-cache-dir` 🕴 🔗 `pip`, ⚫️ ✔️ 🕳 ⏮️ ☁ ⚖️ 📦.

     `--upgrade` 🎛 💬 `pip` ♻ 📦 🚥 👫 ⏪ ❎.

    ↩️ ⏮️ 🔁 🖨 📁 💪 🔍 **☁ 💾**, 👉 🔁 🔜 **⚙️ ☁ 💾** 🕐❔ 💪.

    ⚙️ 💾 👉 🔁 🔜 **🖊** 👆 📚 **🕰** 🕐❔ 🏗 🖼 🔄 &amp; 🔄 ⏮️ 🛠️, ↩️ **⏬ &amp; ❎** 🌐 🔗 **🔠 🕰**.

5️⃣. 📁 `./app` 📁 🔘 `/code` 📁.

    👉 ✔️ 🌐 📟 ❔ ⚫️❔ **🔀 🌅 🛎** ☁ **💾** 🏆 🚫 ⚙️ 👉 ⚖️ 🙆 **📄 🔁** 💪.

    , ⚫️ ⚠ 🚮 👉 **🏘 🔚** `Dockerfile`, 🔬 📦 🖼 🏗 🕰.

6️⃣. ⚒ **📋** 🏃 `uvicorn` 💽.

    `CMD` ✊ 📇 🎻, 🔠 👫 🎻 ⚫️❔ 👆 🔜 🆎 📋 ⏸ 👽 🚀.

    👉 📋 🔜 🏃 ⚪️➡️ **⏮️ 👷 📁**, 🎏 `/code` 📁 👆 ⚒ 🔛 ⏮️ `WORKDIR /code`.

    ↩️ 📋 🔜 ▶️ `/code` &amp; 🔘 ⚫️ 📁 `./app` ⏮️ 👆 📟, **Uvicorn** 🔜 💪 👀 &amp; **🗄** `app` ⚪️➡️ `app.main`.

!!! tip
    📄 ⚫️❔ 🔠 ⏸ 🔨 🖊 🔠 🔢 💭 📟. 👶

👆 🔜 🔜 ✔️ 📁 📊 💖:

```
.
├── app
│   ├── __init__.py
│   └── main.py
├── Dockerfile
└── requirements.txt
```

#### ⛅ 🤝 ❎ 🗳

🚥 👆 🏃‍♂ 👆 📦 ⛅ 🤝 ❎ 🗳 (📐 ⚙) 💖 👌 ⚖️ Traefik, 🚮 🎛 `--proxy-headers`, 👉 🔜 💬 Uvicorn 💙 🎚 📨 👈 🗳 💬 ⚫️ 👈 🈸 🏃 ⛅ 🇺🇸🔍, ♒️.

```Dockerfile
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
```

#### ☁ 💾

📤 ⚠ 🎱 👉 `Dockerfile`, 👥 🥇 📁 **📁 ⏮️ 🔗 😞**, 🚫 🎂 📟. ➡️ 👤 💬 👆 ⚫️❔ 👈.

```Dockerfile
COPY ./requirements.txt /code/requirements.txt
```

☁ &amp; 🎏 🧰 **🏗** 👉 📦 🖼 **🔁**, 🚮 **1️⃣ 🧽 🔛 🔝 🎏**, ▶️ ⚪️➡️ 🔝 `Dockerfile` &amp; ❎ 🙆 📁 ✍ 🔠 👩‍🌾 `Dockerfile`.

☁ &amp; 🎏 🧰 ⚙️ **🔗 💾** 🕐❔ 🏗 🖼, 🚥 📁 🚫 🔀 ↩️ 🏁 🕰 🏗 📦 🖼, ⤴️ ⚫️ 🔜 **🏤-⚙️ 🎏 🧽** ✍ 🏁 🕰, ↩️ 🖨 📁 🔄 &amp; 🏗 🆕 🧽 ⚪️➡️ 🖌.

❎ 📁 📁 🚫 🎯 📉 👜 💁‍♂️ 🌅, ✋️ ↩️ ⚫️ ⚙️ 💾 👈 🔁, ⚫️ 💪 **⚙️ 💾 ⏭ 🔁**. 🖼, ⚫️ 💪 ⚙️ 💾 👩‍🌾 👈 ❎ 🔗 ⏮️:

```Dockerfile
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
```

📁 ⏮️ 📦 📄 **🏆 🚫 🔀 🛎**. , 🖨 🕴 👈 📁, ☁ 🔜 💪 **⚙️ 💾** 👈 🔁.

&amp; ⤴️, ☁ 🔜 💪 **⚙️ 💾 ⏭ 🔁** 👈 ⏬ &amp; ❎ 👈 🔗. &amp; 📥 🌐❔ 👥 **🖊 📚 🕰**. 👶 ...&amp; ❎ 😩 ⌛. 👶 👶

⏬ &amp; ❎ 📦 🔗 **💪 ✊ ⏲**, ✋️ ⚙️ **💾** 🔜 **✊ 🥈** 🌅.

&amp; 👆 🔜 🏗 📦 🖼 🔄 &amp; 🔄 ⏮️ 🛠️ ✅ 👈 👆 📟 🔀 👷, 📤 📚 📈 🕰 👉 🔜 🖊.

⤴️, 🏘 🔚 `Dockerfile`, 👥 📁 🌐 📟. 👉 ⚫️❔ **🔀 🏆 🛎**, 👥 🚮 ⚫️ 🏘 🔚, ↩️ 🌖 🕧, 🕳 ⏮️ 👉 🔁 🔜 🚫 💪 ⚙️ 💾.

```Dockerfile
COPY ./app /code/app
```

### 🏗 ☁ 🖼

🔜 👈 🌐 📁 🥉, ➡️ 🏗 📦 🖼.

* 🚶 🏗 📁 (🌐❔ 👆 `Dockerfile` , ⚗ 👆 `app` 📁).
* 🏗 👆 FastAPI 🖼:

<div class="termy">

```console
$ docker build -t myimage .

---> 100%
```

</div>

!!! tip
    👀 `.` 🔚, ⚫️ 🌓 `./`, ⚫️ 💬 ☁ 📁 ⚙️ 🏗 📦 🖼.

    👉 💼, ⚫️ 🎏 ⏮️ 📁 (`.`).

### ▶️ ☁ 📦

* 🏃 📦 ⚓️ 🔛 👆 🖼:

<div class="termy">

```console
$ docker run -d --name mycontainer -p 80:80 myimage
```

</div>

## ✅ ⚫️

👆 🔜 💪 ✅ ⚫️ 👆 ☁ 📦 📛, 🖼: <a href="http://192.168.99.100/items/5?q=somequery" class="external-link" target="_blank">http://192.168.99.100/items/5?q=somequery</a> ⚖️ <a href="http://127.0.0.1/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1/items/5?q=somequery</a> (⚖️ 🌓, ⚙️ 👆 ☁ 🦠).

👆 🔜 👀 🕳 💖:

```JSON
{"item_id": 5, "q": "somequery"}
```

## 🎓 🛠️ 🩺

🔜 👆 💪 🚶 <a href="http://192.168.99.100/docs" class="external-link" target="_blank">http://192.168.99.100/docs</a> ⚖️ <a href="http://127.0.0.1/docs" class="external-link" target="_blank">http://127.0.0.1/docs</a> (⚖️ 🌓, ⚙️ 👆 ☁ 🦠).

👆 🔜 👀 🏧 🎓 🛠️ 🧾 (🚚 <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">🦁 🎚</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

## 🎛 🛠️ 🩺

&amp; 👆 💪 🚶 <a href="http://192.168.99.100/redoc" class="external-link" target="_blank">http://192.168.99.100/redoc</a> ⚖️ <a href="http://127.0.0.1/redoc" class="external-link" target="_blank">http://127.0.0.1/redoc</a> (⚖️ 🌓, ⚙️ 👆 ☁ 🦠).

👆 🔜 👀 🎛 🏧 🧾 (🚚 <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">📄</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## 🏗 ☁ 🖼 ⏮️ 👁-📁 FastAPI

🚥 👆 FastAPI 👁 📁, 🖼, `main.py` 🍵 `./app` 📁, 👆 📁 📊 💪 👀 💖 👉:

```
.
├── Dockerfile
├── main.py
└── requirements.txt
```

⤴️ 👆 🔜 ✔️ 🔀 🔗 ➡ 📁 📁 🔘 `Dockerfile`:

```{ .dockerfile .annotate hl_lines="10  13" }
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (1)
COPY ./main.py /code/

# (2)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```

1️⃣. 📁 `main.py` 📁 `/code` 📁 🔗 (🍵 🙆 `./app` 📁).

2️⃣. 🏃 Uvicorn &amp; 💬 ⚫️ 🗄 `app` 🎚 ⚪️➡️ `main` (↩️ 🏭 ⚪️➡️ `app.main`).

⤴️ 🔆 Uvicorn 📋 ⚙️ 🆕 🕹 `main` ↩️ `app.main` 🗄 FastAPI 🎚 `app`.

## 🛠️ 🔧

➡️ 💬 🔄 🔃 🎏 [🛠️ 🔧](./concepts.md){.internal-link target=_blank} ⚖ 📦.

📦 ✴️ 🧰 📉 🛠️ **🏗 &amp; 🛠️** 🈸, ✋️ 👫 🚫 🛠️ 🎯 🎯 🍵 👉 **🛠️ 🔧**, &amp; 📤 📚 💪 🎛.

**👍 📰** 👈 ⏮️ 🔠 🎏 🎛 📤 🌌 📔 🌐 🛠️ 🔧. 👶

➡️ 📄 👉 **🛠️ 🔧** ⚖ 📦:

* 🇺🇸🔍
* 🏃‍♂ 🔛 🕴
* ⏏
* 🧬 (🔢 🛠️ 🏃)
* 💾
* ⏮️ 🔁 ⏭ ▶️

## 🇺🇸🔍

🚥 👥 🎯 🔛 **📦 🖼** FastAPI 🈸 (&amp; ⏪ 🏃‍♂ **📦**), 🇺🇸🔍 🛎 🔜 🍵 **🗜** ➕1️⃣ 🧰.

⚫️ 💪 ➕1️⃣ 📦, 🖼 ⏮️ <a href="https://traefik.io/" class="external-link" target="_blank">Traefik</a>, 🚚 **🇺🇸🔍** &amp; **🏧** 🛠️ **📄**.

!!! tip
    Traefik ✔️ 🛠️ ⏮️ ☁, Kubernete, &amp; 🎏, ⚫️ 📶 ⏩ ⚒ 🆙 &amp; 🔗 🇺🇸🔍 👆 📦 ⏮️ ⚫️.

👐, 🇺🇸🔍 💪 🍵 ☁ 🐕‍🦺 1️⃣ 👫 🐕‍🦺 (⏪ 🏃 🈸 📦).

## 🏃‍♂ 🔛 🕴 &amp; ⏏

📤 🛎 ➕1️⃣ 🧰 🈚 **▶️ &amp; 🏃‍♂** 👆 📦.

⚫️ 💪 **☁** 🔗, **☁ ✍**, **Kubernete**, **☁ 🐕‍🦺**, ♒️.

🌅 (⚖️ 🌐) 💼, 📤 🙅 🎛 🛠️ 🏃 📦 🔛 🕴 &amp; 🛠️ ⏏ 🔛 ❌. 🖼, ☁, ⚫️ 📋 ⏸ 🎛 `--restart`.

🍵 ⚙️ 📦, ⚒ 🈸 🏃 🔛 🕴 &amp; ⏮️ ⏏ 💪 ⚠ &amp; ⚠. ✋️ 🕐❔ **👷 ⏮️ 📦** 🌅 💼 👈 🛠️ 🔌 🔢. 👶

## 🧬 - 🔢 🛠️

🚥 👆 ✔️ <abbr title="A group of machines that are configured to be connected and work together in some way.">🌑</abbr> 🎰 ⏮️ **☁**, ☁ 🐝 📳, 🖖, ⚖️ ➕1️⃣ 🎏 🏗 ⚙️ 🛠️ 📎 📦 🔛 💗 🎰, ⤴️ 👆 🔜 🎲 💚 **🍵 🧬** **🌑 🎚** ↩️ ⚙️ **🛠️ 👨‍💼** (💖 🐁 ⏮️ 👨‍🏭) 🔠 📦.

1️⃣ 📚 📎 📦 🧾 ⚙️ 💖 Kubernete 🛎 ✔️ 🛠️ 🌌 🚚 **🧬 📦** ⏪ 🔗 **📐 ⚖** 📨 📨. 🌐 **🌑 🎚**.

📚 💼, 👆 🔜 🎲 💚 🏗 **☁ 🖼 ⚪️➡️ 🖌** [🔬 🔛](#dockerfile), ❎ 👆 🔗, &amp; 🏃‍♂ **👁 Uvicorn 🛠️** ↩️ 🏃‍♂ 🕳 💖 🐁 ⏮️ Uvicorn 👨‍🏭.

### 📐 ⚙

🕐❔ ⚙️ 📦, 👆 🔜 🛎 ✔️ 🦲 **👂 🔛 👑 ⛴**. ⚫️ 💪 🎲 ➕1️⃣ 📦 👈 **🤝 ❎ 🗳** 🍵 **🇺🇸🔍** ⚖️ 🎏 🧰.

👉 🦲 🔜 ✊ **📐** 📨 &amp; 📎 👈 👪 👨‍🏭 (🤞) **⚖** 🌌, ⚫️ 🛎 🤙 **📐 ⚙**.

!!! tip
    🎏 **🤝 ❎ 🗳** 🦲 ⚙️ 🇺🇸🔍 🔜 🎲 **📐 ⚙**.

&amp; 🕐❔ 👷 ⏮️ 📦, 🎏 ⚙️ 👆 ⚙️ ▶️ &amp; 🛠️ 👫 🔜 ⏪ ✔️ 🔗 🧰 📶 **🕸 📻** (✅ 🇺🇸🔍 📨) ⚪️➡️ 👈 **📐 ⚙** (👈 💪 **🤝 ❎ 🗳**) 📦(Ⓜ) ⏮️ 👆 📱.

### 1️⃣ 📐 ⚙ - 💗 👨‍🏭 📦

🕐❔ 👷 ⏮️ **Kubernete** ⚖️ 🎏 📎 📦 🧾 ⚙️, ⚙️ 👫 🔗 🕸 🛠️ 🔜 ✔ 👁 **📐 ⚙** 👈 👂 🔛 👑 **⛴** 📶 📻 (📨) 🎲 **💗 📦** 🏃 👆 📱.

🔠 👫 📦 🏃‍♂ 👆 📱 🔜 🛎 ✔️ **1️⃣ 🛠️** (✅ Uvicorn 🛠️ 🏃 👆 FastAPI 🈸). 👫 🔜 🌐 **🌓 📦**, 🏃‍♂ 🎏 👜, ✋️ 🔠 ⏮️ 🚮 👍 🛠️, 💾, ♒️. 👈 🌌 👆 🔜 ✊ 📈 **🛠️** **🎏 🐚** 💽, ⚖️ **🎏 🎰**.

&amp; 📎 📦 ⚙️ ⏮️ **📐 ⚙** 🔜 **📎 📨** 🔠 1️⃣ 📦 ⏮️ 👆 📱 **🔄**. , 🔠 📨 💪 🍵 1️⃣ 💗 **🔁 📦** 🏃 👆 📱.

&amp; 🛎 👉 **📐 ⚙** 🔜 💪 🍵 📨 👈 🚶 *🎏* 📱 👆 🌑 (✅ 🎏 🆔, ⚖️ 🔽 🎏 📛 ➡ 🔡), &amp; 🔜 📶 👈 📻 ▶️️ 📦 *👈 🎏* 🈸 🏃‍♂ 👆 🌑.

### 1️⃣ 🛠️ 📍 📦

👉 🆎 😐, 👆 🎲 🔜 💚 ✔️ **👁 (Uvicorn) 🛠️ 📍 📦**, 👆 🔜 ⏪ 🚚 🧬 🌑 🎚.

, 👉 💼, 👆 **🔜 🚫** 💚 ✔️ 🛠️ 👨‍💼 💖 🐁 ⏮️ Uvicorn 👨‍🏭, ⚖️ Uvicorn ⚙️ 🚮 👍 Uvicorn 👨‍🏭. 👆 🔜 💚 ✔️ **👁 Uvicorn 🛠️** 📍 📦 (✋️ 🎲 💗 📦).

✔️ ➕1️⃣ 🛠️ 👨‍💼 🔘 📦 (🔜 ⏮️ 🐁 ⚖️ Uvicorn 🛠️ Uvicorn 👨‍🏭) 🔜 🕴 🚮 **🙃 🔀** 👈 👆 🌅 🎲 ⏪ ✊ 💅 ⏮️ 👆 🌑 ⚙️.

### 📦 ⏮️ 💗 🛠️ &amp; 🎁 💼

↗️, 📤 **🎁 💼** 🌐❔ 👆 💪 💚 ✔️ **📦** ⏮️ **🐁 🛠️ 👨‍💼** ▶️ 📚 **Uvicorn 👨‍🏭 🛠️** 🔘.

📚 💼, 👆 💪 ⚙️ **🛂 ☁ 🖼** 👈 🔌 **🐁** 🛠️ 👨‍💼 🏃‍♂ 💗 **Uvicorn 👨‍🏭 🛠️**, &amp; 🔢 ⚒ 🔆 🔢 👨‍🏭 ⚓️ 🔛 ⏮️ 💽 🐚 🔁. 👤 🔜 💬 👆 🌅 🔃 ⚫️ 🔛 [🛂 ☁ 🖼 ⏮️ 🐁 - Uvicorn](#official-docker-image-with-gunicorn-uvicorn).

📥 🖼 🕐❔ 👈 💪 ⚒ 🔑:

#### 🙅 📱

👆 💪 💚 🛠️ 👨‍💼 📦 🚥 👆 🈸 **🙅 🥃** 👈 👆 🚫 💪 (🐥 🚫) 👌-🎶 🔢 🛠️ 💁‍♂️ 🌅, &amp; 👆 💪 ⚙️ 🏧 🔢 (⏮️ 🛂 ☁ 🖼), &amp; 👆 🏃‍♂ ⚫️ 🔛 **👁 💽**, 🚫 🌑.

#### ☁ ✍

👆 💪 🛠️ **👁 💽** (🚫 🌑) ⏮️ **☁ ✍**, 👆 🚫🔜 ✔️ ⏩ 🌌 🛠️ 🧬 📦 (⏮️ ☁ ✍) ⏪ 🛡 🔗 🕸 &amp; **📐 ⚖**.

⤴️ 👆 💪 💚 ✔️ **👁 📦** ⏮️ **🛠️ 👨‍💼** ▶️ **📚 👨‍🏭 🛠️** 🔘.

#### 🤴 &amp; 🎏 🤔

👆 💪 ✔️ **🎏 🤔** 👈 🔜 ⚒ ⚫️ ⏩ ✔️ **👁 📦** ⏮️ **💗 🛠️** ↩️ ✔️ **💗 📦** ⏮️ **👁 🛠️** 🔠 👫.

🖼 (🪀 🔛 👆 🖥) 👆 💪 ✔️ 🧰 💖 🤴 🏭 🎏 📦 👈 🔜 ✔️ 🔐 **🔠 📨** 👈 👟.

👉 💼, 🚥 👆 ✔️ **💗 📦**, 🔢, 🕐❔ 🤴 👟 **✍ ⚖**, ⚫️ 🔜 🤚 🕐 **👁 📦 🔠 🕰** (📦 👈 🍵 👈 🎯 📨), ↩️ 🤚 **📈 ⚖** 🌐 🔁 📦.

⤴️, 👈 💼, ⚫️ 💪 🙅 ✔️ **1️⃣ 📦** ⏮️ **💗 🛠️**, &amp; 🇧🇿 🧰 (✅ 🤴 🏭) 🔛 🎏 📦 📈 🤴 ⚖ 🌐 🔗 🛠️ &amp; 🎦 👈 ⚖ 🔛 👈 👁 📦.

---

👑 ☝, **👌** 👉 **🚫 ✍ 🗿** 👈 👆 ✔️ 😄 ⏩. 👆 💪 ⚙️ 👫 💭 **🔬 👆 👍 ⚙️ 💼** &amp; 💭 ⚫️❔ 👍 🎯 👆 ⚙️, ✅ 👅 ❔ 🛠️ 🔧:

* 💂‍♂ - 🇺🇸🔍
* 🏃‍♂ 🔛 🕴
* ⏏
* 🧬 (🔢 🛠️ 🏃)
* 💾
* ⏮️ 🔁 ⏭ ▶️

## 💾

🚥 👆 🏃 **👁 🛠️ 📍 📦** 👆 🔜 ✔️ 🌅 ⚖️ 🌘 👍-🔬, ⚖, &amp; 📉 💸 💾 🍴 🔠 👈 📦 (🌅 🌘 1️⃣ 🚥 👫 🔁).

&amp; ⤴️ 👆 💪 ⚒ 👈 🎏 💾 📉 &amp; 📄 👆 📳 👆 📦 🧾 ⚙️ (🖼 **Kubernete**). 👈 🌌 ⚫️ 🔜 💪 **🔁 📦** **💪 🎰** ✊ 🔘 🏧 💸 💾 💪 👫, &amp; 💸 💪 🎰 🌑.

🚥 👆 🈸 **🙅**, 👉 🔜 🎲 **🚫 ⚠**, &amp; 👆 💪 🚫 💪 ✔ 🏋️ 💾 📉. ✋️ 🚥 👆 **⚙️ 📚 💾** (🖼 ⏮️ **🎰 🏫** 🏷), 👆 🔜 ✅ ❔ 🌅 💾 👆 😩 &amp; 🔆 **🔢 📦** 👈 🏃 **🔠 🎰** (&amp; 🎲 🚮 🌖 🎰 👆 🌑).

🚥 👆 🏃 **💗 🛠️ 📍 📦** (🖼 ⏮️ 🛂 ☁ 🖼) 👆 🔜 ✔️ ⚒ 💭 👈 🔢 🛠️ ▶️ 🚫 **🍴 🌖 💾** 🌘 ⚫️❔ 💪.

## ⏮️ 🔁 ⏭ ▶️ &amp; 📦

🚥 👆 ⚙️ 📦 (✅ ☁, Kubernete), ⤴️ 📤 2️⃣ 👑 🎯 👆 💪 ⚙️.

### 💗 📦

🚥 👆 ✔️ **💗 📦**, 🎲 🔠 1️⃣ 🏃 **👁 🛠️** (🖼, **Kubernete** 🌑), ⤴️ 👆 🔜 🎲 💚 ✔️ **🎏 📦** 🔨 👷 **⏮️ 📶** 👁 📦, 🏃 👁 🛠️, **⏭** 🏃 🔁 👨‍🏭 📦.

!!! info
    🚥 👆 ⚙️ Kubernete, 👉 🔜 🎲 <a href="https://kubernetes.io/docs/concepts/workloads/pods/init-containers/" class="external-link" target="_blank">🕑 📦</a>.

🚥 👆 ⚙️ 💼 📤 🙅‍♂ ⚠ 🏃‍♂ 👈 ⏮️ 📶 **💗 🕰 🔗** (🖼 🚥 👆 🚫 🏃 💽 🛠️, ✋️ ✅ 🚥 💽 🔜), ⤴️ 👆 💪 🚮 👫 🔠 📦 ▶️️ ⏭ ▶️ 👑 🛠️.

### 👁 📦

🚥 👆 ✔️ 🙅 🖥, ⏮️ **👁 📦** 👈 ⤴️ ▶️ 💗 **👨‍🏭 🛠️** (⚖️ 1️⃣ 🛠️), ⤴️ 👆 💪 🏃 👈 ⏮️ 🔁 🎏 📦, ▶️️ ⏭ ▶️ 🛠️ ⏮️ 📱. 🛂 ☁ 🖼 🐕‍🦺 👉 🔘.

## 🛂 ☁ 🖼 ⏮️ 🐁 - Uvicorn

📤 🛂 ☁ 🖼 👈 🔌 🐁 🏃‍♂ ⏮️ Uvicorn 👨‍🏭, ℹ ⏮️ 📃: [💽 👨‍🏭 - 🐁 ⏮️ Uvicorn](./server-workers.md){.internal-link target=_blank}.

👉 🖼 🔜 ⚠ ✴️ ⚠ 🔬 🔛: [📦 ⏮️ 💗 🛠️ &amp; 🎁 💼](#containers-with-multiple-processes-and-special-cases).

* <a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" class="external-link" target="_blank">tiangolo/uvicorn-🐁-fastapi</a>.

!!! warning
    📤 ↕ 🤞 👈 👆 **🚫** 💪 👉 🧢 🖼 ⚖️ 🙆 🎏 🎏 1️⃣, &amp; 🔜 👻 📆 🏗 🖼 ⚪️➡️ 🖌 [🔬 🔛: 🏗 ☁ 🖼 FastAPI](#build-a-docker-image-for-fastapi).

👉 🖼 ✔️ **🚘-📳** 🛠️ 🔌 ⚒ **🔢 👨‍🏭 🛠️** ⚓️ 🔛 💽 🐚 💪.

⚫️ ✔️ **🤔 🔢**, ✋️ 👆 💪 🔀 &amp; ℹ 🌐 📳 ⏮️ **🌐 🔢** ⚖️ 📳 📁.

⚫️ 🐕‍🦺 🏃 <a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker#pre_start_path" class="external-link" target="_blank">**⏮️ 🔁 ⏭ ▶️**</a> ⏮️ ✍.

!!! tip
    👀 🌐 📳 &amp; 🎛, 🚶 ☁ 🖼 📃: <a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" class="external-link" target="_blank">Tiangolo/uvicorn-🐁-fastapi</a>.

### 🔢 🛠️ 🔛 🛂 ☁ 🖼

**🔢 🛠️** 🔛 👉 🖼 **📊 🔁** ⚪️➡️ 💽 **🐚** 💪.

👉 ⛓ 👈 ⚫️ 🔜 🔄 **🗜** 🌅 **🎭** ⚪️➡️ 💽 💪.

👆 💪 🔆 ⚫️ ⏮️ 📳 ⚙️ **🌐 🔢**, ♒️.

✋️ ⚫️ ⛓ 👈 🔢 🛠️ 🪀 🔛 💽 📦 🏃, **💸 💾 🍴** 🔜 🪀 🔛 👈.

, 🚥 👆 🈸 🍴 📚 💾 (🖼 ⏮️ 🎰 🏫 🏷), &amp; 👆 💽 ✔️ 📚 💽 🐚 **✋️ 🐥 💾**, ⤴️ 👆 📦 💪 🔚 🆙 🔄 ⚙️ 🌅 💾 🌘 ⚫️❔ 💪, &amp; 🤕 🎭 📚 (⚖️ 💥). 👶

### ✍ `Dockerfile`

📥 ❔ 👆 🔜 ✍ `Dockerfile` ⚓️ 🔛 👉 🖼:

```Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app
```

### 🦏 🈸

🚥 👆 ⏩ 📄 🔃 🏗 [🦏 🈸 ⏮️ 💗 📁](../tutorial/bigger-applications.md){.internal-link target=_blank}, 👆 `Dockerfile` 💪 ↩️ 👀 💖:

```Dockerfile hl_lines="7"
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app/app
```

### 🕐❔ ⚙️

👆 🔜 🎲 **🚫** ⚙️ 👉 🛂 🧢 🖼 (⚖️ 🙆 🎏 🎏 1️⃣) 🚥 👆 ⚙️ **Kubernete** (⚖️ 🎏) &amp; 👆 ⏪ ⚒ **🧬** 🌑 🎚, ⏮️ 💗 **📦**. 📚 💼, 👆 👍 📆 **🏗 🖼 ⚪️➡️ 🖌** 🔬 🔛: [🏗 ☁ 🖼 FastAPI](#build-a-docker-image-for-fastapi).

👉 🖼 🔜 ⚠ ✴️ 🎁 💼 🔬 🔛 [📦 ⏮️ 💗 🛠️ &amp; 🎁 💼](#containers-with-multiple-processes-and-special-cases). 🖼, 🚥 👆 🈸 **🙅 🥃** 👈 ⚒ 🔢 🔢 🛠️ ⚓️ 🔛 💽 👷 👍, 👆 🚫 💚 😥 ⏮️ ❎ 🛠️ 🧬 🌑 🎚, &amp; 👆 🚫 🏃 🌅 🌘 1️⃣ 📦 ⏮️ 👆 📱. ⚖️ 🚥 👆 🛠️ ⏮️ **☁ ✍**, 🏃 🔛 👁 💽, ♒️.

## 🛠️ 📦 🖼

⏮️ ✔️ 📦 (☁) 🖼 📤 📚 🌌 🛠️ ⚫️.

🖼:

* ⏮️ **☁ ✍** 👁 💽
* ⏮️ **Kubernete** 🌑
* ⏮️ ☁ 🐝 📳 🌑
* ⏮️ ➕1️⃣ 🧰 💖 🖖
* ⏮️ ☁ 🐕‍🦺 👈 ✊ 👆 📦 🖼 &amp; 🛠️ ⚫️

## ☁ 🖼 ⏮️ 🎶

🚥 👆 ⚙️ <a href="https://python-poetry.org/" class="external-link" target="_blank">🎶</a> 🛠️ 👆 🏗 🔗, 👆 💪 ⚙️ ☁ 👁-▶️ 🏗:

```{ .dockerfile .annotate }
# (1)
FROM python:3.9 as requirements-stage

# (2)
WORKDIR /tmp

# (3)
RUN pip install poetry

# (4)
COPY ./pyproject.toml ./poetry.lock* /tmp/

# (5)
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# (6)
FROM python:3.9

# (7)
WORKDIR /code

# (8)
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

# (9)
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (10)
COPY ./app /code/app

# (11)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

1️⃣. 👉 🥇 ▶️, ⚫️ 🌟 `requirements-stage`.

2️⃣. ⚒ `/tmp` ⏮️ 👷 📁.

    📥 🌐❔ 👥 🔜 🏗 📁 `requirements.txt`

3️⃣. ❎ 🎶 👉 ☁ ▶️.

4️⃣. 📁 `pyproject.toml` &amp; `poetry.lock` 📁 `/tmp` 📁.

    ↩️ ⚫️ ⚙️ `./poetry.lock*` (▶️ ⏮️ `*`), ⚫️ 🏆 🚫 💥 🚥 👈 📁 🚫 💪.

5️⃣. 🏗 `requirements.txt` 📁.

6️⃣. 👉 🏁 ▶️, 🕳 📥 🔜 🛡 🏁 📦 🖼.

7️⃣. ⚒ ⏮️ 👷 📁 `/code`.

8️⃣. 📁 `requirements.txt` 📁 `/code` 📁.

    👉 📁 🕴 🖖 ⏮️ ☁ ▶️, 👈 ⚫️❔ 👥 ⚙️ `--from-requirements-stage` 📁 ⚫️.

9️⃣. ❎ 📦 🔗 🏗 `requirements.txt` 📁.

1️⃣0️⃣. 📁 `app` 📁 `/code` 📁.

1️⃣1️⃣. 🏃 `uvicorn` 📋, 💬 ⚫️ ⚙️ `app` 🎚 🗄 ⚪️➡️ `app.main`.

!!! tip
    🖊 💭 🔢 👀 ⚫️❔ 🔠 ⏸ 🔨.

**☁ ▶️** 🍕 `Dockerfile` 👈 👷 **🍕 📦 🖼** 👈 🕴 ⚙️ 🏗 📁 ⚙️ ⏪.

🥇 ▶️ 🔜 🕴 ⚙️ **❎ 🎶** &amp; **🏗 `requirements.txt`** ⏮️ 👆 🏗 🔗 ⚪️➡️ 🎶 `pyproject.toml` 📁.

👉 `requirements.txt` 📁 🔜 ⚙️ ⏮️ `pip` ⏪ **⏭ ▶️**.

🏁 📦 🖼 **🕴 🏁 ▶️** 🛡. ⏮️ ▶️(Ⓜ) 🔜 ❎.

🕐❔ ⚙️ 🎶, ⚫️ 🔜 ⚒ 🔑 ⚙️ **☁ 👁-▶️ 🏗** ↩️ 👆 🚫 🤙 💪 ✔️ 🎶 &amp; 🚮 🔗 ❎ 🏁 📦 🖼, 👆 **🕴 💪** ✔️ 🏗 `requirements.txt` 📁 ❎ 👆 🏗 🔗.

⤴️ ⏭ (&amp; 🏁) ▶️ 👆 🔜 🏗 🖼 🌅 ⚖️ 🌘 🎏 🌌 🔬 ⏭.

### ⛅ 🤝 ❎ 🗳 - 🎶

🔄, 🚥 👆 🏃‍♂ 👆 📦 ⛅ 🤝 ❎ 🗳 (📐 ⚙) 💖 👌 ⚖️ Traefik, 🚮 🎛 `--proxy-headers` 📋:

```Dockerfile
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
```

## 🌃

⚙️ 📦 ⚙️ (✅ ⏮️ **☁** &amp; **Kubernete**) ⚫️ ▶️️ 📶 🎯 🍵 🌐 **🛠️ 🔧**:

* 🇺🇸🔍
* 🏃‍♂ 🔛 🕴
* ⏏
* 🧬 (🔢 🛠️ 🏃)
* 💾
* ⏮️ 🔁 ⏭ ▶️

🌅 💼, 👆 🎲 🏆 🚫 💚 ⚙️ 🙆 🧢 🖼, &amp; ↩️ **🏗 📦 🖼 ⚪️➡️ 🖌** 1️⃣ ⚓️ 🔛 🛂 🐍 ☁ 🖼.

✊ 💅 **✔** 👩‍🌾 `Dockerfile` &amp; **☁ 💾** 👆 💪 **📉 🏗 🕰**, 📉 👆 📈 (&amp; ❎ 😩). 👶

🎯 🎁 💼, 👆 💪 💚 ⚙️ 🛂 ☁ 🖼 FastAPI. 👶
