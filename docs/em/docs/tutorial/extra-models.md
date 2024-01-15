# ➕ 🏷

▶️ ⏮️ ⏮️ 🖼, ⚫️ 🔜 ⚠ ✔️ 🌅 🌘 1️⃣ 🔗 🏷.

👉 ✴️ 💼 👩‍💻 🏷, ↩️:

*  **🔢 🏷** 💪 💪 ✔️ 🔐.
*  **🔢 🏷** 🔜 🚫 ✔️ 🔐.
*  **💽 🏷** 🔜 🎲 💪 ✔️ #️⃣ 🔐.

!!! danger
    🙅 🏪 👩‍💻 🔢 🔐. 🕧 🏪 "🔐 #️⃣" 👈 👆 💪 ⤴️ ✔.

    🚥 👆 🚫 💭, 👆 🔜 💡 ⚫️❔ "🔐#️⃣" [💂‍♂ 📃](security/simple-oauth2.md#password-hashing){.internal-link target=_blank}.

## 💗 🏷

📥 🏢 💭 ❔ 🏷 💪 👀 💖 ⏮️ 👫 🔐 🏑 &amp; 🥉 🌐❔ 👫 ⚙️:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="9  11  16  22  24  29-30  33-35  40-41"
    {!> ../../../docs_src/extra_models/tutorial001.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="7  9  14  20  22  27-28  31-33  38-39"
    {!> ../../../docs_src/extra_models/tutorial001_py310.py!}
    ```

### 🔃 `**user_in.dict()`

#### Pydantic `.dict()`

`user_in` Pydantic 🏷 🎓 `UserIn`.

Pydantic 🏷 ✔️ `.dict()` 👩‍🔬 👈 📨 `dict` ⏮️ 🏷 💽.

, 🚥 👥 ✍ Pydantic 🎚 `user_in` 💖:

```Python
user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
```

&amp; ⤴️ 👥 🤙:

```Python
user_dict = user_in.dict()
```

👥 🔜 ✔️ `dict` ⏮️ 💽 🔢 `user_dict` (⚫️ `dict` ↩️ Pydantic 🏷 🎚).

&amp; 🚥 👥 🤙:

```Python
print(user_dict)
```

👥 🔜 🤚 🐍 `dict` ⏮️:

```Python
{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}
```

#### 🎁 `dict`

🚥 👥 ✊ `dict` 💖 `user_dict` &amp; 🚶‍♀️ ⚫️ 🔢 (⚖️ 🎓) ⏮️ `**user_dict`, 🐍 🔜 "🎁" ⚫️. ⚫️ 🔜 🚶‍♀️ 🔑 &amp; 💲 `user_dict` 🔗 🔑-💲 ❌.

, ▶️ ⏮️ `user_dict` ⚪️➡️ 🔛, ✍:

```Python
UserInDB(**user_dict)
```

🔜 🏁 🕳 🌓:

```Python
UserInDB(
    username="john",
    password="secret",
    email="john.doe@example.com",
    full_name=None,
)
```

⚖️ 🌅 ⚫️❔, ⚙️ `user_dict` 🔗, ⏮️ ⚫️❔ 🎚 ⚫️ 💪 ✔️ 🔮:

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
)
```

#### Pydantic 🏷 ⚪️➡️ 🎚 ➕1️⃣

🖼 🔛 👥 🤚 `user_dict` ⚪️➡️ `user_in.dict()`, 👉 📟:

```Python
user_dict = user_in.dict()
UserInDB(**user_dict)
```

🔜 🌓:

```Python
UserInDB(**user_in.dict())
```

...↩️ `user_in.dict()` `dict`, &amp; ⤴️ 👥 ⚒ 🐍 "🎁" ⚫️ 🚶‍♀️ ⚫️ `UserInDB` 🔠 ⏮️ `**`.

, 👥 🤚 Pydantic 🏷 ⚪️➡️ 💽 ➕1️⃣ Pydantic 🏷.

#### 🎁 `dict` &amp; ➕ 🇨🇻

&amp; ⤴️ ❎ ➕ 🇨🇻 ❌ `hashed_password=hashed_password`, 💖:

```Python
UserInDB(**user_in.dict(), hashed_password=hashed_password)
```

...🔚 🆙 💆‍♂ 💖:

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    hashed_password = hashed_password,
)
```

!!! warning
    🔗 🌖 🔢 🤖 💪 💧 💽, ✋️ 👫 ↗️ 🚫 🚚 🙆 🎰 💂‍♂.

## 📉 ❎

📉 📟 ❎ 1️⃣ 🐚 💭 **FastAPI**.

📟 ❎ 📈 🤞 🐛, 💂‍♂ ❔, 📟 🔁 ❔ (🕐❔ 👆 ℹ 1️⃣ 🥉 ✋️ 🚫 🎏), ♒️.

&amp; 👉 🏷 🌐 🤝 📚 💽 &amp; ❎ 🔢 📛 &amp; 🆎.

👥 💪 👻.

👥 💪 📣 `UserBase` 🏷 👈 🍦 🧢 👆 🎏 🏷. &amp; ⤴️ 👥 💪 ⚒ 🏿 👈 🏷 👈 😖 🚮 🔢 (🆎 📄, 🔬, ♒️).

🌐 💽 🛠️, 🔬, 🧾, ♒️. 🔜 👷 🛎.

👈 🌌, 👥 💪 📣 🔺 🖖 🏷 (⏮️ 🔢 `password`, ⏮️ `hashed_password` &amp; 🍵 🔐):

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="9  15-16  19-20  23-24"
    {!> ../../../docs_src/extra_models/tutorial002.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="7  13-14  17-18  21-22"
    {!> ../../../docs_src/extra_models/tutorial002_py310.py!}
    ```

## `Union` ⚖️ `anyOf`

👆 💪 📣 📨 `Union` 2️⃣ 🆎, 👈 ⛓, 👈 📨 🔜 🙆 2️⃣.

⚫️ 🔜 🔬 🗄 ⏮️ `anyOf`.

👈, ⚙️ 🐩 🐍 🆎 🔑 <a href="https://docs.python.org/3/library/typing.html#typing.Union" class="external-link" target="_blank">`typing.Union`</a>:

!!! note
    🕐❔ ⚖ <a href="https://pydantic-docs.helpmanual.io/usage/types/#unions" class="external-link" target="_blank">`Union`</a>, 🔌 🏆 🎯 🆎 🥇, ⏩ 🌘 🎯 🆎. 🖼 🔛, 🌖 🎯 `PlaneItem` 👟 ⏭ `CarItem` `Union[PlaneItem, CarItem]`.

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="1  14-15  18-20  33"
    {!> ../../../docs_src/extra_models/tutorial003.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="1  14-15  18-20  33"
    {!> ../../../docs_src/extra_models/tutorial003_py310.py!}
    ```

### `Union` 🐍 3️⃣.1️⃣0️⃣

👉 🖼 👥 🚶‍♀️ `Union[PlaneItem, CarItem]` 💲 ❌ `response_model`.

↩️ 👥 🚶‍♀️ ⚫️ **💲 ❌** ↩️ 🚮 ⚫️ **🆎 ✍**, 👥 ✔️ ⚙️ `Union` 🐍 3️⃣.1️⃣0️⃣.

🚥 ⚫️ 🆎 ✍ 👥 💪 ✔️ ⚙️ ⏸ ⏸,:

```Python
some_variable: PlaneItem | CarItem
```

✋️ 🚥 👥 🚮 👈 `response_model=PlaneItem | CarItem` 👥 🔜 🤚 ❌, ↩️ 🐍 🔜 🔄 🎭 **❌ 🛠️** 🖖 `PlaneItem` &amp; `CarItem` ↩️ 🔬 👈 🆎 ✍.

## 📇 🏷

🎏 🌌, 👆 💪 📣 📨 📇 🎚.

👈, ⚙️ 🐩 🐍 `typing.List` (⚖️ `list` 🐍 3️⃣.9️⃣ &amp; 🔛):

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="1  20"
    {!> ../../../docs_src/extra_models/tutorial004.py!}
    ```

=== "🐍 3️⃣.9️⃣ &amp; 🔛"

    ```Python hl_lines="18"
    {!> ../../../docs_src/extra_models/tutorial004_py39.py!}
    ```

## 📨 ⏮️ ❌ `dict`

👆 💪 📣 📨 ⚙️ ✅ ❌ `dict`, 📣 🆎 🔑 &amp; 💲, 🍵 ⚙️ Pydantic 🏷.

👉 ⚠ 🚥 👆 🚫 💭 ☑ 🏑/🔢 📛 (👈 🔜 💪 Pydantic 🏷) ⏪.

👉 💼, 👆 💪 ⚙️ `typing.Dict` (⚖️ `dict` 🐍 3️⃣.9️⃣ &amp; 🔛):

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="1  8"
    {!> ../../../docs_src/extra_models/tutorial005.py!}
    ```

=== "🐍 3️⃣.9️⃣ &amp; 🔛"

    ```Python hl_lines="6"
    {!> ../../../docs_src/extra_models/tutorial005_py39.py!}
    ```

## 🌃

⚙️ 💗 Pydantic 🏷 &amp; 😖 ➡ 🔠 💼.

👆 🚫 💪 ✔️ 👁 💽 🏷 📍 👨‍💼 🚥 👈 👨‍💼 🔜 💪 ✔️ 🎏 "🇵🇸". 💼 ⏮️ 👩‍💻 "👨‍💼" ⏮️ 🇵🇸 ✅ `password`, `password_hash` &amp; 🙅‍♂ 🔐.
