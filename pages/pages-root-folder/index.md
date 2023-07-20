---
#
# Use the widgets beneath and the content will be
# inserted automagically in the webpage. To make
# this work, you have to use › layout: frontpage
#
layout: frontpage
header:
  title: ""
  image_fullwidth: header.jpg
#widget1:
#  title: "Blog & Portfolio"
#  url: 'http://phlow.github.io/feeling-responsive/blog/'
#  image: widget-1-302x182.jpg
#  text: 'Every good portfolio website has a blog with fresh news, thoughts and develop&shy;ments of your activities. <em>Feeling Responsive</em> offers you a fully functional blog with an archive page to give readers a quick overview of all your posts.'
#
# Use the call for action to show a button on the frontpage
#
# To make internal links, just use a permalink like this
# url: /getting-started/
#
# To style the button in different colors, use no value
# to use the main color or success, alert or secondary.
# To change colors see sass/_01_settings_colors.scss
#
#callforaction:
#  url: https://tinyletter.com/feeling-responsive
#  text: Inform me about new updates and features ›
#  style: alert
permalink: /index.html
#
# This is a nasty hack to make the navigation highlight
# this page as active in the topbar navigation
#
gallery:
  - image_url: schiessen_oben.jpeg
  - image_url: schiessen_unten.jpeg
  - image_url: schiessen_vorne.jpeg
  - image_url: schiessen_hinten.jpeg
  - image_url: umzug_1.jpeg
  - image_url: umzug_2.jpeg
  - image_url: umzug_3.jpeg
  - image_url: umzug_5.jpeg
  - image_url: volleyball.jpeg
  - image_url: ausflug_geiselwind.jpg
    caption: "Schützenfahrt nach Geiselwind"
  - image_url: buergermeister.jpeg
    caption: "erster Schützenmeister Bastian Luff (links) mit Bürgermeister Gerhard Rammler"
  - image_url: buergermeister2.jpeg
    caption: "Ehemaliger erster Schützenmeister Fritz Lothert (Mitte) mit Landtagsabgeordnetem Andreas Schalk (links) und dem Bürgermeister von Burgoberbach Gerhard Rammler (rechts)"
  - image_url: ehrung.jpg
    caption: "Ehrungen"
  - image_url: koenige_2022.jpg
    caption: "Königsproklamation 2022<br>\
	von links nach rechts: 2. Ritter Christian Hammerl, Schützenkönigin Martha Heller, Jugendschützenkönig Jonas Thiele, 1. Ritter Heinz Hammerl"
  - image_url: koenigsessen.jpg
  - image_url: schiessbetrieb.jpg
    caption: "Unser Schießstand mit Schießbetrieb"
  - image_url: schuetzenhaus_mitglieder.jpeg
  - image_url: umzug_6.jpg

homepage: true
---
{% include gallery %}