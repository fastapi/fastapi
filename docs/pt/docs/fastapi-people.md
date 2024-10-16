---
hide:
  - navigation
---

# Pessoas do FastAPI

O FastAPI tem uma comunidade incrível que acolhe pessoas de todos os backgrounds.

## Criador

Oi! 👋

Sou eu:

{% if people %}
<div class="user-list user-list-center">
{% for user in people.maintainers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Respostas: {{ user.answers }}</div><div class="count">Pull Requests: {{ user.prs }}</div></div>
{% endfor %}

</div>
{% endif %}

Eu sou o criador do FastAPI. Você pode ler mais sobre isso em Ajude o FastAPI - Obtenha Ajuda - Conecte-se com o autor.(help-fastapi.md#connect-with-the-author){.internal-link target=_blank}.

...Mas aqui eu quero mostrar a comunidade.

---

O **FastAPI** recebe muito apoio da comunidade. E eu quero destacar suas contribuições.

Estas são as pessoas que:

* [Ajudam outros com perguntas no GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank}.
* [Criam Pull Requests](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}.
* Revisam Pull Requests, [especialmente importante para traduções](contributing.md#translations){.internal-link target=_blank}.
* Ajudam a [gerenciar o repositório](management-tasks.md){.internal-link target=_blank} (membros da equipe).

Todas essas tarefas ajudam a manter o repositório.

Uma salva de palmas para eles. 👏 🙇

## Equipe

Esta é a lista atual de membros da equipe. 😎

Eles têm diferentes níveis de envolvimento e permissões, podendo realizar [tarefas de gerenciamento do repositório](./management-tasks.md){.internal-link target=_blank} e, juntos, [gerenciamos o repositório FastAPI](./management.md){.internal-link target=_blank}.

<div class="user-list user-list-center">
{% for user in members["members"] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatar_url }}"/></div><div class="title">@{{ user.login }}</div></a></div>
{% endfor %}

</div>

Embora os membros da equipe tenham permissões para realizar tarefas privilegiadas, toda [ajuda dos outros que mantêm o FastAPI](./help-fastapi.md#help-maintain-fastapi){.internal-link target=_blank} é muito apreciada! 🙇‍♂️

## Especialistas em FastAPI

Estes são os usuários que mais [têm ajudado os outros com perguntas no GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank}. 🙇

Eles se provaram como **Especialistas em FastAPI** ajudando muitos outros. ✨

/// dica

Você também pode se tornar um Especialista oficial em FastAPI!

Basta [ajudar outros com perguntas no GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank}. 🤓

///

Você pode ver os **Especialistas em FastAPI**:

* [Último Mês](#fastapi-experts-last-month) 🤓
* [3 Meses](#fastapi-experts-3-months) 😎
* [6 Meses](#fastapi-experts-6-months) 🧐
* [1 Ano](#fastapi-experts-1-year) 🧑‍🔬
* [**Todos os Tempos**](#fastapi-experts-all-time) 🧙

### Especialistas em FastAPI - Último Mês

Estes são os usuários que [mais ajudaram outros com perguntas no GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank} durante o último mês. 🤓

{% if people %}
<div class="user-list user-list-center">
{% for user in people.last_month_experts[:10] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Perguntas respondidas: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

### Especialistas em FastAPI - 3 Meses

Estes são os usuários que [mais ajudaram outros com perguntas no GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank} durante os últimos 3 meses. 😎

{% if people %}
<div class="user-list user-list-center">
{% for user in people.three_months_experts[:10] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Perguntas respondidas: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

### Especialistas em FastAPI - 6 Meses

Estes são os usuários que [mais ajudaram outros com perguntas no GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank} durante os últimos 6 meses. 🧐

{% if people %}
<div class="user-list user-list-center">
{% for user in people.six_months_experts[:10] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Perguntas respondidas: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

### Especialistas em FastAPI - 1 Ano

Estes são os usuários que [mais ajudaram outros com perguntas no GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank} durante o último ano. 🧑‍🔬

{% if people %}
<div class="user-list user-list-center">
{% for user in people.one_year_experts[:20] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Perguntas respondidas: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

### Especialistas em FastAPI - Todos os Tempos

Aqui estão os **Especialistas em FastAPI** de todos os tempos. 🤓🤯

Estes são os usuários que [mais ajudaram outros com perguntas no GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank} ao **longo do tempo**. 🧙

{% if people %}
<div class="user-list user-list-center">
{% for user in people.experts[:50] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Perguntas respondidas: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Principais Contribuidores

Aqui estão os **Principais Contribuidores**. 👷

Esses usuários [criaram o maior número de Pull Requests](help-fastapi.md#create-a-pull-request){.internal-link target=_blank} que foram *aceitos*.

Eles contribuíram com código-fonte, documentação, traduções, etc. 📦

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_contributors[:50] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Pull Requests: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

Há muitos outros contribuidores (mais de uma centena), você pode vê-los todos na <a href="https://github.com/fastapi/fastapi/graphs/contributors" class="external-link" target="_blank"> página  de Contribuidores do GitHub do FastAPI</a>. 👷

## Principais Revisores de Traduções

Estes usuários são os **Principais Revisores de Traduções**. 🕵️

Eu falo apenas alguns idiomas (e não muito bem 😅). Portanto, os revisores são os que têm o [**poder de aprovar traduções**](contributing.md#translations){.internal-link target=_blank} da documentação. Sem eles, não haveria documentação em vários outros idiomas.

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_translations_reviewers[:50] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Revisões: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Patrocinadores

Estes são os **Patrocinadores**. 😎

Eles estão apoiando meu trabalho com o **FastAPI** (e outros), principalmente através do <a href="https://github.com/sponsors/tiangolo" class="external-link" target="_blank">GitHub Sponsors</a>.

{% if sponsors %}

{% if sponsors.gold %}

### Patrocinadores de Ouro

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.silver %}

### Patrocinadores de Prata

{% for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.bronze %}

### Patrocinadores de Bronze

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

## Sobre os dados - detalhes técnicos

A principal intenção desta página é destacar o esforço da comunidade em ajudar outros.

Especialmente incluindo esforços que normalmente são menos visíveis, e em muitos casos mais árduos, como ajudar outros com perguntas e revisar Pull Requests de traduções.

Os dados são calculados a cada mês, você pode ler o <a href="https://github.com/fastapi/fastapi/blob/master/.github/actions/people/app/main.py" class="external-link" target="_blank">código-fonte aqui</a>.

Aqui também estou destacando contribuições de patrocinadores.

Eu também reservo o direito de atualizar o algoritmo, seções, limiares, etc. (só para garantir 🤷).
