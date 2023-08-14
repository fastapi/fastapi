# Люди FastAPI

FastAPI має дивовижну спільноту, яка вітає людей різного походження.

## Творець – Супроводжувач

Привіт! 👋

Це я:

{% if people %}
<div class="user-list user-list-center">
{% for user in people.maintainers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Answers: {{ user.answers }}</div><div class="count">Pull Requests: {{ user.prs }}</div></div>
{% endfor %}

</div>
{% endif %}

Я - творець і супроводжувач **FastAPI**. Детальніше про це можна прочитати в [Довідка FastAPI - Отримати довідку - Зв'язатися з автором](help-fastapi.md#connect-with-the-author){.internal-link target=_blank}.

...Але тут я хочу показати вам спільноту.

---

**FastAPI** отримує велику підтримку від спільноти. І я хочу відзначити їхній внесок.

Це люди, які:

* [Допомагають іншим із проблемами (запитаннями) у GitHub](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank}.
* [Створюють пул реквести](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}.
* Переглядають пул реквести, [особливо важливо для перекладів](contributing.md#translations){.internal-link target=_blank}.

Оплески їм. 👏 🙇

## Найбільш активні користувачі минулого місяця

Це користувачі, які [найбільше допомагали іншим із проблемами (запитаннями) у GitHub](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank} протягом минулого місяця. ☕

{% if people %}
<div class="user-list user-list-center">
{% for user in people.last_month_active %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Issues replied: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Експерти

Ось **експерти FastAPI**. 🤓

Це користувачі, які [найбільше допомагали іншим із проблемами (запитаннями) у GitHub](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank} протягом *всього часу*.

Вони зарекомендували себе як експерти, допомагаючи багатьом іншим. ✨

{% if people %}
<div class="user-list user-list-center">
{% for user in people.experts %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Issues replied: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Найкращі контрибютори

Ось **Найкращі контрибютори**. 👷

Ці користувачі [створили найбільшу кількість пул реквестів](help-fastapi.md#create-a-pull-request){.internal-link target=_blank} які були *змержені*.

Вони надали програмний код, документацію, переклади тощо. 📦

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_contributors %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Pull Requests: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

Є багато інших контрибюторів (більше сотні), їх усіх можна побачити на сторінці <a href="https://github.com/tiangolo/fastapi/graphs/contributors" class="external-link" target="_blank">FastAPI GitHub Contributors</a>. 👷

## Найкращі рецензенти

Ці користувачі є **Найкращими рецензентами**. 🕵️

### Рецензенти на переклади

Я розмовляю лише кількома мовами (і не дуже добре 😅). Отже, рецензенти – це ті, хто має [**повноваження схвалювати переклади**](contributing.md#translations){.internal-link target=_blank} документації. Без них не було б документації кількома іншими мовами.

---

**Найкращі рецензенти** 🕵️ переглянули більшість пул реквестів від інших, забезпечуючи якість коду, документації і особливо **перекладів**.

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_reviewers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Reviews: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Спонсори

Це **Спонсори**. 😎

Вони підтримують мою роботу з **FastAPI** (та іншими), переважно через <a href="https://github.com/sponsors/tiangolo" class="external-link" target="_blank">GitHub Sponsors</a>.

{% if sponsors %}

{% if sponsors.gold %}

### Золоті спонсори

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.silver %}

### Срібні спонсори

{% for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.bronze %}

### Бронзові спонсори

{% for sponsor in sponsors.bronze -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% endif %}

### Індивідуальні спонсори

{% if github_sponsors %}
{% for group in github_sponsors.sponsors %}

<div class="user-list user-list-center">

{% for user in group %}
{% if user.login not in sponsors_badge.logins %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a></div>

{% endif %}
{% endfor %}

</div>

{% endfor %}
{% endif %}

## Про дані - технічні деталі

Основна мета цієї сторінки – висвітлити зусилля спільноти, щоб допомогти іншим.

Особливо враховуючи зусилля, які зазвичай менш помітні, а в багатьох випадках більш важкі, як-от допомога іншим із проблемами та перегляд пул реквестів перекладів.

Дані розраховуються щомісяця, ви можете ознайомитися з <a href="https://github.com/tiangolo/fastapi/blob/master/.github/actions/people/app/main.py" class="external-link" target="_blank">вихідним кодом тут</a>.

Тут я також підкреслюю внески спонсорів.

Я також залишаю за собою право оновлювати алгоритми підрахунку, види рейтингів, порогові значення тощо (про всяк випадок 🤷).
