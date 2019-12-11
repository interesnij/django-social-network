
  $('#ajax').on('click', '.member_create', function() {
    var member_create = $(this);
    var pk = member_create.data('id');
  $.ajax({
      url: "/communities/add_community_member/" + pk + "/",
      success: function () {
        $('#ajax').html('').load("/communities/reload/" + pk + "/");
      }
  });
  });

  $('#ajax').on('click', '.member_delete', function() {
    var member_delete = $(this);
    var pk = member_delete.data('id');
  $.ajax({
      url: "/communities/delete_community_member/" + pk + "/",
      success: function () {
        $('#ajax').html('').load("/communities/reload/" + pk + "/");
      }
  });
  });

  $('#ajax').on('click', '.member_follow_create', function() {
    var member_follow_create = $(this);
    var pk = member_follow_create.data('id');
  $.ajax({
      url: "/follows/add_member/" + pk + "/",
      success: function () {
        $('#ajax').html('').load("/communities/reload/" + pk + "/");
      }
  });
  });

  $('#ajax').on('click', '.member_follow_delete', function() {
    var member_follow_delete = $(this);
    var pk = member_follow_delete.data('id');
  $.ajax({
      url: "/follows/delete_member/" + pk + "/",
      success: function () {
        $('#ajax').html('').load("/communities/reload/" + pk + "/");
      }
  });
  });

  $('#ajax').on('click', '.c_comment.comments_close', function() {
    var btn = $(this); var item = btn.closest(".infinite-item"); var uuid = item.attr("item-id"); var pk = btn.data('pk'); var container = item.find(".load_comments");
      $.ajax({
          url: "/community/comment/" + item + "/" + pk + "/", data: {'item': item}, cache: false,
          beforeSend: function() { url.find(".load_comments").html("<span style='display:flex;justify-content: center;'><img src='/static/images/loading.gif'></span>"); },
          success: function(data) { container.html(data.comments); btn.addClass("comments_open").removeClass("comments_close")}
      }); return false;
  });
  $('#ajax').on('click', '.c_comment.comments_open', function() {
    var btn = $(this); var item = btn.closest(".infinite-item"); var container = item.find(".load_comments");
    container.empty(); btn.removeClass('comments_open').addClass("comments_close");
  });

  $("#ajax").on('click', '.c_like', function() {
      var like = $(this); var pk = like.data('id'); var uuid = like.data('uuid'); var dislike = like.next().next();
      $.ajax({
          url: "/votes/community_like/" + uuid + "/" + pk + "/", type: 'POST', data: {'obj': pk},
          success: function(json) {
            like.find("[data-count='like']").text(json.like_count); like.find(".svg_default").toggleClass('svg_success'); like.find(".likes_count").toggleClass('svg_success'); like.siblings('.like_window').html('').load("/votes/c_like_window/" + uuid + "/" + pk + "/");
            dislike.find("[data-count='dislike']").text(json.dislike_count); dislike.find(".svg_default").removeClass('svg_danger'); dislike.find(".dislikes_count").removeClass('svg_danger'); dislike.siblings('.dislike_window').html('').load("/votes/c_dislike_window/" + uuid + "/" + pk + "/")
          }
      }); return false;
  });

  $("#ajax").on('click', '.c_dislike', function() {
          var dislike = $(this); var pk = dislike.data('id'); var uuid = dislike.data('uuid'); var like = dislike.prev().prev();
          $.ajax({
              url: "/votes/community_dislike/" + uuid + "/" + pk + "/", type: 'POST', data: {'obj': pk},
              success: function(json) {
                like.find("[data-count='like']").text(json.like_count); like.find(".svg_default").removeClass('svg_success'); like.find(".likes_count").removeClass('svg_success'); like.siblings('.like_window').html('').load("/votes/c_like_window/" + uuid + "/" + pk + "/");
                dislike.find("[data-count='dislike']").text(json.dislike_count); dislike.find(".svg_default").toggleClass('svg_danger'); dislike.find(".dislikes_count").toggleClass('svg_danger'); dislike.siblings('.dislike_window').html('').load("/votes/c_dislike_window/" + uuid + "/" + pk + "/")
              }
          }); return false;
  });

  $("#ajax").on('click', '.c_like2', function() {
            var like = $(this); var pk = like.data('id'); var uuid = like.data('uuid'); var dislike = like.next().next();
            $.ajax({
                url: "/votes/community_comment/" + uuid + "/" + pk + "/like/", type: 'POST', data: {'obj': pk},
                success: function(json) {
                    like.find("[data-count='like']").text(json.like_count);
                    dislike.find("[data-count='dislike']").text(json.dislike_count);
                    like.addClass("text-success");
                    dislike.removeClass("text-danger");
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
                  dislike.find("[data-count='dislike']").text(json.dislike_count);
                  like.find("[data-count='like']").text(json.like_count);
                  dislike.addClass("text-danger");
                  like.removeClass("text-success");
              }
          });   return false;
  });
