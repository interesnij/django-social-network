$('#ajax .stream').on('click', '.article_detail', function() {
    var item = $(this);
    var item_id = item.data("id");
    $('#article_loader').html('').load("/article/detail/" + item_id)
    $('.article_fullscreen').show();
});
$('#ajax').on('click', '.fullscreen', function() {
    var item = $(this);
    var item_pk = item.data("pk");
    var user_uuid = item.data("uuid");
    $('#item_loader').html('').load("/users/detail/item/" + item_pk + "/" + user_uuid + "/")
    $('.item_fullscreen').show();
});
$('#ajax').on('click', '.c_fullscreen', function() {
    var item = $(this);
    var pk = item.data("pk");
    var uuid = item.data("uuid");
    $('#item_loader').html('').load("/communities/item/" + pk + "/" + uuid + "/")
    $('.item_fullscreen').show();
});
$('.item_fullscreen_hide').on('click', function() {
    $('.item_fullscreen').hide();
    $('#item_loader').empty();
});
$('#ajax').on('click', '.show_replies', function() {
    var element = $(this);
    element.next().toggleClass('replies_open');
});


$('#ajax').on('click', '.u_comment', function() {
    var item = $(this).closest(".infinite-item");
    var uuid = item.attr("item-id");
    var pk = $(this).data('pk');
    $.ajax({
        url: "/user/comment/" + uuid + "/" + pk + "/",
        data: {'uuid': uuid},
        cache: false,
        beforeSend: function() {
            item.find(".load_comments").html("<span style='display:flex;justify-content: center;'><img src='/static/images/loading.gif'></span>");
        },
        success: function(data) {
            item.find(".load_comments").html(data.comments);
        }
    });
    return false;
});

$('#ajax').on('click', '.c_comment', function() {
    var item = $(this).closest(".infinite-item").attr("item-id");
    var pk = $(this).data('pk');
    $.ajax({
        url: "/community/comment/" + item + "/" + pk + "/",
        data: {'item': item},
        cache: false,
        beforeSend: function() {
            url.find(".load_comments").html("<span style='display:flex;justify-content: center;'><img src='/static/images/loading.gif'></span>");
        },
        success: function(data) {
            url.find(".load_comments").html(data.comments);
        }
    });
    return false;
});


$('#ajax').on('click', '.remove', function() {
    var remove = $(this);
    var pk = remove.data('id');
    var uuid = remove.data('uuid');
    $.ajax({
        url: "/user/delete/" + pk + "/" + uuid + "/",
        success: function(data) {
            $(remove).parents('.card').hide();
            $('.activefullscreen').hide();
            $.toast({heading: 'Информация',text: 'Запись успешно удалена!',showHideTransition: 'fade',icon: 'info'})
        },
        error: function(data) {}
    });
});


$('#ajax').on('click', '.fixed', function() {
    var fixed = $(this);
    var pk = fixed.parent().data('id');
    var uuid = fixed.parent().data('uuid');
    $.ajax({
        url: "/user/fixed/" + pk + "/" + uuid + "/",
        success: function(data) {
            fixed.parent().html("<span style='cursor:pointer' class='dropdown-item unfixed'>Открепить</span>");
            $.toast({heading: 'Информация',text: 'Запись закреплена!',showHideTransition: 'fade',icon: 'info'})
        }
    });
});

$('#ajax').on('click', '.unfixed', function() {
    var unfixed = $(this);
    var pk = unfixed.parent().data('id');
    var uuid = unfixed.parent().data('uuid');
    $.ajax({
        url: "/user/unfixed/" + pk + "/" + uuid + "/",
        success: function(data) {
            unfixed.parent().html("<span style='cursor:pointer' class='dropdown-item fixed'>Закрепить</span>");
            $.toast({heading: 'Информация',text: 'Запись откреплена!',showHideTransition: 'fade',icon: 'info'})
        }
    });
});

$('#ajax').on('click', '.u_itemComment', function() {
    button1 = $(this);
    var pk = button1.data('pk');
    var uuid = button1.data('uuid');
    form1 = button1.parent().parent().parent();
    $.ajax({
        url: '/user/post-comment/' + uuid + "/" + pk + "/",
        data: new FormData($(form1)[0]),
        contentType: false,
        cache: false,
        processData: false,
        type: 'POST',
        success: function(data) {
            $(".form-control-rounded").val("");
            $(".stream_comments").append(data);
        },
        error: function(data) {
            $.toast({heading: 'Ошибка',text: 'Для публикации комментария нужно написать что-нибудь и/или вставить изображение(ия)',showHideTransition: 'fade',icon: 'error'});
        },
    });
    return false;
});

