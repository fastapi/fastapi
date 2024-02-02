# 🔢 🔗 &amp; 📄

**FastAPI** ✔️ 👑 👪 🕧 💗.

📤 📚 🏤, 📄, 🧰, &amp; 🏗, 🔗 **FastAPI**.

📥 ❌ 📇 👫.

!!! tip
    🚥 👆 ✔️ 📄, 🏗, 🧰, ⚖️ 🕳 🔗 **FastAPI** 👈 🚫 📇 📥, ✍ <a href="https://github.com/tiangolo/fastapi/edit/master/docs/en/data/external_links.yml" class="external-link" target="_blank">🚲 📨 ❎ ⚫️</a>.

## 📄

{% for section_name, section_content in external_links.items() %}

## {{ section_name }}

{% for lang_name, lang_content in section_content.items() %}

### {{ lang_name }}

{% for item in lang_content %}

* <a href="{{ item.link }}" class="external-link" target="_blank">{{ item.title }}</a> by <a href="{{ item.author_link }}" class="external-link" target="_blank">{{ item.author }}</a>.

{% endfor %}
{% endfor %}
{% endfor %}

## 🏗

⏪ 📂 🏗 ⏮️ ❔ `fastapi`:

<div class="github-topic-projects">
</div>
