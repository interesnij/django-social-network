
$('#ajax').on('click', '.user_block', function() {
  pk = $(this).parent().data("pk");
  $.ajax({
      url: "/users/progs/block/" + pk + "/",
      success: function (data) {$('#button_load').html('').load("/users/load/profile_button/" + pk + "/");}
  });
});
$('#ajax').on('click', '.user_unblock', function() {
  pk = $(this).parent().data("pk");
  $.ajax({
      url: "/users/progs/unblock/" + pk + "/",
      success: function (data) {$('#button_load').html('').load("/users/load/profile_button/" + pk + "/");}
  });
});
$('#ajax').on('click', '.follow_create', function() {
  pk = $(this).data("pk");
  $.ajax({
      url: "/follows/add/" + pk + "/",
      success: function (data) {$('#button_load').html('').load("/users/load/profile_button/" + pk + "/");}
  });
  });
$('#ajax').on('click', '.follow_delete', function() {
  pk = $(this).parent().data("pk");
    $.ajax({
      url: "/follows/delete/" + pk + "/",
      success: function (data) {$('#button_load').html('').load("/users/load/profile_button/" + pk + "/");}
    });
});
$('#ajax').on('click', '.connect_create', function() {
  pk = $(this).parent().data("pk");
  $.ajax({
      url: "/frends/add/" + pk + "/",
      success: function (data) {$('#button_load').html('').load("/users/load/profile_button/" + pk + "/");}
  });
});
$('#ajax').on('click', '.connect_delete', function() {
  pk = $(this).parent().data("pk");
  $.ajax({
      url: "/frends/delete/" + pk + "/",
      success: function (data) {$('#button_load').html('').load("/users/load/profile_button/" + pk + "/");}
  });
});
