---
include_yaml:
  github_sponsors: data/github_sponsors.yml
  people: data/people.yml
  contributors: data/contributors.yml
  translation_reviewers: data/translation_reviewers.yml
  skip_users: data/skip_users.yml
  members: data/members.yml
  sponsors_badge: data/sponsors_badge.yml
  sponsors: data/sponsors.yml
---

# FastAPI People

FastAPI has an amazing community that welcomes people from all backgrounds.

## Creator

Hey! 👋

This is me:

<div class="user-list user-list-center">
{% for user in people.maintainers %}

<div class="user"><a href="{{ contributors.tiangolo.url }}"><div class="avatar-wrapper"><img src="{{ contributors.tiangolo.avatarUrl }}"/></div><div class="title">@{{ contributors.tiangolo.login }}</div></a> <div class="count">Answers: {{ user.answers }}</div><div class="count">Pull Requests: {{ contributors.tiangolo.count }}</div></div>
{% endfor %}

</div>

I'm the creator of **FastAPI**. You can read more about that in [Help FastAPI - Follow the author](help-fastapi.md#follow-the-author).

## Team

This is the current list of team members. 😎

They have different levels of involvement and permissions, they can perform [repository management tasks](https://tiangolo.com/open-source/management-tasks/) and together we [manage the FastAPI repository](./management.md).

<div class="user-list user-list-center">

{% for user in members["members"] %}

<div class="user"><a href="{{ user.url }}"><div class="avatar-wrapper"><img src="{{ user.avatar_url }}"/></div><div class="title">@{{ user.login }}</div></a></div>

{% endfor %}

</div>

## FastAPI Experts

For a long time, answering questions from the community in GitHub Discussions was done by other community volunteers.

They proved they are **FastAPI Experts** by helping many others. ✨

Here's the hall of fame of the first FastAPI Experts:

<div class="user-list user-list-center">

{% for user in people.experts[:30] %}

{% if user.login not in skip_users.users %}

<div class="user"><a href="{{ user.url }}"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Questions replied: {{ user.count }}</div></div>

{% endif %}

{% endfor %}

</div>

## Top Contributors

Currently, most of the code changes in FastAPI are done by the team.

But over the years, there have also been many contributions made by others.

They contributed source code, documentation, etc. 📦

Here's the hall of fame of the first **Top Contributors**. 👷

<div class="user-list user-list-center">

{% for user in (contributors.values() | list)[:30] %}

{% if user.login not in skip_users.users %}

<div class="user"><a href="{{ user.url }}"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Pull Requests: {{ user.count }}</div></div>

{% endif %}

{% endfor %}

</div>

There are hundreds of other contributors, you can see them all in the [FastAPI GitHub Contributors page](https://github.com/fastapi/fastapi/graphs/contributors). 👷

## Top Translation Reviewers

Currently, translations are done using AI tools, steered by the FastAPI team and native speakers.

At some point, FastAPI had some documentation pages that community members translated into other languages by hand.

Here's the hall of fame of the first **Top Translation Reviewers**. 🕵️

<div class="user-list user-list-center">
{% for user in (translation_reviewers.values() | list)[:30] %}

{% if user.login not in skip_users.users %}

<div class="user"><a href="{{ user.url }}"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Reviews: {{ user.count }}</div></div>

{% endif %}

{% endfor %}

</div>

## Sponsors

**Sponsors** support **FastAPI** and friends, mainly through [GitHub Sponsors](https://github.com/sponsors/tiangolo). ✨

{% if sponsors %}

{% if sponsors.gold %}

### Gold Sponsors

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.silver %}

### Silver Sponsors

{% for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.bronze %}

### Bronze Sponsors

{% for sponsor in sponsors.bronze -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% endif %}

### Individual Sponsors

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

## About the data - technical details

The main intention of this page has been to highlight the effort of the community to help others, especially efforts that were normally less visible and, in many cases, more arduous, like helping others with questions and reviewing Pull Requests with translations.

It also highlights contributions from sponsors.

The data used to be calculated continuously, each month.

As of July 2026, most of the work has been done by (paid) team members for quite some time.

GitHub Discussions are answered mostly by team members.

Most of the code changes are done by team members.

And translations are continuously done for the entire documentation in multiple languages, using AI tools, managed by team members.

Additionally, in recent months, there's been an overwhelming amount of AI spam, mainly to cheat the FastAPI Experts system or to get a PR merged by any means and thereby be considered a contributor. You can read more about the point of view in [Automated Code and AI](https://tiangolo.com/open-source/contributing/#automated-code-and-ai).

Because of this, the data for the FastAPI Experts, Top Contributors, and Top Translation Reviewers is no longer continuously updated.

This section is currently kept as a tribute to the humans that helped shape what FastAPI is today. 🙌
