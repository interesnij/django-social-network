$('.user_block').on('click', function() {
  pk = $(this).parent().data("pk");
  $.ajax({
      url: "/users/progs/block/" + pk + "/",
      success: function (data) {$('#button_load').html('').load("/users/load/profile_button/" + pk + "/");}
  });
});

$('.user_unblock').on('click', function() {
  pk = $(this).parent().data("pk");
  $.ajax({
      url: "/users/progs/unblock/" + pk + "/",
      success: function (data) {$('#button_load').html('').load("/users/load/profile_button/" + pk + "/");}
  });
});
$('.follow_create').on('click', function() {
  pk = $(this).data("pk");
  $.ajax({
      url: "/follows/add/" + pk + "/",
      success: function (data) {$('#button_load').html('').load("/users/load/profile_button/" + pk + "/");}
  });
  });

$('.follow_delete').on('click', function() {
  pk = $(this).parent().data("pk");
    $.ajax({
      url: "/follows/delete/" + pk + "/",
      success: function (data) {$('#button_load').html('').load("/users/load/profile_button/" + pk + "/");}
    });
});

$('.connect_create').on('click', function() {
  pk = $(this).parent().data("pk");
  $.ajax({
      url: "/frends/add/" + pk + "/",
      success: function (data) {$('#button_load').html('').load("/users/load/profile_button/" + pk + "/");}
  });
});

$('.connect_delete').on('click', function() {
  pk = $(this).parent().data("pk");
  $.ajax({
      url: "/frends/delete/" + pk + "/",
      success: function (data) {$('#button_load').html('').load("/users/load/profile_button/" + pk + "/");}
  });
});
