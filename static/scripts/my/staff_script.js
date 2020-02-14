

  $('#ajax').on('click', '.community_member_create', function() {
   member_create = $(this);li = member_create.parents(".list-group-item");pk = li.data('pk');uuid = li.data('uuid'); $.ajax({ url: "/communities/progs/add_member/" + pk + "/" + uuid + "/", success: function () { member_create.parent().html("<span class='show_staff_window' style='cursor:pointer'>Изменить полномочия</span> |<span class='community_member_delete' style='cursor:pointer'>Удалить</span>"); li.removeClass("style_removed_object"); }});
   });
   $('#ajax').on('click', '.community_follow_delete', function() {
    community_follow_delete = $(this);
    li = community_follow_delete.parents(".list-group-item");
    pk = li.data('pk');
    uuid = li.data('uuid');
    $.ajax({
      url: "/follows/delete_member/" + pk + "/" + uuid + "/",
      success: function () {
        community_follow_delete.parent().html("<span class='community_follow_create' style='cursor:pointer;color:rgba(0, 0, 0, 1);'>Восстановить</span>");
        li.addClass("style_removed_object"); }
      });
    });
    $('#ajax').on('click', '.member_follow_create', function() {
      member_follow_create = $(this);pk = member_follow_create.data('id');
      $.ajax({url: "/follows/add_member/" + pk + "/", success: function () {$('#ajax').html('').load("/communities/reload/" + pk + "/");}});
    });
    $('#ajax').on('click', '.member_create', function() {var member_create = $(this);var pk = member_create.data('id');$.ajax({url: "/communities/progs/create_member/" + pk + "/",success: function () {$('#ajax').html('').load("/communities/reload/" + pk + "/");}});});
    $('#ajax').on('click', '.member_delete', function() {var member_delete = $(this);var pk = member_delete.data('id');$.ajax({url: "/communities/progs/delete_member/" + pk + "/",success: function () {$('#ajax').html('').load("/communities/reload/" + pk + "/");}});});
    $('#ajax').on('click', '.community_follow_create', function() {
     community_follow_create = $(this);
     li = community_follow_create.parents(".list-group-item");
     pk = li.data('pk');
     uuid = li.data('uuid');
     $.ajax({
       url: "/follows/add_member/" + pk + "/" + uuid + "/",
       success: function () {
         community_follow_create.parent().html("<span class='community_follow_delete' style='cursor:pointer;color:rgba(0, 0, 0, 1);'>Восстановить</span>");
         li.removeClass("style_removed_object"); }
       });
     });
$('#ajax').on('click', '.member_follow_create', function() {member_follow_create = $(this);pk = member_follow_create.data('id');uuid = member_follow_create.data('uuid');$.ajax({url: "/follows/add_member/" + pk + "/" + uuid + "/",success: function () {$('#ajax').html('').load("/communities/reload/" + pk + "/");}});});
$('#ajax').on('click', '.member_follow_delete', function() {member_follow_delete = $(this);pk = member_follow_delete.data('id');uuid = member_follow_delete.data('uuid');$.ajax({url: "/follows/delete_member/" + pk + "/" + uuid + "/",success: function () {$('#ajax').html('').load("/communities/reload/" + pk + "/");}});});
  $('#ajax').on('click', '.community_member_delete', function() {
   member_delete = $(this);li = member_delete.parents(".list-group-item");pk = li.data('pk');uuid = li.data('uuid'); $.ajax({ url: "/communities/progs/delete_member/" + pk + "/" + uuid + "/", success: function () { member_delete.parent().html("<span class='community_member_create' style='cursor:pointer;color:rgba(0, 0, 0, 1);'>Восстановить</span>"); li.addClass("style_removed_object"); }});
   });

$('#ajax').on('click', '.remove_admin', function() {
  remove_admin = $(this);
  li = remove_admin.parents(".list-group-item");
  pk = li.data('pk');
  uuid = li.data('uuid');
  $.ajax({
    url: "/communities/progs/delete_admin/" + pk + "/" + uuid + "/",
    success: function () {
      remove_admin.parent().parent().addClass("small").html("<span class='show_staff_window' style='cursor:pointer'>Назначить руководителем</span> | <span class='member_delete' style='cursor:pointer'>Удалить</span>");
      $.toast({heading: 'Информация',text: 'Администратор успешно лишен полномочий!',showHideTransition: 'fade',icon: 'info'});
    }
  });
});
$('#ajax').on('click', '.remove_moderator', function() {
  remove_admin = $(this);
  li = remove_admin.parents(".list-group-item");
  pk = li.data('pk');
  uuid = li.data('uuid');
  $.ajax({
    url: "/communities/progs/delete_moderator/" + pk + "/" + uuid + "/",
    success: function () {
      remove_admin.parent().parent().addClass("small").html("<span class='show_staff_window' style='cursor:pointer'>Назначить руководителем</span> | <span class='member_delete' style='cursor:pointer'>Удалить</span>");
      $.toast({heading: 'Информация',text: 'Модератор успешно лишен полномочий!',showHideTransition: 'fade',icon: 'info'});
    }
  });
});
$('#ajax').on('click', '.remove_editor', function() {
  remove_admin = $(this);
  li = remove_admin.parents(".list-group-item");
  pk = li.data('pk');
  uuid = li.data('uuid');
  $.ajax({
    url: "/communities/progs/delete_editor/" + pk + "/" + uuid + "/",
    success: function () {
      remove_admin.parent().parent().addClass("small").html("<span class='show_staff_window' style='cursor:pointer'>Назначить руководителем</span> | <span class='member_delete' style='cursor:pointer'>Удалить</span>");
      $.toast({heading: 'Информация',text: 'Редактор успешно лишен полномочий!',showHideTransition: 'fade',icon: 'info'});
    }
  });
});
$('#ajax').on('click', '.remove_advertiser', function() {
  remove_admin = $(this);
  li = remove_admin.parents(".list-group-item");
  pk = li.data('pk');
  uuid = li.data('uuid');
  $.ajax({
    url: "/communities/progs/delete_advertiser/" + pk + "/" + uuid + "/",
    success: function () {
      remove_admin.parent().parent().addClass("small").html("<span class='show_staff_window' style='cursor:pointer'>Назначить руководителем</span> | <span class='member_delete' style='cursor:pointer'>Удалить</span>");
      $.toast({heading: 'Информация',text: 'Рекламодатель успешно лишен полномочий!',showHideTransition: 'fade',icon: 'info'});
    }
  });
});
