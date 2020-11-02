# FastAPI Pessoal

FastAPI has an amazing community that welcomes people from all backgrounds.
FastAPI tem uma comunidade incrível que recebe pessoas de todas as origens.

## Criador - Mantenedor

Hey! 👋

Esse sou eu:

{% if people %}
<div class="user-list user-list-center">
{% for user in people.maintainers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Respostas: {{ user.answers }}</div><div class="count">Pull Requests: {{ user.prs }}</div></div>
{% endfor %}

</div>
{% endif %}

Eu sou o criador e mantenedor do **FastAPI**. Você pode ler mais sobre isso em [Ajuda FastAPI - Obtenha ajuda - Conecte-se com o autor](help-fastapi.md#connect-with-the-author){.internal-link target=_blank}.

...Mas aqui eu quero mostrar a nossa comunidade.

---

**FastAPI** recebe muito apoio da comunidade. E quero destacar suas contribuições.

Estas são as pessoas que:

* [Ajude outras pessoas com problemas (perguntas) no GitHub](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank}.
* [Criam Pull Requests](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}.
* Revise Pull Requests, [especially important for translations](contributing.md#translations){.internal-link target=_blank}.

Uma salva de palmas para eles. 👏 🙇

## Usuários mais ativos no mês passado

Estes são os usuários que mais têm [ajudado outras pessoas com problemas (dúvidas) no GitHub](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank} durante o ultimo mês. ☕

{% if people %}
<div class="user-list user-list-center">
{% for user in people.last_month_active %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Problemas respondidos: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Especialistas

Aqui estão os especialistas **FastAPI**. 🤓

 
Estes são os usuários que mais [ajudaram outras pessoas com problemas (perguntas) no GitHub](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank} desde *sempre*.

They have proven to be experts by helping many others. ✨

{% if people %}
<div class="user-list user-list-center">
{% for user in people.experts %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Issues replied: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Top Contributors

Here are the **Top Contributors**. 👷

These users have [created the most Pull Requests](help-fastapi.md#create-a-pull-request){.internal-link target=_blank} that have been *merged*.

They have contributed source code, documentation, translations, etc. 📦

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_contributors %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Pull Requests: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

There are many other contributors (more than a hundred), you can see them all in the <a href="https://github.com/tiangolo/fastapi/graphs/contributors" class="external-link" target="_blank">FastAPI GitHub Contributors page</a>. 👷

## Top Reviewers

These users are the **Top Reviewers**. 🕵️

### Reviews for Translations

I only speak a few languages (and not very well 😅). So, the reviewers are the ones that have the [**power to approve translations**](contributing.md#translations){.internal-link target=_blank} of the documentation. Without them, there wouldn't be documentation in several other languages.

---

The **Top Reviewers** 🕵️ have reviewed the most Pull Requests from others, ensuring the quality of the code, documentation, and especially, the **translations**.

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_reviewers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Reviews: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Sponsors

These are the **Sponsors**. 😎

They are supporting my work with **FastAPI** (and others) through <a href="https://github.com/sponsors/tiangolo" class="external-link" target="_blank">GitHub Sponsors</a>.

{% if people %}
<div class="user-list user-list-center">
{% for user in people.sponsors %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a></div>
{% endfor %}

</div>
{% endif %}

## About the data - technical details

The intention of this page is to highlight the effort of the community to help others.

Especially including efforts that are normally less visible, and in many cases more arduous, like helping others with issues and reviewing Pull Requests with translations.

The data is calculated each month, you can read the <a href="https://github.com/tiangolo/fastapi/blob/master/.github/actions/people/app/main.py" class="external-link" target="_blank">source code here</a>.

I also reserve the right to update the algorithm, sections, thresholds, etc (just in case 🤷).
