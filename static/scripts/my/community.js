/*!
   card headers manage scripts
  */
$('#ajax').on('click', '.item_community_remove', function() {link = $(this).parent(); pk = link.parents(".infinite-item").attr("community-id");var uuid = link.parents(".infinite-item").attr("item-id");$.ajax({url: "/community/delete/" + pk + "/" + uuid + "/",success: function(data) {$(link).parents('.card').hide();$('.activefullscreen').hide();$.toast({heading: 'Информация',text: 'Запись успешно удалена!',showHideTransition: 'fade',icon: 'info'})}});});
$('#ajax').on('click', '.item_community_fixed', function() {link = $(this).parent(); pk = link.parents(".infinite-item").attr("community-id");var uuid = link.parents(".infinite-item").attr("item-id");$.ajax({url: "/community/fixed/" + pk + "/" + uuid + "/",success: function(data) {link.parent().html("<span class='dropdown-item item_community_unfixed'> Открепить</span>");$.toast({heading: 'Информация',text: 'Запись закреплена!',showHideTransition: 'fade',icon:'info'})}});});
$('#ajax').on('click', '.item_community_unfixed', function() {link = $(this).parent(); pk = link.parents(".infinite-item").attr("community-id");var uuid = link.parents(".infinite-item").attr("item-id");$.ajax({url: "/community/unfixed/" + pk + "/" + uuid + "/",success: function(data) {link.parent().html("<span class='dropdown-item item_community_fixed'>Закрепить</span>");$.toast({heading: 'Информация',text: 'Запись откреплена!',showHideTransition: 'fade',icon: 'info'})}});});
$('#ajax').on('click','.item_community_off_comment',function(){link=$(this).parent(); pk=link.parents(".infinite-item").attr("community-id");uuid=link.parents(".infinite-item").attr("item-id");$.ajax({url: "/community/off_comment/" + pk + "/" + uuid + "/",success: function(data) {link.parent().html("<span class='dropdown-item item_community_unfixed'>Выключить комментарии</span>");$.toast({heading: 'Информация',text: 'Комментарии выключены!',showHideTransition: 'fade',icon:'info'})}});});
$('#ajax').on('click', '.item_community_on_comment', function() {link=$(this).parent(); pk=link.parents(".infinite-item").attr("community-id");uuid=link.parents(".infinite-item").attr("item-id");$.ajax({url: "/community/on_comment/" + pk + "/" + uuid + "/",success: function(data) {link.parent().html("<span class='dropdown-item item_community_fixed'>Включить комментарии</span>");$.toast({heading: 'Информация',text: 'Комментарии включены!',showHideTransition: 'fade',icon: 'info'})}});});
$('#ajax').on('click', '.js-textareacopybtn', function() {btn = $(this);link = btn.find('.js-copytextarea');link.focus();link.select();try {var successful = document.execCommand('copy');var msg = successful ? 'successful' : 'unsuccessful';console.log('Copying text command was ' + msg);} catch (err) {console.log('Oops, unable to copy');}});

    $('body').on('click', '.c_itemComment', function() {
        button1 = $(this); form1 = button1.parent().parent().parent(); upload_block = form1.find(".upload_block");
        $.ajax({
            url: '/community/post-comment/', data: new FormData($(form1)[0]), contentType: false, cache: false, processData: false, type: 'POST',
            success: function(data) { $(".form-control-rounded").val(""); form1.parent().prev().append(data); upload_block.empty()},
            error: function(data) { $.toast({heading: 'Ошибка',text: 'Для публикации комментария нужно написать что-нибудь и/или вставить изображение(ия)',showHideTransition: 'fade',icon: 'error'}); },
        });
        return false;
    });

    $('#ajax').on('click', '.c_replyComment', function() {
        button = $(this); form2 = button.parent().parent().parent().parent(); block = form2.parent(); upload_block = form2.find(".upload_block"); reply_stream = block.next().next(); pk = button.data('pk'); uuid = button.data('uuid');
        $.ajax({
            url: '/community/reply-comment/' + uuid + "/" + pk + "/",
            data: new FormData($(form2)[0]),
            contentType: false, cache: false, processData: false, type: 'POST',
            success: function(data) { $(".form-control-rounded").val(""); reply_stream.append(data); reply_stream.addClass("replies_open"); block.hide(); upload_block.empty(); },
            error: function(data) { $.toast({heading: 'Ошибка',text: 'Для публикации ответа нужно написать что-нибудь и/или вставить изображение(ия)',showHideTransition: 'fade',icon: 'error'}) },
        });
        return false;
    });
    $('body').on('click', '.c_replyParentComment', function() {
        button = $(this); form3 = button.parent().parent().parent().parent(); block = form3.parent(); upload_block = form3.find(".upload_block"); pk = button.data('pk'); uuid = button.data('uuid'); reply_stream = block.parents('.stream_reply_comments');
        $.ajax({
            url: '/community/reply-comment/' + uuid + "/" + pk + "/",
            data: new FormData($(form3)[0]), contentType: false, cache: false, processData: false, type: 'POST',
            success: function(data) { $(".form-control-rounded").val(""); reply_stream.append(data); block.hide(); upload_block.empty();},
            error: function(data) { $.toast({heading: 'Ошибка',text: 'Для публикации ответа нужно написать что-нибудь и/или вставить изображение(ия)',showHideTransition: 'fade',icon: 'error'}) },
        });
        return false;
    });

    /*!
       post create scripts
      */
    $('#ajax').on('click', '.c_add_post', function() {var btn = $(this); var pk = btn.data('pk'); var frm_post = $('#COMM-POST'); var stream = frm_post.parent().next();$.ajax({type: frm_post.attr('method'), url: "/posts/add_post_community/" + pk + "/", data: frm_post.serialize(),success: function(data) {stream.find(".community_stream").prepend(data); stream.find(".post_empty").hide(); $(".id_text").val(""); $(".add_board #for_images_upload").hide(); $(".add_board #for_gallery").hide(); $(".add_board #for_doc").hide(); $(".add_board #for_good").hide(); $(".add_board #for_question").hide(); $(".add_board #for_settings").hide();$.toast({heading: 'Успешно',text: 'Запись успешно создана!',showHideTransition: 'fade',icon: 'success'})},error: function(data) {$.toast({heading: 'Ошибка',text: 'Для публикации записи нужно написать что-нибудь и/или вставить изображение(ия)',showHideTransition: 'fade',icon: 'error'})}}); return false;});

    $('#images_upload').on('click', function() {$('#for_images_upload').show();});
    $('#settings').on('click', function() {$('#for_settings').show();});
    $('#gallery').on('click', function() {$('#for_gallery').show();});
    $('#doc').on('click', function() {$('#for_doc').show();});
    $('#good').on('click', function() {$('#for_good').show();});
    $('#question').on('click', function() {$('#for_question').show();});

      $('#ajax').on('click', '.community_member_create', function() {
       var member_create = $(this); var li = member_create.parents(".list-group-item"); var pk = li.data('pk'); var uuid = li.data('uuid'); $.ajax({ url: "/communities/progs/add_member/" + pk + "/" + uuid + "/", success: function () { member_create.parent().html("<span class='show_staff_window' style='cursor:pointer'>Изменить полномочия</span> |<span class='community_member_delete' style='cursor:pointer'>Удалить</span>"); li.removeClass("style_removed_object"); }});
       });
       $('#ajax').on('click', '.community_follow_delete', function() {
        var community_follow_delete = $(this);
        var li = community_follow_delete.parents(".list-group-item");
        var pk = li.data('pk');
        var uuid = li.data('uuid');
        $.ajax({
          url: "/follows/delete_member/" + pk + "/" + uuid + "/",
          success: function () {
            community_follow_delete.parent().html("<span class='community_follow_create' style='cursor:pointer;color:rgba(0, 0, 0, 1);'>Восстановить</span>");
            li.addClass("style_removed_object"); }
          });
        });
        $('#ajax').on('click', '.member_follow_create', function() {
          var member_follow_create = $(this); var pk = member_follow_create.data('id');
          $.ajax({url: "/follows/add_member/" + pk + "/", success: function () {$('#ajax').html('').load("/communities/reload/" + pk + "/");}});
        });
        $('#ajax').on('click', '.member_create', function() {var member_create = $(this);var pk = member_create.data('id');var uuid = member_create.data('uuid');$.ajax({url: "/communities/progs/add_member/" + pk + "/" + uuid + "/",success: function () {$('#ajax').html('').load("/communities/reload/" + pk + "/");}});});
        $('#ajax').on('click', '.member_delete', function() {var member_delete = $(this);var pk = member_delete.data('id');var uuid = member_create.data('uuid');$.ajax({url: "/communities/progs/delete_member/" + pk + "/" + uuid + "/",success: function () {$('#ajax').html('').load("/communities/reload/" + pk + "/");}});});
        $('#ajax').on('click', '.community_follow_create', function() {
         var community_follow_create = $(this);
         var li = community_follow_create.parents(".list-group-item");
         var pk = li.data('pk');
         var uuid = li.data('uuid');
         $.ajax({
           url: "/follows/add_member/" + pk + "/" + uuid + "/",
           success: function () {
             community_follow_create.parent().html("<span class='community_follow_delete' style='cursor:pointer;color:rgba(0, 0, 0, 1);'>Восстановить</span>");
             li.removeClass("style_removed_object"); }
           });
         });
    $('#ajax').on('click', '.member_follow_create', function() {var member_follow_create = $(this);var pk = member_follow_create.data('id');var uuid = member_follow_create.data('uuid');$.ajax({url: "/follows/add_member/" + pk + "/" + uuid + "/",success: function () {$('#ajax').html('').load("/communities/reload/" + pk + "/");}});});
    $('#ajax').on('click', '.member_follow_delete', function() {var member_follow_delete = $(this);var pk = member_follow_delete.data('id');var uuid = member_follow_delete.data('uuid');$.ajax({url: "/follows/delete_member/" + pk + "/" + uuid + "/",success: function () {$('#ajax').html('').load("/communities/reload/" + pk + "/");}});});
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
