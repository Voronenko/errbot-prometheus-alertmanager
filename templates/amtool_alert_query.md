Fingerprint               Alertname                                Starts At                Summary
{% for alert in alerts %}
{{alert.fingerprint}} {{alert.annotations.title}} {{alert.startsAt}}  {{alert.annotations.summary}}
{% endfor %}
