|Funktion|Name|Kontakt|
|--------|----|-------|{% for vorstand in include.vorstandschaft %}
|{{ vorstand.funktion }}|{{ vorstand.name }}|{% if vorstand.kontakt %}{{ vorstand.kontakt }}{% else %}{%- include todo msg="fehlt" -%}{% endif %}|{% endfor %}
