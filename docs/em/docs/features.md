# ⚒

## FastAPI ⚒

**FastAPI** 🤝 👆 📄:

### ⚓️ 🔛 📂 🐩

* <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>🗄</strong></a> 🛠️ 🏗, ✅ 📄 <abbr title="also known as: endpoints, routes">➡</abbr> <abbr title="also known as HTTP methods, as POST, GET, PUT, DELETE">🛠️</abbr>, 🔢, 💪 📨, 💂‍♂, ♒️.
* 🏧 📊 🏷 🧾 ⏮️ <a href="https://json-schema.org/" class="external-link" target="_blank"><strong>🎻 🔗</strong></a> (🗄 ⚫️ 🧢 🔛 🎻 🔗).
* 🔧 🤭 👫 🐩, ⏮️ 😔 🔬. ↩️ 👎 🧽 🔛 🔝.
* 👉 ✔ ⚙️ 🏧 **👩‍💻 📟 ⚡** 📚 🇪🇸.

### 🏧 🩺

🎓 🛠️ 🧾 &amp; 🔬 🕸 👩‍💻 🔢. 🛠️ ⚓️ 🔛 🗄, 📤 💗 🎛, 2️⃣ 🔌 🔢.

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>🦁 🎚</strong></a>, ⏮️ 🎓 🔬, 🤙 &amp; 💯 👆 🛠️ 🔗 ⚪️➡️ 🖥.

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* 🎛 🛠️ 🧾 ⏮️ <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>📄</strong></a>.

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### 🏛 🐍

⚫️ 🌐 ⚓️ 🔛 🐩 **🐍 3️⃣.6️⃣ 🆎** 📄 (👏 Pydantic). 🙅‍♂ 🆕 ❕ 💡. 🐩 🏛 🐍.

🚥 👆 💪 2️⃣ ⏲ ↗️ ❔ ⚙️ 🐍 🆎 (🚥 👆 🚫 ⚙️ FastAPI), ✅ 📏 🔰: [🐍 🆎](python-types.md){.internal-link target=_blank}.

👆 ✍ 🐩 🐍 ⏮️ 🆎:

```Python
from datetime import date

from pydantic import BaseModel

# Declare a variable as a str
# and get editor support inside the function
def main(user_id: str):
    return user_id


# A Pydantic model
class User(BaseModel):
    id: int
    name: str
    joined: date
```

👈 💪 ⤴️ ⚙️ 💖:

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

!!! info
    `**second_user_data` ⛓:

    🚶‍♀️ 🔑 &amp; 💲 `second_user_data` #️⃣ 🔗 🔑-💲 ❌, 🌓: `User(id=4, name="Mary", joined="2018-11-30")`

### 👨‍🎨 🐕‍🦺

🌐 🛠️ 🏗 ⏩ &amp; 🏋️ ⚙️, 🌐 🚫 💯 🔛 💗 👨‍🎨 ⏭ ▶️ 🛠️, 🚚 🏆 🛠️ 💡.

🏁 🐍 👩‍💻 🔬 ⚫️ 🆑 <a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target="_blank">👈 🌅 ⚙️ ⚒ "✍"</a>.

🎂 **FastAPI** 🛠️ ⚓️ 😌 👈. ✍ 👷 🌐.

👆 🔜 🛎 💪 👟 🔙 🩺.

📥 ❔ 👆 👨‍🎨 💪 ℹ 👆:

*  <a href="https://code.visualstudio.com/" class="external-link" target="_blank">🎙 🎙 📟</a>:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

*  <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">🗒</a>:

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)

👆 🔜 🤚 🛠️ 📟 👆 5️⃣📆 🤔 💪 ⏭. 🖼, `price` 🔑 🔘 🎻 💪 (👈 💪 ✔️ 🐦) 👈 👟 ⚪️➡️ 📨.

🙅‍♂ 🌖 ⌨ ❌ 🔑 📛, 👟 🔙 &amp; ➡ 🖖 🩺, ⚖️ 📜 🆙 &amp; 🔽 🔎 🚥 👆 😒 ⚙️ `username` ⚖️ `user_name`.

### 📏

