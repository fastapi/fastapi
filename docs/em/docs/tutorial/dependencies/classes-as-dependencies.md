# 🎓 🔗

⏭ 🤿 ⏬ 🔘 **🔗 💉** ⚙️, ➡️ ♻ ⏮️ 🖼.

##  `dict` ⚪️➡️ ⏮️ 🖼

⏮️ 🖼, 👥 🛬 `dict` ⚪️➡️ 👆 🔗 ("☑"):

{* ../../docs_src/dependencies/tutorial001.py hl[9] *}

✋️ ⤴️ 👥 🤚 `dict` 🔢 `commons` *➡ 🛠️ 🔢*.

&amp; 👥 💭 👈 👨‍🎨 💪 🚫 🚚 📚 🐕‍🦺 (💖 🛠️) `dict`Ⓜ, ↩️ 👫 💪 🚫 💭 👫 🔑 &amp; 💲 🆎.

👥 💪 👍...

## ⚫️❔ ⚒ 🔗

🆙 🔜 👆 ✔️ 👀 🔗 📣 🔢.

✋️ 👈 🚫 🕴 🌌 📣 🔗 (👐 ⚫️ 🔜 🎲 🌖 ⚠).

🔑 ⚖ 👈 🔗 🔜 "🇧🇲".

"**🇧🇲**" 🐍 🕳 👈 🐍 💪 "🤙" 💖 🔢.

, 🚥 👆 ✔️ 🎚 `something` (👈 💪 _🚫_ 🔢) &amp; 👆 💪 "🤙" ⚫️ (🛠️ ⚫️) 💖:

```Python
something()
```

⚖️

```Python
something(some_argument, some_keyword_argument="foo")
```

⤴️ ⚫️ "🇧🇲".

## 🎓 🔗

👆 5️⃣📆 👀 👈 ✍ 👐 🐍 🎓, 👆 ⚙️ 👈 🎏 ❕.

🖼:

```Python
class Cat:
    def __init__(self, name: str):
        self.name = name


fluffy = Cat(name="Mr Fluffy")
```

👉 💼, `fluffy` 👐 🎓 `Cat`.

&amp; ✍ `fluffy`, 👆 "🤙" `Cat`.

, 🐍 🎓 **🇧🇲**.

⤴️, **FastAPI**, 👆 💪 ⚙️ 🐍 🎓 🔗.

⚫️❔ FastAPI 🤙 ✅ 👈 ⚫️ "🇧🇲" (🔢, 🎓 ⚖️ 🕳 🙆) &amp; 🔢 🔬.

🚥 👆 🚶‍♀️ "🇧🇲" 🔗 **FastAPI**, ⚫️ 🔜 🔬 🔢 👈 "🇧🇲", &amp; 🛠️ 👫 🎏 🌌 🔢 *➡ 🛠️ 🔢*. ✅ 🎧-🔗.

👈 ✔ 🇧🇲 ⏮️ 🙅‍♂ 🔢 🌐. 🎏 ⚫️ 🔜 *➡ 🛠️ 🔢* ⏮️ 🙅‍♂ 🔢.

⤴️, 👥 💪 🔀 🔗 "☑" `common_parameters` ⚪️➡️ 🔛 🎓 `CommonQueryParams`:

{* ../../docs_src/dependencies/tutorial002.py hl[11:15] *}

💸 🙋 `__init__` 👩‍🔬 ⚙️ ✍ 👐 🎓:

{* ../../docs_src/dependencies/tutorial002.py hl[12] *}

...⚫️ ✔️ 🎏 🔢 👆 ⏮️ `common_parameters`:

{* ../../docs_src/dependencies/tutorial001.py hl[9] *}

📚 🔢 ⚫️❔ **FastAPI** 🔜 ⚙️ "❎" 🔗.

👯‍♂️ 💼, ⚫️ 🔜 ✔️:

* 📦 `q` 🔢 🔢 👈 `str`.
*  `skip` 🔢 🔢 👈 `int`, ⏮️ 🔢 `0`.
*  `limit` 🔢 🔢 👈 `int`, ⏮️ 🔢 `100`.

👯‍♂️ 💼 💽 🔜 🗜, ✔, 📄 🔛 🗄 🔗, ♒️.

## ⚙️ ⚫️

🔜 👆 💪 📣 👆 🔗 ⚙️ 👉 🎓.

{* ../../docs_src/dependencies/tutorial002.py hl[19] *}

**FastAPI** 🤙 `CommonQueryParams` 🎓. 👉 ✍ "👐" 👈 🎓 &amp; 👐 🔜 🚶‍♀️ 🔢 `commons` 👆 🔢.

## 🆎 ✍ 🆚 `Depends`

👀 ❔ 👥 ✍ `CommonQueryParams` 🕐 🔛 📟:

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

🏁 `CommonQueryParams`,:

```Python
... = Depends(CommonQueryParams)
```

...⚫️❔ **FastAPI** 🔜 🤙 ⚙️ 💭 ⚫️❔ 🔗.

⚪️➡️ ⚫️ 👈 FastAPI 🔜 ⚗ 📣 🔢 &amp; 👈 ⚫️❔ FastAPI 🔜 🤙 🤙.

---

👉 💼, 🥇 `CommonQueryParams`,:

```Python
commons: CommonQueryParams ...
```

...🚫 ✔️ 🙆 🎁 🔑 **FastAPI**. FastAPI 🏆 🚫 ⚙️ ⚫️ 💽 🛠️, 🔬, ♒️. (⚫️ ⚙️ `= Depends(CommonQueryParams)` 👈).

👆 💪 🤙 ✍:

```Python
commons = Depends(CommonQueryParams)
```

...:

{* ../../docs_src/dependencies/tutorial003.py hl[19] *}

✋️ 📣 🆎 💡 👈 🌌 👆 👨‍🎨 🔜 💭 ⚫️❔ 🔜 🚶‍♀️ 🔢 `commons`, &amp; ⤴️ ⚫️ 💪 ℹ 👆 ⏮️ 📟 🛠️, 🆎 ✅, ♒️:

<img src="/img/tutorial/dependencies/image02.png">

## ⌨

✋️ 👆 👀 👈 👥 ✔️ 📟 🔁 📥, ✍ `CommonQueryParams` 🕐:

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

**FastAPI** 🚚 ⌨ 👫 💼, 🌐❔ 🔗 *🎯* 🎓 👈 **FastAPI** 🔜 "🤙" ✍ 👐 🎓 ⚫️.

📚 🎯 💼, 👆 💪 📄:

↩️ ✍:

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

...👆 ✍:

```Python
commons: CommonQueryParams = Depends()
```

👆 📣 🔗 🆎 🔢, &amp; 👆 ⚙️ `Depends()` 🚮 "🔢" 💲 (👈 ⏮️ `=`) 👈 🔢 🔢, 🍵 🙆 🔢 `Depends()`, ↩️ ✔️ ✍ 🌕 🎓 *🔄* 🔘 `Depends(CommonQueryParams)`.

🎏 🖼 🔜 ⤴️ 👀 💖:

{* ../../docs_src/dependencies/tutorial004.py hl[19] *}

...&amp; **FastAPI** 🔜 💭 ⚫️❔.

/// tip

🚥 👈 😑 🌅 😨 🌘 👍, 🤷‍♂ ⚫️, 👆 🚫 *💪* ⚫️.

⚫️ ⌨. ↩️ **FastAPI** 💅 🔃 🤝 👆 📉 📟 🔁.

///
