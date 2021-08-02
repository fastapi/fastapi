# La communauté FastAPI

FastAPI a une communauté extraordinaire qui accueille des personnes de tous horizons.

## Créateur - Mainteneur

Salut! 👋

C'est moi :

{% if people %}
<div class="user-list user-list-center">
{% for user in people.maintainers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Réponses: {{ user.answers }}</div><div class="count">Pull Requests: {{ user.prs }}</div></div>
{% endfor %}

</div>
{% endif %}

Je suis le créateur et le responsable de **FastAPI**. Vous pouvez en lire plus à ce sujet dans [Aide FastAPI - Obtenir de l'aide - Se rapprocher de l'auteur](help-fastapi.md#connect-with-the-author){.internal-link target=_blank}.

...Mais ici, je veux vous montrer la communauté.

---

**FastAPI** reçoit beaucoup de soutien de la part de la communauté. Et je tiens à souligner leurs contributions.

Ce sont ces personnes qui :

* [Aident les autres à résoudre des problèmes (questions) dans GitHub](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank}.
* [Créent des Pull Requests](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}.
* Review les Pull Requests, [particulièrement important pour les traductions](contributing.md#translations){.internal-link target=_blank}.

Une salve d'applaudissements pour eux. 👏 🙇

## Utilisateurs les plus actifs le mois dernier

Ce sont les utilisateurs qui ont [aidé le plus les autres avec des problèmes (questions) dans GitHub](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank} au cours du dernier mois. ☕

{% if people %}
<div class="user-list user-list-center">
{% for user in people.last_month_active %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Questions répondues: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Experts

Voici les **Experts FastAPI**. 🤓

Ce sont les utilisateurs qui ont [aidé le plus les autres avec des problèmes (questions) dans GitHub](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank} depuis *toujours*.

Ils ont prouvé qu'ils étaient des experts en aidant beaucoup d'autres personnes. ✨

{% if people %}
<div class="user-list user-list-center">
{% for user in people.experts %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Questions répondues: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Principaux contributeurs

Ces utilisateurs sont les **Principaux contributeurs**. 👷

Ces utilisateurs ont [créé le plus grand nombre de demandes Pull Request](help-fastapi.md#create-a-pull-request){.internal-link target=_blank} qui ont été *merged*.

Ils ont contribué au code source, à la documentation, aux traductions, etc. 📦

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_contributors %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Pull Requests: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

Il existe de nombreux autres contributeurs (plus d'une centaine), vous pouvez les voir tous dans la <a href="https://github.com/tiangolo/fastapi/graphs/contributors" class="external-link" target="_blank">Page des contributeurs de FastAPI GitHub</a>. 👷

## Principaux Reviewers

Ces utilisateurs sont les **Principaux Reviewers**. 🕵️

### Reviewers des traductions

Je ne parle que quelques langues (et pas très bien 😅). Ainsi, les reviewers sont ceux qui ont le [**pouvoir d'approuver les traductions**](contributing.md#translations){.internal-link target=_blank} de la documentation. Sans eux, il n'y aurait pas de documentation dans plusieurs autres langues.

---

Les **Principaux Reviewers** 🕵️ ont examiné le plus grand nombre de demandes Pull Request des autres, assurant la qualité du code, de la documentation, et surtout, des **traductions**.

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_reviewers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Reviews: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Sponsors

Ce sont les **Sponsors**. 😎

Ils soutiennent mon travail avec **FastAPI** (et d'autres) avec <a href="https://github.com/sponsors/tiangolo" class="external-link" target="_blank">GitHub Sponsors</a>.

### Gold Sponsors

{% if sponsors %}
{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

### Silver Sponsors

{% if sponsors %}
{% for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

### Bronze Sponsors

{% if sponsors %}
{% for sponsor in sponsors.bronze -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

### Individual Sponsors

{% if people %}
{% if people.sponsors_50 %}

<div class="user-list user-list-center">
{% for user in people.sponsors_50 %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a></div>
{% endfor %}

</div>

{% endif %}
{% endif %}

{% if people %}
<div class="user-list user-list-center">
{% for user in people.sponsors %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a></div>
{% endfor %}

</div>
{% endif %}

## À propos des données - détails techniques

L'intention de cette page est de souligner l'effort de la communauté pour aider les autres.

Notamment en incluant des efforts qui sont normalement moins visibles, et, dans de nombreux cas, plus difficile, comme aider d'autres personnes à résoudre des problèmes et examiner les Pull Requests de traduction.

Les données sont calculées chaque mois, vous pouvez lire le <a href="https://github.com/tiangolo/fastapi/blob/master/.github/actions/people/app/main.py" class="external-link" target="_blank">code source ici</a>.

Je me réserve également le droit de mettre à jour l'algorithme, les sections, les seuils, etc. (juste au cas où 🤷).
