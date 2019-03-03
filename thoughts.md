---
layout: default_with_index
---

{% assign thoughts = site.thought | sort: 'published_date' | reverse %}
{% assign topics = site.topics %}

<div class="mv3 ph3 center mw-container">
  <div class="measure f1-l f3-m f4-s lh-title">
    <h1 class="f1 normal mt0 mb4">Thoughts</h1>
  </div>
</div>

<div class="mw-container center ph3">
 <div class="mv5">
    <div class="pa0 lh-copy bb b--black-10">
      {% for topic in topics %} 
        <section class="flex-ns bt b--black-10 pv3">
          <h1 class="f5 ttu ma0 mb1-s pr4 w-20-l w-40-m">{{ topic }}</h1>
          <ul class="bullet-list list w-80-l w-60-m ma0 pr4 black-50">
            {% for thought in thoughts %}
              {% assign thought_topics = thought.topics %}
              {% if thought_topics contains topic %}
                <li><a class="no-underline" href="/thought/{{ thought.name }}">{{ thought.title }}</a></li>
              {% endif %}
            {% endfor %}
          </ul>
        </section>
      {% endfor %}
  </div>
</div>

{% for thought in thoughts %}
<h1 class="f1 normal mt0 mb4"><a href="/thought/{{ thought.name }}">{{ thought.title }}</a></h1>
<div class="content measure-wide lh-copy f3-ns">
        {{ thought.content }}
        <hr>

{% endfor %}

</div>
