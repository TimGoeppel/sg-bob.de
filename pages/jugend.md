---
layout: page
title: "Jugend"
subheadline: "Unsere Schützenjugend"
permalink: "/jugend/"
header: no
image:
  title: "jugend.jpg"
---
<img style="float: right;" src="{{ site.urlimg }}kjr.png" width="240px" alt="Teil des Kreisjugendrings Ansbach">
## Angebot
- Gewehre, Blasrohre, Schießbekleidung, und Munition werden für Schüler und Jugendliche kostenfrei zur Verfügung gestellt
- ab 6 Jahren: Training mit Lasergewehr
- ab 12 Jahren: Training auf neuen elektronischen Schießständen

- Training für alle Altersgruppen jeden Donnerstag ab 18:30 Uhr{% include termine %}{% assign termin = termine | where: "name", "Training" | first %}{% include termin termin=termin customname="Die nächste Trainingseinheit findet" pre="
  - " post=" statt." %}
- Schützenzwerge (6-12 Jahre) jeden ersten Samstag im Monat (siehe unten)
- jährliches Ferienprogramm (siehe unten)

## Schützenzwerge
{: #schuetzenzwerge}
<img src="{{ site.urlimg }}schuetzenzwerge.jpeg" width="100%" alt="Schützenzwerge">

Jeden ersten Samstag im Monat findet für alle 6- bis 12-Jährigen von 10:00 bis 11:30 Uhr unser kostenfreies Programm „Schützenzwerge” unter der Anleitung von Jugendleiter Kevin Schreier und anderen Helfern statt.

Neben dem Schießen mit dem Lasergewehr werden auch viele weitere Disziplinen wie Bogenschießen, Blasrohrschießen und Kegeln angeboten.{% include termine %}{% assign termin = termine | where: "name", "Schützenzwerge" | first %}{% include termin termin=termin customname="Nächster Termin" pre="

" post="." %}

## Ferienprogramm
Jedes Jahr findet in den Sommerferien unser Ferienprogramm statt.{% include termine %}{% assign termin = termine | where: "name", "Ferienprogramm" | first %}{% include termin termin=termin customname="Nächstes Ferienprogramm" pre="

" post="." %}

## Jugendleiter{% assign jugendleiter = site.data.vorstandschaft.erwachsene | where: "funktion", "Jugendleiter" | first %}  
<img style="float: right;" src="{{ site.urlimg }}jugendleiter.jpg" width="240px" alt="Der momentane Jugendleiter {{ jugendleiter.name }}">

{{ jugendleiter.name }}  
{{ jugendleiter.kontakt }}