---
layout: page
title: "Rundenwettkämpfe"
subheadline: "Wettkämpfe im Schützengau Ansbach"
permalink: "/rwk/"
header: no
image:
  title: "rundenwettkaempfe.jpeg"
chartjs: true
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
<ul class="accordion" data-accordion>
{% for mannschaft in disziplin.mannschaften %}
  <li class="accordion-navigation">{% capture panel %}{{ disziplin.disziplin }} {{ disziplin.sportjahr }} mannschaft{{ mannschaft.mannschafts_nr }} {{ mannschaft.klassen_name }}{% endcapture %}{% assign panel = panel | downcase | replace: ' ', '_' %}
  <a href="#panel{{ panel }}"><b><center>{% if mannschaft.mannschafts_nr and mannschaft.klassen_name %}{{ mannschaft.mannschafts_nr }}. Mannschaft ({{ mannschaft.klassen_name }}){% else %}{{ mannschaft.gruppe }}{% endif %}</center></b></a>
  <div id="panel{{ panel }}" class="content">
  Schützen:
  <ul>
  {% for schuetze in mannschaft.schuetzen %}
  <li>{% if schuetze.max != 0 %}<a onclick="alert('Ergebnisse von {{ schuetze.vorname }} {{ schuetze.nachname }}:\nMaximum: {{ schuetze.max }}\nMinimum: {{ schuetze.min }}{% assign anzahl = schuetze.anzahl_stamm | plus: schuetze.anzahl_ersatz %}{% if schuetze.anzahl_stamm != 0 and schuetze.anzahl_ersatz != 0 %}\nDurchschnitt: {{ schuetze.avg }} ({{ anzahl }}){% endif %}{% if schuetze.anzahl_stamm != 0 %}\nDurchschnitt (Stamm): {{ schuetze.avg_stamm }} ({{ schuetze.anzahl_stamm }}){% endif %}{% if schuetze.anzahl_ersatz != 0 %}\nDurchschnitt (Ersatz): {{ schuetze.avg_ersatz }} ({{ schuetze.anzahl_ersatz }}){% endif %}')">{% endif %}{{ schuetze.vorname }} {{ schuetze.nachname }}{% if schuetze.max != 0 %}</a>{% endif %}</li>
  {% endfor %}
  </ul>
  {% assign info = mannschaft.info %}
  {% if mannschaft.info %}
  {% include download_calendar calendar=info.kalender hover="Wettkampfkalender herunterladen (.ics)" name="Termine" %}
  <div style="overflow-y: scroll;">
  <table>
  <tr><th>Tabelle {{ mannschaft.gruppe }} {{ mannschaft.gruppen_nr }}</th></tr>
  <tr><th>Platz</th><th>Mannschaft</th><th>Ringe</th><th>Punkte</th></tr>
  {% for m in info.tabelle %}{% capture bs %}{% if mannschaft.vereinsnummer == m.vereinsnummer and mannschaft.mannschafts_nr == m.mannschafts_nr %}<b>{% else %}{% endif %}{% endcapture %}{% capture be %}{% if mannschaft.vereinsnummer == m.vereinsnummer and mannschaft.mannschafts_nr == m.mannschafts_nr %}</b>{% else %}{% endif %}{% endcapture %}<tr><td>{{ bs }}{{ m.platzierung }}{{ be }}</td><td>{{ bs }}{{ m.name }} {{ m.mannschafts_nr }}{{ be }}</td><td>{{ bs }}{{ m.ringe }} (&#8960; {% assign g = m.anzahl_geschossen | times: 1.0 %}{{ m.ringe | divided_by: g | round }}){{ be }}</td><td>{{ bs }}{{ m.punkte_gewonnen }}:{{ m.punkte_verloren }}{{ be }}</td></tr>{% endfor %}
  </table>
  </div>
  <div style="overflow-y: scroll;">
  <table>
  <tr><th>Durchgänge</th></tr>
  <tr><th>Runde</th><th>Datum</th><th>Heimmannschaft</th><th>Gastmannschaft</th><th>Ergebnis</th><th>Punkte</th></tr>
  {% for durchgang in info.durchgaenge %}
  <tr{% if durchgang.sieg %} class="durchgang_{% if durchgang.sieg == 1 %}win{% elsif durchgang.sieg == 0%}tie{% else %}def{% endif %}"{% endif %}><td>{{ durchgang.wettkampftag }}. {{ durchgang.runde }}</td><td>{{ durchgang.zeit | date: "%d.%m.%Y %H:%M" }}</td><td>{{ durchgang.heim_name }} {{ durchgang.heim_mannschafts_nr }}</td><td>{{ durchgang.gast_name }} {{ durchgang.gast_mannschafts_nr }}</td><td>{% if durchgang.heim_ringe and durchgang.gast_ringe %}{{ durchgang.heim_ringe }} : {{ durchgang.gast_ringe }}{% endif %}</td><td>{{ durchgang.punkte }}</td></tr>
  {% endfor %}
  </table>
  </div>
{% endif %}
{% if mannschaft.chartjs %}
{% assign chartid = "chart_" | append: disziplin.id | append: "_" | append: mannschaft.klasse | append: "_" | append: mannschaft.gruppen_nr | replace: " ", "_" | downcase %}
{% include chart id=chartid %}
<script>
(async function() {
new Chart(document.getElementById('{{ chartid }}'), {
    type: 'line',
    data: JSON.parse('{{ mannschaft.chartjs.data | jsonify }}'),
    options: {
        locale: 'de-DE',
        scales: {
            y: {
                title: { display: true, text: 'Ringe' },
                suggestedMin: {{ mannschaft.chartjs.suggested_min }},
                max: {{ mannschaft.chartjs.max }},
                ticks: {
                    callback: function(val, index) {
                      return (val == {{ mannschaft.chartjs.max }}) ? 'Max. ' + this.getLabelForValue(val) : this.getLabelForValue(val);
                    }
                }
            }
        },
        interaction: {
            intersect: false,
            mode: 'index'
        },
        plugins: {
            tooltip: {
                callbacks: { footer: function(tooltipItems) {
                    diff = 0;
                    tooltipItems.forEach((tooltipItem) => {
                        diff += tooltipItem.parsed.y;
                        if(diff > 0) {
                            diff *= -1;
                        }
                    });
                    return "Differenz: " + (-diff);
                } }
             }
        }
    }
})
})();
</script>
{% endif %}
</div>
</li>
{% endfor %}
</ul>
{% endfor %}
