
  $('.member_create').on('click', function() {
  $.ajax({
      url: '{% url "add_community_member" object.pk %}',
      success: function () {
        $('#ajax').html('').load("{% url 'community_detail_reload' object.pk %}");
        $('title').text('{{ object.name }}');
      }
  });
  });

  $('.member_delete').on('click', function() {
  $.ajax({
      url: '{% url "delete_community_member" object.pk %}',
      success: function () {
        $('#ajax').html('').load("{% url 'community_detail_reload' object.pk %}");
        $('title').text('{{ object.name }}');
      }
  });
  });
