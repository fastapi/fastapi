# 🦏 🈸 - 💗 📁

🚥 👆 🏗 🈸 ⚖️ 🕸 🛠️, ⚫️ 🛎 💼 👈 👆 💪 🚮 🌐 🔛 👁 📁.

**FastAPI** 🚚 🏪 🧰 📊 👆 🈸 ⏪ 🚧 🌐 💪.

!!! info
    🚥 👆 👟 ⚪️➡️ 🏺, 👉 🔜 🌓 🏺 📗.

## 🖼 📁 📊

➡️ 💬 👆 ✔️ 📁 📊 💖 👉:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   └── routers
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── internal
│       ├── __init__.py
│       └── admin.py
```

!!! tip
    📤 📚 `__init__.py` 📁: 1️⃣ 🔠 📁 ⚖️ 📁.

    👉 ⚫️❔ ✔ 🏭 📟 ⚪️➡️ 1️⃣ 📁 🔘 ➕1️⃣.

    🖼, `app/main.py` 👆 💪 ✔️ ⏸ 💖:

    ```
    from app.routers import items
    ```

*  `app` 📁 🔌 🌐. &amp; ⚫️ ✔️ 🛁 📁 `app/__init__.py`, ⚫️ "🐍 📦" (🗃 "🐍 🕹"): `app`.
* ⚫️ 🔌 `app/main.py` 📁. ⚫️ 🔘 🐍 📦 (📁 ⏮️ 📁 `__init__.py`), ⚫️ "🕹" 👈 📦: `app.main`.
* 📤 `app/dependencies.py` 📁, 💖 `app/main.py`, ⚫️ "🕹": `app.dependencies`.
* 📤 📁 `app/routers/` ⏮️ ➕1️⃣ 📁 `__init__.py`, ⚫️ "🐍 📦": `app.routers`.
* 📁 `app/routers/items.py` 🔘 📦, `app/routers/`,, ⚫️ 🔁: `app.routers.items`.
* 🎏 ⏮️ `app/routers/users.py`, ⚫️ ➕1️⃣ 🔁: `app.routers.users`.
* 📤 📁 `app/internal/` ⏮️ ➕1️⃣ 📁 `__init__.py`, ⚫️ ➕1️⃣ "🐍 📦": `app.internal`.
*  &amp; 📁 `app/internal/admin.py` ➕1️⃣ 🔁: `app.internal.admin`.

<img src="/img/tutorial/bigger-applications/package.svg">

🎏 📁 📊 ⏮️ 🏤:

```
.
├── app                  # "app" is a Python package
│   ├── __init__.py      # this file makes "app" a "Python package"
│   ├── main.py          # "main" module, e.g. import app.main
│   ├── dependencies.py  # "dependencies" module, e.g. import app.dependencies
│   └── routers          # "routers" is a "Python subpackage"
│   │   ├── __init__.py  # makes "routers" a "Python subpackage"
│   │   ├── items.py     # "items" submodule, e.g. import app.routers.items
│   │   └── users.py     # "users" submodule, e.g. import app.routers.users
│   └── internal         # "internal" is a "Python subpackage"
│       ├── __init__.py  # makes "internal" a "Python subpackage"
│       └── admin.py     # "admin" submodule, e.g. import app.internal.admin
```

## `APIRouter`

➡️ 💬 📁 💡 🚚 👩‍💻 🔁 `/app/routers/users.py`.

👆 💚 ✔️ *➡ 🛠️* 🔗 👆 👩‍💻 👽 ⚪️➡️ 🎂 📟, 🚧 ⚫️ 🏗.

✋️ ⚫️ 🍕 🎏 **FastAPI** 🈸/🕸 🛠️ (⚫️ 🍕 🎏 "🐍 📦").

👆 💪 ✍ *➡ 🛠️* 👈 🕹 ⚙️ `APIRouter`.

### 🗄 `APIRouter`

👆 🗄 ⚫️ &amp; ✍ "👐" 🎏 🌌 👆 🔜 ⏮️ 🎓 `FastAPI`:

```Python hl_lines="1  3"
{!../../../docs_src/bigger_applications/app/routers/users.py!}
```

### *➡ 🛠️* ⏮️ `APIRouter`

&amp; ⤴️ 👆 ⚙️ ⚫️ 📣 👆 *➡ 🛠️*.

⚙️ ⚫️ 🎏 🌌 👆 🔜 ⚙️ `FastAPI` 🎓:

```Python hl_lines="6  11  16"
{!../../../docs_src/bigger_applications/app/routers/users.py!}
```

👆 💪 💭 `APIRouter` "🐩 `FastAPI`" 🎓.

🌐 🎏 🎛 🐕‍🦺.

🌐 🎏 `parameters`, `responses`, `dependencies`, `tags`, ♒️.

!!! tip
    👉 🖼, 🔢 🤙 `router`, ✋️ 👆 💪 📛 ⚫️ 👐 👆 💚.

👥 🔜 🔌 👉 `APIRouter` 👑 `FastAPI` 📱, ✋️ 🥇, ➡️ ✅ 🔗 &amp; ➕1️⃣ `APIRouter`.

## 🔗

👥 👀 👈 👥 🔜 💪 🔗 ⚙️ 📚 🥉 🈸.

👥 🚮 👫 👫 👍 `dependencies` 🕹 (`app/dependencies.py`).

👥 🔜 🔜 ⚙️ 🙅 🔗 ✍ 🛃 `X-Token` 🎚:

```Python hl_lines="1  4-6"
{!../../../docs_src/bigger_applications/app/dependencies.py!}
```

!!! tip
    👥 ⚙️ 💭 🎚 📉 👉 🖼.

    ✋️ 🎰 💼 👆 🔜 🤚 👍 🏁 ⚙️ 🛠️ [💂‍♂ 🚙](./security/index.md){.internal-link target=_blank}.

## ➕1️⃣ 🕹 ⏮️ `APIRouter`

➡️ 💬 👆 ✔️ 🔗 💡 🚚 "🏬" ⚪️➡️ 👆 🈸 🕹 `app/routers/items.py`.

👆 ✔️ *➡ 🛠️* :

* `/items/`
* `/items/{item_id}`

⚫️ 🌐 🎏 📊 ⏮️ `app/routers/users.py`.

✋️ 👥 💚 🙃 &amp; 📉 📟 🍖.

👥 💭 🌐 *➡ 🛠️* 👉 🕹 ✔️ 🎏:

* ➡ `prefix`: `/items`.
* `tags`: (1️⃣ 🔖: `items`).
* ➕ `responses`.
* `dependencies`: 👫 🌐 💪 👈 `X-Token` 🔗 👥 ✍.

, ↩️ ❎ 🌐 👈 🔠 *➡ 🛠️*, 👥 💪 🚮 ⚫️ `APIRouter`.

```Python hl_lines="5-10  16  21"
{!../../../docs_src/bigger_applications/app/routers/items.py!}
```

➡ 🔠 *➡ 🛠️* ✔️ ▶️ ⏮️ `/`, 💖:

```Python hl_lines="1"
@router.get("/{item_id}")
async def read_item(item_id: str):
    ...
