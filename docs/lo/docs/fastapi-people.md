# FastAPI ຜູ້ຄົນ

FastAPI ມີຊຸມຊົນທີນ່າຕື່ນຕາຕື່ນໃຈທີຍິນດີຕ້ອນຮັບຜູ້ຄົນຈາກທຸກຂົງເຂດ.

## ຜູ້ສ້າງ - ຜູ້ເບິ່ງແຍງ

ສະບາຍດີ! 👋

ນີ້ແມ່ນຂ້ອຍ:

{% if people %}
<div class="user-list user-list-center">
{% for user in people.maintainers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Answers: {{ user.answers }}</div><div class="count">Pull Requests: {{ user.prs }}</div></div>
{% endfor %}

</div>
{% endif %}

ຂ້ອຍແມ່ນຜູ້ສ້າງ ແລະ ຜູ້ເບິ່ງແຍງ **FastAPI**. ທ່ານສາມາດອ່ານຂໍ້ມູນເພີ່ມເຕີມໄດ້ທີ [ຊ່ວຍເຫຼືອ FastAPI - ຊ່ວຍເຫຼືອ - ຕິດຕໍ່ກັບຜູ້ຂຽນ](help-fastapi.md#connect-with-the-author){.internal-link target=_blank}.

...ແຕ່ ຂ້ອຍຢາກໃຫ້ທ່ານເຫັນຊຸມຊົນ.

---

**FastAPI** ຮັບການສະໜັບສະໜູນຫຼາຍຈາກຊຸມຊົນ. ແລະ ຂ້ອຍຕ້ອງການໃຫ້ເຫັນເຖິງຄວາມສຳຄັນຂອງການມີສ່ວນຮ່ວມຂອງພວກເຂົາ.

ນີ້ແມ່ນບັນດາຜູ້ຄົນທີ:

* [ຊ່ວຍເຫຼືອຜູ້ອື່ນດ້ວຍການຕັ້ງຄຳຖາມໃນ github](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank}.
* [ສ້າງ Pull Requests](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}.
* ກວດ Pull Requests, [ໂດຍສະເພາະແມ່ນການແປ](contributing.md#translations){.internal-link target=_blank}.

ສຽງຕົບມືໃຫ້ພວກເຂົາ. 👏 🙇

## ບັນດາຜູ້ໃຊ້ທີມີການເຄື່ອນໄຫວຫຼາຍສຸດໃນເດືອນແລ້ວນີ້

These are the users that have been [helping others the most with questions in GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank} during the last month. ☕

{% if people %}
<div class="user-list user-list-center">
{% for user in people.last_month_active %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Questions replied: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## ຜູ້ຊ່ຽວຊານ

ນີ້ແມ່ນ **ຜູ້ຊ່ຽວຊານ FastAPI**. 🤓

These are the users that have [helped others the most with questions in GitHub](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank} through *all time*.

They have proven to be experts by helping many others. ✨

{% if people %}
<div class="user-list user-list-center">
{% for user in people.experts %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Questions replied: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## ຜູ້ມີສ່ວນຮ່ວມສູງສຸດ

ນີ້ແມ່ນບັນດາ **ຜູ້ມີສ່ວນຮ່ວມສູງສຸດ**. 👷

ບັນດາຜູ້ຄົນເຫຼົ່ານີ້ໄດ້ [ສ້າງ Pull Requests](help-fastapi.md#create-a-pull-request){.internal-link target=_blank} ທີໄດ້ຖືກ *ລວມເຂົ້າກັນ*.

ພວກເຂົາໄດ້ມີສ່ວນຮ່ວມໃນ source code, ເອກະສານ, ການແປ ແລະ ອື່ນໆ. 📦

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_contributors %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Pull Requests: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

There are many other contributors (more than a hundred), you can see them all in the <a href="https://github.com/tiangolo/fastapi/graphs/contributors" class="external-link" target="_blank">FastAPI GitHub Contributors page</a>. 👷

## ຜູ້ກວດສູງສຸດ

ນີ້ແມ່ນບັນດາ  **ຜູ້ກວດສູງສຸດ**. 🕵️

### ກວດການແປ

ຂ້ອຍເວົ້າໄດ້ບໍ່ເທົ່າໃດພາສາ (ລະກະບໍ່ຄ່ອຍເກັ່ງອີກ 😅). ດັ່ງນັ້ນຜູ້ກວດຈິງເປັນຜູ້ໜຶ່ງ [**ທີມີອຳນາດໃນການອະນຸມັດ**](contributing.md#translations){.internal-link target=_blank}ການແປເອກະສານ. ຫາກບໍ່ມີພວກເຂົາ, ກໍຈະບໍ່ມີເອກະສານໃນພາສາອື່ນໆ ອີກຫຼາຍພາສາ.

---

The **Top Reviewers** 🕵️ have reviewed the most Pull Requests from others, ensuring the quality of the code, documentation, and especially, the **translations**.

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_reviewers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Reviews: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## ຜູ້ສະໜັບສະໜູນ

ນີ້ແມ່ນບັນດາ **ຜູ້ສະໜັບສະໜູນ**. 😎

They are supporting my work with **FastAPI** (and others), mainly through <a href="https://github.com/sponsors/tiangolo" class="external-link" target="_blank">GitHub Sponsors</a>.

{% if sponsors %}

{% if sponsors.gold %}

### ຜູ້ສະໜັບສະໜູນຊັ້ນຄໍາ

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.silver %}

### ຜູ້ສະໜັບສະໜູນຊັ້ນເງິນ

{% for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.bronze %}

### ຜູ້ສະໜັບສະໜູນຊັ້ນທອງ

{% for sponsor in sponsors.bronze -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% endif %}

### ຜູ້ສະໜັບສະໜູນລາຍບຸກຄົນ

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

## ກ່ຽວກັບຂໍ້ມູນ - ຂໍ້ມູນທາງເທັກນິກ

The main intention of this page is to highlight the effort of the community to help others.

Especially including efforts that are normally less visible, and in many cases more arduous, like helping others with questions and reviewing Pull Requests with translations.

The data is calculated each month, you can read the <a href="https://github.com/tiangolo/fastapi/blob/master/.github/actions/people/app/main.py" class="external-link" target="_blank">source code here</a>.

Here I'm also highlighting contributions from sponsors.

I also reserve the right to update the algorithm, sections, thresholds, etc (just in case 🤷).
