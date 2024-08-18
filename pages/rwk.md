---
layout: page
title: "Rundenwettkämpfe"
subheadline: "Wettkämpfe im Schützengau Ansbach"
permalink: "/rwk/"
header: no
image:
  title: "rundenwettkaempfe.jpeg"
---
Rundenwettkämpfe im [Schützengau Ansbach](https://gau-ansbach.de/){:target="_blank"}_
{% for disziplin in site.data.rwk_data.disziplinen %}

## {{ disziplin.disziplin }}
{% for mannschaft in disziplin.mannschaften %}

<details>
  <summary><b><center>{{ mannschaft.mannschafts_nr }}. Mannschaft ({{ mannschaft.klassen_name }})</center></b></summary>
  Schützen:
  <ul>
  {% for schuetze in mannschaft.schuetzen %}
  <li><a onclick="alert('Ergebnisse:\nMaximum: {{ schuetze.max }}\nMinimum: {{ schuetze.min }}{% assign anzahl = schuetze.anzahl_stamm | plus: schuetze.anzahl_ersatz %}{% if schuetze.anzahl_stamm != 0 and schuetze.anzahl_ersatz != 0 %}\nDurchschnitt: {{ schuetze.avg }} ({{ anzahl }}){% endif %}{% if schuetze.anzahl_stamm != 0 %}\nDurchschnitt (Stamm): {{ schuetze.avg_stamm }} ({{ schuetze.anzahl_stamm }}){% endif %}{% if schuetze.anzahl_ersatz != 0 %}\nDurchschnitt (Ersatz): {{ schuetze.avg_ersatz }} ({{ schuetze.anzahl_ersatz }}){% endif %}')">{{ schuetze.vorname }} {{ schuetze.nachname }}</a></li>
  {% endfor %}
  </ul>
</details>
{% endfor %}
{% endfor %}
