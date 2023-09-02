# Ludzie FastAPI

FastAPI posiada wspaniałą społeczność, która jest otwarta dla ludzi z każdego środowiska.

## Twórca - Opienik

Cześć! 👋

To ja:

{% if people %}
<div class="user-list user-list-center">
{% for user in people.maintainers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Liczba odpowiedzi: {{ user.answers }}</div><div class="count">Pull Requesty: {{ user.prs }}</div></div>
{% endfor %}

</div>
{% endif %}

Jestem twórcą i opiekunem **FastAPI**. Możesz przeczytać więcej na ten temat w [Pomoc FastAPI - Uzyskaj pomoc - Skontaktuj się z autorem](help-fastapi.md#connect-with-the-author){.internal-link target=_blank}.

...Ale tutaj chcę pokazać Ci społeczność.

---

**FastAPI** otrzymuje wiele wsparcia od społeczności. Chciałbym podkreślić ich wkład.

To są ludzie, którzy:

* [Pomagają innym z pytaniami na GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank}.
* [Tworzą Pull Requesty](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}.
* Oceniają Pull Requesty, [to szczególnie ważne dla tłumaczeń](contributing.md#translations){.internal-link target=_blank}.

Proszę o brawa dla nich. 👏 🙇

## Najaktywniejsi użytkownicy w zeszłym miesiącu

Oto niektórzy użytkownicy, którzy [pomagali innym w największej liczbie pytań na GitHubie](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank} podczas ostatniego miesiąca. ☕

{% if people %}
<div class="user-list user-list-center">
{% for user in people.last_month_active %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Udzielonych odpowiedzi: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Eksperci

Oto **eksperci FastAPI**. 🤓

To użytkownicy, którzy [pomogli innym z największa liczbą pytań na GitHubie](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank} od *samego początku*.

Poprzez pomoc wielu innym, udowodnili, że są ekspertami. ✨

{% if people %}
<div class="user-list user-list-center">
{% for user in people.experts %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Udzielonych odpowiedzi: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Najlepsi Kontrybutorzy

Oto **Najlepsi Kontrybutorzy**. 👷

Ci użytkownicy [stworzyli najwięcej Pull Requestów](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}, które zostały *wcalone*.

Współtworzyli kod źródłowy, dokumentację, tłumaczenia itp. 📦

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_contributors %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Pull Requesty: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

Jest wielu więcej kontrybutorów (ponad setka), możesz zobaczyć ich wszystkich na stronie <a href="https://github.com/tiangolo/fastapi/graphs/contributors" class="external-link" target="_blank">Kontrybutorzy FastAPI na GitHub</a>. 👷

## Najlepsi Oceniajacy

Ci uzytkownicy są **Najlepszymi oceniającymi**. 🕵️

### Oceny Tłumaczeń

Ja mówię tylko kilkoma językami (i to niezbyt dobrze 😅). Zatem oceniający są tymi, którzy mają [**moc zatwierdzania tłumaczeń**](contributing.md#translations){.internal-link target=_blank} dokumentacji. Bez nich nie byłoby dokumentacji w kilku innych językach.

---

**Najlepsi Oceniający** 🕵️ przejrzeli więcej Pull Requestów, niż inni, zapewniając jakość kodu, dokumentacji, a zwłaszcza **tłumaczeń**.

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_reviewers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Liczba ocen: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Sponsorzy

Oto **Sponsorzy**. 😎

Wspierają moją pracę nad **FastAPI** (i innymi), głównie poprzez <a href="https://github.com/sponsors/tiangolo" class="external-link" target="_blank">GitHub Sponsors</a>.

{% if sponsors %}

{% if sponsors.gold %}

### Złoci Sponsorzy

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.silver %}

### Srebrni Sponsorzy

{% for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.bronze %}

### Brązowi Sponsorzy

{% for sponsor in sponsors.bronze -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% endif %}

### Indywidualni Sponsorzy

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

## Techniczne szczegóły danych

Głównym celem tej strony jest podkreślenie wysiłku społeczności w pomaganiu innym.

Szczególnie włączając wysiłki, które są zwykle mniej widoczne, a w wielu przypadkach bardziej żmudne, tak jak pomaganie innym z pytaniami i ocenianie Pull Requestów z tłumaczeniami.

Dane są obliczane każdego miesiąca, możesz przeczytać <a href="https://github.com/tiangolo/fastapi/blob/master/.github/actions/people/app/main.py" class="external-link" target="_blank">kod źródłowy tutaj</a>.

Tutaj również podkreślam wkład od sponsorów.

Zastrzegam sobie prawo do aktualizacji algorytmu, sekcji, progów itp. (na wszelki wypadek 🤷).
