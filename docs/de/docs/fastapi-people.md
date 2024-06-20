---
hide:
  - navigation
---

# FastAPI Leute

FastAPI hat eine großartige Gemeinschaft, die Menschen mit unterschiedlichstem Hintergrund willkommen heißt.

## Erfinder - Betreuer

Hey! 👋

Das bin ich:

{% if people %}
<div class="user-list user-list-center">
{% for user in people.maintainers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Answers: {{ user.answers }}</div><div class="count">Pull Requests: {{ user.prs }}</div></div>
{% endfor %}

</div>
{% endif %}

Ich bin der Erfinder und Betreuer von **FastAPI**. Sie können mehr darüber in [FastAPI helfen – Hilfe erhalten – Mit dem Autor vernetzen](help-fastapi.md#mit-dem-autor-vernetzen){.internal-link target=_blank} erfahren.

... Aber hier möchte ich Ihnen die Gemeinschaft vorstellen.

---

**FastAPI** erhält eine Menge Unterstützung aus der Gemeinschaft. Und ich möchte ihre Beiträge hervorheben.

Das sind die Menschen, die:

* [Anderen bei Fragen auf GitHub helfen](help-fastapi.md#anderen-bei-fragen-auf-github-helfen){.internal-link target=_blank}.
* [<abbr title='Pull Request – „Zieh-Anfrage“: Geänderten Quellcode senden, mit dem Vorschlag, ihn mit dem aktuellen Quellcode zu verschmelzen'>Pull Requests</abbr> erstellen](help-fastapi.md#einen-pull-request-erstellen){.internal-link target=_blank}.
* Pull Requests überprüfen (Review), [besonders wichtig für Übersetzungen](contributing.md#ubersetzungen){.internal-link target=_blank}.

Eine Runde Applaus für sie. 👏 🙇

## Aktivste Benutzer im letzten Monat

Hier die Benutzer, die im letzten Monat am meisten [anderen mit Fragen auf Github](help-fastapi.md#anderen-bei-fragen-auf-github-helfen){.internal-link target=_blank} geholfen haben. ☕

{% if people %}
<div class="user-list user-list-center">
{% for user in people.last_month_active %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Fragen beantwortet: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Experten

Hier die **FastAPI-Experten**. 🤓

Das sind die Benutzer, die *insgesamt* [anderen am meisten mit Fragen auf GitHub geholfen haben](help-fastapi.md#anderen-bei-fragen-auf-github-helfen){.internal-link target=_blank}.

Sie haben bewiesen, dass sie Experten sind, weil sie vielen anderen geholfen haben. ✨

{% if people %}
<div class="user-list user-list-center">
{% for user in people.experts %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Fragen beantwortet: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Top-Mitwirkende

Hier sind die **Top-Mitwirkenden**. 👷

Diese Benutzer haben [die meisten Pull Requests erstellt](help-fastapi.md#einen-pull-request-erstellen){.internal-link target=_blank} welche *<abbr title="Mergen – Zusammenführen: Unterschiedliche Versionen eines Quellcodes zusammenführen">gemerged</abbr>* wurden.

Sie haben Quellcode, Dokumentation, Übersetzungen, usw. beigesteuert. 📦

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_contributors %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Pull Requests: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

Es gibt viele andere Mitwirkende (mehr als hundert), Sie können sie alle auf der <a href="https://github.com/tiangolo/fastapi/graphs/contributors" class="external-link" target="_blank">FastAPI GitHub Contributors-Seite</a> sehen. 👷

## Top-Rezensenten

Diese Benutzer sind die **Top-Rezensenten**. 🕵️

### Rezensionen für Übersetzungen

Ich spreche nur ein paar Sprachen (und nicht sehr gut 😅). Daher bestätigen Reviewer [**Übersetzungen der Dokumentation**](contributing.md#ubersetzungen){.internal-link target=_blank}. Ohne sie gäbe es keine Dokumentation in mehreren anderen Sprachen.

---

Die **Top-Reviewer** 🕵️ haben die meisten Pull Requests von anderen überprüft und stellen die Qualität des Codes, der Dokumentation und insbesondere der **Übersetzungen** sicher.

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_reviewers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Reviews: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Sponsoren

Dies sind die **Sponsoren**. 😎

Sie unterstützen meine Arbeit an **FastAPI** (und andere), hauptsächlich durch <a href="https://github.com/sponsors/tiangolo" class="external-link" target="_blank">GitHub-Sponsoren</a>.

### Gold Sponsoren

{% if sponsors %}
{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}"></a>
{% endfor %}
{% endif %}

### Silber Sponsoren

{% if sponsors %}
{% for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}"></a>
{% endfor %}
{% endif %}

{% if people %}
{% if people.sponsors_50 %}

### Bronze Sponsoren

<div class="user-list user-list-center">
{% for user in people.sponsors_50 %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a></div>
{% endfor %}

</div>

{% endif %}
{% endif %}

### Individuelle Sponsoren

{% if people %}
<div class="user-list user-list-center">
{% for user in people.sponsors %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a></div>
{% endfor %}

</div>
{% endif %}

## Über diese Daten - technische Details

Der Hauptzweck dieser Seite ist es zu zeigen, wie die Gemeinschaft anderen hilft.

Das beinhaltet auch Hilfe, die normalerweise weniger sichtbar und in vielen Fällen mühsamer ist, wie, anderen bei Problemen zu helfen und Pull Requests mit Übersetzungen zu überprüfen.

Diese Daten werden jeden Monat berechnet, Sie können den <a href="https://github.com/tiangolo/fastapi/blob/master/.github/actions/people/app/main.py" class="external-link" target="_blank">Quellcode hier lesen</a>.

Hier weise ich auch auf Beiträge von Sponsoren hin.

Ich behalte mir auch das Recht vor, den Algorithmus, die Abschnitte, die Schwellenwerte usw. zu aktualisieren (nur für den Fall 🤷).
