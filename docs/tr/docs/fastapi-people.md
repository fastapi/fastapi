# FastAPI Topluluğu

FastAPI, her kökenden insanı ağırlayan harika bir topluluğa sahip.

## Yazan - Geliştiren

Hey! 👋

İşte bu benim:

{% if people %}
<div class="user-list user-list-center">
{% for user in people.maintainers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Answers: {{ user.answers }}</div><div class="count">Pull Requests: {{ user.prs }}</div></div>
{% endfor %}

</div>
{% endif %}

Ben **FastAPI** 'nin yazarı ve geliştiricisiyim. Bununla ilgili daha fazla bilgiyi şurada okuyabilirsiniz:
 [FastAPI yardım - yardım al - Yazar ile iletişime geç](help-fastapi.md#connect-with-the-author){.internal-link target=_blank}.

... Burada size harika FastAPI topluluğunu göstermek istiyorum.

---

**FastAPI** topluluğundan destek alıyor. Ve katkıda bulunanları vurgulamak istiyorum.

İşte o mükemmel insanlar:

* [GitHubdaki sorunları (issues) çözmelerinde diğerlerine yardım et](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank}.
* [Pull Requests oluşturun](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}.
* Pull Requests 'leri gözden geçirin, [özelliklede çevirileri](contributing.md#translations){.internal-link target=_blank}.

Onlara bir alkış. 👏 🙇

## Geçen ayın en aktif kullanıcıları

Bunlar geçen ay boyunca [GitHub' da başkalarına sorunlarında (issues) en çok yardımcı olan ](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank} kullanıcılar  ☕

{% if people %}
<div class="user-list user-list-center">
{% for user in people.last_month_active %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Issues replied: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Uzmanlar

İşte **FastAPI Uzmanları**. 🤓

Bunlar *tüm zamanlar boyunca* [GitHub' da başkalarına sorunlarında (issues) en çok yardımcı olan](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank} kullanıcılar.

Başkalarına yardım ederek uzman olduklarını kanıtladılar. ✨

{% if people %}
<div class="user-list user-list-center">
{% for user in people.experts %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Issues replied: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## En fazla katkıda bulunanlar

işte **En fazla katkıda bulunanlar**. 👷

Bu kullanıcılar en çok [Pull Requests oluşturan](help-fastapi.md#create-a-pull-request){.internal-link target=_blank} ve onu kaynak koduna *birleştirenler*.

Kaynak koduna, belgelere, çevirilere vb. katkıda bulundular. 📦

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_contributors %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Pull Requests: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

Çok fazla katkıda bulunan var (binden fazla), hepsini şurda görebilirsin: <a href="https://github.com/tiangolo/fastapi/graphs/contributors" class="external-link" target="_blank">FastAPI GitHub Katkıda Bulunanlar</a>. 👷

## En fazla inceleme yapanlar

İşte **En fazla inceleme yapanlar**. 🕵️

### Çeviri için İncelemeler

Yalnızca birkaç dil konuşabiliyorum (ve çok da iyi değilim 😅). Bu yüzden döküman çevirilerini [**onaylama yetkisi**](contributing.md#translations){.internal-link target=_blank} siz inceleyenlere aittir. Sizler olmadan diğer birkaç dilde dokümantasyon olmazdı.

---

**En fazla inceleme yapanlar** 🕵️ kodun, belgelerin ve özellikle **çevirilerin** kalitesini sağlamak için diğerlerinden daha fazla pull requests incelemiştir.

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_reviewers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Reviews: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Sponsorlar

işte **Sponsorlarımız**. 😎

**FastAPI** ve diğer projelerde çalışmamı destekliyorlar, özellikle de <a href="https://github.com/sponsors/tiangolo" class="external-link" target="_blank">GitHub Sponsorları</a>.

### Altın Sponsorlar

{% if sponsors %}
{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

### Gümüş Sponsorlar

{% if sponsors %}
{% for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

### Bronz Sponsorlar

{% if sponsors %}
{% for sponsor in sponsors.bronze -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

### Bireysel Sponsorlar

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

## Veriler hakkında - Teknik detaylar

Bu sayfanın temel amacı, topluluğun başkalarına yardım etme çabasını vurgulamaktır.

Özellikle normalde daha az görünür olan ve çoğu durumda daha zahmetli olan, diğerlerine sorunlar konusunda yardımcı olmak ve pull requests'leri gözden geçirmek gibi çabalar dahil.

Veriler ayda bir hesaplanır, işte kaynak kodu okuyabilirsin :<a href="https://github.com/tiangolo/fastapi/blob/master/.github/actions/people/app/main.py" class="external-link" target="_blank">source code here</a>.

Burada sponsorların katkılarını da tekrardan vurgulamak isterim.

Ayrıca algoritmayı, bölümleri, eşikleri vb. güncelleme hakkımı da saklı tutarım (her ihtimale karşı 🤷).
