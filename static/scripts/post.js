/*!
   item post scripts for user
  */

  $("body").on('click', '.u_like', function() {
      like = $(this); item = like.parents('.infinite-item');pk = item.attr("user-id");uuid = item.attr("item-id");dislike = like.next().next();
      $.ajax({url: "/votes/user_like/" + uuid + "/" + pk + "/",type: 'POST',data: {'obj': pk},
          success: function(json) {
              like.find("[data-count='like']").text(json.like_count); like.toggleClass('btn_success'); like.next().html('').load("/window/u_like_window/" + uuid + "/" + pk + "/");
              dislike.find("[data-count='dislike']").text(json.dislike_count); dislike.removeClass('btn_danger'); dislike.next().html('').load("/window/u_dislike_window/" + uuid + "/" + pk + "/")
          }
      });return false;
  });
  $("body").on('click', '.u_dislike', function() {
          dislike = $(this); item = dislike.parents('.infinite-item');pk = item.attr("user-id");uuid = item.attr("item-id");like = dislike.prev().prev();
          $.ajax({
              url: "/votes/user_dislike/" + uuid + "/" + pk + "/", type: 'POST', data: {'obj': pk},
              success: function(json) {
                like.find("[data-count='like']").text(json.like_count); like.removeClass('btn_success'); like.removeClass('btn_success'); like.next().html('').load("/window/u_like_window/" + uuid + "/" + pk + "/");
                dislike.find("[data-count='dislike']").text(json.dislike_count); dislike.toggleClass('btn_danger'); dislike.next().html('').load("/window/u_dislike_window/" + uuid + "/" + pk + "/")
              }
          });return false;
  });
