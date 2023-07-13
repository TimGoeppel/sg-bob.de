---
layout: page
title: "Jugend"
subheadline: "Unsere Schützenjugend"
permalink: "/jugend/"
header:
  image: "jugend.jpg"
  background-color: "#ffffff"
---
<img style="float: right;" src="{{ site.urlimg }}kjr.png" width="240px" alt="Teil des Kreisjugendrings Ansbach">
## Angebot
- Gewehre, Blasrohre, Schießbekleidung, und Munition werden für Schüler und Jugendliche kostenfrei zur Verfügung gestellt
- ab 6 Jahren: Training mit Lasergewehr
- ab 12 Jahren: Training auf neuen elektronischen Schießständen

- Training jeden Donnerstag ab 18:30 Uhr
- [Schützenzwerge](schuetzenzwerge) (6-12 Jahre) jeden ersten Samstag im Monat von 10:00&mdash;11:30 Uhr

## Jugendleiter{% assign jugendleiter = site.data.vorstandschaft.erwachsene | where: "funktion", "Jugendleiter" | first %}  
{{ jugendleiter.name }}  
{{ jugendleiter.kontakt }}