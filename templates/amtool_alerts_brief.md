{% for alert in alerts %}
**Alert Firing:**
{{alert.annotations.title}}
**Details:** 
{% for label_name, label_value in alert.labels.items() %} _{{label_name}}:_ **{{label_value}}** {% endfor %}

**Annotations:** 
{% for name, value in alert.annotations.items() %} `{{name}}:` _{{value}}_ {% endfor %}
****

Suppress:

_!amtool suppress {{ alert.fingerprint }}_ 
{% endfor %}


