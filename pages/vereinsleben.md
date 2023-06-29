---
layout: page
show_meta: false
title: "Das bieten wir:"
subheadline: "Unser Vereinsleben"
#header:
#   image_fullwidth: "header_unsplash_5.jpg"
permalink: "/vereinsleben/"
---
<ul>
    {% for post in site.categories.vereinsleben %}
    <li><a href="{{ site.url }}{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a></li>
    {% endfor %}
</ul>