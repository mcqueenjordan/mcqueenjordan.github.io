---
layout: default
---

<h1 class="f0 normal mt0 mb4">Things</h1>

{% assign things = site.thing | sort: 'published_date' | reverse %}
{% for thing in things %}


<h1 class="f1 normal mt0 mb4"><a href="/thing/{{ thing.name }}">{{ thing.title }}</a></h1>
<div class="content measure-wide lh-copy f2-ns">
        {{ thing.content }}
</div>

---

{% endfor %}
