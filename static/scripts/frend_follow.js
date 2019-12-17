$('.user_block').on('click', function() {
  $.ajax({
      url: '{% url "user_block" user.pk %}',
      success: function (data) {
        $('#button_load').html('').load("{% url 'profile_button_reload' user.pk %}");
      }
  });
});

$('.user_unblock').on('click', function() {
  $.ajax({
      url: '{% url "user_unblock" user.pk %}',
      success: function (data) {$('#button_load').html('').load("{% url 'profile_button_reload' user.pk %}");}
  });
});
$('.follow_create').on('click', function() {
  $.ajax({
      url: '{% url "create_follow" user.pk %}',
      success: function (data) {$('#button_load').html('').load("{% url 'profile_button_reload' user.pk %}");}
  });
  });

$('.follow_delete').on('click', function() {
    $.ajax({
      url: '{% url "delete_follow" user.pk %}',
      success: function (data) {$('#button_load').html('').load("{% url 'profile_button_reload' user.pk %}");}
    });
});

$('.connect_create').on('click', function() {
  $.ajax({
      url: '{% url "create_connect" user.pk %}',
      success: function (data) {$('#button_load').html('').load("{% url 'profile_button_reload' user.pk %}");}
  });
});

$('.connect_delete').on('click', function() {
  $.ajax({
      url: '{% url "delete_connect" user.pk %}',
      success: function (data) {$('#button_load').html('').load("{% url 'profile_button_reload' user.pk %}");}
  });
});
