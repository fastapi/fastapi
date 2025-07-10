# ⚙️ 🎻

FastAPI 🏗 🔛 🔝 **Pydantic**, &amp; 👤 ✔️ 🌏 👆 ❔ ⚙️ Pydantic 🏷 📣 📨 &amp; 📨.

✋️ FastAPI 🐕‍🦺 ⚙️ <a href="https://docs.python.org/3/library/dataclasses.html" class="external-link" target="_blank">`dataclasses`</a> 🎏 🌌:

{* ../../docs_src/dataclasses/tutorial001.py hl[1,7:12,19:20] *}

👉 🐕‍🦺 👏 **Pydantic**, ⚫️ ✔️ <a href="https://docs.pydantic.dev/latest/concepts/dataclasses/#use-of-stdlib-dataclasses-with-basemodel" class="external-link" target="_blank">🔗 🐕‍🦺 `dataclasses`</a>.

, ⏮️ 📟 🔛 👈 🚫 ⚙️ Pydantic 🎯, FastAPI ⚙️ Pydantic 🗜 📚 🐩 🎻 Pydantic 👍 🍛 🎻.

&amp; ↗️, ⚫️ 🐕‍🦺 🎏:

* 💽 🔬
* 💽 🛠️
* 💽 🧾, ♒️.

👉 👷 🎏 🌌 ⏮️ Pydantic 🏷. &amp; ⚫️ 🤙 🏆 🎏 🌌 🔘, ⚙️ Pydantic.

/// info

✔️ 🤯 👈 🎻 💪 🚫 🌐 Pydantic 🏷 💪.

, 👆 5️⃣📆 💪 ⚙️ Pydantic 🏷.

✋️ 🚥 👆 ✔️ 📚 🎻 🤥 🤭, 👉 👌 🎱 ⚙️ 👫 🏋️ 🕸 🛠️ ⚙️ FastAPI. 👶

///

## 🎻 `response_model`

👆 💪 ⚙️ `dataclasses` `response_model` 🔢:

{* ../../docs_src/dataclasses/tutorial002.py hl[1,7:13,19] *}

🎻 🔜 🔁 🗜 Pydantic 🎻.

👉 🌌, 🚮 🔗 🔜 🎦 🆙 🛠️ 🩺 👩‍💻 🔢:

<img src="/img/tutorial/dataclasses/image01.png">

## 🎻 🔁 📊 📊

👆 💪 🌀 `dataclasses` ⏮️ 🎏 🆎 ✍ ⚒ 🐦 📊 📊.

💼, 👆 💪 ✔️ ⚙️ Pydantic ⏬ `dataclasses`. 🖼, 🚥 👆 ✔️ ❌ ⏮️ 🔁 🏗 🛠️ 🧾.

👈 💼, 👆 💪 🎯 💱 🐩 `dataclasses` ⏮️ `pydantic.dataclasses`, ❔ 💧-♻:

```{ .python .annotate hl_lines="1  5  8-11  14-17  23-25  28" }
{!../../docs_src/dataclasses/tutorial003.py!}
```

1️⃣. 👥 🗄 `field` ⚪️➡️ 🐩 `dataclasses`.

2️⃣. `pydantic.dataclasses` 💧-♻ `dataclasses`.

3️⃣. `Author` 🎻 🔌 📇 `Item` 🎻.

4️⃣. `Author` 🎻 ⚙️ `response_model` 🔢.

5️⃣. 👆 💪 ⚙️ 🎏 🐩 🆎 ✍ ⏮️ 🎻 📨 💪.

    👉 💼, ⚫️ 📇 `Item` 🎻.

6️⃣. 📥 👥 🛬 📖 👈 🔌 `items` ❔ 📇 🎻.

    FastAPI 🎯 <abbr title="converting the data to a format that can be transmitted">✍</abbr> 💽 🎻.

7️⃣. 📥 `response_model` ⚙️ 🆎 ✍ 📇 `Author` 🎻.

    🔄, 👆 💪 🌀 `dataclasses` ⏮️ 🐩 🆎 ✍.

8️⃣. 👀 👈 👉 *➡ 🛠️ 🔢* ⚙️ 🥔 `def` ↩️ `async def`.

    🕧, FastAPI 👆 💪 🌀 `def` &amp; `async def` 💪.

    🚥 👆 💪 ↗️ 🔃 🕐❔ ⚙️ ❔, ✅ 👅 📄 _"🏃 ❓" _ 🩺 🔃 <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank" class="internal-link">`async` &amp; `await`</a>.

9️⃣. 👉 *➡ 🛠️ 🔢* 🚫 🛬 🎻 (👐 ⚫️ 💪), ✋️ 📇 📖 ⏮️ 🔗 💽.

    FastAPI 🔜 ⚙️ `response_model` 🔢 (👈 🔌 🎻) 🗜 📨.

👆 💪 🌀 `dataclasses` ⏮️ 🎏 🆎 ✍ 📚 🎏 🌀 📨 🏗 📊 📊.

✅-📟 ✍ 💁‍♂ 🔛 👀 🌅 🎯 ℹ.

## 💡 🌅

👆 💪 🌀 `dataclasses` ⏮️ 🎏 Pydantic 🏷, 😖 ⚪️➡️ 👫, 🔌 👫 👆 👍 🏷, ♒️.

💡 🌅, ✅ <a href="https://docs.pydantic.dev/latest/concepts/dataclasses/" class="external-link" target="_blank">Pydantic 🩺 🔃 🎻</a>.

## ⏬

👉 💪 ↩️ FastAPI ⏬ `0.67.0`. 👶
