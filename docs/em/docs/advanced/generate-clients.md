# 🏗 👩‍💻

**FastAPI** ⚓️ 🔛 🗄 🔧, 👆 🤚 🏧 🔗 ⏮️ 📚 🧰, 🔌 🏧 🛠️ 🩺 (🚚 🦁 🎚).

1️⃣ 🎯 📈 👈 🚫 🎯 ⭐ 👈 👆 💪 **🏗 👩‍💻** (🕣 🤙 <abbr title="Software Development Kits">**📱**</abbr> ) 👆 🛠️, 📚 🎏 **🛠️ 🇪🇸**.

## 🗄 👩‍💻 🚂

📤 📚 🧰 🏗 👩‍💻 ⚪️➡️ **🗄**.

⚠ 🧰 <a href="https://openapi-generator.tech/" class="external-link" target="_blank">🗄 🚂</a>.

🚥 👆 🏗 **🕸**, 📶 😌 🎛 <a href="https://github.com/hey-api/openapi-ts" class="external-link" target="_blank">🗄-📕-🇦🇪</a>.

## 🏗 📕 🕸 👩‍💻

➡️ ▶️ ⏮️ 🙅 FastAPI 🈸:

{* ../../docs_src/generate_clients/tutorial001.py hl[9:11,14:15,18,19,23] *}

👀 👈 *➡ 🛠️* 🔬 🏷 👫 ⚙️ 📨 🚀 &amp; 📨 🚀, ⚙️ 🏷 `Item` &amp; `ResponseMessage`.

### 🛠️ 🩺

🚥 👆 🚶 🛠️ 🩺, 👆 🔜 👀 👈 ⚫️ ✔️ **🔗** 📊 📨 📨 &amp; 📨 📨:

<img src="/img/tutorial/generate-clients/image01.png">

👆 💪 👀 👈 🔗 ↩️ 👫 📣 ⏮️ 🏷 📱.

👈 ℹ 💪 📱 **🗄 🔗**, &amp; ⤴️ 🎦 🛠️ 🩺 (🦁 🎚).

&amp; 👈 🎏 ℹ ⚪️➡️ 🏷 👈 🔌 🗄 ⚫️❔ 💪 ⚙️ **🏗 👩‍💻 📟**.

### 🏗 📕 👩‍💻

🔜 👈 👥 ✔️ 📱 ⏮️ 🏷, 👥 💪 🏗 👩‍💻 📟 🕸.

#### ❎ `openapi-ts`

👆 💪 ❎ `openapi-ts` 👆 🕸 📟 ⏮️:

<div class="termy">

```console
$ npm install @hey-api/openapi-ts --save-dev

---> 100%
```

</div>

#### 🏗 👩‍💻 📟

🏗 👩‍💻 📟 👆 💪 ⚙️ 📋 ⏸ 🈸 `openapi-ts` 👈 🔜 🔜 ❎.

↩️ ⚫️ ❎ 🇧🇿 🏗, 👆 🎲 🚫🔜 💪 🤙 👈 📋 🔗, ✋️ 👆 🔜 🚮 ⚫️ 🔛 👆 `package.json` 📁.

⚫️ 💪 👀 💖 👉:

```JSON  hl_lines="7"
{
  "name": "frontend-app",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "generate-client": "openapi-ts --input http://localhost:8000/openapi.json --output ./src/client --client axios"
  },
  "author": "",
  "license": "",
  "devDependencies": {
    "@hey-api/openapi-ts": "^0.27.38",
    "typescript": "^4.6.2"
  }
}
```

⏮️ ✔️ 👈 ☕ `generate-client` ✍ 📤, 👆 💪 🏃 ⚫️ ⏮️:

<div class="termy">

```console
$ npm run generate-client

frontend-app@1.0.0 generate-client /home/user/code/frontend-app
> openapi-ts --input http://localhost:8000/openapi.json --output ./src/client --client axios
```

</div>

👈 📋 🔜 🏗 📟 `./src/client` &amp; 🔜 ⚙️ `axios` (🕸 🇺🇸🔍 🗃) 🔘.

### 🔄 👅 👩‍💻 📟

🔜 👆 💪 🗄 &amp; ⚙️ 👩‍💻 📟, ⚫️ 💪 👀 💖 👉, 👀 👈 👆 🤚 ✍ 👩‍🔬:

<img src="/img/tutorial/generate-clients/image02.png">

👆 🔜 🤚 ✍ 🚀 📨:

<img src="/img/tutorial/generate-clients/image03.png">

/// tip

👀 ✍ `name` &amp; `price`, 👈 🔬 FastAPI 🈸, `Item` 🏷.

///

👆 🔜 ✔️ ⏸ ❌ 📊 👈 👆 📨:

<img src="/img/tutorial/generate-clients/image04.png">

📨 🎚 🔜 ✔️ ✍:

<img src="/img/tutorial/generate-clients/image05.png">

## FastAPI 📱 ⏮️ 🔖

📚 💼 👆 FastAPI 📱 🔜 🦏, &amp; 👆 🔜 🎲 ⚙️ 🔖 🎏 🎏 👪 *➡ 🛠️*.

🖼, 👆 💪 ✔️ 📄 **🏬** &amp; ➕1️⃣ 📄 **👩‍💻**, &amp; 👫 💪 👽 🔖:


{* ../../docs_src/generate_clients/tutorial002.py hl[23,28,36] *}

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

{* ../../docs_src/generate_clients/tutorial003.py hl[8:9,12] *}

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

{* ../../docs_src/generate_clients/tutorial004.py *}

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
    "generate-client": "openapi-ts --input ./openapi.json --output ./src/client --client axios"
  },
  "author": "",
  "license": "",
  "devDependencies": {
    "@hey-api/openapi-ts": "^0.27.38",
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
