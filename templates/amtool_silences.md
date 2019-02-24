Silences

{% for silence in silences %}

{{silence.id}} {{silence.status.state}}
{{silence.comment}} {{silence.createdAt}}

{% for match in silence.matchers %}
  {{match.name}}:{{match.value}}
{% endfor %}

{% endfor %}
