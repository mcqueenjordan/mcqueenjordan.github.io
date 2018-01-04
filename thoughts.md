---
layout: default
---

# Thoughts


{% assign thoughts = site.thought | sort: 'published_date' | reverse %}
{% for thought in thoughts %}

<h2><a href="/thought/{{ thought.name }}">{{ thought.title }}</a><br>
{% if thought.category != "quote" %}
{{ thought.subtitle }}
{% endif %}
<em>{{ thought.published_date }}</em>
</h2>

{{ thought.content }}

---

{% endfor %}

