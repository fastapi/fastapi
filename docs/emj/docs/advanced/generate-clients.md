# 🏗 👩‍💻

**FastAPI** ⚓️ 🔛 🗄 🔧, 👆 🤚 🏧 🔗 ⏮️ 📚 🧰, 🔌 🏧 🛠️ 🩺 (🚚 🦁 🎚).

1️⃣ 🎯 📈 👈 🚫 🎯 ⭐ 👈 👆 💪 **🏗 👩‍💻** (🕣 🤙 <abbr title="Software Development Kits">**📱**</abbr> ) 👆 🛠️, 📚 🎏 **🛠️ 🇪🇸**.

## 🗄 👩‍💻 🚂

📤 📚 🧰 🏗 👩‍💻 ⚪️➡️ **🗄**.

⚠ 🧰 <a href="https://openapi-generator.tech/" class="external-link" target="_blank">🗄 🚂</a>.

🚥 👆 🏗 **🕸**, 📶 😌 🎛 <a href="https://github.com/ferdikoomen/openapi-typescript-codegen" class="external-link" target="_blank">🗄-📕-🇦🇪</a>.

## 🏗 📕 🕸 👩‍💻

➡️ ▶️ ⏮️ 🙅 FastAPI 🈸:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="9-11  14-15  18  19  23"
    {!> ../../../docs_src/generate_clients/tutorial001.py!}
    ```

=== "🐍 3️⃣.9️⃣ &amp; 🔛"

    ```Python hl_lines="7-9  12-13  16-17  21"
    {!> ../../../docs_src/generate_clients/tutorial001_py39.py!}
    ```

👀 👈 *➡ 🛠️* 🔬 🏷 👫 ⚙️ 📨 🚀 &amp; 📨 🚀, ⚙️ 🏷 `Item` &amp; `ResponseMessage`.

### 🛠️ 🩺

🚥 👆 🚶 🛠️ 🩺, 👆 🔜 👀 👈 ⚫️ ✔️ **🔗** 📊 📨 📨 &amp; 📨 📨:

<img src="/img/tutorial/generate-clients/image01.png">

👆 💪 👀 👈 🔗 ↩️ 👫 📣 ⏮️ 🏷 📱.

👈 ℹ 💪 📱 **🗄 🔗**, &amp; ⤴️ 🎦 🛠️ 🩺 (🦁 🎚).

&amp; 👈 🎏 ℹ ⚪️➡️ 🏷 👈 🔌 🗄 ⚫️❔ 💪 ⚙️ **🏗 👩‍💻 📟**.

### 🏗 📕 👩‍💻

🔜 👈 👥 ✔️ 📱 ⏮️ 🏷, 👥 💪 🏗 👩‍💻 📟 🕸.

#### ❎ `openapi-typescript-codegen`

👆 💪 ❎ `openapi-typescript-codegen` 👆 🕸 📟 ⏮️:

<div class="termy">

```console
$ npm install openapi-typescript-codegen --save-dev

---> 100%
```

</div>

#### 🏗 👩‍💻 📟

🏗 👩‍💻 📟 👆 💪 ⚙️ 📋 ⏸ 🈸 `openapi` 👈 🔜 🔜 ❎.

↩️ ⚫️ ❎ 🇧🇿 🏗, 👆 🎲 🚫🔜 💪 🤙 👈 📋 🔗, ✋️ 👆 🔜 🚮 ⚫️ 🔛 👆 `package.json` 📁.

⚫️ 💪 👀 💖 👉:

```JSON  hl_lines="7"
{
  "name": "frontend-app",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "generate-client": "openapi --input http://localhost:8000/openapi.json --output ./src/client --client axios"
  },
  "author": "",
  "license": "",
  "devDependencies": {
    "openapi-typescript-codegen": "^0.20.1",
    "typescript": "^4.6.2"
  }
}
```

⏮️ ✔️ 👈 ☕ `generate-client` ✍ 📤, 👆 💪 🏃 ⚫️ ⏮️:

<div class="termy">

```console
$ npm run generate-client