⚫️ ✔️ 🤔 **🔢** 🌐, ⏮️ 📦 📳 🌐. 🌐 🔢 💪 👌-🎧 ⚫️❔ 👆 💪 &amp; 🔬 🛠️ 👆 💪.

✋️ 🔢, ⚫️ 🌐 **"👷"**.

### 🔬

* 🔬 🌅 (⚖️ 🌐 ❓) 🐍 **💽 🆎**, 🔌:
    * 🎻 🎚 (`dict`).
    * 🎻 🎻 (`list`) ⚖ 🏬 🆎.
    * 🎻 (`str`) 🏑, 🔬 🕙 &amp; 👟 📐.
    * 🔢 (`int`, `float`) ⏮️ 🕙 &amp; 👟 💲, ♒️.

* 🔬 🌅 😍 🆎, 💖:
    * 📛.
    * 📧.
    * 🆔.
    * ...&amp; 🎏.

🌐 🔬 🍵 👍-🏛 &amp; 🏋️ **Pydantic**.

### 💂‍♂ &amp; 🤝

💂‍♂ &amp; 🤝 🛠️. 🍵 🙆 ⚠ ⏮️ 💽 ⚖️ 📊 🏷.

🌐 💂‍♂ ⚖ 🔬 🗄, 🔌:

* 🇺🇸🔍 🔰.
* **Oauth2️⃣** (⏮️ **🥙 🤝**). ✅ 🔰 🔛 [Oauth2️⃣ ⏮️ 🥙](tutorial/security/oauth2-jwt.md){.internal-link target=_blank}.
* 🛠️ 🔑:
    * 🎚.
    * 🔢 🔢.
    * 🍪, ♒️.

➕ 🌐 💂‍♂ ⚒ ⚪️➡️ 💃 (🔌 **🎉 🍪**).

🌐 🏗 ♻ 🧰 &amp; 🦲 👈 ⏩ 🛠️ ⏮️ 👆 ⚙️, 📊 🏪, 🔗 &amp; ☁ 💽, ♒️.

### 🔗 💉

FastAPI 🔌 📶 ⏩ ⚙️, ✋️ 📶 🏋️ <abbr title='also known as "components", "resources", "services", "providers"'><strong>🔗 💉</strong></abbr> ⚙️.

* 🔗 💪 ✔️ 🔗, 🏗 🔗 ⚖️ **"📊" 🔗**.
* 🌐 **🔁 🍵** 🛠️.
* 🌐 🔗 💪 🚚 💽 ⚪️➡️ 📨 &amp; **↔ ➡ 🛠️** ⚛ &amp; 🏧 🧾.
* **🏧 🔬** *➡ 🛠️* 🔢 🔬 🔗.
* 🐕‍🦺 🏗 👩‍💻 🤝 ⚙️, **💽 🔗**, ♒️.
* **🙅‍♂ ⚠** ⏮️ 💽, 🕸, ♒️. ✋️ ⏩ 🛠️ ⏮️ 🌐 👫.

### ♾ "🔌-🔌"

⚖️ 🎏 🌌, 🙅‍♂ 💪 👫, 🗄 &amp; ⚙️ 📟 👆 💪.

🙆 🛠️ 🏗 🙅 ⚙️ (⏮️ 🔗) 👈 👆 💪 ✍ "🔌-" 👆 🈸 2️⃣ ⏸ 📟 ⚙️ 🎏 📊 &amp; ❕ ⚙️ 👆 *➡ 🛠️*.

### 💯

* 1️⃣0️⃣0️⃣ 💯 <abbr title="The amount of code that is automatically tested">💯 💰</abbr>.
* 1️⃣0️⃣0️⃣ 💯 <abbr title="Python type annotations, with this your editor and external tools can give you better support">🆎 ✍</abbr> 📟 🧢.
* ⚙️ 🏭 🈸.

## 💃 ⚒

**FastAPI** 🍕 🔗 ⏮️ (&amp; ⚓️ 🔛) <a href="https://www.starlette.io/" class="external-link" target="_blank"><strong>💃</strong></a>. , 🙆 🌖 💃 📟 👆 ✔️, 🔜 👷.

