---
hide:
  - navigation
---

# Personas de FastAPI

FastAPI tiene una comunidad increíble que da la bienvenida a personas de todo tipo.

## Creador - Mantenedor

¡Hola! 👋

Este soy yo:

{% if people %}
<div class="user-list user-list-center">
{% for user in people.maintainers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Respuestas: {{ user.answers }}</div><div class="count">Pull Requests: {{ user.prs }}</div></div>
{% endfor %}

</div>
{% endif %}

Yo soy el creador y el mantenedor de **FastAPI**. Puedes leer más sobre eso en [Ayuda FastAPI - Obtener ayuda - Conectar con el autor](help-fastapi.md#connect-with-the-author){.internal-link target=_blank}.

...Pero aquí quiero mostrarte la comunidad.

---

**FastAPI** recibe mucho apoyo de la comunidad. Y quiero resaltar sus contribuciones.

Estas son las personas que:

* [Ayuda a otros con preguntas en GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank}.
* [Crea Pull Requests](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}.
* Revisa Pull Requests, [especialmente importante para las traducciones](contributing.md#translations){.internal-link target=_blank}.

Un aplauso para ellos. 👏 🙇

## Usuarios más activos el mes pasado

Estos son los usuarios que han estado [ayudando más a otros con preguntas en GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank} durante el mes pasado. ☕

{% if people %}
<div class="user-list user-list-center">
{% for user in people.last_month_active %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Preguntas respondidas: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Expertos

Aquí están los **Expertos de FastAPI**. 🤓

Estos son los usuarios que han [ayudado más a otros con preguntas en GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank} durante *todo el tiempo*.

Han demostrado ser expertos ayudando a muchos otros. ✨

{% if people %}
<div class="user-list user-list-center">
{% for user in people.experts %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Preguntas respondidas: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Principales Colaboradores

Aquí están los **Principales Colaboradores**. 👷

Estos usuarios han [creado la mayor cantidad de Pull Requests](help-fastapi.md#create-a-pull-request){.internal-link target=_blank} que se han *<abbr title="en español conocido como: fusionado, mezclado">merged</abbr>*.

Han contribuido con código fuente, documentación, traducciones, etc. 📦

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_contributors %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Pull Requests: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

Hay muchos otros Colaboradores (más de cien), puedes verlos a todos en <a href="https://github.com/tiangolo/fastapi/graphs/contributors" class="external-link" target=" _blank">Página de Colaboradores de FastAPI GitHub</a>. 👷

## Principales Revisores

Estos usuarios son los **Principales Revisores**. 🕵️

### Revisiones sobre Traducciones

Sólo hablo algunos idiomas (y no muy bien 😅). Entonces, los revisores son los que tienen el [**poder de aprobar traducciones**](contributing.md#translations){.internal-link target=_blank} de la documentación. Sin ellos, no habría documentación en otros idiomas.

---

Los **Principales Revisores** 🕵️ han revisado la mayoría de los Pull Requests de otros, asegurando la calidad del código, la documentación y, especialmente, las **traducciones**.

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_reviewers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Revisiones: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Patrocinadores

Estos son los **Patrocinadores**. 😎

Están apoyando mi trabajo con **FastAPI** (y otros proyectos), principalmente a través de <a href="https://github.com/sponsors/tiangolo" class="external-link" target="_blank">Patrocinadores de GitHub. </a>.

{% if sponsors %}

{% if sponsors.gold %}

### Patrocinadores de Oro

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.silver %}

### Patrocinadores de Plata

{% for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.bronze %}

### Patrocinadores de Bronce

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

## Acerca de los datos - detalles técnicos

La principal intención de esta página es resaltar el esfuerzo de la comunidad por ayudar a los demás.

Especialmente incluyendo esfuerzos que normalmente son menos visibles y, en muchos casos, más arduos, como ayudar a otros con preguntas y revisar Pull Requests con traducciones.

Los datos se calculan cada mes, puedes leer el <a href="https://github.com/tiangolo/fastapi/blob/master/.github/actions/people/app/main.py" class="external- link" target="_blank">código fuente aquí</a>.

Aquí también destaco las contribuciones de los patrocinadores.

También me reservo el derecho de actualizar el algoritmo, secciones, umbrales, etc (por si acaso 🤷).
