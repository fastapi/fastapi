# FastAPI Суполка

FastAPI мае дзіўную суполку, якая вітае людзей з розным вопытам і ведамі.

## Стваральнік - Суправаджальнік

Хэй! 👋

Гэта я:

{% if people %}
<div class="user-list user-list-center">
{% for user in people.maintainers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Answers: {{ user.answers }}</div><div class="count">Pull Requests: {{ user.prs }}</div></div>
{% endfor %}

</div>
{% endif %}

Я стварыў і суправаджаю **FastAPI**. Даведацца пра мяне больш магчыма тут [Дапамагчы FastAPI - Атрымаць Дапамогу - Звязацца з аўтарам](help-fastapi.md#connect-with-the-author){.internal-link target=_blank}.

...Але тут я хачу пазнаёмиць Вас з нашай суполкай.

---

**FastAPI** атрымлівае вялікую падтрымку з боку супольнасці. І я хачу адзначыць іх уклад.

Вось гэтыя людзі, якія:

* [Дапамагяюць адказамі на пытанні на GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank}.
* [Ствараюць пул-рэквесты](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}.
* Рэцэнзіруюць пул-рэквесты, [што асабліва важна для перакладаў](contributing.md#translations){.internal-link target=_blank}.

Апладысменты ім. 👏 🙇

## Самыя актыўныя карыстальнікі за мінулы месяц

Гэта карыстальнікі, [якія больш за усіх дапамагалі адказамі на пытанні на GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank} на працягу апошняга месяца. ☕

{% if people %}
<div class="user-list user-list-center">
{% for user in people.last_month_active %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Questions replied: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Эксперты

Тут адзначаны **Эксперты FastAPI**. 🤓

Гэта карыстальнікі, [якія больш за усіх дапамагалі адказамі на пытанні на GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank} за *ўвесь час*.

Яны зарэкамендавалі сябе як эксперты, дапамагаючы многім іншым. ✨

{% if people %}
<div class="user-list user-list-center">
{% for user in people.experts %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Questions replied: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Рэйтынг удзельнікаў, якія ўнеслі ўклад у код

Тут прадстаўлен **рэйтынг удзельнікаў, якія ўнеслі ўклад у код**. 👷

Гэтыя карыстальнікі [стварылі найбольшую колькасць пул-рэквестаў](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}, *уключаных у асноўны код*.

Яны стваралі зыходны код, дакументацыю, пераклады і г.д. 📦

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_contributors %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Pull Requests: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

Ёсць шмат іншых удзельнікаў (больш за сотню), вы можаце ўбачыць іх усіх на старонцы <a href="https://github.com/tiangolo/fastapi/graphs/contributors" class="external-link" target="_blank">FastAPI GitHub Contributors page</a>. 👷

## Рэйтынг рэўюераў

Тут прадстаўлены **Рэйтынг рэўюераў**. 🕵️

### Рэцэнзіі на пераклады

Я размаўляю толькі на некалькіх мовах (і ня вельмі добра 😅). Такім чынам, рэцэнзенты - гэта тыя людзі, якія маюць [**паўнамоцтвы зацвярджаць пераклады**](contributing.md#translations){.internal-link target=_blank} дакументацыі. Без іх не існавала б дакументацыя на розных мовах.

---

Гэта **Лепшыя рэцэнзенты** 🕵️, якія прагледзелі большасць пул-рэквестаў ад іншых удзельнікаў, гарантуючы якасць кода, дакументацыі і асабліва **перакладаў**.

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_reviewers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Reviews: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Спонсары

Тут прадстаўлены **Sponsors**. 😎

Яны падтрымліваюць маю працу над FastAPI (і іншымі праектамі), у асноўным праз <a href="https://github.com/sponsors/tiangolo" class="external-link" target="_blank">GitHub Sponsors</a>.

{% if sponsors %}

{% if sponsors.gold %}

### Залатыя Спонсары

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.silver %}

### Срэбныя Спонсары

{% for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.bronze %}

### Бронзавыя Спонсары

{% for sponsor in sponsors.bronze -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% endif %}

### Індывідуальныя Спонсары

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

## Аб дадзеных - тэхнічныя дэталі

Асноўная мэта гэтай старонкі - падкрэсліць намаганні супольнасці дапамагчы іншым.

Асабліва намаганні, якія звычайна менш прыкметныя і ў многіх выпадках больш цяжкія, напрыклад, дапамога іншым з вырашэннем праблем і прагляд пул-рэквестаў з перакладамі.

Дадзеныя разлічваюцца штомесяц, вы можате ўбачыць <a href="https://github.com/tiangolo/fastapi/blob/master/.github/actions/people/app/main.py" class="external-link" target="_blank">зыходны код тут</a>.

Тут я таксама вылучаю ўзносы спонсараў.

Я таксама пакідаю за сабой права абнаўляць алгарытм, раздзелы, парогавыя значэнні і г.д. (на ўсялякі выпадак 🤷).
