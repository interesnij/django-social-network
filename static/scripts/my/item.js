
/*!
   card headers manage scripts
  */
$('#ajax').on('click', '.item_user_remove', function() {var remove = $(this); var uuid = remove.parents(".infinite-item").attr("item-id");$.ajax({url: "/user/delete/" + uuid + "/",success: function(data) {$(remove).parents('.card').hide();$('.activefullscreen').hide();$.toast({heading: 'Информация',text: 'Запись успешно удалена!',showHideTransition: 'fade',icon: 'info'})}});});
$('#ajax').on('click', '.item_user_fixed', function() {var fixed = $(this);var uuid = fixed.parents(".infinite-item").attr("item-id");$.ajax({url: "/user/fixed/" + uuid + "/",success: function(data) {fixed.parent().html("<span class='dropdown-item item_user_unfixed'>Открепить</span>");$.toast({heading: 'Информация',text: 'Запись закреплена!',showHideTransition: 'fade',icon: 'info'})}});});
$('#ajax').on('click', '.item_user_unfixed', function() {var unfixed = $(this); var uuid = unfixed.parents(".infinite-item").attr("item-id");$.ajax({url: "/user/unfixed/" + uuid + "/",success: function(data) {unfixed.parent().html("<span class='dropdown-item item_user_fixed'>Закрепить</span>");$.toast({heading: 'Информация',text: 'Запись откреплена!',showHideTransition: 'fade',icon: 'info'})}});});
$('#ajax').on('click', '.item_user_off_comment', function() {var off = $(this);var uuid = off.parents(".infinite-item").attr("item-id");$.ajax({url: "/user/off_comment/" + uuid + "/",success: function(data) {off.parent().html("<span class='dropdown-item item_user_on_comment'>Включить комментарии</span>");$.toast({heading: 'Информация',text: 'Комментарии выключены!',showHideTransition: 'fade',icon: 'info'})}});});
$('#ajax').on('click', '.item_user_on_comment', function() {var on = $(this); var uuid = on.parents(".infinite-item").attr("item-id");$.ajax({url: "/user/on_comment/" + uuid + "/",success: function(data) {on.parent().html("<span class='dropdown-item item_user_off_comment'>Выключить комментарии</span>");$.toast({heading: 'Информация',text: 'Комментарии включены!',showHideTransition: 'fade',icon: 'info'})}});});
$('#ajax').on('click', '.js-textareacopybtn', function() {btn = $(this);link = btn.find('.js-copytextarea');link.focus();link.select();try {var successful = document.execCommand('copy');var msg = successful ? 'successful' : 'unsuccessful';console.log('Copying text command was ' + msg);} catch (err) {console.log('Oops, unable to copy');}});

/*!
   votes post scripts for user items
  */
$("body").on('click', '.u_like', function() {
    like = $(this); item = like.parents('.infinite-item'); var pk = item.attr("user-id"); var uuid = item.attr("item-id"); var dislike = like.next().next();
    $.ajax({url: "/votes/user_like/" + uuid + "/" + pk + "/",type: 'POST',data: {'obj': pk},
        success: function(json) {
            like.find("[data-count='like']").text(json.like_count); like.find(".svg_default").toggleClass('svg_success'); like.find(".likes_count").toggleClass('svg_success'); like.siblings('.like_window').html('').load("/window/u_like_window/" + uuid + "/" + pk + "/");
            dislike.find("[data-count='dislike']").text(json.dislike_count); dislike.find(".svg_default").removeClass('svg_danger'); dislike.find(".dislikes_count").removeClass('svg_danger'); dislike.siblings('.dislike_window').html('').load("/window/u_dislike_window/" + uuid + "/" + pk + "/")
        }
    });return false;
});
$("#ajax").on('click', '.u_dislike', function() {
        var dislike = $(this); item = dislike.parents('.infinite-item');var pk = item.attr("user-id"); var uuid = item.attr("item-id"); var like = dislike.prev().prev();
        $.ajax({
            url: "/votes/user_dislike/" + uuid + "/" + pk + "/", type: 'POST', data: {'obj': pk},
            success: function(json) {
              like.find("[data-count='like']").text(json.like_count); like.find(".svg_default").removeClass('svg_success'); like.find(".likes_count").removeClass('svg_success'); like.siblings('.like_window').html('').load("/window/u_like_window/" + uuid + "/" + pk + "/");
              dislike.find("[data-count='dislike']").text(json.dislike_count); dislike.find(".svg_default").toggleClass('svg_danger'); dislike.find(".dislikes_count").toggleClass('svg_danger'); dislike.siblings('.dislike_window').html('').load("/window/u_dislike_window/" + uuid + "/" + pk + "/")
            }
        });return false;
});

