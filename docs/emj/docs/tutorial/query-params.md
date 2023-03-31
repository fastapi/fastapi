# 🔢 🔢

🕐❔ 👆 📣 🎏 🔢 🔢 👈 🚫 🍕 ➡ 🔢, 👫 🔁 🔬 "🔢" 🔢.

```Python hl_lines="9"
{!../../../docs_src/query_params/tutorial001.py!}
```

🔢 ⚒ 🔑-💲 👫 👈 🚶 ⏮️ `?` 📛, 🎏 `&` 🦹.

🖼, 📛:

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

...🔢 🔢:

* `skip`: ⏮️ 💲 `0`
* `limit`: ⏮️ 💲 `10`

👫 🍕 📛, 👫 "🛎" 🎻.

✋️ 🕐❔ 👆 📣 👫 ⏮️ 🐍 🆎 (🖼 🔛, `int`), 👫 🗜 👈 🆎 &amp; ✔ 🛡 ⚫️.

🌐 🎏 🛠️ 👈 ⚖ ➡ 🔢 ✔ 🔢 🔢:

* 👨‍🎨 🐕‍🦺 (🎲)
* 💽 <abbr title="converting the string that comes from an HTTP request into Python data">"✍"</abbr>
* 💽 🔬
* 🏧 🧾

## 🔢

🔢 🔢 🚫 🔧 🍕 ➡, 👫 💪 📦 &amp; 💪 ✔️ 🔢 💲.

🖼 🔛 👫 ✔️ 🔢 💲 `skip=0` &amp; `limit=10`.

, 🔜 📛:

```
http://127.0.0.1:8000/items/
```

🔜 🎏 🔜:

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

✋️ 🚥 👆 🚶, 🖼:

```
http://127.0.0.1:8000/items/?skip=20
```

🔢 💲 👆 🔢 🔜:

* `skip=20`: ↩️ 👆 ⚒ ⚫️ 📛
* `limit=10`: ↩️ 👈 🔢 💲

## 📦 🔢

🎏 🌌, 👆 💪 📣 📦 🔢 🔢, ⚒ 👫 🔢 `None`:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params/tutorial002.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params/tutorial002_py310.py!}
    ```

👉 💼, 🔢 🔢 `q` 🔜 📦, &amp; 🔜 `None` 🔢.

!!! check
    👀 👈 **FastAPI** 🙃 🥃 👀 👈 ➡ 🔢 `item_id` ➡ 🔢 &amp; `q` 🚫,, ⚫️ 🔢 🔢.

## 🔢 🔢 🆎 🛠️

👆 💪 📣 `bool` 🆎, &amp; 👫 🔜 🗜:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params/tutorial003.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params/tutorial003_py310.py!}
    ```

👉 💼, 🚥 👆 🚶:

```
http://127.0.0.1:8000/items/foo?short=1
```

⚖️

```
http://127.0.0.1:8000/items/foo?short=True
```

⚖️

```
http://127.0.0.1:8000/items/foo?short=true
```

⚖️

```
http://127.0.0.1:8000/items/foo?short=on
```

⚖️

```
http://127.0.0.1:8000/items/foo?short=yes
```

⚖️ 🙆 🎏 💼 📈 (🔠, 🥇 🔤 🔠, ♒️), 👆 🔢 🔜 👀 🔢 `short` ⏮️ `bool` 💲 `True`. ⏪ `False`.


## 💗 ➡ &amp; 🔢 🔢

👆 💪 📣 💗 ➡ 🔢 &amp; 🔢 🔢 🎏 🕰, **FastAPI** 💭 ❔ ❔.

&amp; 👆 🚫 ✔️ 📣 👫 🙆 🎯 ✔.

👫 🔜 🔬 📛:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="8  10"
    {!> ../../../docs_src/query_params/tutorial004.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="6  8"
    {!> ../../../docs_src/query_params/tutorial004_py310.py!}
    ```

## ✔ 🔢 🔢

🕐❔ 👆 📣 🔢 💲 🚫-➡ 🔢 (🔜, 👥 ✔️ 🕴 👀 🔢 🔢), ⤴️ ⚫️ 🚫 ✔.

🚥 👆 🚫 💚 🚮 🎯 💲 ✋️ ⚒ ⚫️ 📦, ⚒ 🔢 `None`.

✋️ 🕐❔ 👆 💚 ⚒ 🔢 🔢 ✔, 👆 💪 🚫 📣 🙆 🔢 💲:

```Python hl_lines="6-7"
{!../../../docs_src/query_params/tutorial005.py!}
```

📥 🔢 🔢 `needy` ✔ 🔢 🔢 🆎 `str`.

🚥 👆 📂 👆 🖥 📛 💖:

```
http://127.0.0.1:8000/items/foo-item
```

...🍵 ❎ ✔ 🔢 `needy`, 👆 🔜 👀 ❌ 💖:

```JSON
{
    "detail": [
        {
            "loc": [
                "query",
                "needy"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}
```

`needy` 🚚 🔢, 👆 🔜 💪 ⚒ ⚫️ 📛:

```
http://127.0.0.1:8000/items/foo-item?needy=sooooneedy
```

...👉 🔜 👷:

```JSON
{
    "item_id": "foo-item",
    "needy": "sooooneedy"
}
```

&amp; ↗️, 👆 💪 🔬 🔢 ✔, ✔️ 🔢 💲, &amp; 🍕 📦:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params/tutorial006.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params/tutorial006_py310.py!}
    ```

👉 💼, 📤 3️⃣ 🔢 🔢:

* `needy`, ✔ `str`.
* `skip`, `int` ⏮️ 🔢 💲 `0`.
* `limit`, 📦 `int`.

!!! tip
    👆 💪 ⚙️ `Enum`Ⓜ 🎏 🌌 ⏮️ [➡ 🔢](path-params.md#predefined-values){.internal-link target=_blank}.