```

...🔡 🔜 🚫 🔌 🏁 `/`.

, 🔡 👉 💼 `/items`.

👥 💪 🚮 📇 `tags` &amp; ➕ `responses` 👈 🔜 ✔ 🌐 *➡ 🛠️* 🔌 👉 📻.

&amp; 👥 💪 🚮 📇 `dependencies` 👈 🔜 🚮 🌐 *➡ 🛠️* 📻 &amp; 🔜 🛠️/❎ 🔠 📨 ⚒ 👫.

!!! tip
    🗒 👈, 🌅 💖 [🔗 *➡ 🛠️ 👨‍🎨*](dependencies/dependencies-in-path-operation-decorators.md){.internal-link target=_blank}, 🙅‍♂ 💲 🔜 🚶‍♀️ 👆 *➡ 🛠️ 🔢*.

🔚 🏁 👈 🏬 ➡ 🔜:

* `/items/`
* `/items/{item_id}`

...👥 🎯.

* 👫 🔜 ™ ⏮️ 📇 🔖 👈 🔌 👁 🎻 `"items"`.
    * 👫 "🔖" ✴️ ⚠ 🏧 🎓 🧾 ⚙️ (⚙️ 🗄).
* 🌐 👫 🔜 🔌 🔁 `responses`.
* 🌐 👫 *➡ 🛠️* 🔜 ✔️ 📇 `dependencies` 🔬/🛠️ ⏭ 👫.
    * 🚥 👆 📣 🔗 🎯 *➡ 🛠️*, **👫 🔜 🛠️ 💁‍♂️**.
    * 📻 🔗 🛠️ 🥇, ⤴️ [`dependencies` 👨‍🎨](dependencies/dependencies-in-path-operation-decorators.md){.internal-link target=_blank}, &amp; ⤴️ 😐 🔢 🔗.
    * 👆 💪 🚮 [`Security` 🔗 ⏮️ `scopes`](../advanced/security/oauth2-scopes.md){.internal-link target=_blank}.

!!! tip
    ✔️ `dependencies` `APIRouter` 💪 ⚙️, 🖼, 🚚 🤝 🎂 👪 *➡ 🛠️*. 🚥 🔗 🚫 🚮 📦 🔠 1️⃣ 👫.

!!! check
     `prefix`, `tags`, `responses`, &amp; `dependencies` 🔢 (📚 🎏 💼) ⚒ ⚪️➡️ **FastAPI** ℹ 👆 ❎ 📟 ❎.

### 🗄 🔗

👉 📟 👨‍❤‍👨 🕹 `app.routers.items`, 📁 `app/routers/items.py`.

&amp; 👥 💪 🤚 🔗 🔢 ⚪️➡️ 🕹 `app.dependencies`, 📁 `app/dependencies.py`.

👥 ⚙️ ⚖ 🗄 ⏮️ `..` 🔗:

```Python hl_lines="3"
{!../../../docs_src/bigger_applications/app/routers/items.py!}
```

#### ❔ ⚖ 🗄 👷

!!! tip
    🚥 👆 💭 👌 ❔ 🗄 👷, 😣 ⏭ 📄 🔛.

👁 ❣ `.`, 💖:

```Python
from .dependencies import get_token_header
```

🔜 ⛓:

* ▶️ 🎏 📦 👈 👉 🕹 (📁 `app/routers/items.py`) 🖖 (📁 `app/routers/`)...
* 🔎 🕹 `dependencies` (👽 📁 `app/routers/dependencies.py`)...
*  &amp; ⚪️➡️ ⚫️, 🗄 🔢 `get_token_header`.

✋️ 👈 📁 🚫 🔀, 👆 🔗 📁 `app/dependencies.py`.

💭 ❔ 👆 📱/📁 📊 👀 💖:

<img src="/img/tutorial/bigger-applications/package.svg">

---

2️⃣ ❣ `..`, 💖:

```Python
from ..dependencies import get_token_header
```

⛓:

* ▶️ 🎏 📦 👈 👉 🕹 (📁 `app/routers/items.py`) 🖖 (📁 `app/routers/`)...
* 🚶 👪 📦 (📁 `app/`)...
*  &amp; 📤, 🔎 🕹 `dependencies` (📁 `app/dependencies.py`)...
*  &amp; ⚪️➡️ ⚫️, 🗄 🔢 `get_token_header`.

👈 👷 ☑ ❗ 👶

---

🎏 🌌, 🚥 👥 ✔️ ⚙️ 3️⃣ ❣ `...`, 💖:

```Python
from ...dependencies import get_token_header
```

that 🔜 ⛓:

* ▶️ 🎏 📦 👈 👉 🕹 (📁 `app/routers/items.py`) 🖖 (📁 `app/routers/`)...
* 🚶 👪 📦 (📁 `app/`)...
* ⤴️ 🚶 👪 👈 📦 (📤 🙅‍♂ 👪 📦, `app` 🔝 🎚 👶)...
*  &amp; 📤, 🔎 🕹 `dependencies` (📁 `app/dependencies.py`)...
*  &amp; ⚪️➡️ ⚫️, 🗄 🔢 `get_token_header`.

👈 🔜 🔗 📦 🔛 `app/`, ⏮️ 🚮 👍 📁 `__init__.py`, ♒️. ✋️ 👥 🚫 ✔️ 👈. , 👈 🔜 🚮 ❌ 👆 🖼. 👶

✋️ 🔜 👆 💭 ❔ ⚫️ 👷, 👆 💪 ⚙️ ⚖ 🗄 👆 👍 📱 🙅‍♂ 🤔 ❔ 🏗 👫. 👶

### 🚮 🛃 `tags`, `responses`, &amp; `dependencies`

👥 🚫 ❎ 🔡 `/items` 🚫 `tags=["items"]` 🔠 *➡ 🛠️* ↩️ 👥 🚮 👫 `APIRouter`.

✋️ 👥 💪 🚮 _🌅_ `tags` 👈 🔜 ✔ 🎯 *➡ 🛠️*, &amp; ➕ `responses` 🎯 👈 *➡ 🛠️*:

```Python hl_lines="30-31"
{!../../../docs_src/bigger_applications/app/routers/items.py!}
```

!!! tip
    👉 🏁 ➡ 🛠️ 🔜 ✔️ 🌀 🔖: `["items", "custom"]`.

     &amp; ⚫️ 🔜 ✔️ 👯‍♂️ 📨 🧾, 1️⃣ `404` &amp; 1️⃣ `403`.

## 👑 `FastAPI`

🔜, ➡️ 👀 🕹 `app/main.py`.

📥 🌐❔ 👆 🗄 &amp; ⚙️ 🎓 `FastAPI`.

👉 🔜 👑 📁 👆 🈸 👈 👔 🌐 👯‍♂️.

&amp; 🏆 👆 ⚛ 🔜 🔜 🖖 🚮 👍 🎯 🕹, 👑 📁 🔜 🙅.

### 🗄 `FastAPI`

👆 🗄 &amp; ✍ `FastAPI` 🎓 🛎.

&amp; 👥 💪 📣 [🌐 🔗](dependencies/global-dependencies.md){.internal-link target=_blank} 👈 🔜 🌀 ⏮️ 🔗 🔠 `APIRouter`:

```Python hl_lines="1  3  7"
{!../../../docs_src/bigger_applications/app/main.py!}
```

### 🗄 `APIRouter`

🔜 👥 🗄 🎏 🔁 👈 ✔️ `APIRouter`Ⓜ:

```Python hl_lines="5"
{!../../../docs_src/bigger_applications/app/main.py!}
```

📁 `app/routers/users.py` &amp; `app/routers/items.py` 🔁 👈 🍕 🎏 🐍 📦 `app`, 👥 💪 ⚙️ 👁 ❣ `.` 🗄 👫 ⚙️ "⚖ 🗄".

### ❔ 🏭 👷

📄:

```Python
from .routers import items, users
```

⛓:

* ▶️ 🎏 📦 👈 👉 🕹 (📁 `app/main.py`) 🖖 (📁 `app/`)...
* 👀 📦 `routers` (📁 `app/routers/`)...
*  &amp; ⚪️➡️ ⚫️, 🗄 🔁 `items` (📁 `app/routers/items.py`) &amp; `users` (📁 `app/routers/users.py`)...

🕹 `items` 🔜 ✔️ 🔢 `router` (`items.router`). 👉 🎏 1️⃣ 👥 ✍ 📁 `app/routers/items.py`, ⚫️ `APIRouter` 🎚.

&amp; ⤴️ 👥 🎏 🕹 `users`.

👥 💪 🗄 👫 💖:

```Python
from app.routers import items, users
```

!!! info
    🥇 ⏬ "⚖ 🗄":

    ```Python
    from .routers import items, users
    ```

    🥈 ⏬ "🎆 🗄":

    ```Python
    from app.routers import items, users
    ```

    💡 🌅 🔃 🐍 📦 &amp; 🕹, ✍ <a href="https://docs.python.org/3/tutorial/modules.html" class="external-link" target="_blank">🛂 🐍 🧾 🔃 🕹</a>.

### ❎ 📛 💥

👥 🏭 🔁 `items` 🔗, ↩️ 🏭 🚮 🔢 `router`.

👉 ↩️ 👥 ✔️ ➕1️⃣ 🔢 📛 `router` 🔁 `users`.

🚥 👥 ✔️ 🗄 1️⃣ ⏮️ 🎏, 💖:

```Python
from .routers.items import router
from .routers.users import router
```

`router` ⚪️➡️ `users` 🔜 📁 1️⃣ ⚪️➡️ `items` &amp; 👥 🚫🔜 💪 ⚙️ 👫 🎏 🕰.

, 💪 ⚙️ 👯‍♂️ 👫 🎏 📁, 👥 🗄 🔁 🔗:

```Python hl_lines="4"
{!../../../docs_src/bigger_applications/app/main.py!}
```

### 🔌 `APIRouter`Ⓜ `users` &amp; `items`

🔜, ➡️ 🔌 `router`Ⓜ ⚪️➡️ 🔁 `users` &amp; `items`:

```Python hl_lines="10-11"
{!../../../docs_src/bigger_applications/app/main.py!}
```

!!! info
    `users.router` 🔌 `APIRouter` 🔘 📁 `app/routers/users.py`.

     &amp; `items.router` 🔌 `APIRouter` 🔘 📁 `app/routers/items.py`.

⏮️ `app.include_router()` 👥 💪 🚮 🔠 `APIRouter` 👑 `FastAPI` 🈸.

⚫️ 🔜 🔌 🌐 🛣 ⚪️➡️ 👈 📻 🍕 ⚫️.

!!! note "📡 ℹ"
    ⚫️ 🔜 🤙 🔘 ✍ *➡ 🛠️* 🔠 *➡ 🛠️* 👈 📣 `APIRouter`.

    , ⛅ 🎑, ⚫️ 🔜 🤙 👷 🚥 🌐 🎏 👁 📱.

!!! check
    👆 🚫 ✔️ 😟 🔃 🎭 🕐❔ ✅ 📻.

    👉 🔜 ✊ ⏲ &amp; 🔜 🕴 🔨 🕴.

    ⚫️ 🏆 🚫 📉 🎭. 👶

### 🔌 `APIRouter` ⏮️ 🛃 `prefix`, `tags`, `responses`, &amp; `dependencies`

🔜, ➡️ 🌈 👆 🏢 🤝 👆 `app/internal/admin.py` 📁.

⚫️ 🔌 `APIRouter` ⏮️ 📡 *➡ 🛠️* 👈 👆 🏢 💰 🖖 📚 🏗.

👉 🖼 ⚫️ 🔜 💎 🙅. ✋️ ➡️ 💬 👈 ↩️ ⚫️ 💰 ⏮️ 🎏 🏗 🏢, 👥 🚫🔜 🔀 ⚫️ &amp; 🚮 `prefix`, `dependencies`, `tags`, ♒️. 🔗 `APIRouter`:

```Python hl_lines="3"
{!../../../docs_src/bigger_applications/app/internal/admin.py!}
```

✋️ 👥 💚 ⚒ 🛃 `prefix` 🕐❔ ✅ `APIRouter` 👈 🌐 🚮 *➡ 🛠️* ▶️ ⏮️ `/admin`, 👥 💚 🔐 ⚫️ ⏮️ `dependencies` 👥 ⏪ ✔️ 👉 🏗, &amp; 👥 💚 🔌 `tags` &amp; `responses`.

👥 💪 📣 🌐 👈 🍵 ✔️ 🔀 ⏮️ `APIRouter` 🚶‍♀️ 👈 🔢 `app.include_router()`:

```Python hl_lines="14-17"
{!../../../docs_src/bigger_applications/app/main.py!}
```

👈 🌌, ⏮️ `APIRouter` 🔜 🚧 ⚗, 👥 💪 💰 👈 🎏 `app/internal/admin.py` 📁 ⏮️ 🎏 🏗 🏢.

🏁 👈 👆 📱, 🔠 *➡ 🛠️* ⚪️➡️ `admin` 🕹 🔜 ✔️:

* 🔡 `/admin`.
* 🔖 `admin`.
* 🔗 `get_token_header`.
* 📨 `418`. 👶

✋️ 👈 🔜 🕴 📉 👈 `APIRouter` 👆 📱, 🚫 🙆 🎏 📟 👈 ⚙️ ⚫️.

, 🖼, 🎏 🏗 💪 ⚙️ 🎏 `APIRouter` ⏮️ 🎏 🤝 👩‍🔬.

### 🔌 *➡ 🛠️*

👥 💪 🚮 *➡ 🛠️* 🔗 `FastAPI` 📱.

📥 👥 ⚫️... 🎦 👈 👥 💪 🤷:

```Python hl_lines="21-23"
{!../../../docs_src/bigger_applications/app/main.py!}
```

&amp; ⚫️ 🔜 👷 ☑, 👯‍♂️ ⏮️ 🌐 🎏 *➡ 🛠️* 🚮 ⏮️ `app.include_router()`.

!!! info "📶 📡 ℹ"
    **🗒**: 👉 📶 📡 ℹ 👈 👆 🎲 💪 **🚶**.

    ---

     `APIRouter`Ⓜ 🚫 "🗻", 👫 🚫 👽 ⚪️➡️ 🎂 🈸.

    👉 ↩️ 👥 💚 🔌 👫 *➡ 🛠️* 🗄 🔗 &amp; 👩‍💻 🔢.

    👥 🚫🔜 ❎ 👫 &amp; "🗻" 👫 ➡ 🎂, *➡ 🛠️* "🖖" (🏤-✍), 🚫 🔌 🔗.

## ✅ 🏧 🛠️ 🩺

🔜, 🏃 `uvicorn`, ⚙️ 🕹 `app.main` &amp; 🔢 `app`:

<div class="termy">

```console
$ uvicorn app.main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

