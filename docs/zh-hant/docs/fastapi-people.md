---
hide:
  - navigation
---

# FastAPI 社群

FastAPI 有一個非常棒的社群，歡迎來自不同背景的朋友參與。

## 作者

嘿! 👋

關於我:

{% if people %}
<div class="user-list user-list-center">
{% for user in people.maintainers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">解答問題: {{ user.answers }}</div><div class="count">Pull Requests: {{ user.prs }}</div></div>
{% endfor %}

</div>
{% endif %}

我是 **FastAPI** 的作者。你可以在[幫助 FastAPI - 獲得幫助 - 與作者聯繫](help-fastapi.md#connect-with-the-author){.internal-link target=_blank} 中閱讀更多相關資訊。

...但在這裡，我想向你介紹這個社群。

---

**FastAPI** 獲得了許多社群的大力支持。我想特別表揚他們的貢獻。

這些人包括：

* [在 GitHub 中幫助他人解答問題](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank}。
* [建立 Pull Requests](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}。
* 審查 Pull Requests，[尤其是翻譯方面的貢獻](contributing.md#translations){.internal-link target=_blank}。

讓我們為他們熱烈鼓掌。 👏 🙇

## FastAPI 專家

這些是在 [GitHub 中幫助其他人解決問題最多的用戶](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank}。 🙇

他們透過幫助其他人，證明了自己是 **FastAPI 專家**。 ✨

!!! 提示
    你也可以成為官方的 FastAPI 專家！

    只需要在 [GitHub 中幫助他人解答問題](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank}。 🤓

你可以查看這些期間的 **FastAPI 專家**：

* [上個月](#fastapi-experts-last-month) 🤓
* [過去 3 個月](#fastapi-experts-3-months) 😎
* [過去 6 個月](#fastapi-experts-6-months) 🧐
* [過去 1 年](#fastapi-experts-1-year) 🧑‍🔬
* [**所有時間**](#fastapi-experts-all-time) 🧙

### FastAPI 專家 - 上個月

上個月在 [GitHub 中幫助他人解決問題最多的](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank}用戶。 🤓

{% if people %}
<div class="user-list user-list-center">
{% for user in people.last_month_experts[:10] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">回答問題數： {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

### FastAPI 專家 - 過去 3 個月

過去三個月在 [GitHub 中幫助他人解決問題最多的](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank}用戶。 😎

{% if people %}
<div class="user-list user-list-center">
{% for user in people.three_months_experts[:10] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">回答問題數： {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

### FastAPI 專家 - 過去 6 個月

過去六個月在 [GitHub 中幫助他人解決問題最多的](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank}用戶。 🧐

{% if people %}
<div class="user-list user-list-center">
{% for user in people.six_months_experts[:10] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">回答問題數： {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

### FastAPI 專家 - 過去一年

過去一年在 [GitHub 中幫助他人解決最多問題的](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank}用戶。 🧑‍🔬

{% if people %}
<div class="user-list user-list-center">
{% for user in people.one_year_experts[:20] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">回答問題數： {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

### FastAPI 專家 - 全部時間

以下是全部時間的 **FastAPI 專家**。 🤓🤯

過去在 [GitHub 中幫助他人解決問題最多的](help-fastapi.md#help-others-with-questions-in-github){.internal-link target=_blank}用戶。 🧙

{% if people %}
<div class="user-list user-list-center">
{% for user in people.experts[:50] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">回答問題數： {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## 主要貢獻者

以下是**主要貢獻者**。 👷

這些用戶[建立了最多已被**合併**的 Pull Requests](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}。

他們貢獻了原始碼、文件和翻譯等。 📦

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_contributors[:50] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Pull Requests: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

還有許多其他的貢獻者（超過一百位），你可以在 <a href="https://github.com/tiangolo/fastapi/graphs/contributors" class="external-link" target="_blank">FastAPI GitHub 貢獻者頁面</a>查看。 👷

## 主要翻譯審核者

以下是 **主要翻譯審核者**。 🕵️

我只會講幾種語言（而且不是很流利 😅），所以審核者[**擁有批准翻譯**](contributing.md#translations){.internal-link target=_blank}文件的權限。沒有他們，就不會有多語言版本的文件。

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_translations_reviewers[:50] %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Reviews: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## 贊助者

以下是**贊助者**。 😎

他們主要透過 <a href="https://github.com/sponsors/tiangolo" class="external-link" target="_blank">GitHub Sponsors</a> 支持我在 **FastAPI**（以及其他項目）上的工作。

{% if sponsors %}

{% if sponsors.gold %}

### 金牌贊助商

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.silver %}

### 銀牌贊助商

{% for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.bronze %}

### 銅牌贊助商

{% for sponsor in sponsors.bronze -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% endif %}

### 個人贊助商

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

## 關於數據 - 技術細節

這個頁面的主要目的是突顯社群幫助他人所做的努力

特別是那些通常不太顯眼但往往更加艱辛的工作，例如幫助他人解答問題和審查包含翻譯的 Pull Requests。

這些數據每月計算一次，你可以在這查看<a href="https://github.com/tiangolo/fastapi/blob/master/.github/actions/people/app/main.py" class="external-link" target="_blank">原始碼</a>。

此外，我也特別表揚贊助者的貢獻。

我也保留更新演算法、章節、門檻值等的權利（以防萬一 🤷）。
