# ➡ 🔢 &amp; 🔢 🔬

🎏 🌌 👈 👆 💪 📣 🌅 🔬 &amp; 🗃 🔢 🔢 ⏮️ `Query`, 👆 💪 📣 🎏 🆎 🔬 &amp; 🗃 ➡ 🔢 ⏮️ `Path`.

## 🗄 ➡

🥇, 🗄 `Path` ⚪️➡️ `fastapi`:

{* ../../docs_src/path_params_numeric_validations/tutorial001.py hl[3] *}

## 📣 🗃

👆 💪 📣 🌐 🎏 🔢 `Query`.

🖼, 📣 `title` 🗃 💲 ➡ 🔢 `item_id` 👆 💪 🆎:

{* ../../docs_src/path_params_numeric_validations/tutorial001.py hl[10] *}

/// note

➡ 🔢 🕧 ✔ ⚫️ ✔️ 🍕 ➡.

, 👆 🔜 📣 ⚫️ ⏮️ `...` ™ ⚫️ ✔.

👐, 🚥 👆 📣 ⚫️ ⏮️ `None` ⚖️ ⚒ 🔢 💲, ⚫️ 🔜 🚫 📉 🕳, ⚫️ 🔜 🕧 🚚.

///

## ✔ 🔢 👆 💪

➡️ 💬 👈 👆 💚 📣 🔢 🔢 `q` ✔ `str`.

&amp; 👆 🚫 💪 📣 🕳 🙆 👈 🔢, 👆 🚫 🤙 💪 ⚙️ `Query`.

✋️ 👆 💪 ⚙️ `Path` `item_id` ➡ 🔢.

🐍 🔜 😭 🚥 👆 🚮 💲 ⏮️ "🔢" ⏭ 💲 👈 🚫 ✔️ "🔢".

✋️ 👆 💪 🏤-✔ 👫, &amp; ✔️ 💲 🍵 🔢 (🔢 🔢 `q`) 🥇.

⚫️ 🚫 🤔 **FastAPI**. ⚫️ 🔜 🔍 🔢 👫 📛, 🆎 &amp; 🔢 📄 (`Query`, `Path`, ♒️), ⚫️ 🚫 💅 🔃 ✔.

, 👆 💪 📣 👆 🔢:

{* ../../docs_src/path_params_numeric_validations/tutorial002.py hl[7] *}

## ✔ 🔢 👆 💪, 🎱

🚥 👆 💚 📣 `q` 🔢 🔢 🍵 `Query` 🚫 🙆 🔢 💲, &amp; ➡ 🔢 `item_id` ⚙️ `Path`, &amp; ✔️ 👫 🎏 ✔, 🐍 ✔️ 🐥 🎁 ❕ 👈.

🚶‍♀️ `*`, 🥇 🔢 🔢.

🐍 🏆 🚫 🕳 ⏮️ 👈 `*`, ✋️ ⚫️ 🔜 💭 👈 🌐 📄 🔢 🔜 🤙 🇨🇻 ❌ (🔑-💲 👫), 💭 <abbr title="From: K-ey W-ord Arg-uments"><code>kwargs</code></abbr>. 🚥 👫 🚫 ✔️ 🔢 💲.

{* ../../docs_src/path_params_numeric_validations/tutorial003.py hl[7] *}

## 🔢 🔬: 👑 🌘 ⚖️ 🌓

⏮️ `Query` &amp; `Path` (&amp; 🎏 👆 🔜 👀 ⏪) 👆 💪 📣 🔢 ⚛.

📥, ⏮️ `ge=1`, `item_id` 🔜 💪 🔢 🔢 "`g`🅾 🌘 ⚖️ `e`🅾" `1`.

{* ../../docs_src/path_params_numeric_validations/tutorial004.py hl[8] *}

## 🔢 🔬: 🌘 🌘 &amp; 🌘 🌘 ⚖️ 🌓

🎏 ✔:

* `gt`: `g`🅾 `t`👲
* `le`: `l`👭 🌘 ⚖️ `e`🅾

{* ../../docs_src/path_params_numeric_validations/tutorial005.py hl[9] *}

## 🔢 🔬: 🎈, 🌘 🌘 &amp; 🌘 🌘

🔢 🔬 👷 `float` 💲.

📥 🌐❔ ⚫️ ▶️️ ⚠ 💪 📣 <abbr title="greater than"><code>gt</code></abbr> &amp; 🚫 <abbr title="greater than or equal"><code>ge</code></abbr>. ⏮️ ⚫️ 👆 💪 🚚, 🖼, 👈 💲 🔜 👑 🌘 `0`, 🚥 ⚫️ 🌘 🌘 `1`.

, `0.5` 🔜 ☑ 💲. ✋️ `0.0` ⚖️ `0` 🔜 🚫.

&amp; 🎏 <abbr title="less than"><code>lt</code></abbr>.

{* ../../docs_src/path_params_numeric_validations/tutorial006.py hl[11] *}

## 🌃

⏮️ `Query`, `Path` (&amp; 🎏 👆 🚫 👀) 👆 💪 📣 🗃 &amp; 🎻 🔬 🎏 🌌 ⏮️ [🔢 🔢 &amp; 🎻 🔬](query-params-str-validations.md){.internal-link target=_blank}.

&amp; 👆 💪 📣 🔢 🔬:

* `gt`: `g`🅾 `t`👲
* `ge`: `g`🅾 🌘 ⚖️ `e`🅾
* `lt`: `l`👭 `t`👲
* `le`: `l`👭 🌘 ⚖️ `e`🅾

/// info

`Query`, `Path`, &amp; 🎏 🎓 👆 🔜 👀 ⏪ 🏿 ⚠ `Param` 🎓.

🌐 👫 💰 🎏 🔢 🌖 🔬 &amp; 🗃 👆 ✔️ 👀.

///

/// note | 📡 ℹ

🕐❔ 👆 🗄 `Query`, `Path` &amp; 🎏 ⚪️➡️ `fastapi`, 👫 🤙 🔢.

👈 🕐❔ 🤙, 📨 👐 🎓 🎏 📛.

, 👆 🗄 `Query`, ❔ 🔢. &amp; 🕐❔ 👆 🤙 ⚫️, ⚫️ 📨 👐 🎓 🌟 `Query`.

👫 🔢 📤 (↩️ ⚙️ 🎓 🔗) 👈 👆 👨‍🎨 🚫 ™ ❌ 🔃 👫 🆎.

👈 🌌 👆 💪 ⚙️ 👆 😐 👨‍🎨 &amp; 🛠️ 🧰 🍵 ✔️ 🚮 🛃 📳 🤷‍♂ 📚 ❌.

///
