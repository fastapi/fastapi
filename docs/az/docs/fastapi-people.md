---
hide:
  - navigation
---

# FastAPI İnsanlar

FastAPI-ın bütün mənşəli insanları qəbul edən heyrətamiz icması var.



## Yaradıcı - İcraçı

Salam! 👋

Bu mənəm:

{% if people %}
<div class="user-list user-list-center">
{% for user in people.maintainers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Cavablar: {{ user.answers }}</div><div class="count">Pull Request-lər: {{ user.prs }}</div></div>
{% endfor %}

</div>
{% endif %}

Mən **FastAPI**-ın yaradıcısı və icraçısıyam. Əlavə məlumat almaq üçün [Yardım FastAPI - Yardım alın - Müəlliflə əlaqə qurun](help-fastapi.md#connect-with-the-author){.internal-link target=_blank} səhifəsinə baxa bilərsiniz.

...Burada isə sizə icmanı göstərmək istəyirəm.

---

**FastAPI** icmadan çoxlu dəstək alır və mən onların əməyini vurğulamaq istəyirəm.

Bu insanlar:

* [GitHub-da başqalarının suallarına kömək edirlər](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank}.
* [Pull Request-lər yaradırlar](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}.
* Pull Request-ləri ([xüsusilə tərcümələr üçün vacib olan](contributing.md#translations){.internal-link target=_blank}.) nəzərdən keçirirlər.

Bu insanlara təşəkkür edirəm. 👏 🙇

## Keçən ayın ən fəal istifadəçiləri

Bu istifadəçilər keçən ay [GitHub-da başqalarının suallarına](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank} ən çox kömək edənlərdir. ☕

{% if people %}
<div class="user-list user-list-center">
{% for user in people.last_month_experts[:10] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Cavablandırılmış suallar: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Mütəxəssislər

Burada **FastAPI Mütəxəssisləri** var. 🤓

Bu istifadəçilər indiyə qədər [GitHub-da başqalarının suallarına](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank} ən çox kömək edənlərdir.

Onlar bir çox insanlara kömək edərək mütəxəssis olduqlarını sübut ediblər. ✨

{% if people %}
<div class="user-list user-list-center">
{% for user in people.experts[:50] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Cavablandırılmış suallar: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Ən yaxşı əməkdaşlar

Burada **Ən yaxşı əməkdaşlar** var. 👷

Bu istifadəçilərin ən çox *birləşdirilmiş* [Pull Request-ləri var](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}.

Onlar mənbə kodu, sənədləmə, tərcümələr və s. barədə əmək göstərmişlər. 📦

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_contributors[:50] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Pull Request-lər: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

Bundan başqa bir neçə (yüzdən çox) əməkdaş var ki, onları <a href="https://github.com/tiangolo/fastapi/graphs/contributors" class="external-link" target="_blank">FastAPI GitHub Əməkdaşlar səhifəsində</a> görə bilərsiniz. 👷

## Ən çox rəy verənlər

Bu istifadəçilər **ən çox rəy verənlər**dir.

### Tərcümələr üçün rəylər

Mən yalnız bir neçə dildə danışıram (və çox da yaxşı deyil 😅). Bu səbəbdən, rəy verənlər sənədlərin [**tərcümələrini təsdiqləmək üçün gücə malik olanlar**](contributing.md#translations){.internal-link target=_blank}dır. Onlar olmadan, bir çox dilə tərcümə olunmuş sənədlər olmazdı.

---

Başqalarının Pull Request-lərinə **Ən çox rəy verənlər** 🕵️ kodun, sənədlərin və xüsusilə də **tərcümələrin** keyfiyyətini təmin edirlər.

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_translations_reviewers[:50] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Rəylər: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Sponsorlar

Bunlar **Sponsorlar**dır. 😎

Onlar mənim **FastAPI** (və digər) işlərimi əsasən <a href="https://github.com/sponsors/tiangolo" class="external-link" target="_blank">GitHub Sponsorlar</a> vasitəsilə dəstəkləyirlər.

{% if sponsors %}

{% if sponsors.gold %}

### Qızıl Sponsorlar

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.silver %}

### Gümüş Sponsorlar

{% for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.bronze %}

### Bürünc Sponsorlar

{% for sponsor in sponsors.bronze -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% endif %}

### Fərdi Sponsorlar

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

## Məlumatlar haqqında - texniki detallar

Bu səhifənin əsas məqsədi, icmanın başqalarına kömək etmək üçün göstərdiyi əməyi vurğulamaqdır.

Xüsusilə də normalda daha az görünən və bir çox hallarda daha çətin olan, başqalarının suallarına kömək etmək və tərcümələrlə bağlı Pull Request-lərə rəy vermək kimi səy göstərmək.

Bu səhifənin məlumatları hər ay hesablanır və siz <a href="https://github.com/tiangolo/fastapi/blob/master/.github/actions/people/app/main.py" class="external-link" target="_blank">buradan mənbə kodunu</a> oxuya bilərsiniz.

Burada sponsorların əməyini də vurğulamaq istəyirəm.

Mən həmçinin alqoritmi, bölmələri, eşikləri və s. yeniləmək hüququnu da qoruyuram (hər ehtimala qarşı 🤷).
