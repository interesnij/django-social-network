/*!
   fullscreen's script of community
  */
$('#ajax').on('click', '.c_article_detail', function() {var item = $(this).parent(); var pk = item.attr("community-id"); var uuid = item.attr("item-id"); $('#article_loader').html('').load("/article/read/" + pk + "/" + uuid + "/"); $('.article_fullscreen').show();});
$('#ajax').on('click', '.c_fullscreen', function() {var item = $(this).parent(); var pk = item.attr("community-id"); var uuid = item.attr("item-id");$('#item_loader').html('').load("/communities/item/" + pk + "/" + uuid + "/"); $('.item_fullscreen').show();});
$('#ajax').on('click', '.c_all_likes', function() {var btn = $(this); item = $(this).parents('.infinite-item'); var pk = item.attr("community-id"); var uuid = item.attr("item-id");$('#votes_loader').html('').load("/window/all_community_like/" + uuid + "/" + pk + "/"); $('.votes_fullscreen').show();});
$('#ajax').on('click', '.c_all_dislikes', function() {var btn = $(this); item = $(this).parents('.infinite-item'); var pk = item.attr("community-id"); var uuid = item.attr("item-id");$('#votes_loader').html('').load("/window/all_community_dislike/" + uuid + "/" + pk + "/"); $('.votes_fullscreen').show();});
$('#ajax').on('click', '.c_all_reposts', function() {var btn = $(this); item = $(this).parents('.infinite-item'); var pk = item.attr("community-id"); var uuid = item.attr("item-id");$('#votes_loader').html('').load("/window/all_community_reposts/" + uuid + "/" + pk + "/"); $('.votes_fullscreen').show();});

$('#ajax').on('click', '.photo_fullscreen_hide', function() { $('.photo_fullscreen').hide(); $('#photo_loader').empty(); });
$('#ajax').on('click', '.item_fullscreen_hide', function() { $('.item_fullscreen').hide(); $('#item_loader').empty(); });
$('#ajax').on('click', '.votes_fullscreen_hide', function() { $('.votes_fullscreen').hide(); $('#votes_loader').empty(); });
$('#ajax').on('click', '.article_fullscreen_hide', function() {$('.article_fullscreen').hide(); $('#article_loader').empty();});
$('#ajax').on('click', '.community_fullscreen_hide', function() {$('.community_fullscreen').hide();$('#community_loader').empty();});
$('#ajax').on('click', '.community_add', function() {$('#community_loader').html('').load("/communities/add/progs/");$('.community_fullscreen').show();})

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
   get comment script of community
  */
$('#ajax').on('click', '.show_replies', function() { var element = $(this); element.next().toggleClass('replies_open'); });
$('#ajax').on('click', '.c_comment.comments_close', function() {var btn = $(this); var item = btn.closest(".infinite-item"); var uuid = item.attr("item-id"); var pk = item.attr("community-id"); var container = item.find(".load_comments");$.ajax({url: "/community/comment/" + uuid + "/" + pk + "/", data: {'uuid': uuid}, cache: false,beforeSend: function() {item.find(".load_comments").html("<span style='display:flex;justify-content: center;'><img src='/static/images/loading.gif'></span>");},success:function(data){container.html(data.comments);btn.addClass("comments_open").removeClass("comments_close");}}); return false;});

$('#ajax').on('click', '.c_comment.comments_open', function() {var btn = $(this); var item = btn.closest(".infinite-item"); var container = item.find(".load_comments");container.empty(); btn.removeClass('comments_open').addClass("comments_close");});

$("#ajax").on('click', '.reply_comment', function() {var reply_comment_form = $(this); var objectUser = reply_comment_form.prev().text().trim(); var form = reply_comment_form.next().find(".text-comment"); form.val(objectUser + ', '); reply_comment_form.next().show(); form.focus();})

/*!
   get votes script of community
  */
$("#ajax").on('click', '.c_like', function() {like = $(this); item = like.parents('.infinite-item'); var uuid = item.attr("item-id"); var pk = item.attr("community-id"); dislike = like.next().next();$.ajax({url: "/votes/community_like/" + uuid + "/" + pk + "/", type: 'POST', data: {'obj': pk},success: function(json) {like.find("[data-count='like']").text(json.like_count); like.find(".svg_default").toggleClass('svg_success'); like.find(".likes_count").toggleClass('svg_success'); like.siblings('.like_window').html('').load("/window/c_like_window/" + uuid + "/" + pk + "/");dislike.find("[data-count='dislike']").text(json.dislike_count);dislike.find(".svg_default").removeClass('svg_danger'); dislike.find(".dislikes_count").removeClass('svg_danger');dislike.siblings('.dislike_window').html('').load("/window/c_dislike_window/" + uuid + "/" + pk + "/")}}); return false;});

$("#ajax").on('click', '.c_dislike', function() {var dislike = $(this); item = dislike.parents('.infinite-item'); var uuid = item.attr("item-id"); var pk = item.attr("community-id"); var like = dislike.prev().prev();$.ajax({url: "/votes/community_dislike/" + uuid + "/" + pk + "/", type: 'POST', data: {'obj': pk},success: function(json) {like.find("[data-count='like']").text(json.like_count); like.find(".svg_default").removeClass('svg_success'); like.find(".likes_count").removeClass('svg_success'); like.siblings('.like_window').html('').load("/window/c_like_window/" + uuid + "/" + pk + "/");dislike.find("[data-count='dislike']").text(json.dislike_count); dislike.find(".svg_default").toggleClass('svg_danger');dislike.find(".dislikes_count").toggleClass('svg_danger');dislike.siblings('.dislike_window').html('').load("/window/c_dislike_window/" + uuid + "/" + pk + "/")}}); return false;});

