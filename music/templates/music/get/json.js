{
    "li": [
      {% for object in list %}
      {
        "@attributes": {
            "data-path": "{{ track.uri }}",
            "data-title": "{{ track.title }}",
            "data-thumbpath": "{{ track.artwork_url }}"
        }
    },
    {% endfor %}
  ]
}
