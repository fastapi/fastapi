
# Люди, поддерживающие FastAPI

У FastAPI замечательное сообщество, которое доброжелательно к людям с любым уровнем знаний.

## Создатель и хранитель

Ку! 👋

Это я:

{% if people %}
<div class="user-list user-list-center">
{% for user in people.maintainers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Answers: {{ user.answers }}</div><div class="count">Pull Requests: {{ user.prs }}</div></div>
{% endfor %}

</div>
{% endif %}

Я создал и продолжаю поддерживать **FastAPI**. Узнать обо мне больше можно тут [Помочь FastAPI - Получить помощь - Связаться с автором](help-fastapi.md#connect-with-the-author){.internal-link target=_blank}.

... но на этой странице я хочу показать вам наше сообщество.

---

**FastAPI** получает огромную поддержку от своего сообщества. И я хочу отметить вклад его участников.

Это люди, которые:

* [Помогают другим с их проблемами (вопросами) на GitHub](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank}.
* [Создают пул-реквесты](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}.
* Делают ревью пул-реквестов, [что особенно важно для переводов на другие языки](contributing.md#translations){.internal-link target=_blank}.

Поаплодируем им! 👏 🙇

## Самые активные участники за прошедший месяц

Эти участники [оказали наибольшую помощь другим с решением их проблем (вопросов) на GitHub](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank} в течение последнего месяца. ☕

{% if people %}
<div class="user-list user-list-center">
{% for user in people.last_month_active %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Issues replied: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Эксперты

Здесь представлены **Эксперты FastAPI**. 🤓

Эти участники [оказали наибольшую помощь другим с решением их проблем (вопросов) на GitHub](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank} за *всё время*.

Оказывая помощь многим другим, они подтвердили свой уровень знаний. ✨

{% if people %}
<div class="user-list user-list-center">
{% for user in people.experts %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Issues replied: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Рейтинг участников, внёсших вклад в код

Здесь представлен **Рейтинг участников, внёсших вклад в код**. 👷

Эти люди [сделали наибольшее количество пул-реквестов](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}, *включённых в основной код*.

Они сделали наибольший вклад в исходный код, документацию, переводы и т.п. 📦

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_contributors %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Pull Requests: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

На самом деле таких людей довольно много (более сотни), вы можете увидеть всех на этой странице <a href="https://github.com/tiangolo/fastapi/graphs/contributors" class="external-link" target="_blank">FastAPI GitHub Contributors page</a>. 👷

## Рейтинг ревьюеров

Здесь представлен **Рейтинг ревьюеров**. 🕵️

### Проверки переводов на другие языки

Я знаю не очень много языков (и не очень хорошо 😅).
Итак, ревьюеры - это люди, которые могут [**подтвердить предложенный вами перевод** документации](contributing.md#translations){.internal-link target=_blank}. Без них не было бы документации на многих языках.

---

В **Рейтинге ревьюеров** 🕵️ представлены те, кто проверил наибольшее количество пул-реквестов других участников, обеспечивая качество кода, документации и, особенно, **переводов на другие языки**.

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_reviewers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Reviews: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Спонсоры

Здесь представлены **Спонсоры**. 😎

Спонсоры поддерживают мою работу над **FastAPI** (и другими проектами) главным образом через <a href="https://github.com/sponsors/tiangolo" class="external-link" target="_blank">GitHub Sponsors</a>.

{% if sponsors %}

{% if sponsors.gold %}

### Золотые спонсоры

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.silver %}

### Серебрянные спонсоры

{% for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.bronze %}

### Бронзовые спонсоры

{% for sponsor in sponsors.bronze -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% endif %}

### Индивидуальные спонсоры

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

## О данных - технические детали

Основная цель этой страницы - подчеркнуть усилия сообщества по оказанию помощи другим.

Особенно это касается усилий, которые обычно менее заметны и во многих случаях более трудоемки, таких как помощь другим в решении проблем и проверка пул-реквестов с переводами.

Данные рейтинги подсчитываются каждый месяц, ознакомиться с тем, как это работает можно <a href="https://github.com/tiangolo/fastapi/blob/master/.github/actions/people/app/main.py" class="external-link" target="_blank">тут</a>.

Кроме того, я также подчеркиваю вклад спонсоров.

И я оставляю за собой право обновлять алгоритмы подсчёта, виды рейтингов, пороговые значения и т.д. (так, на всякий случай 🤷).
