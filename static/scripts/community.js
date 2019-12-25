/*!
   fullscreen's script of community
  */

$('.article_fullscreen_hide').on('click', function() {$('.article_fullscreen').hide(); $('#article_loader').empty();});
$('#ajax .stream').on('click', '.article_detail', function() {var item = $(this); var item_id = item.data("id");$('#article_loader').html('').load("/article/detail/" + item_id); $('.article_fullscreen').show();});
$('#ajax').on('click', '.c_fullscreen', function() {var item = $(this); var pk = item.data("pk"); var uuid = item.data("uuid");$('#item_loader').html('').load("/communities/item/" + pk + "/" + uuid + "/"); $('.item_fullscreen').show();});

$('#ajax').on('click', '.photo_fullscreen_hide', function() { $('.photo_fullscreen').hide(); $('#photo_loader').empty(); });
$('.item_fullscreen_hide').on('click', function() { $('.item_fullscreen').hide(); $('#item_loader').empty(); });
$('#ajax').on('click', '.votes_fullscreen_hide', function() { $('.votes_fullscreen').hide(); $('#votes_loader').empty(); });


/*!
   manage script of community
  */
$('#ajax').on('click', '.member_create', function() {var member_create = $(this);var pk = member_create.data('id');$.ajax({url: "/communities/add_community_member/" + pk + "/",success: function () {$('#ajax').html('').load("/communities/reload/" + pk + "/");}});});
$('#ajax').on('click', '.member_delete', function() {var member_delete = $(this);var pk = member_delete.data('id');$.ajax({url: "/communities/delete_community_member/" + pk + "/",success: function () {$('#ajax').html('').load("/communities/reload/" + pk + "/");}});});
$('#ajax').on('click', '.member_follow_create', function() {var member_follow_create = $(this);var pk = member_follow_create.data('id');$.ajax({url: "/follows/add_member/" + pk + "/",success: function () {$('#ajax').html('').load("/communities/reload/" + pk + "/");}});});
$('#ajax').on('click', '.member_follow_delete', function() {var member_follow_delete = $(this);var pk = member_follow_delete.data('id');$.ajax({url: "/follows/delete_member/" + pk + "/",success: function () {$('#ajax').html('').load("/communities/reload/" + pk + "/");}});});


/*!
   get comment script of community
  */
$('#ajax').on('click', '.c_comment.comments_close', function() {var btn = $(this); var item = btn.closest(".infinite-item"); var uuid = item.attr("item-id"); var pk = btn.data('pk'); var container = item.find(".load_comments")$.ajax({url: "/community/comment/" + uuid + "/" + pk + "/", data: {'uuid': uuid}, cache: false,beforeSend: function() {item.find(".load_comments").html("<span style='display:flex;justify-content: center;'><img src='/static/images/loading.gif'></span>");},success:function(data){container.html(data.comments);btn.addClass("comments_open").removeClass("comments_close");}}); return false;});

$('#ajax').on('click', '.c_comment.comments_open', function() {var btn = $(this); var item = btn.closest(".infinite-item"); var container = item.find(".load_comments");container.empty(); btn.removeClass('comments_open').addClass("comments_close");});

$("#ajax").on('click', '.reply_comment', function() {var reply_comment_form = $(this); var objectUser = reply_comment_form.prev().text().trim(); var form = reply_comment_form.next().find(".text-comment"); form.val(objectUser + ', '); reply_comment_form.next().show(); form.focus();})

/*!
   get votes script of community
  */
$("#ajax").on('click', '.c_like', function() {var like = $(this); var pk = like.data('id'); var uuid = like.data('uuid'); var dislike = like.next().next();$.ajax({url: "/votes/community_like/" + uuid + "/" + pk + "/", type: 'POST', data: {'obj': pk},success: function(json) {like.find("[data-count='like']").text(json.like_count); like.find(".svg_default").toggleClass('svg_success'); like.find(".likes_count").toggleClass('svg_success'); like.siblings('.like_window').html('').load("/window/c_like_window/" + uuid + "/" + pk + "/");dislike.find("[data-count='dislike']").text(json.dislike_count);dislike.find(".svg_default").removeClass('svg_danger'); dislike.find(".dislikes_count").removeClass('svg_danger');dislike.siblings('.dislike_window').html('').load("/window/c_dislike_window/" + uuid + "/" + pk + "/")}}); return false;});

$("#ajax").on('click', '.c_dislike', function() {var dislike = $(this); var pk = dislike.data('id'); var uuid = dislike.data('uuid'); var like = dislike.prev().prev();$.ajax({url: "/votes/community_dislike/" + uuid + "/" + pk + "/", type: 'POST', data: {'obj': pk},success: function(json) {like.find("[data-count='like']").text(json.like_count); like.find(".svg_default").removeClass('svg_success'); like.find(".likes_count").removeClass('svg_success'); like.siblings('.like_window').html('').load("/window/c_like_window/" + uuid + "/" + pk + "/");dislike.find("[data-count='dislike']").text(json.dislike_count); dislike.find(".svg_default").toggleClass('svg_danger');dislike.find(".dislikes_count").toggleClass('svg_danger');dislike.siblings('.dislike_window').html('').load("/window/c_dislike_window/" + uuid + "/" + pk + "/")}}); return false;});