`FastAPI` 🤙 🎧-🎓 `Starlette`. , 🚥 👆 ⏪ 💭 ⚖️ ⚙️ 💃, 🌅 🛠️ 🔜 👷 🎏 🌌.

⏮️ **FastAPI** 👆 🤚 🌐 **💃**'Ⓜ ⚒ (FastAPI 💃 🔛 💊):

* 🤙 🎆 🎭. ⚫️ <a href="https://github.com/encode/starlette#performance" class="external-link" target="_blank">1️⃣ ⏩ 🐍 🛠️ 💪, 🔛 🇷🇪 ⏮️ **✳** &amp; **🚶**</a>.
* ** *️⃣ ** 🐕‍🦺.
* -🛠️ 🖥 📋.
* 🕴 &amp; 🤫 🎉.
* 💯 👩‍💻 🏗 🔛 🇸🇲.
* **⚜**, 🗜, 🎻 📁, 🎏 📨.
* **🎉 &amp; 🍪** 🐕‍🦺.
* 1️⃣0️⃣0️⃣ 💯 💯 💰.
* 1️⃣0️⃣0️⃣ 💯 🆎 ✍ ✍.

## Pydantic ⚒

**FastAPI** 🍕 🔗 ⏮️ (&amp; ⚓️ 🔛) <a href="https://pydantic-docs.helpmanual.io" class="external-link" target="_blank"><strong>Pydantic</strong></a>. , 🙆 🌖 Pydantic 📟 👆 ✔️, 🔜 👷.

✅ 🔢 🗃 ⚓️ 🔛 Pydantic, <abbr title="Object-Relational Mapper">🐜</abbr>Ⓜ, <abbr title="Object-Document Mapper">🏭</abbr>Ⓜ 💽.

👉 ⛓ 👈 📚 💼 👆 💪 🚶‍♀️ 🎏 🎚 👆 🤚 ⚪️➡️ 📨 **🔗 💽**, 🌐 ✔ 🔁.

🎏 ✔ 🎏 🌌 🤭, 📚 💼 👆 💪 🚶‍♀️ 🎚 👆 🤚 ⚪️➡️ 💽 **🔗 👩‍💻**.

⏮️ **FastAPI** 👆 🤚 🌐 **Pydantic**'Ⓜ ⚒ (FastAPI ⚓️ 🔛 Pydantic 🌐 💽 🚚):

* **🙅‍♂ 🔠**:
    * 🙅‍♂ 🆕 🔗 🔑 ◾-🇪🇸 💡.
    * 🚥 👆 💭 🐍 🆎 👆 💭 ❔ ⚙️ Pydantic.
* 🤾 🎆 ⏮️ 👆 **<abbr title="Integrated Development Environment, similar to a code editor">💾</abbr>/<abbr title="A program that checks for code errors">🧶</abbr>/🧠**:
    * ↩️ Pydantic 📊 📊 👐 🎓 👆 🔬; 🚘-🛠️, 🧽, ✍ &amp; 👆 🤔 🔜 🌐 👷 ☑ ⏮️ 👆 ✔ 💽.
* **⏩**:
    *  <a href="https://pydantic-docs.helpmanual.io/benchmarks/" class="external-link" target="_blank">📇</a> Pydantic ⏩ 🌘 🌐 🎏 💯 🗃.
* ✔ **🏗 📊**:
    * ⚙️ 🔗 Pydantic 🏷, 🐍 `typing`'Ⓜ `List` &amp; `Dict`, ♒️.
    *  &amp; 💳 ✔ 🏗 💽 🔗 🎯 &amp; 💪 🔬, ✅ &amp; 📄 🎻 🔗.
    * 👆 💪 ✔️ 🙇 **🐦 🎻** 🎚 &amp; ✔️ 👫 🌐 ✔ &amp; ✍.
* **🏧**:
    * Pydantic ✔ 🛃 📊 🆎 🔬 ⚖️ 👆 💪 ↔ 🔬 ⏮️ 👩‍🔬 🔛 🏷 🎀 ⏮️ 💳 👨‍🎨.
* 1️⃣0️⃣0️⃣ 💯 💯 💰.
