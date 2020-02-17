/*!
   item post scripts for user
  */

  $("body").on('click', '.u_like', function() {
      like = $(this); item = like.parents('.infinite-item');pk = item.attr("user-id");uuid = item.attr("item-id");dislike = like.next().next();
      $.ajax({url: "/votes/user_like/" + uuid + "/" + pk + "/",type: 'POST',data: {'obj': pk},
          success: function(json) {
              like.find("[data-count='like']").text(json.like_count); like.toggleClass('btn_success btn_default'); like.next().html('').load("/window/u_like_window/" + uuid + "/" + pk + "/");
              dislike.find("[data-count='dislike']").text(json.dislike_count); dislike.removeClass('btn_danger').addClass("btn_default"); dislike.next().html('').load("/window/u_dislike_window/" + uuid + "/" + pk + "/")
          }
      });return false;
  });
  $("body").on('click', '.u_dislike', function() {
          dislike = $(this); item = dislike.parents('.infinite-item');pk = item.attr("user-id");uuid = item.attr("item-id");like = dislike.prev().prev();
          $.ajax({
              url: "/votes/user_dislike/" + uuid + "/" + pk + "/", type: 'POST', data: {'obj': pk},
              success: function(json) {
                like.find("[data-count='like']").text(json.like_count); like.removeClass('btn_success').addClass("btn_default"); like.next().html('').load("/window/u_like_window/" + uuid + "/" + pk + "/");
                dislike.find("[data-count='dislike']").text(json.dislike_count); dislike.toggleClass('btn_danger btn_default'); dislike.next().html('').load("/window/u_dislike_window/" + uuid + "/" + pk + "/")
              }
          });return false;
  });

  $("body").on('click', '.u_like2', function() {
            like = $(this);pk = like.data('pk');uuid = like.data('uuid');dislike = like.next().next();
            $.ajax({
                url: "/votes/user_comment/" + uuid + "/" + pk + "/like/", type: 'POST', data: {'obj': pk},
                success: function(json) {
                    like.find("[data-count='like']").text(json.like_count); like.toggleClass('btn_success btn_default'); like.next().html('').load("/window/u_comment_like_window/" + uuid + "/" + pk + "/");
                    dislike.find("[data-count='dislike']").text(json.dislike_count); dislike.removeClass('btn_danger').addClass("btn_default"); dislike.next().html('').load("/window/u_comment_dislike_window/" + uuid + "/" + pk + "/")
                }
            });return false;
        });
  $("body").on('click', '.u_dislike2', function() {
          dislike = $(this);pk = dislike.data('pk');uuid = dislike.data('uuid');like = dislike.prev().prev();
          $.ajax({
              url: "/votes/user_comment/" + uuid + "/" + pk + "/dislike/", type: 'POST', data: {'obj': pk},
              success: function(json) {
                  like.find("[data-count='like']").text(json.like_count); like.removeClass('btn_success').addClass("btn_default"); like.next().html('').load("/window/u_comment_like_window/" + uuid + "/" + pk + "/");
                  dislike.find("[data-count='dislike']").text(json.dislike_count); dislike.toggleClass('btn_danger btn_default'); dislike.next().html('').load("/window/u_comment_dislike_window/" + uuid + "/" + pk + "/")
              }
          });return false;
  });