$('#ajax').on('click', '.u_replyComment', function() {
    var button = $(this);
    var form2 = button.parent().parent().parent().parent();
    var block = form2.parent();
    var pk = button.data('pk');
    var uuid = button.data('uuid');
    $.ajax({
        url: '/user/reply-comment/' + uuid + "/" + pk + "/",
        data: new FormData($(form2)[0]),
        contentType: false,
        cache: false,
        processData: false,
        type: 'POST',
        success: function(data) {
            $(".form-control-rounded").val("");
            $(".stream_reply_comments").append(data);
            block.hide();
        },
        error: function(data) {
            $.toast({heading: 'Ошибка',text: 'Для публикации ответа нужно написать что-нибудь и/или вставить изображение(ия)',showHideTransition: 'fade',icon: 'error'})
        },
    });
    return false;
});

$('#ajax').on('click', '.u_replyParentComment', function() {
    var button = $(this);
    var form3 = button.parent().parent().parent().parent();
    var block = form3.parent();
    var pk = button.data('pk');
    var uuid = button.data('uuid');
    $.ajax({
        url: '/user/reply-comment/' + uuid + "/" + pk + "/",
        data: new FormData($(form3)[0]),
        contentType: false,
        cache: false,
        processData: false,
        type: 'POST',
        success: function(data) {
            $(".form-control-rounded").val("");
            $(".stream_reply_comments").append(data);
            block.hide();
        },
        error: function(data) {
            $.toast({heading: 'Ошибка',text: 'Для публикации ответа нужно написать что-нибудь и/или вставить изображение(ия)',showHideTransition: 'fade',icon: 'error'})
        },
    });
    return false;
});

$("#ajax").on('click', '.reply_comment', function() {
    var reply_comment_form = $(this);
    var objectUser = reply_comment_form.prev().text().trim();
    var form = reply_comment_form.next().find(".text-comment");
    form.val(objectUser + ', ');
    reply_comment_form.next().show();
    form.focus();
})

$('.R_U').on('click', function() {
    var item = $(this);
    var item_id = item.data("uuid");
    $('#user_item_pk').html(item_id);
    var pk = item.data("pk");
});


$("#ajax").on('click', '.u_like', function() {
    var like = $(this);
    var pk = like.data('id');
		var uuid = like.data('uuid');
    var dislike = like.next().next();
    $.ajax({
        url: "/votes/user_like/" + uuid + "/" + pk + "/",
        type: 'POST',
        data: {
            'obj': pk
        },
        success: function(json) {
            like.find("[data-count='like']").text(json.like_count);
            dislike.find("[data-count='dislike']").text(json.dislike_count);
            like.find(".svg_default").toggleClass('svg_success');
            like.find(".likes_count").toggleClass('svg_success');
            like.siblings('.like_window').html('').load("/votes/like_window/" + uuid + "/" + pk + "/");
            dislike.siblings('.dislike_window').html('').load("/votes/dislike_window/" + uuid + "/" + pk + "/")

        }
    });
    return false;
});

$("#ajax").on('click', '.u_dislike', function() {
        var dislike = $(this);
        var pk = dislike.data('id');
        var uuid = dislike.data('uuid');
        var like = dislike.prev().prev();
        $.ajax({
            url: "/votes/user_dislike/" + uuid + "/" + pk + "/",
            type: 'POST',
            data: {
                'obj': pk
            },
            success: function(json) {
                dislike.find("[data-count='dislike']").text(json.dislike_count);
                like.find("[data-count='like']").text(json.like_count);
                dislike.find(".dislike").hide();
                dislike.find(".dislike_act").show();
                like.find(".like_act").hide();
                like.find(".like").show();
                like.siblings('.like_window').html('').load("/votes/like_window/" + uuid + "/" + pk + "/");
                dislike.siblings('.dislike_window').html('').load("/votes/dislike_window/" + uuid + "/" + pk + "/")
            }
        });
        return false;
});