$('#ajax').on('click', '.c_repost', function() {var item = $(this); var item_id = item.data("uuid"); $('#user_item_pk').html(item_id);});

  $("#ajax").on('click', '.c_like2', function() {
            var like = $(this); var pk = like.data('id'); var uuid = like.data('uuid'); var dislike = like.next().next();
            $.ajax({
                url: "/votes/community_comment/" + uuid + "/" + pk + "/like/", type: 'POST', data: {'obj': pk},
                success: function(json) {
                  like.find("[data-count='like']").text(json.like_count); like.find(".svg_default").removeClass('svg_success'); like.find(".likes_count").removeClass('svg_success'); like.siblings('.like_window').html('').load("/window/c_like_window/" + uuid + "/" + pk + "/");
                  dislike.find("[data-count='dislike']").text(json.dislike_count); dislike.find(".svg_default").toggleClass('svg_danger'); dislike.find(".dislikes_count").toggleClass('svg_danger'); dislike.siblings('.dislike_window').html('').load("/window/c_dislike_window/" + uuid + "/" + pk + "/")
                }
            }); return false;
        });

  $("#ajax").on('click', '.c_dislike2', function() {
          var dislike = $(this); var pk = dislike.data('id'); var uuid = dislike.data('uuid'); var like = dislike.prev().prev();
          $.ajax({
              url: "/votes/community_comment/" + uuid + "/" + pk + "/dislike/",
              type: 'POST',
              data: { 'obj': pk },
              success: function(json) {
                like.find("[data-count='like']").text(json.like_count); like.find(".svg_default").removeClass('svg_success'); like.find(".likes_count").removeClass('svg_success'); like.siblings('.like_window').html('').load("/window/c_like_window/" + uuid + "/" + pk + "/");
                dislike.find("[data-count='dislike']").text(json.dislike_count); dislike.find(".svg_default").toggleClass('svg_danger'); dislike.find(".dislikes_count").toggleClass('svg_danger'); dislike.siblings('.dislike_window').html('').load("/window/c_dislike_window/" + uuid + "/" + pk + "/")
              }
          });   return false;
  });


  /*!
     post script of community
    */

  $('#ajax').on('click', '.c_add_post', function() {
    var btn = $(this); var pk = btn.data('pk'); var frm_post = $('#COMM-POST'); var stream = frm_post.parent().next().next();
        $.ajax({
            type: frm_post.attr('method'), url: "/posts/add_post_community/" + pk + "/", data: frm_post.serialize(),
            success: function(data) {
                stream.prepend(data); stream.find(".post_empty").hide(); $(".id_text").val(""); $(".add_board #for_images_upload").hide(); $(".add_board #for_gallery").hide(); $(".add_board #for_doc").hide(); $(".add_board #for_good").hide(); $(".add_board #for_question").hide(); $(".add_board #for_settings").hide();
                $.toast({heading: 'Успешно',text: 'Запись успешно создана!',showHideTransition: 'fade',icon: 'success'})},
            error: function(data) {
                $.toast({heading: 'Ошибка',text: 'Для публикации записи нужно написать что-нибудь и/или вставить изображение(ия)',showHideTransition: 'fade',icon: 'error'})
            }

        }); return false;
    });

    $('#ajax').on('click', '.с_itemComment', function() {
        button1 = $(this); var form1 = button1.parent().parent().parent(); var img_block = button1.parent().prev()
        $.ajax({
            url: '/community/post-comment/', data: new FormData($(form1)[0]), contentType: false, cache: false, processData: false, type: 'POST',
            success: function(data) { $(".form-control-rounded").val(""); form1.parent().prev().prev().append(data); form1.find('.img_block').empty()},
            error: function(data) { $.toast({heading: 'Ошибка',text: 'Для публикации комментария нужно написать что-нибудь и/или вставить изображение(ия)',showHideTransition: 'fade',icon: 'error'}); },
        });
        return false;
    });

    $('#ajax').on('click', '.c_replyComment', function() {
        var button = $(this); var form2 = button.parent().parent().parent().parent(); var block = form2.parent(); var reply_stream = block.next().next(); var pk = button.data('pk'); var uuid = button.data('uuid');
        $.ajax({
            url: '/community/reply-comment/' + uuid + "/" + pk + "/",
            data: new FormData($(form2)[0]),
            contentType: false, cache: false, processData: false, type: 'POST',
            success: function(data) { $(".form-control-rounded").val(""); reply_stream.append(data); reply_stream.addClass("replies_open"); block.hide(); },
            error: function(data) { $.toast({heading: 'Ошибка',text: 'Для публикации ответа нужно написать что-нибудь и/или вставить изображение(ия)',showHideTransition: 'fade',icon: 'error'}) },
        });
        return false;
    });
    $('#ajax').on('click', '.c_replyParentComment', function() {
        var button = $(this); var form3 = button.parent().parent().parent().parent(); var block = form3.parent(); var pk = button.data('pk'); var uuid = button.data('uuid');
        $.ajax({
            url: '/community/reply-comment/' + uuid + "/" + pk + "/",
            data: new FormData($(form3)[0]), contentType: false, cache: false, processData: false, type: 'POST',
            success: function(data) { $(".form-control-rounded").val(""); form3.parent().prev().append(data); block.hide(); },
            error: function(data) { $.toast({heading: 'Ошибка',text: 'Для публикации ответа нужно написать что-нибудь и/или вставить изображение(ия)',showHideTransition: 'fade',icon: 'error'}) },
        });
        return false;
    });
