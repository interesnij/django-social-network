/*!
   card headers manage scripts
  */
$('#ajax').on('click', '.item_community_remove', function() {link = $(this).parent(); pk = link.parents(".infinite-item").attr("community-id");var uuid = link.parents(".infinite-item").attr("item-id");$.ajax({url: "/community/delete/" + pk + "/" + uuid + "/",success: function(data) {$(link).parents('.card').hide();$('.activefullscreen').hide();$.toast({heading: 'Информация',text: 'Запись успешно удалена!',showHideTransition: 'fade',icon: 'info'})}});});
$('#ajax').on('click', '.item_community_fixed', function() {link = $(this).parent(); pk = link.parents(".infinite-item").attr("community-id");var uuid = link.parents(".infinite-item").attr("item-id");$.ajax({url: "/community/fixed/" + pk + "/" + uuid + "/",success: function(data) {link.parent().html("<span class='dropdown-item item_community_unfixed'> Открепить</span>");$.toast({heading: 'Информация',text: 'Запись закреплена!',showHideTransition: 'fade',icon:'info'})}});});
$('#ajax').on('click', '.item_community_unfixed', function() {link = $(this).parent(); pk = link.parents(".infinite-item").attr("community-id");var uuid = link.parents(".infinite-item").attr("item-id");$.ajax({url: "/community/unfixed/" + pk + "/" + uuid + "/",success: function(data) {link.parent().html("<span class='dropdown-item item_community_fixed'>Закрепить</span>");$.toast({heading: 'Информация',text: 'Запись откреплена!',showHideTransition: 'fade',icon: 'info'})}});});
$('#ajax').on('click','.item_community_off_comment',function(){link=$(this).parent(); pk=link.parents(".infinite-item").attr("community-id");uuid=link.parents(".infinite-item").attr("item-id");$.ajax({url: "/community/off_comment/" + pk + "/" + uuid + "/",success: function(data) {link.parent().html("<span class='dropdown-item item_community_unfixed'>Выключить комментарии</span>");$.toast({heading: 'Информация',text: 'Комментарии выключены!',showHideTransition: 'fade',icon:'info'})}});});
$('#ajax').on('click', '.item_community_on_comment', function() {link=$(this).parent(); pk=link.parents(".infinite-item").attr("community-id");uuid=link.parents(".infinite-item").attr("item-id");$.ajax({url: "/community/on_comment/" + pk + "/" + uuid + "/",success: function(data) {link.parent().html("<span class='dropdown-item item_community_fixed'>Включить комментарии</span>");$.toast({heading: 'Информация',text: 'Комментарии включены!',showHideTransition: 'fade',icon: 'info'})}});});
$('#ajax').on('click', '.js-textareacopybtn', function() {btn = $(this);link = btn.find('.js-copytextarea');link.focus();link.select();try {var successful = document.execCommand('copy');var msg = successful ? 'successful' : 'unsuccessful';console.log('Copying text command was ' + msg);} catch (err) {console.log('Oops, unable to copy');}});

/*!
   get votes script of community
  */
$("body").on('click', '.c_like', function() {like = $(this); item = like.parents('.infinite-item'); var uuid = item.attr("item-id"); var pk = item.attr("community-id"); dislike = like.next().next();$.ajax({url: "/votes/community_like/" + uuid + "/" + pk + "/", type: 'POST', data: {'obj': pk},success: function(json) {like.find("[data-count='like']").text(json.like_count); like.find(".svg_default").toggleClass('svg_success'); like.find(".likes_count").toggleClass('svg_success'); like.siblings('.like_window').html('').load("/window/c_like_window/" + uuid + "/" + pk + "/");dislike.find("[data-count='dislike']").text(json.dislike_count);dislike.find(".svg_default").removeClass('svg_danger'); dislike.find(".dislikes_count").removeClass('svg_danger');dislike.siblings('.dislike_window').html('').load("/window/c_dislike_window/" + uuid + "/" + pk + "/")}}); return false;});

$("body").on('click', '.c_dislike', function() {var dislike = $(this); item = dislike.parents('.infinite-item'); var uuid = item.attr("item-id"); var pk = item.attr("community-id"); var like = dislike.prev().prev();$.ajax({url: "/votes/community_dislike/" + uuid + "/" + pk + "/", type: 'POST', data: {'obj': pk},success: function(json) {like.find("[data-count='like']").text(json.like_count); like.find(".svg_default").removeClass('svg_success'); like.find(".likes_count").removeClass('svg_success'); like.siblings('.like_window').html('').load("/window/c_like_window/" + uuid + "/" + pk + "/");dislike.find("[data-count='dislike']").text(json.dislike_count); dislike.find(".svg_default").toggleClass('svg_danger');dislike.find(".dislikes_count").toggleClass('svg_danger');dislike.siblings('.dislike_window').html('').load("/window/c_dislike_window/" + uuid + "/" + pk + "/")}}); return false;});

$('body').on('click', '.c_repost', function() {var item = $(this).parents('.infinite-item'); var item_id = item.attr("item-id"); $('#user_item_pk').html(item_id);});

$("body").on('click', '.c_like2', function() {var like = $(this); var pk = like.data('pk'); var uuid = like.data('uuid'); var dislike = like.next().next();$.ajax({url: "/votes/community_comment/" + uuid + "/" + pk + "/like/", type: 'POST', data: {'obj': pk},success: function(json) {like.find("[data-count='like']").text(json.like_count); like.find(".svg_default").toggleClass('svg_success'); like.find(".likes_count").toggleClass('svg_success'); like.siblings('.comment_like_window').html('').load("/window/c_comment_like_window/" + uuid + "/" + pk + "/");dislike.find("[data-count='dislike']").text(json.dislike_count); dislike.find(".svg_default").removeClass('svg_danger'); dislike.find(".dislikes_count").removeClass('svg_danger'); dislike.siblings('.comment_dislike_window').html('').load("/window/c_comment_dislike_window/" + uuid + "/" + pk + "/")}}); return false;});

$("body").on('click', '.c_dislike2', function() {var dislike = $(this); var pk = dislike.data('pk'); var uuid = dislike.data('uuid'); var like = dislike.prev().prev();$.ajax({url: "/votes/community_comment/" + uuid + "/" + pk + "/dislike/",type: 'POST',data: { 'obj': pk },success: function(json) {like.find("[data-count='like']").text(json.like_count); like.find(".svg_default").removeClass('svg_success'); like.find(".likes_count").removeClass('svg_success'); like.siblings('.comment_like_window').html('').load("/window/c_comment_like_window/" + uuid + "/" + pk + "/");dislike.find("[data-count='dislike']").text(json.dislike_count); dislike.find(".svg_default").toggleClass('svg_danger'); dislike.find(".dislikes_count").toggleClass('svg_danger'); dislike.siblings('.comment_dislike_window').html('').load("/window/c_comment_dislike_window/" + uuid + "/" + pk + "/")}});return false;});

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
