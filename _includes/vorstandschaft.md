|Funktion|Name|Kontakt|
|--------|----|-------|{% for vorstand in include.vorstandschaft %}
|{{ vorstand.funktion }}|{{ vorstand.name }}|{{ vorstand.kontakt }}|{% endfor %}