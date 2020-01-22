
$('#ajax').on('click', '.photo_detail', function() {
    photo = $(this); photo_id = photo.data("id"); user_uuid = photo.data("uuid");
    $('#photo_loader').html('').load("/gallery/load/photo/" + photo_id + "/" + user_uuid + "/")
    $('.photo_fullscreen').show();
});

$('#ajax').on('click', '.album_photo_detail', function() {
    photo = $(this); pk = photo.data("pk"); uuid = photo.parent().data("uuid"); uuid2 = photo.parent().data("uuid2");
    $('#photo_loader').html('').load("/gallery/load/u_photo/" + pk + "/" + uuid + "/" + uuid2 + "/")
    $('.photo_fullscreen').show();
});

$('#ajax').on('click', '.photos_add', function() { $('#photos_add_window').show(); })
$('#ajax').on('click', '.albums_add', function() { var user = $(this); var user_id = user.data("uuid"); $('#photo_add_loader').html('').load("/gallery/user/add_album/" + user_id + "/"); $('.add_fullscreen').show(); })
$('#ajax').on('click', '.add_fullscreen_hide', function() { $('.add_fullscreen').hide(); $('#photo_loader').empty(); });
$('#ajax').on('click', '.photo_fullscreen_hide', function() { $('.photo_fullscreen').hide(); $('#photo_loader').empty(); });


$('#ajax').on('click', '.u_photo_edit', function() {
  $('#block_description_form').show();
});

 $('#ajax').on('click', '.u_photo_description_btn', function() {
     var button = $(this);
     var form2 = button.parent().parent().parent();
     display = button.parents(".data_display");
     description_block = form2.parent().prev();
     var pk = display.data('pk');
     var uuid = display.data('uuid');
     $.ajax({
         url: '/gallery/user_progs/description/' + pk + "/" + uuid + "/",
         method:'post',
         success: function(data) {
           description = $("#id_description").val();
           description_block.append(description + "<br><span style='cursor:pointer' class='u_photo_edit'>Редактировать</span>");
           form2.parent().hide();
         }});
     return false;
 });

 $('#ajax').on('click', '#user_photo_remove', function() {
     button = $(this);
     display = button.parents(".data_display");
     remove_block = button.parent();
     pk = display.data('pk');
     uuid = display.data('uuid');
     $.ajax({
         url: '/gallery/user_progs/delete/' + pk + "/" + uuid + "/",
         success: function(data) {
           remove_block.empty().append("<span style='cursor:pointer;color:rgba(0, 0, 0, 1);' id='user_photo_abort_remove'>Восстановить</span>");
           display.addClass("style_removed_object");
           $.toast({heading: 'Информация',text: 'Фотография успешно удалена',showHideTransition: 'fade',icon: 'link'});
         }});
     return false;
 });


 $('#ajax').on('click', '.u_photo_off_comment', function() {
     button = $(this);
     display = button.parents(".data_display");
     remove_block = button.parent();
     pk = display.data('pk');
     uuid = display.data('uuid');
     $.ajax({
         url: '/gallery/user_progs/close_comment/' + pk + "/" + uuid + "/",
         success: function(data) {
           remove_block.empty().append('<span style="cursor:pointer" class="u_photo_on_comment">Включить комментарии</span>');
           $.toast({heading: 'Информация',text: 'Комментарии успешно отключены',showHideTransition: 'fade',icon: 'link'});
         }});
     return false;
 });
 $('#ajax').on('click', '.u_photo_on_comment', function() {
     button = $(this);
     display = button.parents(".data_display");
     remove_block = button.parent();
     pk = display.data('pk');
     uuid = display.data('uuid');
     $.ajax({
         url: '/gallery/user_progs/close_comment/' + pk + "/" + uuid + "/",
         success: function(data) {
           remove_block.empty().append('<span style="cursor:pointer" class="u_photo_off_comment">Выключить комментарии</span>');
           $.toast({heading: 'Информация',text: 'Комментарии успешно включены',showHideTransition: 'fade',icon: 'link'});
         }});
     return false;
 });
 $('#ajax').on('click', '.u_photo_on_private', function() {
     button = $(this);
     display = button.parents(".data_display");
     remove_block = button.parent();
     pk = display.data('pk');
     uuid = display.data('uuid');
     $.ajax({
         url: '/gallery/user_progs/on_private/' + pk + "/" + uuid + "/",
         success: function(data) {
           remove_block.empty().append('<span style="cursor:pointer" class="u_photo_off_private">Отключить приватность</span>');
           $.toast({heading: 'Информация',text: 'Приватность успешно включена',showHideTransition: 'fade',icon: 'link'});
         }});
     return false;
 });
 $('#ajax').on('click', '.u_photo_off_private', function() {
     button = $(this);
     display = button.parents(".data_display");
     remove_block = button.parent();
     pk = display.data('pk');
     uuid = display.data('uuid');
     $.ajax({
         url: '/gallery/user_progs/off_private/' + pk + "/" + uuid + "/",
         success: function(data) {
           remove_block.empty().append('<span style="cursor:pointer" class="u_photo_on_private">Включить приватность</span>');
           $.toast({heading: 'Информация',text: 'Приватность успешно отключена',showHideTransition: 'fade',icon: 'link'});
         }});
     return false;
 });

 $('#ajax').on('click', '.u_unset_avatar', function() {
     button = $(this);
     display = button.parents(".data_display");
     remove_block = button.parent();
     pk = display.data('pk');
     uuid = display.data('uuid');
     $.ajax({
         url: '/gallery/user_progs/remove_avatar/' + pk + "/" + uuid + "/",
         success: function(data) {
           remove_block.empty().append('<span style="cursor:pointer" class="u_set_avatar">На аватар</span>');
           $.toast({heading: 'Информация',text: 'Аватар успешно обновился',showHideTransition: 'fade',icon: 'link'});
         }});
     return false;
 });
 $('#ajax').on('click', '.u_set_avatar', function() {
     button = $(this);
     display = button.parents(".data_display");
     remove_block = button.parent();
     pk = display.data('pk');
     uuid = display.data('uuid');
     $.ajax({
         url: '/gallery/user_progs/add_avatar/' + pk + "/" + uuid + "/",
         success: function(data) {
           remove_block.empty().append('<span style="cursor:pointer" class="u_unset_avatar">Убрать аватар</span>');
           $.toast({heading: 'Информация',text: 'Аватар успешно обновился',showHideTransition: 'fade',icon: 'link'});
         }});
     return false;
 });
