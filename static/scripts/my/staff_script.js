
$('#ajax').on('click', '.show_staff_window', function() {
  var btn = $(this).parents(".list-group-item");
  var pk = btn.data("pk");
  var uuid = btn.data("uuid");
  $('#load_staff_window').html('').load("/communities/manage/staff_window/" + pk + "/" + uuid + "/");
  $('.manage_window_fullscreen').show();
});

$('#ajax').on('click', '.manage_window_fullscreen_hide', function() {
   $('.manage_window_fullscreen').hide();
   $('#load_staff_window').empty();
 });

 $('#ajax').on('click', '.show_staff_window', function() {
   var btn = $(this).parents(".list-group-item");
   var pk = btn.data("pk");
   var uuid = btn.data("uuid");
   $('#load_staff_window').html('').load("/communities/manage/staff_window/" + pk + "/" + uuid + "/");
   $('.manage_window_fullscreen').show();
 });

 $('#ajax').on('click', '.manage_window_fullscreen_hide', function() {
    $('.manage_window_fullscreen').hide();
    $('#load_staff_window').empty();
  });
  $('#ajax').on('click', '.community_member_create', function() {
   var member_create = $(this); var li = member_create.parents(".list-group-item"); var pk = li.data('pk'); var uuid = li.data('uuid'); $.ajax({ url: "/communities/progs/add_member/" + pk + "/" + uuid + "/", success: function () { member_create.parent().html("<span class='show_staff_window' style='cursor:pointer'>Изменить полномочия</span> |<span class='community_member_delete' style='cursor:pointer'>Удалить</span>"); li.removeClass("style_removed_object"); }});
   });
   $('#ajax').on('click', '.community_follow_delete', function() {
    var community_follow_delete = $(this); var li = community_follow_delete.parents(".list-group-item"); var pk = li.data('pk'); var uuid = li.data('uuid'); $.ajax({ url: "/follows/progs/delete_member/" + pk + "/" + uuid + "/", success: function () { community_follow_delete.parent().html("<span class='community_member_create' style='cursor:pointer;color:rgba(0, 0, 0, 1);'>Восстановить</span>""); li.addClass("style_removed_object"); }});
    });
  $('#ajax').on('click', '.community_member_delete', function() {
   var member_delete = $(this); var li = member_delete.parents(".list-group-item"); var pk = li.data('pk'); var uuid = li.data('uuid'); $.ajax({ url: "/communities/progs/delete_member/" + pk + "/" + uuid + "/", success: function () { member_delete.parent().html("<span class='community_member_create' style='cursor:pointer;color:rgba(0, 0, 0, 1);'>Восстановить</span>"); li.addClass("style_removed_object"); }});
   });

$('#ajax').on('click', '.remove_admin', function() {
  var remove_admin = $(this);
  var li = remove_admin.parents(".list-group-item");
  var pk = li.data('pk');
  var uuid = li.data('uuid');
  $.ajax({
    url: "/communities/progs/delete_admin/" + pk + "/" + uuid + "/",
    success: function () {
      remove_admin.parent().parent().addClass("small").html("<span class='show_staff_window' style='cursor:pointer'>Назначить руководителем</span> | <span class='member_delete' style='cursor:pointer'>Удалить</span>");
      $.toast({heading: 'Информация',text: 'Администратор успешно лишен полномочий!',showHideTransition: 'fade',icon: 'info'});
    }
  });
});
$('#ajax').on('click', '.remove_moderator', function() {
  var remove_admin = $(this);
  var li = remove_admin.parents(".list-group-item");
  var pk = li.data('pk');
  var uuid = li.data('uuid');
  $.ajax({
    url: "/communities/progs/delete_moderator/" + pk + "/" + uuid + "/",
    success: function () {
      remove_admin.parent().parent().addClass("small").html("<span class='show_staff_window' style='cursor:pointer'>Назначить руководителем</span> | <span class='member_delete' style='cursor:pointer'>Удалить</span>");
      $.toast({heading: 'Информация',text: 'Модератор успешно лишен полномочий!',showHideTransition: 'fade',icon: 'info'});
    }
  });
});
$('#ajax').on('click', '.remove_editor', function() {
  var remove_admin = $(this);
  var li = remove_admin.parents(".list-group-item");
  var pk = li.data('pk');
  var uuid = li.data('uuid');
  $.ajax({
    url: "/communities/progs/delete_editor/" + pk + "/" + uuid + "/",
    success: function () {
      remove_admin.parent().parent().addClass("small").html("<span class='show_staff_window' style='cursor:pointer'>Назначить руководителем</span> | <span class='member_delete' style='cursor:pointer'>Удалить</span>");
      $.toast({heading: 'Информация',text: 'Редактор успешно лишен полномочий!',showHideTransition: 'fade',icon: 'info'});
    }
  });
});
$('#ajax').on('click', '.remove_advertiser', function() {
  var remove_admin = $(this);
  var li = remove_admin.parents(".list-group-item");
  var pk = li.data('pk');
  var uuid = li.data('uuid');
  $.ajax({
    url: "/communities/progs/delete_advertiser/" + pk + "/" + uuid + "/",
    success: function () {
      remove_admin.parent().parent().addClass("small").html("<span class='show_staff_window' style='cursor:pointer'>Назначить руководителем</span> | <span class='member_delete' style='cursor:pointer'>Удалить</span>");
      $.toast({heading: 'Информация',text: 'Рекламодатель успешно лишен полномочий!',showHideTransition: 'fade',icon: 'info'});
    }
  });
});
