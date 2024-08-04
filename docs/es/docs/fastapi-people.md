---
hide:
  - navigation
---

# Personas de FastAPI

FastAPI tiene una increíble comunidad que da la bienvenida a personas de todos los orígenes.

## Creador

Hey! 👋

Este soy yo:

{% if people %}
<div class="user-list user-list-center">
{% for user in people.maintainers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Respuestas: {{ user.answers }}</div><div class="count">Pull Requests: {{ user.prs }}</div></div>
{% endfor %}

</div>
{% endif %}

Soy el creador de **FastAPI**. Puedes leer más sobre eso en [Ayuda FastAPI - Obtener Ayuda - Conectar con el autor](help-fastapi.md#connect-with-the-author){.internal-link target=_blank}.

...Pero aquí quiero mostrarte la comunidad.

---

**FastAPI** recibe mucho apoyo de la comunidad. Y quiero destacar sus contribuciones.

Aquí están las personas que:

* [Ayudan a otros con preguntas en GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank}.
* [Crean Pull Requests](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}.
* Revisan Pull Rquests, [especialmente importante para traducciones](contributing.md#translations){.internal-link target=_blank}.
* Ayudan a [mantener el repositorio](management-tasks.md){.internal-link target=_blank} (miembros del equipo).

Todas estas tareas ayudan a mantener el repositorio.

Una ronda de aplausos para ellos. 👏 🙇

## Equipo

Esta es la lista actual de miembros del equipo. 😎

Ellos tienen diferentes niveles de participación y permisos, pueden realizar [tareas de gestión del repositorio](./management-tasks.md){.internal-link target=_blank} y juntos [administramos el repositorio de FastAPI](./management.md){.internal-link target=_blank}.

{% if members %}

<div class="user-list user-list-center">
{% for user in members["members"] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatar_url }}"/></div><div class="title">@{{ user.login }}</div></a></div>
{% endfor %}

</div>

Aunque los miembros del equipo tienen los permisos para realizar tareas privilegiadas, ¡se agradece mucho toda la [ayuda de otros para mantener FastAPI](./help-fastapi.md#help-maintain-fastapi){.internal-link target=_blank}! 🙇‍♂️

{% endif %}

## Expertos en FastAPI

Estos son los usuarios que más han estado [ayudando a otros con preguntas en GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank}. 🙇

Ellos han demostrado ser **Expertos en FastAPI** ayudando a muchos otros. ✨

!!! tip "Consejo"
    Podrías convertirte en un Experto en FastAPI también.

    Solo [necesitas responder preguntas en Github](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank}. 🤓

Puedes ver los **Expertos en FastAPI** para:

* [Último Mes](#fastapi-experts-last-month) 🤓
* [3 Meses](#fastapi-experts-3-months) 😎
* [6 Meses](#fastapi-experts-6-months) 🧐
* [1 Año](#fastapi-experts-1-year) 🧑‍🔬
* [**Todos los tiempos**](#fastapi-experts-all-time) 🧙

### Expertos en FastAPI - Último Mes

Estos son los usuarios que más han estado [ayudando a otros con preguntas en GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank} durante el último mes. 🤓

{% if people %}
<div class="user-list user-list-center">
{% for user in people.last_month_experts[:10] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Preguntas respondidas: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

### Expertos en FastAPI - 3 Meses

Estos son los usuarios que más han estado [ayudando a otros con preguntas en GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank} durante los últimos 3 meses. 😎

{% if people %}
<div class="user-list user-list-center">
{% for user in people.three_months_experts[:10] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Preguntas respondidas: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

### Expertos en FastAPI - 6 Meses

Estos son los usuarios que más han estado [ayudando a otros con preguntas en GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank} durante los últimos 6 meses. 🧐

{% if people %}
<div class="user-list user-list-center">
{% for user in people.six_months_experts[:10] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Preguntas respondidas: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

### Expertos en FastAPI - 1 Año

Estos son los usuarios que más han estado [ayudando a otros con preguntas en GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank} durante el último año. 🧑‍🔬

{% if people %}
<div class="user-list user-list-center">
{% for user in people.one_year_experts[:20] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Preguntas respondidas: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

### Expertos en FastAPI - Todos los Tiempos

Aquí están los **Expertos en FastAPI** de todos los tiempos. 🤓🤯

Estos son los usuarios que más han estado [ayudando a otros con preguntas en GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank} a lo largo de *todos los tiempos*. 🧙

{% if people %}
<div class="user-list user-list-center">
{% for user in people.experts[:50] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Preguntas respondidas: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Principales Colaboradores

Aquí están los **Principales Colaboradores**. 👷

Estos usuarios han [creado la mayoría de las Pull Requests](help-fastapi.md#create-a-pull-request){.internal-link target=_blank} que han sido *merged*.

Ellos han contribuido con código fuente, documentación, traducciones, etc. 📦

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_contributors[:50] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Pull Requests: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

Hay muchos otros colaboradores (más de cien), puedes verlos a todos en la <a href="https://github.com/fastapi/fastapi/graphs/contributors" class="external-link" target="_blank">página de Colaboradores de GitHub de FastAPI</a>. 👷

## Principales Revisores de Traducción

Estos usuarios son los **Principales Revisores de Traducción**. 🕵️

Solo hablo algunos idiomas (y no muy bien 😅). Por lo tanto, los revisores son los que tienen el [**poder de aprobar traducciones**](contributing.md#translations){.internal-link target=_blank} de la documentación. Sin ellos, no habría documentación en varios otros idiomas.

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_translations_reviewers[:50] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Reseñas: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Patrocinadores

EStos son los **Patrocinadores**. 😎

Ellos están apoyando mi trabajo con **FastAPI** (y otros), principalmente a través de <a href="https://github.com/sponsors/tiangolo" class="external-link" target="_blank">GitHub Sponsors</a>.

{% if sponsors %}

{% if sponsors.gold %}

## Patrocinadores Oro

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.silver %}

### Patrocinadores Plata

{% for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.bronze %}

### Patrocinadores Bronce

{% for sponsor in sponsors.bronze -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% endif %}

### Patrocinadores Individuales

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

## Sobre los datos - detalles técnicos

La intención principal de esta página es destacar el esfuerzo de la comunidad para ayudar a otros.

Especialmente incluyendo esfuerzos que normalmente son menos visibles, y en muchos casos más arduos, como ayudar a otros con preguntas y revisar Pull Requests con traducciones.

Los datos se calculan cada mes, puedes leer el <a href="https://github.com/fastapi/fastapi/blob/master/.github/actions/people/app/main.py" class="external-link" target="_blank">código fuente aquí</a>.

Aquí también destaco las contribuciones de los patrocinadores.

Tambiém me reservo el derecho de actualizar el algoritmo, secciones, umbrales, etc (por si acaso 🤷).
