# 🔢 🔢 &amp; 🎻 🔬

**FastAPI** ✔ 👆 📣 🌖 ℹ &amp; 🔬 👆 🔢.

➡️ ✊ 👉 🈸 🖼:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial001.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial001_py310.py!}
    ```

🔢 🔢 `q` 🆎 `Union[str, None]` (⚖️ `str | None` 🐍 3️⃣.1️⃣0️⃣), 👈 ⛓ 👈 ⚫️ 🆎 `str` ✋️ 💪 `None`, &amp; 👐, 🔢 💲 `None`, FastAPI 🔜 💭 ⚫️ 🚫 ✔.

!!! note
    FastAPI 🔜 💭 👈 💲 `q` 🚫 ✔ ↩️ 🔢 💲 `= None`.

     `Union` `Union[str, None]` 🔜 ✔ 👆 👨‍🎨 🤝 👆 👍 🐕‍🦺 &amp; 🔍 ❌.

## 🌖 🔬

👥 🔜 🛠️ 👈 ✋️ `q` 📦, 🕐❔ ⚫️ 🚚, **🚮 📐 🚫 📉 5️⃣0️⃣ 🦹**.

### 🗄 `Query`

🏆 👈, 🥇 🗄 `Query` ⚪️➡️ `fastapi`:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="3"
    {!> ../../../docs_src/query_params_str_validations/tutorial002.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="1"
    {!> ../../../docs_src/query_params_str_validations/tutorial002_py310.py!}
    ```

## ⚙️ `Query` 🔢 💲

&amp; 🔜 ⚙️ ⚫️ 🔢 💲 👆 🔢, ⚒ 🔢 `max_length` 5️⃣0️⃣:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial002.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial002_py310.py!}
    ```

👥 ✔️ ❎ 🔢 💲 `None` 🔢 ⏮️ `Query()`, 👥 💪 🔜 ⚒ 🔢 💲 ⏮️ 🔢 `Query(default=None)`, ⚫️ 🍦 🎏 🎯 ⚖ 👈 🔢 💲.

:

```Python
q: Union[str, None] = Query(default=None)
```

...⚒ 🔢 📦, 🎏:

```Python
q: Union[str, None] = None
```

&amp; 🐍 3️⃣.1️⃣0️⃣ &amp; 🔛:

```Python
q: str | None = Query(default=None)
```

...⚒ 🔢 📦, 🎏:

```Python
q: str | None = None
```

✋️ ⚫️ 📣 ⚫️ 🎯 💆‍♂ 🔢 🔢.

!!! info
    ✔️ 🤯 👈 🌅 ⚠ 🍕 ⚒ 🔢 📦 🍕:

    ```Python
    = None
    ```

    ⚖️:

    ```Python
    = Query(default=None)
    ```

    ⚫️ 🔜 ⚙️ 👈 `None` 🔢 💲, &amp; 👈 🌌 ⚒ 🔢 **🚫 ✔**.

     `Union[str, None]` 🍕 ✔ 👆 👨‍🎨 🚚 👻 🐕‍🦺, ✋️ ⚫️ 🚫 ⚫️❔ 💬 FastAPI 👈 👉 🔢 🚫 ✔.

⤴️, 👥 💪 🚶‍♀️ 🌅 🔢 `Query`. 👉 💼, `max_length` 🔢 👈 ✔ 🎻:

```Python
q: Union[str, None] = Query(default=None, max_length=50)
```

👉 🔜 ✔ 📊, 🎦 🆑 ❌ 🕐❔ 📊 🚫 ☑, &amp; 📄 🔢 🗄 🔗 *➡ 🛠️*.

## 🚮 🌅 🔬

👆 💪 🚮 🔢 `min_length`:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial003.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial003_py310.py!}
    ```

## 🚮 🥔 🧬

