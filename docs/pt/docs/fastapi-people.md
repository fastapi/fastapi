# Agentes FastAPI

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

* [Ajudam outras pessoas com problemas (perguntas) no GitHub](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank}.
* [Criam Pull Requests](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}.
* Revisam Pull Requests, [importante especialmente para as traduções](contributing.md#translations){.internal-link target=_blank}.

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

Eles provaram ser especialistas ao ajudar muitos outros. ✨

{% if people %}
<div class="user-list user-list-center">
{% for user in people.experts %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Problemas respondidos: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Principais contribuidores

Aqui estão os **Principais Colaboradores**. 👷

Esses usuários [criaram a maioria dos Pull Requests](help-fastapi.md#create-a-pull-request){.internal-link target=_blank} que foram *mergiadas*.

Eles contribuíram com o código-fonte, documentação, traduções, etc. 📦

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_contributors %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Pull Requests: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

Existem muitos outros contribuidores (mais de cem), você pode vê-los todos na <a href="https://github.com/tiangolo/fastapi/graphs/contributors" class="external-link" target="_blank">página FastAPI GitHub Contributors</a>. 👷

## Principais Revisores

Esses usuários são os **Principais Revisores**. 🕵️

### Críticas para traduções

Eu só falo algumas línguas (e não muito bem 😅). Portanto, os revisores são os que têm o [**poder de aprovar traduções**](contributing.md#translations){.internal-link target=_blank} da documentação. Sem eles, não haveria documentação em vários outros idiomas.

---

Os **Principais Revisores** revisaram a maioria dos Pull Requests de outros, garantindo a qualidade do código, da documentação e, principalmente, das **traduções**.

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_reviewers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Revisões: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Patrocinadores

Estes são os **patrocinadores**. 😎

Eles estão apoiando meu trabalho com **FastAPI** (e outros) por meio do <a href="https://github.com/sponsors/tiangolo" class="external-link" target="_blank">GitHub Sponsors</a>.

{% if people %}
<div class="user-list user-list-center">
{% for user in people.sponsors %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a></div>
{% endfor %}

</div>
{% endif %}

## Sobre os dados - detalhes técnicos

A intenção desta página é destacar o esforço da comunidade para ajudar os outros.

Especialmente incluindo esforços que normalmente são menos visíveis e, em muitos casos, mais árduos, como ajudar outras pessoas com problemas e revisar Pull Requests com traduções.

Os dados são calculados a cada mês, você pode ler o <a href="https://github.com/tiangolo/fastapi/blob/master/.github/actions/people/app/main.py" class="external-link" target="_blank">código-fonte aqui</a>.

Eu também me reservo o direito de atualizar o algoritmo, seções, limites, etc (apenas no caso 🤷).
