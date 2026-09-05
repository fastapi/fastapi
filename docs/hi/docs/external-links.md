---
include_yaml:
  topic_repos: data/topic_repos.yml
---

# बाहरी लिंक्स (External Links) { #external-links }

**FastAPI** की एक बेहतरीन community है जो लगातार बढ़ रही है।

**FastAPI** से जुड़े कई posts, articles, tools और projects मौजूद हैं।

आप FastAPI से संबंधित कई resources खोजने के लिए किसी search engine या video platform का आसानी से उपयोग कर सकते हैं।

/// note | टिप्पणी

पहले, इस page पर बाहरी articles के लिंक्स सूचीबद्ध होते थे।

लेकिन अब जब FastAPI सभी भाषाओं में सबसे अधिक GitHub stars वाला backend framework है, और Python में सबसे अधिक starred और उपयोग किया जाने वाला framework है, तो इसके बारे में लिखे गए सभी articles को सूचीबद्ध करने का प्रयास करना अब समझदारी नहीं है।

///

## GitHub Repositories { #github-repositories }

[`fastapi` topic वाले सबसे अधिक starred GitHub repositories](https://github.com/topics/fastapi):

{% for repo in topic_repos.repos %}

<a href={{repo.html_url}} target="_blank">★ {{repo.stars}} - {{repo.name}}</a> by <a href={{repo.owner_html_url}} target="_blank">@{{repo.owner_login}}</a>.

{% endfor %}
