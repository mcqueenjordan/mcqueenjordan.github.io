---
layout: default
---

# Thoughts

{% for thought in site.thought %}

<h2><a href="/thought/{{ thought.name }}">{{ thought.title }}</a></h2>
<h3>{{ thought.subtitle }}</h3>

{{ thought.content }}

---

{% endfor %}