👆 💪 🔬 <abbr title="A regular expression, regex or regexp is a sequence of characters that define a search pattern for strings.">🥔 🧬</abbr> 👈 🔢 🔜 🏏:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial004.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial004_py310.py!}
    ```

👉 🎯 🥔 🧬 ✅ 👈 📨 🔢 💲:

* `^`: ▶️ ⏮️ 📄 🦹, 🚫 ✔️ 🦹 ⏭.
* `fixedquery`: ✔️ ☑ 💲 `fixedquery`.
* `$`: 🔚 📤, 🚫 ✔️ 🙆 🌖 🦹 ⏮️ `fixedquery`.

🚥 👆 💭 💸 ⏮️ 🌐 👉 **"🥔 🧬"** 💭, 🚫 😟. 👫 🏋️ ❔ 📚 👫👫. 👆 💪 📚 💩 🍵 💆‍♂ 🥔 🧬.

✋️ 🕐❔ 👆 💪 👫 &amp; 🚶 &amp; 💡 👫, 💭 👈 👆 💪 ⏪ ⚙️ 👫 🔗 **FastAPI**.

## 🔢 💲

🎏 🌌 👈 👆 💪 🚶‍♀️ `None` 💲 `default` 🔢, 👆 💪 🚶‍♀️ 🎏 💲.

➡️ 💬 👈 👆 💚 📣 `q` 🔢 🔢 ✔️ `min_length` `3`, &amp; ✔️ 🔢 💲 `"fixedquery"`:

```Python hl_lines="7"
{!../../../docs_src/query_params_str_validations/tutorial005.py!}
```

!!! note
    ✔️ 🔢 💲 ⚒ 🔢 📦.

## ⚒ ⚫️ ✔

🕐❔ 👥 🚫 💪 📣 🌅 🔬 ⚖️ 🗃, 👥 💪 ⚒ `q` 🔢 🔢 ✔ 🚫 📣 🔢 💲, 💖:

```Python
q: str
```

↩️:

```Python
q: Union[str, None] = None
```

✋️ 👥 🔜 📣 ⚫️ ⏮️ `Query`, 🖼 💖:

```Python
q: Union[str, None] = Query(default=None, min_length=3)
```

, 🕐❔ 👆 💪 📣 💲 ✔ ⏪ ⚙️ `Query`, 👆 💪 🎯 🚫 📣 🔢 💲:

```Python hl_lines="7"
{!../../../docs_src/query_params_str_validations/tutorial006.py!}
```

### ✔ ⏮️ ❕ (`...`)

📤 🎛 🌌 🎯 📣 👈 💲 ✔. 👆 💪 ⚒ `default` 🔢 🔑 💲 `...`:

```Python hl_lines="7"
{!../../../docs_src/query_params_str_validations/tutorial006b.py!}
```

!!! info
    🚥 👆 🚫 👀 👈 `...` ⏭: ⚫️ 🎁 👁 💲, ⚫️ <a href="https://docs.python.org/3/library/constants.html#Ellipsis" class="external-link" target="_blank">🍕 🐍 &amp; 🤙 "❕"</a>.

    ⚫️ ⚙️ Pydantic &amp; FastAPI 🎯 📣 👈 💲 ✔.

👉 🔜 ➡️ **FastAPI** 💭 👈 👉 🔢 ✔.

### ✔ ⏮️ `None`

👆 💪 📣 👈 🔢 💪 🚫 `None`, ✋️ 👈 ⚫️ ✔. 👉 🔜 ⚡ 👩‍💻 📨 💲, 🚥 💲 `None`.

👈, 👆 💪 📣 👈 `None` ☑ 🆎 ✋️ ⚙️ `default=...`:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial006c.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial006c_py310.py!}
    ```

!!! tip
    Pydantic, ❔ ⚫️❔ 🏋️ 🌐 💽 🔬 &amp; 🛠️ FastAPI, ✔️ 🎁 🎭 🕐❔ 👆 ⚙️ `Optional` ⚖️ `Union[Something, None]` 🍵 🔢 💲, 👆 💪 ✍ 🌅 🔃 ⚫️ Pydantic 🩺 🔃 <a href="https://pydantic-docs.helpmanual.io/usage/models/#required-optional-fields" class="external-link" target="_blank">✔ 📦 🏑</a>.

### ⚙️ Pydantic `Required` ↩️ ❕ (`...`)

🚥 👆 💭 😬 ⚙️ `...`, 👆 💪 🗄 &amp; ⚙️ `Required` ⚪️➡️ Pydantic:

```Python hl_lines="2  8"
{!../../../docs_src/query_params_str_validations/tutorial006d.py!}
```

!!! tip
    💭 👈 🌅 💼, 🕐❔ 🕳 🚚, 👆 💪 🎯 🚫 `default` 🔢, 👆 🛎 🚫 ✔️ ⚙️ `...` 🚫 `Required`.

## 🔢 🔢 📇 / 💗 💲

🕐❔ 👆 🔬 🔢 🔢 🎯 ⏮️ `Query` 👆 💪 📣 ⚫️ 📨 📇 💲, ⚖️ 🙆‍♀ 🎏 🌌, 📨 💗 💲.

🖼, 📣 🔢 🔢 `q` 👈 💪 😑 💗 🕰 📛, 👆 💪 ✍:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial011.py!}
    ```

=== "🐍 3️⃣.9️⃣ &amp; 🔛"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial011_py39.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial011_py310.py!}
    ```

⤴️, ⏮️ 📛 💖:

```
http://localhost:8000/items/?q=foo&q=bar
```

👆 🔜 📨 💗 `q` *🔢 🔢'* 💲 (`foo` &amp; `bar`) 🐍 `list` 🔘 👆 *➡ 🛠️ 🔢*, *🔢 🔢* `q`.

