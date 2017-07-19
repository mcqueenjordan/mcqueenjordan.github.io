---
layout: default
---

# Thoughts

{% for thought in site.thought %}

<h2><a href="/thought/{{ thought.name }}">{{ thought.title }}</a><br>
{% if thought.category != "quote" %}
{{ thought.subtitle }}
{% endif %}
</h2>

{{ thought.content }}

---

{% endfor %}

