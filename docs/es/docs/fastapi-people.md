# Personas de FastAPI

FastAPI tiene una increíble comunidad que le brinda la bienvenida a personas de todo tipo.

## Creador - Mantenedor

Hola! 👋

Este soy yo:

{% if people %}
<div class="user-list user-list-center">
{% for user in people.maintainers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Answers: {{ user.answers }}</div><div class="count">Pull Requests: {{ user.prs }}</div></div>
{% endfor %}

</div>
{% endif %}

Soy el creador y el encargado de dar mantenimiento a **FastAPI**. Puedes leer mas sobre eso en [Help FastAPI - Get Help - Connect with the author](help-fastapi.md#conecta-con-el-autor){.internal-link target=_blank}.

...Pero aquí quiero mostrarte a la comunidad.

---

**FastAPI** recibe demasiada ayuda de la comunidad. Y quiero resaltar sus contribuciones.

Aquí están las persona que:

* [Ayudan a otros con issues (preguntas) en GitHub](help-fastapi.md#ayuda-a-otros-con-issues-de-github){.internal-link target=_blank}.
* [Crean Pull Requests](help-fastapi.md#crea-un-pull-request){.internal-link target=_blank}.
* Revisan los Pull Requests, [de especialidad importancia para las traducciones](contributing.md#translations){.internal-link target=_blank}.

Una ronda de aplausos a todos ellos. 👏 🙇

## Usuarios mas activos durante el mes pasado

Estos son los usuarios que han estado [ayudando a otros con mas issues (preguntas) en GitHub](help-fastapi.md#ayuda-a-otros-con-issues-de-github){.internal-link target=_blank} durante el último mes. ☕

{% if people %}
<div class="user-list user-list-center">
{% for user in people.last_month_active %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Issues replied: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Expertos

Aquí están los **Expertos en FastAPI**. 🤓

Estos son los usuarios que han [ayudado a otros con mas issues (preguntas) en GitHub](help-fastapi.md#ayuda-a-otros-con-issues-de-github){.internal-link target=_blank} por *todo el tiempo*.

Ellos han demostrado ser expertos al ayudar a muchos otros. ✨

{% if people %}
<div class="user-list user-list-center">
{% for user in people.experts %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Issues replied: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Top Contributors

Aquí están los **Top Contributors**. 👷

Estos son los usuarios que han [creado la mayor cantidad de Pull Requests](help-fastapi.md#crea-un-pull-request){.internal-link target=_blank} que han sido incorporados al proyecto (*merged*).

Ellos han contribuido al código fuente, documentación, traducciones, etc. 📦

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_contributors %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Pull Requests: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

Hay muchos mas contribuidores (más de cien), tu puedes ver todos en <a href="https://github.com/tiangolo/fastapi/graphs/contributors" class="external-link" target="_blank">la página de contribuidores de FastAPI en GitHub</a>. 👷

## Top Reviewers

Estos usuarios son los **Top Reviewers**. 🕵️

### Revisiones de Traducciones.

Solo hablo pocos idiomas (y no muy bien 😅). Por lo que, los reviewers son aquellos que tienen el [**poder de aprobar las traducciones**](contributing.md#translations){.internal-link target=_blank} de la documentación. Sin ellos, no habría documentación en algunos idiomas.

---

Los **Top Reviewers** 🕵️ han revisado la mayor cantidad de Pull Requests de otros, asegurando la calidad del código, documentación, y sobre todo, las **traducciones**.

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_reviewers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Reviews: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Sponsors

Estos son los patrocinadores, **Sponsors**. 😎

Ellos están soportando mi trabajo con **FastAPI** (y otros), principalmente mediante <a href="https://github.com/sponsors/tiangolo" class="external-link" target="_blank">GitHub Sponsors</a>.

### Gold Sponsors

{% if sponsors %}
{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}"></a>
{% endfor %}
{% endif %}

### Silver Sponsors

{% if sponsors %}
{% for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}"></a>
{% endfor %}
{% endif %}

{% if people %}
{% if people.sponsors_50 %}

### Bronze Sponsors

<div class="user-list user-list-center">
{% for user in people.sponsors_50 %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a></div>
{% endfor %}

</div>

{% endif %}
{% endif %}

### Individual Sponsors

{% if people %}
<div class="user-list user-list-center">
{% for user in people.sponsors %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a></div>
{% endfor %}

</div>
{% endif %}

## Sobre los datos - detalles técnicos

La intención principal de esta pagina es reconocer el esfuerzo de la comunidad por ayudar a otros.

Especialmente destacar los esfuerzos que están normalmente menos visibles, y que en muchos casos son mas arduos, como ayudar a otros con problemas y revisar los Pull Requests con traducciones.

Los datos son calculados cada mes, puedes leer el <a href="https://github.com/tiangolo/fastapi/blob/master/.github/actions/people/app/main.py" class="external-link" target="_blank">código fuente aquí</a>.

Ademas aquí reconozco las contribuciones de los patrocinadores (sponsors)

También me reservo el derecho de actualizar los algoritmos, secciones, umbrales, etc (solo por si acaso 🤷).
