ID                                    Matchers                        Ends At                  Created By       Comment
{% for silence in silences %}
{{silence.id}}    {% for match in silence.matchers %}{{match.name}}:{{match.value}}{% endfor %}   {{silence.endsAt}}  {{silence.created_by}}  {{silence.comment}}
{% endfor %}
