---
layout: default
---

# Thoughts

{% for thought in site.thought %}

<h2><a href="/thought/{{ thought.name }}">{{ thought.title }}</a><br>
{{ thought.subtitle }}</h2>

{{ thought.content }}

---

{% endfor %}