$("#ajax").on('click', '.u_like2', function() {
          var like = $(this);
          var pk = like.data('id');
          var uuid = like.data('uuid');
          var dislike = like.next().next();
          $.ajax({
              url: "/votes/user_comment/" + uuid + "/" + pk + "/like/",
              type: 'POST',
              data: {
                  'obj': pk
              },
              success: function(json) {
                  like.find("[data-count='like']").text(json.like_count);
                  dislike.find("[data-count='dislike']").text(json.dislike_count);
                  like.find(".like").hide();
                  like.find(".like_act").show();
                  dislike.find(".dislike").show();
                  dislike.find(".dislike_act").hide();
                  like.siblings('.comment_like_window').html('').load("/votes/comment_like_window/" + uuid + "/" + pk + "/");
                  dislike.siblings('.comment_dislike_window').html('').load("/votes/comment_dislike_window/" + uuid + "/" + pk + "/")
              }
          });
          return false;
      });

$("#ajax").on('click', '.u_dislike2', function() {
        var dislike = $(this);
        var pk = dislike.data('id');
        var uuid = dislike.data('uuid');
        var like = dislike.prev().prev();
        $.ajax({
            url: "/votes/user_comment/" + uuid + "/" + pk + "/dislike/",
            type: 'POST',
            data: {
                'obj': pk
            },
            success: function(json) {
                dislike.find("[data-count='dislike']").text(json.dislike_count);
                like.find("[data-count='like']").text(json.like_count);
                dislike.find(".dislike").hide();
                dislike.find(".dislike_act").show();
                like.find(".like_act").hide();
                like.find(".like").show();
                like.siblings('.comment_like_window').html('').load("/votes/comment_like_window/" + uuid + "/" + pk + "/");
                dislike.siblings('.comment_dislike_window').html('').load("/votes/comment_dislike_window/" + uuid + "/" + pk + "/")
            }
        });
        return false;
});

$("#ajax").on('click', '.c_like', function() {
    var like = $(this);
    var pk = like.data('id');
		var uuid = like.data('uuid');
    var dislike = like.next().next();
    $.ajax({
        url: "/votes/community_like/" + uuid + "/" + pk + "/",
        type: 'POST',
        data: {
            'obj': pk
        },
        success: function(json) {
            like.find("[data-count='like']").text(json.like_count);
            dislike.find("[data-count='dislike']").text(json.dislike_count);
            $(".like").addClass("text-success");
            $(".dislike").removeClass("text-danger");
        }
    });
    return false;
});

$("#ajax").on('click', '.c_dislike', function() {
        var dislike = $(this);
        var pk = dislike.data('id');
        var uuid = dislike.data('uuid');
        var like = dislike.prev().prev();
        $.ajax({
            url: "/votes/community_dislike/" + uuid + "/" + pk + "/",
            type: 'POST',
            data: {
                'obj': pk
            },
            success: function(json) {
                dislike.find("[data-count='dislike']").text(json.dislike_count);
                like.find("[data-count='like']").text(json.like_count);
                $(".dislike").addClass("text-danger");
                $(".like").removeClass("text-success");
            }
        });
        return false;
});

$("#ajax").on('click', '.c_like2', function() {
          var like = $(this);
          var pk = like.data('id');
          var uuid = like.data('uuid');
          var dislike = like.next().next();
          $.ajax({
              url: "/votes/community_comment/" + uuid + "/" + pk + "/like/",
              type: 'POST',
              data: {
                  'obj': pk
              },
              success: function(json) {
                  like.find("[data-count='like']").text(json.like_count);
                  dislike.find("[data-count='dislike']").text(json.dislike_count);
                  like.addClass("text-success");
                  dislike.removeClass("text-danger");
              }
          });
          return false;
      });

$("#ajax").on('click', '.c_dislike2', function() {
        var dislike = $(this);
        var pk = dislike.data('id');
        var uuid = dislike.data('uuid');
        var like = dislike.prev().prev();
        $.ajax({
            url: "/votes/community_comment/" + uuid + "/" + pk + "/dislike/",
            type: 'POST',
            data: {
                'obj': pk
            },
            success: function(json) {
                dislike.find("[data-count='dislike']").text(json.dislike_count);
                like.find("[data-count='like']").text(json.like_count);
                dislike.addClass("text-danger");
                like.removeClass("text-success");
            }
        });
        return false;
});
