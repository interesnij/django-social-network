{
    "li": [
      {% for object in list %}
      {
        "@attributes": {
            "data-path": "{{ object.uri }}",
            "data-title": "{{ object.title }}",
            "data-thumbpath": "{{ object.artwork_url }}"
        }
    },
    {% endfor %}
  ]
}
