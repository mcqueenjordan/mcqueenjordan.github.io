---
layout: default
---

<h1 class="f0 normal mt0 mb4">Thoughts</h1>

{% assign thoughts = site.thought | sort: 'published_date' | reverse %}
{% for thought in thoughts %}


<h1 class="f1 normal mt0 mb4"><a href="/thought/{{ thought.name }}">{{ thought.title }}</a><br>
{% if thought.category != "quote" %}
{{ thought.subtitle }}
{% endif %}
<em>{{ thought.published_date }}</em>
</h1>

<div class="content measure-wide lh-copy f2-ns">
        {{ thought.content }}
</div>

---

{% endfor %}