frontend-app@1.0.0 generate-client /home/user/code/frontend-app
> openapi --input http://localhost:8000/openapi.json --output ./src/client --client axios
```

</div>

👈 📋 🔜 🏗 📟 `./src/client` &amp; 🔜 ⚙️ `axios` (🕸 🇺🇸🔍 🗃) 🔘.

### 🔄 👅 👩‍💻 📟

🔜 👆 💪 🗄 &amp; ⚙️ 👩‍💻 📟, ⚫️ 💪 👀 💖 👉, 👀 👈 👆 🤚 ✍ 👩‍🔬:

<img src="/img/tutorial/generate-clients/image02.png">

👆 🔜 🤚 ✍ 🚀 📨:

<img src="/img/tutorial/generate-clients/image03.png">

!!! tip
    👀 ✍ `name` &amp; `price`, 👈 🔬 FastAPI 🈸, `Item` 🏷.

👆 🔜 ✔️ ⏸ ❌ 📊 👈 👆 📨:

<img src="/img/tutorial/generate-clients/image04.png">

📨 🎚 🔜 ✔️ ✍:

<img src="/img/tutorial/generate-clients/image05.png">

## FastAPI 📱 ⏮️ 🔖

📚 💼 👆 FastAPI 📱 🔜 🦏, &amp; 👆 🔜 🎲 ⚙️ 🔖 🎏 🎏 👪 *➡ 🛠️*.

🖼, 👆 💪 ✔️ 📄 **🏬** &amp; ➕1️⃣ 📄 **👩‍💻**, &amp; 👫 💪 👽 🔖:


=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="23  28  36"
    {!> ../../../docs_src/generate_clients/tutorial002.py!}
    ```

=== "🐍 3️⃣.9️⃣ &amp; 🔛"

    ```Python hl_lines="21  26  34"
    {!> ../../../docs_src/generate_clients/tutorial002_py39.py!}
    ```

### 🏗 📕 👩‍💻 ⏮️ 🔖

🚥 👆 🏗 👩‍💻 FastAPI 📱 ⚙️ 🔖, ⚫️ 🔜 🛎 🎏 👩‍💻 📟 ⚓️ 🔛 🔖.

👉 🌌 👆 🔜 💪 ✔️ 👜 ✔ &amp; 👪 ☑ 👩‍💻 📟:

<img src="/img/tutorial/generate-clients/image06.png">

👉 💼 👆 ✔️:

* `ItemsService`
* `UsersService`

### 👩‍💻 👩‍🔬 📛

▶️️ 🔜 🏗 👩‍🔬 📛 💖 `createItemItemsPost` 🚫 👀 📶 🧹:

```TypeScript
ItemsService.createItemItemsPost({name: "Plumbus", price: 5})
```

...👈 ↩️ 👩‍💻 🚂 ⚙️ 🗄 🔗 **🛠️ 🆔** 🔠 *➡ 🛠️*.

🗄 🚚 👈 🔠 🛠️ 🆔 😍 🤭 🌐 *➡ 🛠️*, FastAPI ⚙️ **🔢 📛**, **➡**, &amp; **🇺🇸🔍 👩‍🔬/🛠️** 🏗 👈 🛠️ 🆔, ↩️ 👈 🌌 ⚫️ 💪 ⚒ 💭 👈 🛠️ 🆔 😍.

✋️ 👤 🔜 🎦 👆 ❔ 📉 👈 ⏭. 👶

## 🛃 🛠️ 🆔 &amp; 👍 👩‍🔬 📛

👆 💪 **🔀** 🌌 👫 🛠️ 🆔 **🏗** ⚒ 👫 🙅 &amp; ✔️ **🙅 👩‍🔬 📛** 👩‍💻.

👉 💼 👆 🔜 ✔️ 🚚 👈 🔠 🛠️ 🆔 **😍** 🎏 🌌.

🖼, 👆 💪 ⚒ 💭 👈 🔠 *➡ 🛠️* ✔️ 🔖, &amp; ⤴️ 🏗 🛠️ 🆔 ⚓️ 🔛 **🔖** &amp; *➡ 🛠️* **📛** (🔢 📛).

### 🛃 🏗 😍 🆔 🔢

FastAPI ⚙️ **😍 🆔** 🔠 *➡ 🛠️*, ⚫️ ⚙️ **🛠️ 🆔** &amp; 📛 🙆 💪 🛃 🏷, 📨 ⚖️ 📨.

👆 💪 🛃 👈 🔢. ⚫️ ✊ `APIRoute` &amp; 🔢 🎻.

🖼, 📥 ⚫️ ⚙️ 🥇 🔖 (👆 🔜 🎲 ✔️ 🕴 1️⃣ 🔖) &amp; *➡ 🛠️* 📛 (🔢 📛).

