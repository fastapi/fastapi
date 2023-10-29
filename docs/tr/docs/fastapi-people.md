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

Ben **FastAPI**'nin yazarı ve geliştiricisiyim. Bununla ilgili daha fazla bilgiyi şurada okuyabilirsiniz:
 [FastAPI yardım - yardım al - Yazar ile iletişime geç](help-fastapi.md#connect-with-the-author){.internal-link target=_blank}.

... Burada size harika FastAPI topluluğunu göstermek istiyorum.

---

**FastAPI**, topluluğundan çok destek alıyor. Ben de onların katkısını vurgulamak istiyorum.

O mükemmel insanlar:

* [GitHubdaki sorunları (issues) çözmelerinde diğerlerine yardım ediyor](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank}.
* [Pull Requests oluşturuyor](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}.
* Pull Requests'leri gözden geçiriyorlar, [özellikle çeviriler için bu çok önemli](contributing.md#translations){.internal-link target=_blank}.

Onları bir alkışlayalım. 👏 🙇

## Geçen Ayın En Aktif Kullanıcıları

Bunlar geçen ay boyunca [GitHub'da başkalarına en çok yardımcı olan](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank} kullanıcılar. ☕

{% if people %}
<div class="user-list user-list-center">
{% for user in people.last_month_active %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Issues replied: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Uzmanlar

İşte **FastAPI Uzmanları**. 🤓

Uzmanlarımız ise *tüm zamanlar boyunca* [GitHub'da diğerlerine sorunlarında en çok yardımcı olan](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank} insanlar.

Bir çok kullanıcıya yardım ederek uzman olduklarını kanıtladılar! ✨

{% if people %}
<div class="user-list user-list-center">
{% for user in people.experts %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Issues replied: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## En Fazla Katkıda Bulunanlar

Şimdi ise sıra **en fazla katkıda bulunanlar**da. 👷

Bu kullanıcılar en çok [kaynak koduyla birleştirilen Pull Request'lere](help-fastapi.md#create-a-pull-request){.internal-link target=_blank} sahip!

Kaynak koduna, dökümantasyona, çevirilere ve bir sürü şeye katkıda bulundular. 📦

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_contributors %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Pull Requests: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

Bunlar dışında katkıda bulunan bir sürü insan var (yüzden fazla), hepsini <a href="https://github.com/tiangolo/fastapi/graphs/contributors" class="external-link" target="_blank">FastAPI GitHub Katkıda Bulunanlar</a> sayfasında görebilirsin. 👷

## En Fazla Değerlendirme Yapanlar

İşte **en çok değerlendirme yapanlar**. 🕵️

### Çeviri Değerlendirmeleri

Yalnızca birkaç dil konuşabiliyorum (ve çok da iyi değilim 😅). Bu yüzden değerlendirme yapanların da döküman çevirilerini [**onaylama yetkisi**](contributing.md#translations){.internal-link target=_blank} var. Onlar olmasaydı çeşitli dillerde dökümantasyon da olmazdı.

---

**En fazla değerlendirme yapanlar** 🕵️ kodun, dökümantasyonun ve özellikle **çevirilerin** Pull Request'lerini inceleyerek kalitesinden emin oldular.

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_reviewers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Reviews: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Sponsorlar

işte **Sponsorlarımız**. 😎

Çoğunlukla <a href="https://github.com/sponsors/tiangolo" class="external-link" target="_blank">GitHub Sponsorları</a> aracılığıyla olmak üzere, **FastAPI** ve diğer projelerde çalışmamı destekliyorlar.

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

Özellikle normalde daha az görünür olan ve çoğu durumda daha zahmetli olan, diğerlerine sorunlar konusunda yardımcı olmak ve Pull Request'leri gözden geçirmek gibi çabalar dahil.

Veriler ayda bir hesaplanır, <a href="https://github.com/tiangolo/fastapi/blob/master/.github/actions/people/app/main.py" class="external-link" target="_blank">kaynak kodu buradan</a> okuyabilirsin.

Burada sponsorların katkılarını da vurguluyorum.

Ayrıca algoritmayı, bölümleri, eşikleri vb. güncelleme hakkımı da saklı tutuyorum (her ihtimale karşı 🤷).