/*!
   votes post scripts for user item comments
  */
$("#ajax").on('click', '.u_like2', function() {
          var like = $(this); var pk = like.data('pk'); var uuid = like.data('uuid'); var dislike = like.next().next();
          $.ajax({
              url: "/votes/user_comment/" + uuid + "/" + pk + "/like/", type: 'POST', data: {'obj': pk},
              success: function(json) {
                  like.find("[data-count='like']").text(json.like_count); like.find(".svg_default").toggleClass('svg_success'); like.find(".likes_count").toggleClass('svg_success'); like.siblings('.comment_like_window').html('').load("/window/u_comment_like_window/" + uuid + "/" + pk + "/");
                  dislike.find("[data-count='dislike']").text(json.dislike_count); dislike.find(".svg_default").removeClass('svg_danger'); dislike.find(".dislikes_count").removeClass('svg_danger'); dislike.siblings('.comment_dislike_window').html('').load("/window/u_comment_dislike_window/" + uuid + "/" + pk + "/")
              }
          });return false;
      });
$("#ajax").on('click', '.u_dislike2', function() {
        var dislike = $(this); var pk = dislike.data('pk'); var uuid = dislike.data('uuid'); var like = dislike.prev().prev();
        $.ajax({
            url: "/votes/user_comment/" + uuid + "/" + pk + "/dislike/", type: 'POST', data: {'obj': pk},
            success: function(json) {
                like.find("[data-count='like']").text(json.like_count); like.find(".svg_default").removeClass('svg_success'); like.find(".likes_count").removeClass('svg_success'); like.siblings('.comment_like_window').html('').load("/window/u_comment_like_window/" + uuid + "/" + pk + "/");
                dislike.find("[data-count='dislike']").text(json.dislike_count); dislike.find(".svg_default").toggleClass('svg_danger'); dislike.find(".dislikes_count").toggleClass('svg_danger'); dislike.siblings('.comment_dislike_window').html('').load("/window/u_comment_dislike_window/" + uuid + "/" + pk + "/")
            }
        });return false;
});

/*!
   comment create scripts
  */

$('#ajax').on('click', '.u_itemComment', function() {
    button1 = $(this); var form1 = button1.parent().parent().parent(); var upload_block = form1.find(".upload_block");
    $.ajax({
        url: '/user/post-comment/', data: new FormData($(form1)[0]), contentType: false, cache: false, processData: false, type: 'POST',
        success: function(data) { $(".form-control-rounded").val(""); form1.parent().prev().append(data); upload_block.empty()},
        error: function(data) { $.toast({heading: 'Ошибка',text: 'Для публикации комментария нужно написать что-нибудь и/или вставить изображение(ия)',showHideTransition: 'fade',icon: 'error'}); },
    });
    return false;
});

$('#ajax').on('click', '.u_replyComment', function() {
    var button = $(this); var form2 = button.parent().parent().parent().parent(); var block = form2.parent(); var upload_block = form2.find(".upload_block"); var reply_stream = block.next().next(); var pk = button.data('pk'); var uuid = button.data('uuid');
    $.ajax({
        url: '/user/reply-comment/' + uuid + "/" + pk + "/", data: new FormData($(form2)[0]), contentType: false, cache: false, processData: false, type: 'POST',
        success: function(data) { $(".form-control-rounded").val(""); reply_stream.append(data); reply_stream.addClass("replies_open"); block.hide(); upload_block.empty(); },
        error: function(data) { $.toast({heading: 'Ошибка',text: 'Для публикации ответа нужно написать что-нибудь и/или вставить изображение(ия)',showHideTransition: 'fade',icon: 'error'}) },
    });
    return false;
});
$('#ajax').on('click', '.u_replyParentComment', function() {
    var button = $(this); var form3 = button.parent().parent().parent().parent(); var block = form3.parent(); var upload_block = form3.find(".upload_block"); var pk = button.data('pk'); var uuid = button.data('uuid'); var reply_stream = block.parents('.stream_reply_comments');
    $.ajax({
        url: '/user/reply-comment/' + uuid + "/" + pk + "/",
        data: new FormData($(form3)[0]), contentType: false, cache: false, processData: false, type: 'POST',
        success: function(data) { $(".form-control-rounded").val(""); reply_stream.append(data); block.hide(); upload_block.empty();},
        error: function(data) { $.toast({heading: 'Ошибка',text: 'Для публикации ответа нужно написать что-нибудь и/или вставить изображение(ия)',showHideTransition: 'fade',icon: 'error'}) },
    });
    return false;
});
