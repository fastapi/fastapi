# ➡ 🔢 &amp; 🔢 🔬

🎏 🌌 👈 👆 💪 📣 🌅 🔬 &amp; 🗃 🔢 🔢 ⏮️ `Query`, 👆 💪 📣 🎏 🆎 🔬 &amp; 🗃 ➡ 🔢 ⏮️ `Path`.

## 🗄 ➡

🥇, 🗄 `Path` ⚪️➡️ `fastapi`:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="3"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial001.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="1"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial001_py310.py!}
    ```

## 📣 🗃

👆 💪 📣 🌐 🎏 🔢 `Query`.

🖼, 📣 `title` 🗃 💲 ➡ 🔢 `item_id` 👆 💪 🆎:

=== "🐍 3️⃣.6️⃣ &amp; 🔛"

    ```Python hl_lines="10"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial001.py!}
    ```

=== "🐍 3️⃣.1️⃣0️⃣ &amp; 🔛"

    ```Python hl_lines="8"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial001_py310.py!}
    ```

!!! note
    ➡ 🔢 🕧 ✔ ⚫️ ✔️ 🍕 ➡.

    , 👆 🔜 📣 ⚫️ ⏮️ `...` ™ ⚫️ ✔.

    👐, 🚥 👆 📣 ⚫️ ⏮️ `None` ⚖️ ⚒ 🔢 💲, ⚫️ 🔜 🚫 📉 🕳, ⚫️ 🔜 🕧 🚚.

## ✔ 🔢 👆 💪

➡️ 💬 👈 👆 💚 📣 🔢 🔢 `q` ✔ `str`.

&amp; 👆 🚫 💪 📣 🕳 🙆 👈 🔢, 👆 🚫 🤙 💪 ⚙️ `Query`.

✋️ 👆 💪 ⚙️ `Path` `item_id` ➡ 🔢.

🐍 🔜 😭 🚥 👆 🚮 💲 ⏮️ "🔢" ⏭ 💲 👈 🚫 ✔️ "🔢".

✋️ 👆 💪 🏤-✔ 👫, &amp; ✔️ 💲 🍵 🔢 (🔢 🔢 `q`) 🥇.

⚫️ 🚫 🤔 **FastAPI**. ⚫️ 🔜 🔍 🔢 👫 📛, 🆎 &amp; 🔢 📄 (`Query`, `Path`, ♒️), ⚫️ 🚫 💅 🔃 ✔.

, 👆 💪 📣 👆 🔢:

```Python hl_lines="7"
{!../../../docs_src/path_params_numeric_validations/tutorial002.py!}
```

## ✔ 🔢 👆 💪, 🎱

🚥 👆 💚 📣 `q` 🔢 🔢 🍵 `Query` 🚫 🙆 🔢 💲, &amp; ➡ 🔢 `item_id` ⚙️ `Path`, &amp; ✔️ 👫 🎏 ✔, 🐍 ✔️ 🐥 🎁 ❕ 👈.

🚶‍♀️ `*`, 🥇 🔢 🔢.

🐍 🏆 🚫 🕳 ⏮️ 👈 `*`, ✋️ ⚫️ 🔜 💭 👈 🌐 📄 🔢 🔜 🤙 🇨🇻 ❌ (🔑-💲 👫), 💭 <abbr title="From: K-ey W-ord Arg-uments"><code>kwargs</code></abbr>. 🚥 👫 🚫 ✔️ 🔢 💲.

```Python hl_lines="7"
{!../../../docs_src/path_params_numeric_validations/tutorial003.py!}
```

## 🔢 🔬: 👑 🌘 ⚖️ 🌓

⏮️ `Query` &amp; `Path` (&amp; 🎏 👆 🔜 👀 ⏪) 👆 💪 📣 🔢 ⚛.

📥, ⏮️ `ge=1`, `item_id` 🔜 💪 🔢 🔢 "`g`🅾 🌘 ⚖️ `e`🅾" `1`.

```Python hl_lines="8"
{!../../../docs_src/path_params_numeric_validations/tutorial004.py!}
```

## 🔢 🔬: 🌘 🌘 &amp; 🌘 🌘 ⚖️ 🌓

🎏 ✔:

* `gt`: `g`🅾 `t`👲
* `le`: `l`👭 🌘 ⚖️ `e`🅾

```Python hl_lines="9"
{!../../../docs_src/path_params_numeric_validations/tutorial005.py!}
```

## 🔢 🔬: 🎈, 🌘 🌘 &amp; 🌘 🌘

🔢 🔬 👷 `float` 💲.

📥 🌐❔ ⚫️ ▶️️ ⚠ 💪 📣 <abbr title="greater than"><code>gt</code></abbr> &amp; 🚫 <abbr title="greater than or equal"><code>ge</code></abbr>. ⏮️ ⚫️ 👆 💪 🚚, 🖼, 👈 💲 🔜 👑 🌘 `0`, 🚥 ⚫️ 🌘 🌘 `1`.

, `0.5` 🔜 ☑ 💲. ✋️ `0.0` ⚖️ `0` 🔜 🚫.

&amp; 🎏 <abbr title="less than"><code>lt</code></abbr>.

```Python hl_lines="11"
{!../../../docs_src/path_params_numeric_validations/tutorial006.py!}
```

## 🌃

⏮️ `Query`, `Path` (&amp; 🎏 👆 🚫 👀) 👆 💪 📣 🗃 &amp; 🎻 🔬 🎏 🌌 ⏮️ [🔢 🔢 &amp; 🎻 🔬](query-params-str-validations.md){.internal-link target=_blank}.

&amp; 👆 💪 📣 🔢 🔬:

* `gt`: `g`🅾 `t`👲
* `ge`: `g`🅾 🌘 ⚖️ `e`🅾
* `lt`: `l`👭 `t`👲
* `le`: `l`👭 🌘 ⚖️ `e`🅾

!!! info
    `Query`, `Path`, &amp; 🎏 🎓 👆 🔜 👀 ⏪ 🏿 ⚠ `Param` 🎓.

    🌐 👫 💰 🎏 🔢 🌖 🔬 &amp; 🗃 👆 ✔️ 👀.

!!! note "📡 ℹ"
    🕐❔ 👆 🗄 `Query`, `Path` &amp; 🎏 ⚪️➡️ `fastapi`, 👫 🤙 🔢.

    👈 🕐❔ 🤙, 📨 👐 🎓 🎏 📛.

    , 👆 🗄 `Query`, ❔ 🔢. &amp; 🕐❔ 👆 🤙 ⚫️, ⚫️ 📨 👐 🎓 🌟 `Query`.

    👫 🔢 📤 (↩️ ⚙️ 🎓 🔗) 👈 👆 👨‍🎨 🚫 ™ ❌ 🔃 👫 🆎.

    👈 🌌 👆 💪 ⚙️ 👆 😐 👨‍🎨 &amp; 🛠️ 🧰 🍵 ✔️ 🚮 🛃 📳 🤷‍♂ 📚 ❌.
