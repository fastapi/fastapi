# 🎧-🔗

👆 💪 ✍ 🔗 👈 ✔️ **🎧-🔗**.

👫 💪 **⏬** 👆 💪 👫.

**FastAPI** 🔜 ✊ 💅 🔬 👫.

## 🥇 🔗 "☑"

👆 💪 ✍ 🥇 🔗 ("☑") 💖:

{* ../../docs_src/dependencies/tutorial005.py hl[8:9] *}

⚫️ 📣 📦 🔢 🔢 `q` `str`, &amp; ⤴️ ⚫️ 📨 ⚫️.

👉 🙅 (🚫 📶 ⚠), ✋️ 🔜 ℹ 👥 🎯 🔛 ❔ 🎧-🔗 👷.

## 🥈 🔗, "☑" &amp; "⚓️"

⤴️ 👆 💪 ✍ ➕1️⃣ 🔗 🔢 ("☑") 👈 🎏 🕰 📣 🔗 🚮 👍 (⚫️ "⚓️" 💁‍♂️):

{* ../../docs_src/dependencies/tutorial005.py hl[13] *}

➡️ 🎯 🔛 🔢 📣:

* ✋️ 👉 🔢 🔗 ("☑") ⚫️, ⚫️ 📣 ➕1️⃣ 🔗 (⚫️ "🪀" 🔛 🕳 🙆).
    * ⚫️ 🪀 🔛 `query_extractor`, &amp; 🛠️ 💲 📨 ⚫️ 🔢 `q`.
* ⚫️ 📣 📦 `last_query` 🍪, `str`.
    * 🚥 👩‍💻 🚫 🚚 🙆 🔢 `q`, 👥 ⚙️ 🏁 🔢 ⚙️, ❔ 👥 🖊 🍪 ⏭.

## ⚙️ 🔗

⤴️ 👥 💪 ⚙️ 🔗 ⏮️:

{* ../../docs_src/dependencies/tutorial005.py hl[22] *}

/// info

👀 👈 👥 🕴 📣 1️⃣ 🔗 *➡ 🛠️ 🔢*, `query_or_cookie_extractor`.

✋️ **FastAPI** 🔜 💭 👈 ⚫️ ✔️ ❎ `query_extractor` 🥇, 🚶‍♀️ 🏁 👈 `query_or_cookie_extractor` ⏪ 🤙 ⚫️.

///

```mermaid
graph TB

query_extractor(["query_extractor"])
query_or_cookie_extractor(["query_or_cookie_extractor"])

read_query["/items/"]

query_extractor --> query_or_cookie_extractor --> read_query
```

## ⚙️ 🎏 🔗 💗 🕰

🚥 1️⃣ 👆 🔗 📣 💗 🕰 🎏 *➡ 🛠️*, 🖼, 💗 🔗 ✔️ ⚠ 🎧-🔗, **FastAPI** 🔜 💭 🤙 👈 🎧-🔗 🕴 🕐 📍 📨.

&amp; ⚫️ 🔜 🖊 📨 💲 <abbr title="A utility/system to store computed/generated values, to re-use them instead of computing them again.">"💾"</abbr> &amp; 🚶‍♀️ ⚫️ 🌐 "⚓️" 👈 💪 ⚫️ 👈 🎯 📨, ↩️ 🤙 🔗 💗 🕰 🎏 📨.

🏧 😐 🌐❔ 👆 💭 👆 💪 🔗 🤙 🔠 🔁 (🎲 💗 🕰) 🎏 📨 ↩️ ⚙️ "💾" 💲, 👆 💪 ⚒ 🔢 `use_cache=False` 🕐❔ ⚙️ `Depends`:

```Python hl_lines="1"
async def needy_dependency(fresh_value: str = Depends(get_value, use_cache=False)):
    return {"fresh_value": fresh_value}
```

## 🌃

↖️ ⚪️➡️ 🌐 🎀 🔤 ⚙️ 📥, **🔗 💉** ⚙️ 🙅.

🔢 👈 👀 🎏 *➡ 🛠️ 🔢*.

✋️, ⚫️ 📶 🏋️, &amp; ✔ 👆 📣 🎲 🙇 🐦 🔗 "📊" (🌲).

/// tip

🌐 👉 💪 🚫 😑 ⚠ ⏮️ 👫 🙅 🖼.

✋️ 👆 🔜 👀 ❔ ⚠ ⚫️ 📃 🔃 **💂‍♂**.

 &amp; 👆 🔜 👀 💸 📟 ⚫️ 🔜 🖊 👆.

///