$('#ajax').on('click', '.c_repost', function() {var item = $(this).parents('.infinite-item'); var item_id = item.attr("item-id"); $('#user_item_pk').html(item_id);});

$("#ajax").on('click', '.c_like2', function() {var like = $(this); var pk = like.data('pk'); var uuid = like.data('uuid'); var dislike = like.next().next();$.ajax({url: "/votes/community_comment/" + uuid + "/" + pk + "/like/", type: 'POST', data: {'obj': pk},success: function(json) {like.find("[data-count='like']").text(json.like_count); like.find(".svg_default").toggleClass('svg_success'); like.find(".likes_count").toggleClass('svg_success'); like.siblings('.comment_like_window').html('').load("/window/c_comment_like_window/" + uuid + "/" + pk + "/");dislike.find("[data-count='dislike']").text(json.dislike_count); dislike.find(".svg_default").removeClass('svg_danger'); dislike.find(".dislikes_count").removeClass('svg_danger'); dislike.siblings('.comment_dislike_window').html('').load("/window/c_comment_dislike_window/" + uuid + "/" + pk + "/")}}); return false;});

$("#ajax").on('click', '.c_dislike2', function() {var dislike = $(this); var pk = dislike.data('pk'); var uuid = dislike.data('uuid'); var like = dislike.prev().prev();$.ajax({url: "/votes/community_comment/" + uuid + "/" + pk + "/dislike/",type: 'POST',data: { 'obj': pk },success: function(json) {like.find("[data-count='like']").text(json.like_count); like.find(".svg_default").removeClass('svg_success'); like.find(".likes_count").removeClass('svg_success'); like.siblings('.comment_like_window').html('').load("/window/c_comment_like_window/" + uuid + "/" + pk + "/");dislike.find("[data-count='dislike']").text(json.dislike_count); dislike.find(".svg_default").toggleClass('svg_danger'); dislike.find(".dislikes_count").toggleClass('svg_danger'); dislike.siblings('.comment_dislike_window').html('').load("/window/c_comment_dislike_window/" + uuid + "/" + pk + "/")}});return false;});


  /*!
     comment create scripts
    */
  $('#ajax').on('click', '.comment_image', function() {
  		var photo = $(this); var pk = photo.data("id"); var uuid = photo.data("uuid");
  		$('#photo_loader').html('').load("/gallery/load/comment/" + pk + "/" + uuid + "/"); $('.photo_fullscreen').show();
  });
  $('#ajax').on('click', '.upload_photo', function() {
    btn = $(this); img_block = btn.parent().parent().prev();
    if (!img_block.empty()){img_block.empty()};
    img_block.append('<span class="close_upload_block" title="Закрыть панель загрузки фото"><svg fill="currentColor" style="width:15px" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span><div class="col-lg-6 col-md-6"><a href="#" style="display:none" class="delete_thumb1">Удалить</a><input class="file1 hide_image" type="file" name="photo" accept="image/*" id="id_item_comment_photo"><div class="comment_photo1"><h4 class="svg_default"><svg width="35" height="35" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/>+<path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg></h4></div></div><div class="col-lg-6 col-md-6"><a href="#" style="display:none" class="delete_thumb1">Удалить</a><input class="file2 hide_image" type="file" name="photo2" accept="image/*" id="id_item_comment_photo2"><div class="comment_photo2"><h4 class="svg_default"><svg width="35" height="35" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">+<path d="M0 0h24v24H0z" fill="none"/><path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg></h4></div></div>');img_block.show();
  });

  $('#ajax').on('click', '.delete_thumb1', function(e) {e.preventDefault(); var a = $(this); a.parent().empty().append('<a href="#" style="display:none" class="delete_thumb1">Удалить</a><input class="file1 hide_image" type="file" name="photo" accept="image/*" id="id_item_comment_photo"><div class="comment_photo1"><h4 class="svg_default"><svg width="35" height="35" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none" /><path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z" /></svg></h4></div>');});
  $('#ajax').on('click', '.close_upload_block', function() {$(this).parent().empty();});

  $("#ajax").on('click', '.reply_comment', function() {var reply_comment_form = $(this); var objectUser = reply_comment_form.prev().text().trim(); var form = reply_comment_form.next().find(".text-comment"); form.val(objectUser + ', '); reply_comment_form.next().show(); form.focus();})
  $('#ajax').on('click', '.u_comment.comments_open', function() {
    var btn = $(this); var item = btn.closest(".infinite-item"); var container = item.find(".load_comments"); container.empty(); btn.removeClass('comments_open').addClass("comments_close");
  });
  $('#ajax').on('click', '.select_photo', function() {uuid = $(this).data("uuid");$('#photo_loader').html("").load("/users/load/img_load/" + uuid + "/"); $('.photo_fullscreen').show();});


    $('#ajax').on('click', '.c_itemComment', function() {
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
    $('#ajax').on('click', '.c_replyParentComment', function() {
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

    $('#ajax').on('click', '#community_article_add', function() {var btn = $(this); var pk = btn.data('pk');$('#article_loader').html('').load("/article/add_community/" + pk + "/");$('.article_fullscreen').show();})

    $('#images_upload').on('click', function() {$('#for_images_upload').show();});
    $('#settings').on('click', function() {$('#for_settings').show();});
    $('#gallery').on('click', function() {$('#for_gallery').show();});
    $('#doc').on('click', function() {$('#for_doc').show();});
    $('#good').on('click', function() {$('#for_good').show();});
    $('#question').on('click', function() {$('#for_question').show();});



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