, 📨 👈 📛 🔜:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

!!! tip
    📣 🔢 🔢 ⏮️ 🆎 `list`, 💖 🖼 🔛, 👆 💪 🎯 ⚙️ `Query`, ⏪ ⚫️ 🔜 🔬 📨 💪.

🎓 🛠️ 🩺 🔜 ℹ ➡️, ✔ 💗 💲:

<img src="/img/tutorial/query-params-str-validations/image02.png">

### 🔢 🔢 📇 / 💗 💲 ⏮️ 🔢

&amp; 👆 💪 🔬 🔢 `list` 💲 🚥 👌 🚚:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial012.py!}
    ```

=== "🐍 3️⃣.9️⃣ &amp; 🔛"

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial012_py39.py!}
    ```

🚥 👆 🚶:

```
http://localhost:8000/items/
```

🔢 `q` 🔜: `["foo", "bar"]` &amp; 👆 📨 🔜:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

#### ⚙️ `list`

👆 💪 ⚙️ `list` 🔗 ↩️ `List[str]` (⚖️ `list[str]` 🐍 3️⃣.9️⃣ ➕):

```Python hl_lines="7"
{!../../../docs_src/query_params_str_validations/tutorial013.py!}
```

!!! note
    ✔️ 🤯 👈 👉 💼, FastAPI 🏆 🚫 ✅ 🎚 📇.

    🖼, `List[int]` 🔜 ✅ (&amp; 📄) 👈 🎚 📇 🔢. ✋️ `list` 😞 🚫🔜.

## 📣 🌅 🗃

👆 💪 🚮 🌅 ℹ 🔃 🔢.

👈 ℹ 🔜 🔌 🏗 🗄 &amp; ⚙️ 🧾 👩‍💻 🔢 &amp; 🔢 🧰.

!!! note
    ✔️ 🤯 👈 🎏 🧰 5️⃣📆 ✔️ 🎏 🎚 🗄 🐕‍🦺.

    👫 💪 🚫 🎦 🌐 ➕ ℹ 📣, 👐 🌅 💼, ❌ ⚒ ⏪ 📄 🛠️.

👆 💪 🚮 `title`:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial007.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params_str_validations/tutorial007_py310.py!}
    ```

&amp; `description`:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="13"
    {!> ../../../docs_src/query_params_str_validations/tutorial008.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="12"
    {!> ../../../docs_src/query_params_str_validations/tutorial008_py310.py!}
    ```

## 📛 🔢

🌈 👈 👆 💚 🔢 `item-query`.

💖:

```
http://127.0.0.1:8000/items/?item-query=foobaritems
```

✋️ `item-query` 🚫 ☑ 🐍 🔢 📛.

🔐 🔜 `item_query`.

✋️ 👆 💪 ⚫️ ⚫️❔ `item-query`...

⤴️ 👆 💪 📣 `alias`, &amp; 👈 📛 ⚫️❔ 🔜 ⚙️ 🔎 🔢 💲:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial009.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial009_py310.py!}
    ```

## 😛 🔢

🔜 ➡️ 💬 👆 🚫 💖 👉 🔢 🚫🔜.

👆 ✔️ 👈 ⚫️ 📤 ⏪ ↩️ 📤 👩‍💻 ⚙️ ⚫️, ✋️ 👆 💚 🩺 🎯 🎦 ⚫️ <abbr title="obsolete, recommended not to use it">😢</abbr>.

⤴️ 🚶‍♀️ 🔢 `deprecated=True` `Query`:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="18"
    {!> ../../../docs_src/query_params_str_validations/tutorial010.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="17"
    {!> ../../../docs_src/query_params_str_validations/tutorial010_py310.py!}
    ```

🩺 🔜 🎦 ⚫️ 💖 👉:

<img src="/img/tutorial/query-params-str-validations/image01.png">

## 🚫 ⚪️➡️ 🗄

🚫 🔢 🔢 ⚪️➡️ 🏗 🗄 🔗 (&amp; ➡️, ⚪️➡️ 🏧 🧾 ⚙️), ⚒ 🔢 `include_in_schema` `Query` `False`:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial014.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params_str_validations/tutorial014_py310.py!}
    ```

## 🌃

👆 💪 📣 🌖 🔬 &amp; 🗃 👆 🔢.

💊 🔬 &amp; 🗃:

* `alias`
* `title`
* `description`
* `deprecated`

🔬 🎯 🎻:

* `min_length`
* `max_length`
* `regex`

👫 🖼 👆 👀 ❔ 📣 🔬 `str` 💲.

👀 ⏭ 📃 👀 ❔ 📣 🔬 🎏 🆎, 💖 🔢.
