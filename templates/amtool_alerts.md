For **active** {{ criteria.active }}, **silenced** {{ criteria.silenced }}, **inhibited** {{ criteria.inhibited }}, **unprocessed** {{ criteria.unprocessed }}, **filter** {{ criteria.filter }}, **receiver** {{ criteria.receiver }}

Found **{{ count }}** alerts.
{% for alert in alerts %}
**Alert Firing:**
{{alert.annotations.title}};{{alert.annotations.summary}}; **{{alert.annotations.value}}**

{{alert.annotations.description}}

**Details:**
{% for label_name, label_value in alert.labels.items() %} **{{label_name}}:** `{{label_value}}` {% endfor %}

> State `{{ alert.status.state }}`, inhibited by `{{ alert.status.inhibitedBy }}`, silenced by {{ alert.status.silencedBy }}
> Started `{{ alert.startsAt }}` , updated  `{{ alert.updatedAt }}`

_!amtool suppress {{ alert.fingerprint }}_
****
{% endfor %}


