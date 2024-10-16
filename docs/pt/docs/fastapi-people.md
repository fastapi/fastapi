---
hide:
  - navigation
---

# Pessoas do FastAPI

FastAPI tem uma comunidade incrível que acolhe pessoas de todos os tipos.

## Criador

Olá! 👋

Esse sou eu:

{% if people %}
<div class="user-list user-list-center">
{% for user in people.maintainers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Respostas: {{ user.answers }}</div><div class="count">Pull Requests: {{ user.prs }}</div></div>
{% endfor %}

</div>
{% endif %}

Eu sou o criador do **FastAPI**. Você pode ler mais sobre isso em [Ajuda FastAPI - Obtenha Ajuda - Conecte-se com o autor](help-fastapi.md#conecte-se-com-o-autor){.internal-link target=_blank}.

...Mas aqui eu quero te mostrar a comunidade.

---

**FastAPI** recebe muito apoio da comunidade. E eu quero destacar suas contribuições.

Essas são as pessoas que:

* [Ajudam outros com questões no github](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank}.
* [Criam Pull Requests](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}.
* Revisam Pull Requests, [especialmente importante para traduções](contributing.md#translations){.internal-link target=_blank}.
* Ajudam [a gerenciar o repositório](management-tasks.md){.internal-link target=_blank} (membros da equipe).

Todas essas tarefas ajudam a manter o repositório.

Uma salva de palmas para eles. 👏 🙇

## Time

Essa é a lista atual de membros da equipe. 😎

Eles tem diferentes níveis de envolvimento e permissões, eles podem realizar [tarefas de gerenciamento de repositório](./management-tasks.md){.internal-link target=_blank} e juntos nós [gerenciamos o repositório FastAPI](./management.md){.internal-link target=_blank}.

<div class="user-list user-list-center">
{% for user in members["members"] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatar_url }}"/></div><div class="title">@{{ user.login }}</div></a></div>
{% endfor %}

</div>

Apesar de os membros da equipe terem permissões para realizar tarefas privilegiadas, toda a [ajuda de outros mantendo o FastAPI](./help-fastapi.md#help-maintain-fastapi){.internal-link target=_blank} é muito apreciada! 🙇‍♂️

## Expeerts FastAPI

Esses são os usuários que [mais ajudaram os outros com perguntas no GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank}. 🙇

Eles provaram ser **Experts FASTApi** ajudando muitos outros. ✨

/// dica

Você também pode se tornar um **FastAPI Expert**!

Somente ao [ajudar os outros com perguntas no GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank}. 🤓

///

Você pode ver os **Experts FASTApi** para:

* [Último Mês](#fastapi-experts-last-month) 🤓
* [3 Meses](#fastapi-experts-3-months) 😎
* [6 Meses](#fastapi-experts-6-months) 🧐
* [1 Ano](#fastapi-experts-1-year) 🧑‍🔬
* [All Time](#fastapi-experts-all-time) 🧙

### Experts FastAPI - Último Mês

Esses são os usuários que estiveram [ajudando os outros com perguntas no GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank} durante o último mês. 🤓

{% if people %}
<div class="user-list user-list-center">
{% for user in people.last_month_experts[:10] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Perguntas Respondidas: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

### Experts FastAPI - 3 Meses

Esses são os usuários que estiveram [ajudando os outros com perguntas no GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank} durante os últimos 3 meses. 😎

{% if people %}
<div class="user-list user-list-center">
{% for user in people.three_months_experts[:10] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Perguntas Respondidas: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

### Experts FastAPI - 6 Meses

Esses são os usuários que estiveram [ajudando os outros com perguntas no GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank} durante os últimos 6 meses. 🧐

{% if people %}
<div class="user-list user-list-center">
{% for user in people.six_months_experts[:10] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Perguntas Respondidas: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

### Experts FastAPI - 1 Ano

Esses são os usuários que estiveram [ajudando os outros com perguntas no GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank} durante o último ano. 🧑‍🔬

{% if people %}
<div class="user-list user-list-center">
{% for user in people.one_year_experts[:20] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Perguntas Respondidas: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

### Experts FastAPI - All Time

Aqui estão os **Experts FASTApi** de todos os tempos. 🤓🤯

Esses são os usuários que [mais ajudaram os outros com perguntas no GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank} *de todos os tempos*. 🧙

{% if people %}
<div class="user-list user-list-center">
{% for user in people.experts[:50] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Perguntas Respondidas: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Principais Contribuidores

Aqui estão os **Principais Contribuidores**. 👷

Esses usários [criaram mais Pull Requests](help-fastapi.md#create-a-pull-request){.internal-link target=_blank} que foram *mesclados*.

Eles contribuíram com código fonte, documentação, traduções, etc. 📦

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_contributors[:50] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Pull Requests: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

Tem muitos outros contribuidores (mais de cem), você pode ver todos na <a href="https://github.com/fastapi/fastapi/graphs/contributors" class="external-link" target="_blank">FastAPI GitHub Contributors page</a>. 👷

## Principais Revisores de Tradução

Esses usuários são os **Principais Revisores de Tradução**. 🕵️

Eu falo apenas algumas línguas (e não muito bem 😅). Então, os revisores são aqueles que têm o [**poder de aprovar traduções**](contributing.md#translations){.internal-link target=_blank} da documentação. Sem eles, não haveria documentação em várias outras línguas.

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_translations_reviewers[:50] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Reviews: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Patrocinadores

Esses são os **Patrocinadores**. 😎

Eles estão apoiando meu trabalho com a **FastAPI** (e outros), principalmente pelo <a href="https://github.com/sponsors/tiangolo" class="external-link" target="_blank">GitHub Sponsors</a>.

{% if sponsors %}

{% if sponsors.gold %}

### Patrocinadores Ouro

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.silver %}

### Patrocinadores Prata

{% for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.bronze %}

### Patrocinadores Bronze

{% for sponsor in sponsors.bronze -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% endif %}

### Patrocinadores Individuais

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
=

## Sobre os dados - detalhes técnicos

A principal intenção desta página é destacar o esforço da comunidade para ajudar os outros.

Especialmente incluindo esforços que normalmente são menos visíveis, e em muitos casos mais árduos, como ajudar os outros com perguntas e revisar Pull Requests com traduções.

Esses dados são calculados mensalmente, você pode ler o <a href="https://github.com/fastapi/fastapi/blob/master/.github/actions/people/app/main.py" class="external-link" target="_blank">código fonte aqui</a>.

Aqui também estou destacando as contribuições dos patrocinadores.

Eu também me reservo o direito de atualizar o algoritmo, seções, limites, etc (só por precaução 🤷).
