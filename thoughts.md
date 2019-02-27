---
layout: default
---

<h1 class="f0 normal mt0 mb4">Thoughts</h1>

{% assign thoughts = site.thought | sort: 'published_date' | reverse %}
{% for thought in thoughts %}


<h1 class="f1 normal mt0 mb4"><a href="/thought/{{ thought.name }}">{{ thought.title }}</a></h1>
<div class="content measure-wide lh-copy f3-ns">
        {{ thought.content }}
</div>

---

{% endfor %}