👆 💪 ⤴️ 🚶‍♀️ 👈 🛃 🔢 **FastAPI** `generate_unique_id_function` 🔢:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="8-9  12"
    {!> ../../../docs_src/generate_clients/tutorial003.py!}
    ```

=== "🐍 3️⃣.9️⃣ &amp; 🔛"

    ```Python hl_lines="6-7  10"
    {!> ../../../docs_src/generate_clients/tutorial003_py39.py!}
    ```

### 🏗 📕 👩‍💻 ⏮️ 🛃 🛠️ 🆔

🔜 🚥 👆 🏗 👩‍💻 🔄, 👆 🔜 👀 👈 ⚫️ ✔️ 📉 👩‍🔬 📛:

<img src="/img/tutorial/generate-clients/image07.png">

👆 👀, 👩‍🔬 📛 🔜 ✔️ 🔖 &amp; ⤴️ 🔢 📛, 🔜 👫 🚫 🔌 ℹ ⚪️➡️ 📛 ➡ &amp; 🇺🇸🔍 🛠️.

### 🗜 🗄 🔧 👩‍💻 🚂

🏗 📟 ✔️ **❎ ℹ**.

👥 ⏪ 💭 👈 👉 👩‍🔬 🔗 **🏬** ↩️ 👈 🔤 `ItemsService` (✊ ⚪️➡️ 🔖), ✋️ 👥 ✔️ 📛 🔡 👩‍🔬 📛 💁‍♂️. 👶

👥 🔜 🎲 💚 🚧 ⚫️ 🗄 🏢, 👈 🔜 🚚 👈 🛠️ 🆔 **😍**.

✋️ 🏗 👩‍💻 👥 💪 **🔀** 🗄 🛠️ 🆔 ▶️️ ⏭ 🏭 👩‍💻, ⚒ 👈 👩‍🔬 📛 👌 &amp; **🧹**.

👥 💪 ⏬ 🗄 🎻 📁 `openapi.json` &amp; ⤴️ 👥 💪 **❎ 👈 🔡 🔖** ⏮️ ✍ 💖 👉:

```Python
{!../../../docs_src/generate_clients/tutorial004.py!}
```

⏮️ 👈, 🛠️ 🆔 🔜 📁 ⚪️➡️ 👜 💖 `items-get_items` `get_items`, 👈 🌌 👩‍💻 🚂 💪 🏗 🙅 👩‍🔬 📛.

### 🏗 📕 👩‍💻 ⏮️ 🗜 🗄

🔜 🔚 🏁 📁 `openapi.json`, 👆 🔜 🔀 `package.json` ⚙️ 👈 🇧🇿 📁, 🖼:

```JSON  hl_lines="7"
{
  "name": "frontend-app",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "generate-client": "openapi --input ./openapi.json --output ./src/client --client axios"
  },
  "author": "",
  "license": "",
  "devDependencies": {
    "openapi-typescript-codegen": "^0.20.1",
    "typescript": "^4.6.2"
  }
}
```

⏮️ 🏭 🆕 👩‍💻, 👆 🔜 🔜 ✔️ **🧹 👩‍🔬 📛**, ⏮️ 🌐 **✍**, **⏸ ❌**, ♒️:

<img src="/img/tutorial/generate-clients/image08.png">

## 💰

🕐❔ ⚙️ 🔁 🏗 👩‍💻 👆 🔜 **✍** :

* 👩‍🔬.
* 📨 🚀 💪, 🔢 🔢, ♒️.
* 📨 🚀.

👆 🔜 ✔️ **⏸ ❌** 🌐.

&amp; 🕐❔ 👆 ℹ 👩‍💻 📟, &amp; **♻** 🕸, ⚫️ 🔜 ✔️ 🙆 🆕 *➡ 🛠️* 💪 👩‍🔬, 🗝 🕐 ❎, &amp; 🙆 🎏 🔀 🔜 🎨 🔛 🏗 📟. 👶

👉 ⛓ 👈 🚥 🕳 🔀 ⚫️ 🔜 **🎨** 🔛 👩‍💻 📟 🔁. &amp; 🚥 👆 **🏗** 👩‍💻 ⚫️ 🔜 ❌ 👅 🚥 👆 ✔️ 🙆 **🔖** 📊 ⚙️.

, 👆 🔜 **🔍 📚 ❌** 📶 ⏪ 🛠️ 🛵 ↩️ ✔️ ⌛ ❌ 🎦 🆙 👆 🏁 👩‍💻 🏭 &amp; ⤴️ 🔄 ℹ 🌐❔ ⚠. 👶