&amp; 📂 🩺 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

👆 🔜 👀 🏧 🛠️ 🩺, ✅ ➡ ⚪️➡️ 🌐 🔁, ⚙️ ☑ ➡ (&amp; 🔡) &amp; ☑ 🔖:

<img src="/img/tutorial/bigger-applications/image01.png">

## 🔌 🎏 📻 💗 🕰 ⏮️ 🎏 `prefix`

👆 💪 ⚙️ `.include_router()` 💗 🕰 ⏮️ *🎏* 📻 ⚙️ 🎏 🔡.

👉 💪 ⚠, 🖼, 🎦 🎏 🛠️ 🔽 🎏 🔡, ✅ `/api/v1` &amp; `/api/latest`.

👉 🏧 ⚙️ 👈 👆 5️⃣📆 🚫 🤙 💪, ✋️ ⚫️ 📤 💼 👆.

## 🔌 `APIRouter` ➕1️⃣

🎏 🌌 👆 💪 🔌 `APIRouter` `FastAPI` 🈸, 👆 💪 🔌 `APIRouter` ➕1️⃣ `APIRouter` ⚙️:

```Python
router.include_router(other_router)
```

⚒ 💭 👆 ⚫️ ⏭ 🔌 `router` `FastAPI` 📱, 👈 *➡ 🛠️* ⚪️➡️ `other_router` 🔌.
