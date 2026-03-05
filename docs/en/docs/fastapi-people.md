---
hide:
  - navigation
---

# FastAPI People

FastAPI has an amazing community that welcomes people from all backgrounds.

## Creator

Hey! 👋

This is me:

<div class="user-list user-list-center">
{% for user in people.maintainers %}

<div class="user"><a href="{{ contributors.tiangolo.url }}"><div class="avatar-wrapper"><img src="{{ contributors.tiangolo.avatarUrl }}"/></div><div class="title">@{{ contributors.tiangolo.login }}</div></a> <div class="count">Answers: {{ user.answers }}</div><div class="count">Pull Requests: {{ contributors.tiangolo.count }}</div></div>
{% endfor %}

</div>

I'm the creator of **FastAPI**. You can read more about that in [Help FastAPI - Get Help - Connect with the author](help-fastapi.md#connect-with-the-author).

...But here I want to show you the community.

---

**FastAPI** receives a lot of support from the community. And I want to highlight their contributions.

These are the people that:

* [Help others with questions in GitHub](help-fastapi.md#help-others-with-questions-in-github).
* [Create Pull Requests](help-fastapi.md#create-a-pull-request).
* Review Pull Requests, [especially important for translations](contributing.md#translations).
* Help [manage the repository](management-tasks.md) (team members).

All these tasks help maintain the repository.

A round of applause to them. 👏 🙇

## Team

This is the current list of team members. 😎

They have different levels of involvement and permissions, they can perform [repository management tasks](./management-tasks.md) and together we  [manage the FastAPI repository](./management.md).

<div class="user-list user-list-center">

{% for user in members["members"] %}

<div class="user"><a href="{{ user.url }}"><div class="avatar-wrapper"><img src="{{ user.avatar_url }}"/></div><div class="title">@{{ user.login }}</div></a></div>

{% endfor %}

</div>

Although the team members have the permissions to perform privileged tasks, all the [help from others maintaining FastAPI](./help-fastapi.md#help-maintain-fastapi) is very much appreciated! 🙇‍♂️

## FastAPI Experts

These are the users that have been [helping others the most with questions in GitHub](help-fastapi.md#help-others-with-questions-in-github). 🙇

They have proven to be **FastAPI Experts** by helping many others. ✨

/// tip

You could become an official FastAPI Expert too!

Just [help others with questions in GitHub](help-fastapi.md#help-others-with-questions-in-github). 🤓

///

You can see the **FastAPI Experts** for:

* [Last Month](#fastapi-experts-last-month) 🤓
* [3 Months](#fastapi-experts-3-months) 😎
* [6 Months](#fastapi-experts-6-months) 🧐
* [1 Year](#fastapi-experts-1-year) 🧑‍🔬
* [**All Time**](#fastapi-experts-all-time) 🧙

### FastAPI Experts - Last Month

These are the users that have been [helping others the most with questions in GitHub](help-fastapi.md#help-others-with-questions-in-github) during the last month. 🤓

<div class="user-list user-list-center">

{% for user in people.last_month_experts[:10] %}

{% if user.login not in skip_users %}

<div class="user"><a href="{{ user.url }}"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Questions replied: {{ user.count }}</div></div>

{% endif %}

{% endfor %}

</div>

### FastAPI Experts - 3 Months

These are the users that have been [helping others the most with questions in GitHub](help-fastapi.md#help-others-with-questions-in-github) during the last 3 months. 😎

<div class="user-list user-list-center">

{% for user in people.three_months_experts[:10] %}

{% if user.login not in skip_users %}

<div class="user"><a href="{{ user.url }}"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Questions replied: {{ user.count }}</div></div>

{% endif %}

{% endfor %}

</div>

### FastAPI Experts - 6 Months

These are the users that have been [helping others the most with questions in GitHub](help-fastapi.md#help-others-with-questions-in-github) during the last 6 months. 🧐

<div class="user-list user-list-center">

{% for user in people.six_months_experts[:10] %}

{% if user.login not in skip_users %}

<div class="user"><a href="{{ user.url }}"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Questions replied: {{ user.count }}</div></div>

{% endif %}

{% endfor %}

</div>

### FastAPI Experts - 1 Year

These are the users that have been [helping others the most with questions in GitHub](help-fastapi.md#help-others-with-questions-in-github) during the last year. 🧑‍🔬

<div class="user-list user-list-center">

{% for user in people.one_year_experts[:20] %}

{% if user.login not in skip_users %}

<div class="user"><a href="{{ user.url }}"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Questions replied: {{ user.count }}</div></div>

{% endif %}

{% endfor %}

</div>

### FastAPI Experts - All Time

Here are the all time **FastAPI Experts**. 🤓🤯

These are the users that have [helped others the most with questions in GitHub](help-fastapi.md#help-others-with-questions-in-github) through *all time*. 🧙

<div class="user-list user-list-center">

{% for user in people.experts[:50] %}

{% if user.login not in skip_users %}

<div class="user"><a href="{{ user.url }}"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Questions replied: {{ user.count }}</div></div>

{% endif %}

{% endfor %}

</div>

## Top Contributors

Here are the **Top Contributors**. 👷

These users have [created the most Pull Requests](help-fastapi.md#create-a-pull-request) that have been *merged*.

They have contributed source code, documentation, etc. 📦

<div class="user-list user-list-center">

{% for user in (contributors.values() | list)[:50] %}

{% if user.login not in skip_users %}

<div class="user"><a href="{{ user.url }}"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Pull Requests: {{ user.count }}</div></div>

{% endif %}

{% endfor %}

</div>

There are hundreds of other contributors, you can see them all in the [FastAPI GitHub Contributors page](https://github.com/fastapi/fastapi/graphs/contributors). 👷

## Top Translation Reviewers

These users are the **Top Translation Reviewers**. 🕵️

Translation reviewers have the [**power to approve translations**](contributing.md#translations) of the documentation. Without them, there wouldn't be documentation in several other languages.

<div class="user-list user-list-center">
{% for user in (translation_reviewers.values() | list)[:50] %}

{% if user.login not in skip_users %}

<div class="user"><a href="{{ user.url }}"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Reviews: {{ user.count }}</div></div>

{% endif %}

{% endfor %}

</div>

## Sponsors

These are the **Sponsors**. 😎

They are supporting my work with **FastAPI** (and others), mainly through [GitHub Sponsors](https://github.com/sponsors/tiangolo).

{% if sponsors %}

{% if sponsors.gold %}

### Gold Sponsors

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.silver %}

### Silver Sponsors

{% for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.bronze %}

### Bronze Sponsors

{% for sponsor in sponsors.bronze -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% endif %}

### Individual Sponsors

{% if github_sponsors %}
{% for group in github_sponsors.sponsors %}

<div class="user-list user-list-center">

{% for user in group %}
{% if user.login not in sponsors_badge.logins %}

<div class="user"><a href="{{ user.url }}"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a></div>

{% endif %}
{% endfor %}

</div>

{% endfor %}
{% endif %}

## About the data - technical details

The main intention of this page is to highlight the effort of the community to help others.

Especially including efforts that are normally less visible, and in many cases more arduous, like helping others with questions and reviewing Pull Requests with translations.

The data is calculated each month, you can read the [source code here](https://github.com/fastapi/fastapi/blob/master/scripts/).

Here I'm also highlighting contributions from sponsors.

I also reserve the right to update the algorithm, sections, thresholds, etc (just in case 🤷).
