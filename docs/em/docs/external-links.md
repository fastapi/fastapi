# 🔢 🔗 &amp; 📄

**FastAPI** ✔️ 👑 👪 🕧 💗.

📤 📚 🏤, 📄, 🧰, &amp; 🏗, 🔗 **FastAPI**.

📥 ❌ 📇 👫.

!!! tip
    🚥 👆 ✔️ 📄, 🏗, 🧰, ⚖️ 🕳 🔗 **FastAPI** 👈 🚫 📇 📥, ✍ <a href="https://github.com/tiangolo/fastapi/edit/master/docs/en/data/external_links.yml" class="external-link" target="_blank">🚲 📨 ❎ ⚫️</a>.

## 📄

### 🇪🇸

{% if external_links %}
{% for article in external_links.articles.english %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

### 🇯🇵

{% if external_links %}
{% for article in external_links.articles.japanese %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

### 🇻🇳

{% if external_links %}
{% for article in external_links.articles.vietnamese %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

### 🇷🇺

{% if external_links %}
{% for article in external_links.articles.russian %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

### 🇩🇪

{% if external_links %}
{% for article in external_links.articles.german %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

### 🇹🇼

{% if external_links %}
{% for article in external_links.articles.taiwanese %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

## 📻

{% if external_links %}
{% for article in external_links.podcasts.english %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

## 💬

{% if external_links %}
{% for article in external_links.talks.english %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

## 🏗

⏪ 📂 🏗 ⏮️ ❔ `fastapi`:

<div class="github-topic-projects">
</div>
