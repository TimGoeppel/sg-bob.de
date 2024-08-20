---
layout: page
title: "Rundenwettkämpfe"
subheadline: "Wettkämpfe im Schützengau Ansbach"
permalink: "/rwk/"
header: no
image:
  title: "rundenwettkaempfe.jpeg"
---
<style>
.durchgang_win {
    border-left: 5px solid darkgreen;
}
.durchgang_tie {
    border-left: 5px solid blue;
}
.durchgang_def {
    border-left: 5px solid firebrick;
}
</style>

Rundenwettkämpfe im [Schützengau Ansbach](https://gau-ansbach.de/){:target="_blank"}.
{% for disziplin in site.data.rwk_data.disziplinen %}

## {{ disziplin.disziplin }} {{ disziplin.sportjahr }}
{% for mannschaft in disziplin.mannschaften %}

<details>
  <summary><b><center>{{ mannschaft.mannschafts_nr }}. Mannschaft ({{ mannschaft.klassen_name }})</center></b></summary>
  Schützen:
  <ul>
  {% for schuetze in mannschaft.schuetzen %}
  <li><a onclick="alert('Ergebnisse von {{ schuetze.vorname }} {{ schuetze.nachname }}:\nMaximum: {{ schuetze.max }}\nMinimum: {{ schuetze.min }}{% assign anzahl = schuetze.anzahl_stamm | plus: schuetze.anzahl_ersatz %}{% if schuetze.anzahl_stamm != 0 and schuetze.anzahl_ersatz != 0 %}\nDurchschnitt: {{ schuetze.avg }} ({{ anzahl }}){% endif %}{% if schuetze.anzahl_stamm != 0 %}\nDurchschnitt (Stamm): {{ schuetze.avg_stamm }} ({{ schuetze.anzahl_stamm }}){% endif %}{% if schuetze.anzahl_ersatz != 0 %}\nDurchschnitt (Ersatz): {{ schuetze.avg_ersatz }} ({{ schuetze.anzahl_ersatz }}){% endif %}')">{{ schuetze.vorname }} {{ schuetze.nachname }}</a></li>
  {% endfor %}
  </ul>
  {% assign info = mannschaft.info %}
  <table>
  <tr><th>Tabelle {{ mannschaft.gruppe }} {{ mannschaft.gruppen_nr }}</th></tr>
  <tr><th>Platz</th><th>Mannschaft</th><th>Ringe</th><th>Punkte</th></tr>
  {% for m in info.tabelle %}{% capture bs %}{% if mannschaft.vereinsnummer == m.vereinsnummer and mannschaft.mannschafts_nr == m.mannschafts_nr %}<b>{% else %}{% endif %}{% endcapture %}{% capture be %}{% if mannschaft.vereinsnummer == m.vereinsnummer and mannschaft.mannschafts_nr == m.mannschafts_nr %}</b>{% else %}{% endif %}{% endcapture %}<tr><td>{{ bs }}{{ m.platzierung }}{{ be }}</td><td>{{ bs }}{{ m.name }} {{ m.mannschafts_nr }}{{ be }}</td><td>{{ bs }}{{ m.ringe }} (&#8960; {% assign g = m.anzahl_geschossen | times: 1.0 %}{{ m.ringe | divided_by: g | round }}){{ be }}</td><td>{{ bs }}{{ m.punkte_gewonnen }}:{{ m.punkte_verloren }}{{ be }}</td></tr>{% endfor %}
  </table>

  <table>
  <tr><th>Durchgänge</th></tr>
  <tr><th>Runde</th><th>Datum</th><th>Heimmannschaft</th><th>Gastmannschaft</th><th>Ergebnis</th><th>Punkte</th></tr>
  {% for durchgang in info.durchgaenge %}
  <tr{% if durchgang.sieg %} class="durchgang_{% if durchgang.sieg == 1 %}win{% elsif durchgang.sieg == 0%}tie{% else %}def{% endif %}"{% endif %}><td>{{ durchgang.wettkampftag }}. {{ durchgang.runde }}</td><td>{{ durchgang.datum_iso | date: "%d.%m.%Y %H:%M" }}</td><td>{{ durchgang.heim_name }} {{ durchgang.heim_mannschafts_nr }}</td><td>{{ durchgang.gast_name }} {{ durchgang.gast_mannschafts_nr }}</td><td>{% if durchgang.heim_ringe and durchgang.gast_ringe %}{{ durchgang.heim_ringe }} : {{ durchgang.gast_ringe }}{% endif %}</td><td>{{ durchgang.punkte }}</td></tr>
  {% endfor %}
  </table>
</details>
{% endfor %}
{% endfor %}
