---
hide:
  - navigation
---

# FastAPI کے لوگ

FastAPI کی ایک حیرت انگیز کمیونٹی ہے جو ہر پس منظر سے لوگوں کا خیرمقدم کرتی ہے۔

## بانی

ارے! 👋

یہ میں ہوں:

<div class="user-list user-list-center">
{% for user in people.maintainers %}

<div class="user"><a href="{{ contributors.tiangolo.url }}"><div class="avatar-wrapper"><img src="{{ contributors.tiangolo.avatarUrl }}"/></div><div class="title">@{{ contributors.tiangolo.login }}</div></a> <div class="count">Answers: {{ user.answers }}</div><div class="count">Pull Requests: {{ contributors.tiangolo.count }}</div></div>
{% endfor %}

</div>

میں **FastAPI** کا بانی ہوں۔ آپ اس کے بارے میں مزید [FastAPI کی مدد کریں - مدد حاصل کریں - مصنف سے جڑیں](help-fastapi.md#connect-with-the-author) میں پڑھ سکتے ہیں۔

...لیکن یہاں میں آپ کو کمیونٹی دکھانا چاہتا ہوں۔

---

**FastAPI** کو کمیونٹی سے بہت زیادہ حمایت ملتی ہے۔ اور میں ان کے تعاون کو نمایاں کرنا چاہتا ہوں۔

یہ وہ لوگ ہیں جو:

* [GitHub میں سوالات کے ساتھ دوسروں کی مدد کرتے ہیں](help-fastapi.md#help-others-with-questions-in-github)۔
* [Pull Requests بناتے ہیں](help-fastapi.md#create-a-pull-request)۔
* Pull Requests کا Review کرتے ہیں، [خاص طور پر تراجم کے لیے اہم](contributing.md#translations)۔
* [Repository منظم](management-tasks.md) کرنے میں مدد کرتے ہیں (ٹیم ممبران)۔

یہ سب کام repository کو برقرار رکھنے میں مدد کرتے ہیں۔

ان کے لیے تالیاں۔ 👏 🙇

## ٹیم

یہ موجودہ ٹیم ممبران کی فہرست ہے۔ 😎

ان کی شمولیت اور اجازتوں کی مختلف سطحیں ہیں، وہ [repository management tasks](./management-tasks.md) انجام دے سکتے ہیں اور مل کر ہم [FastAPI repository کو منظم کرتے ہیں](./management.md)۔

<div class="user-list user-list-center">

{% for user in members["members"] %}

<div class="user"><a href="{{ user.url }}"><div class="avatar-wrapper"><img src="{{ user.avatar_url }}"/></div><div class="title">@{{ user.login }}</div></a></div>

{% endfor %}

</div>

حالانکہ ٹیم ممبران کے پاس خصوصی کام انجام دینے کی اجازتیں ہیں، [FastAPI کو برقرار رکھنے میں دوسروں کی ہر مدد](./help-fastapi.md#help-maintain-fastapi) کی بہت قدر کی جاتی ہے! 🙇‍♂️

## FastAPI Experts

یہ وہ صارفین ہیں جو [GitHub میں سوالات کے ساتھ سب سے زیادہ دوسروں کی مدد](help-fastapi.md#help-others-with-questions-in-github) کرتے رہے ہیں۔ 🙇

انہوں نے بہت سے دوسروں کی مدد کرکے ثابت کیا ہے کہ وہ **FastAPI Experts** ہیں۔ ✨

/// tip | مشورہ

آپ بھی سرکاری FastAPI Expert بن سکتے ہیں!

بس [GitHub میں سوالات کے ساتھ دوسروں کی مدد کریں](help-fastapi.md#help-others-with-questions-in-github)۔ 🤓

///

آپ **FastAPI Experts** یہاں دیکھ سکتے ہیں:

* [پچھلا مہینہ](#fastapi-experts-last-month) 🤓
* [3 مہینے](#fastapi-experts-3-months) 😎
* [6 مہینے](#fastapi-experts-6-months) 🧐
* [1 سال](#fastapi-experts-1-year) 🧑‍🔬
* [**ہمیشہ**](#fastapi-experts-all-time) 🧙

### FastAPI Experts - پچھلا مہینہ

یہ وہ صارفین ہیں جو پچھلے مہینے [GitHub میں سوالات کے ساتھ سب سے زیادہ دوسروں کی مدد](help-fastapi.md#help-others-with-questions-in-github) کرتے رہے ہیں۔ 🤓

<div class="user-list user-list-center">

{% for user in people.last_month_experts[:10] %}

{% if user.login not in skip_users %}

<div class="user"><a href="{{ user.url }}"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Questions replied: {{ user.count }}</div></div>

{% endif %}

{% endfor %}

</div>

### FastAPI Experts - 3 مہینے

یہ وہ صارفین ہیں جو پچھلے 3 مہینوں میں [GitHub میں سوالات کے ساتھ سب سے زیادہ دوسروں کی مدد](help-fastapi.md#help-others-with-questions-in-github) کرتے رہے ہیں۔ 😎

<div class="user-list user-list-center">

{% for user in people.three_months_experts[:10] %}

{% if user.login not in skip_users %}

<div class="user"><a href="{{ user.url }}"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Questions replied: {{ user.count }}</div></div>

{% endif %}

{% endfor %}

</div>

### FastAPI Experts - 6 مہینے

یہ وہ صارفین ہیں جو پچھلے 6 مہینوں میں [GitHub میں سوالات کے ساتھ سب سے زیادہ دوسروں کی مدد](help-fastapi.md#help-others-with-questions-in-github) کرتے رہے ہیں۔ 🧐

<div class="user-list user-list-center">

{% for user in people.six_months_experts[:10] %}

{% if user.login not in skip_users %}

<div class="user"><a href="{{ user.url }}"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Questions replied: {{ user.count }}</div></div>

{% endif %}

{% endfor %}

</div>

### FastAPI Experts - 1 سال

یہ وہ صارفین ہیں جو پچھلے سال [GitHub میں سوالات کے ساتھ سب سے زیادہ دوسروں کی مدد](help-fastapi.md#help-others-with-questions-in-github) کرتے رہے ہیں۔ 🧑‍🔬

<div class="user-list user-list-center">

{% for user in people.one_year_experts[:20] %}

{% if user.login not in skip_users %}

<div class="user"><a href="{{ user.url }}"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Questions replied: {{ user.count }}</div></div>

{% endif %}

{% endfor %}

</div>

### FastAPI Experts - ہمیشہ

یہ ہیں ہمیشہ کے **FastAPI Experts**۔ 🤓🤯

یہ وہ صارفین ہیں جنہوں نے *ہمیشہ سے* [GitHub میں سوالات کے ساتھ سب سے زیادہ دوسروں کی مدد](help-fastapi.md#help-others-with-questions-in-github) کی ہے۔ 🧙

<div class="user-list user-list-center">

{% for user in people.experts[:50] %}

{% if user.login not in skip_users %}

<div class="user"><a href="{{ user.url }}"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Questions replied: {{ user.count }}</div></div>

{% endif %}

{% endfor %}

</div>

## اعلیٰ شراکت دار

یہ ہیں **اعلیٰ شراکت دار**۔ 👷

ان صارفین نے سب سے زیادہ [Pull Requests بنائی ہیں](help-fastapi.md#create-a-pull-request) جو *merge* ہو چکی ہیں۔

انہوں نے source code، documentation وغیرہ میں تعاون کیا ہے۔ 📦

<div class="user-list user-list-center">

{% for user in (contributors.values() | list)[:50] %}

{% if user.login not in skip_users %}

<div class="user"><a href="{{ user.url }}"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Pull Requests: {{ user.count }}</div></div>

{% endif %}

{% endfor %}

</div>

سینکڑوں دوسرے شراکت دار بھی ہیں، آپ انہیں [FastAPI GitHub Contributors page](https://github.com/fastapi/fastapi/graphs/contributors) پر دیکھ سکتے ہیں۔ 👷

## اعلیٰ ترجمہ جائزہ کار

یہ صارفین **اعلیٰ ترجمہ جائزہ کار** ہیں۔ 🕵️

ترجمہ جائزہ کاروں کے پاس documentation کے [**تراجم کی منظوری**](contributing.md#translations) دینے کا اختیار ہے۔ ان کے بغیر، کئی دوسری زبانوں میں documentation نہ ہوتی۔

<div class="user-list user-list-center">
{% for user in (translation_reviewers.values() | list)[:50] %}

{% if user.login not in skip_users %}

<div class="user"><a href="{{ user.url }}"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Reviews: {{ user.count }}</div></div>

{% endif %}

{% endfor %}

</div>

## سرپرست

یہ ہیں **سرپرست**۔ 😎

وہ **FastAPI** (اور دوسرے) کے ساتھ میرے کام کی حمایت کر رہے ہیں، بنیادی طور پر [GitHub Sponsors](https://github.com/sponsors/tiangolo) کے ذریعے۔

{% if sponsors %}

{% if sponsors.gold %}

### گولڈ سرپرست

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.silver %}

### سلور سرپرست

{% for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.bronze %}

### برانز سرپرست

{% for sponsor in sponsors.bronze -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% endif %}

### انفرادی سرپرست

{% if github_sponsors %}
{% for group in github_sponsors.sponsors %}

<div class="user-list user-list-center">

{% for user in group %}
{% if user.login not in sponsors_badge.logins %}

<div class="user"><a href="{{ user.url }}"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a></div>

{% endif %}
{% endfor %}

</div>

{% endfor %}
{% endif %}

## ڈیٹا کے بارے میں - تکنیکی تفصیلات

اس صفحے کا بنیادی مقصد کمیونٹی کی دوسروں کی مدد کرنے کی کوششوں کو نمایاں کرنا ہے۔

خاص طور پر ایسی کوششوں کو شامل کرتے ہوئے جو عام طور پر کم نظر آتی ہیں، اور بہت سے معاملات میں زیادہ محنت طلب ہوتی ہیں، جیسے سوالات میں دوسروں کی مدد کرنا اور تراجم کے ساتھ Pull Requests کا review کرنا۔

ڈیٹا ہر مہینے حساب کیا جاتا ہے، آپ [source code یہاں](https://github.com/fastapi/fastapi/blob/master/scripts/) پڑھ سکتے ہیں۔

یہاں میں سرپرستوں کے تعاون کو بھی نمایاں کر رہا ہوں۔

میں algorithm، سیکشنز، thresholds وغیرہ کو اپڈیٹ کرنے کا حق بھی محفوظ رکھتا ہوں (احتیاطاً 🤷)۔
