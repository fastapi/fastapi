# 🎧 🈸 - 🗻

🚥 👆 💪 ✔️ 2⃣ 🔬 FastAPI 🈸, ⏮ 👫 👍 🔬 🗄 &amp; 👫 👍 🩺 ⚜, 👆 💪 ✔️ 👑 📱 &amp; "🗻" 1⃣ (⚖️ 🌅) 🎧-🈸(Ⓜ).

## 🗜 **FastAPI** 🈸

"🗜" ⛓ ❎ 🍕 "🔬" 🈸 🎯 ➡, 👈 ⤴ ✊ 💅 🚚 🌐 🔽 👈 ➡, ⏮ _➡ 🛠_ 📣 👈 🎧-🈸.

### 🔝-🎚 🈸

🥇, ✍ 👑, 🔝-🎚, **FastAPI** 🈸, &amp; 🚮 *➡ 🛠*:

```Python hl_lines="3  6-8"
{!../../../docs_src/sub_applications/tutorial001.py!}
```

### 🎧-🈸

⤴, ✍ 👆 🎧-🈸, &amp; 🚮 *➡ 🛠*.

👉 🎧-🈸 ➕1️⃣ 🐩 FastAPI 🈸, ✋️ 👉 1⃣ 👈 🔜 "🗻":

```Python hl_lines="11  14-16"
{!../../../docs_src/sub_applications/tutorial001.py!}
```

### 🗻 🎧-🈸

👆 🔝-🎚 🈸, `app`, 🗻 🎧-🈸, `subapi`.

👉 💼, ⚫️ 🔜 📌 ➡ `/subapi`:

```Python hl_lines="11  19"
{!../../../docs_src/sub_applications/tutorial001.py!}
```

### ✅ 🏧 🛠 🩺

🔜, 🏃 `uvicorn` ⏮ 👑 📱, 🚥 👆 📁 `main.py`, ⚫️ 🔜:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

&amp; 📂 🩺 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">Http://127.0.0.1:8000/docs</a>.

👆 🔜 👀 🏧 🛠 🩺 👑 📱, 🔌 🕴 🚮 👍 _➡ 🛠_:

<img src="/img/tutorial/sub-applications/image01.png">

&amp; ⤴, 📂 🩺 🎧-🈸, <a href="http://127.0.0.1:8000/subapi/docs" class="external-link" target="_blank">Http://127.0.0.1:8000/subapi/docs</a>.

👆 🔜 👀 🏧 🛠 🩺 🎧-🈸, ✅ 🕴 🚮 👍 _➡ 🛠_, 🌐 🔽 ☑ 🎧-➡ 🔡 `/subapi`:

<img src="/img/tutorial/sub-applications/image02.png">

🚥 👆 🔄 🔗 ⏮ 🙆 2⃣ 👩‍💻 🔢, 👫 🔜 👷 ☑, ↩️ 🖥 🔜 💪 💬 🔠 🎯 📱 ⚖️ 🎧-📱.

### 📡 ℹ: `root_path`

🕐❔ 👆 🗻 🎧-🈸 🔬 🔛, FastAPI 🔜 ✊ 💅 🔗 🗻 ➡ 🎧-🈸 ⚙️ 🛠 ⚪️➡️ 🔫 🔧 🤙 `root_path`.

👈 🌌, 🎧-🈸 🔜 💭 ⚙️ 👈 ➡ 🔡 🩺 🎚.

&amp; 🎧-🈸 💪 ✔️ 🚮 👍 📌 🎧-🈸 &amp; 🌐 🔜 👷 ☑, ↩️ FastAPI 🍵 🌐 👉 `root_path`Ⓜ 🔁.

👆 🔜 💡 🌅 🔃 `root_path` &amp; ❔ ⚙️ ⚫️ 🎯 📄 🔃 [⛅ 🗳](./behind-a-proxy.md){.internal-link target=_blank}.
