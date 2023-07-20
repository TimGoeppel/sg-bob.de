---
layout: page
show_meta: false
title: "Das bieten wir:"
subheadline: "Unser Vereinsleben"
permalink: "/vereinsleben/"
---
<ul>
    {% for post in site.categories.vereinsleben %}
    <li><a href="{{ site.url }}{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a></li>
    {% endfor %}
</ul>