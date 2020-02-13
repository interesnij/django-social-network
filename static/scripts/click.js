/*!
   fullscreen open/close scripts
  */

$('#ajax').on('click', '.u_article_detail', function() {var item = $(this).parents(".infinite-item"); var pk = item.attr("user-id");  var uuid = item.attr("item-id"); $('#article_loader').html('').load("/article/detail/" + pk + "/" + uuid + "/"); $('.article_fullscreen').show().addClass("article_open_100");console.log("article user open")});
$('#ajax').on('click', '.fullscreen', function() {var item = $(this).parents(".infinite-item"); var pk = item.attr("user-id"); var uuid = item.attr("item-id");$('#item_loader').html('').load("/users/detail/item/" + pk + "/" + uuid + "/"); $('.item_fullscreen').show();console.log("item user open")});
$('#ajax').on('click', '.u_all_likes', function() {var btn = $(this); item = $(this).parents('.infinite-item'); var pk = item.attr("user-id"); var uuid = item.attr("item-id");$('#votes_loader').html('').load("/window/all_user_like/" + uuid + "/" + pk + "/"); $('.votes_fullscreen').show();console.log("likes user open")});
$('#ajax').on('click', '.u_all_dislikes', function() {var btn = $(this); item = $(this).parents('.infinite-item'); var pk = item.attr("user-id"); var uuid = item.attr("item-id");$('#votes_loader').html('').load("/window/all_user_dislike/" + uuid + "/" + pk + "/"); $('.votes_fullscreen').show();console.log("dislikes user open")});
$('#ajax').on('click', '.u_all_reposts', function() {var btn = $(this); item = $(this).parents('.infinite-item'); var pk = item.attr("user-id"); var uuid = item.attr("item-id");$('#votes_loader').html('').load("/window/all_user_reposts/" + uuid + "/" + pk + "/"); $('.votes_fullscreen').show();console.log("reposts user open")});
$('.photo_fullscreen_hide').click(function() { $('.photo_fullscreen').hide(); $('#photo_loader').empty();console.log("photo closed") });
$('.votes_fullscreen_hide').click(function() { $('.votes_fullscreen').hide(); $('#votes_loader').empty();console.log("votes closed") });
$('.article_fullscreen_hide').click(function() {$('.article_fullscreen').hide(); $('#article_loader').empty();console.log("article closed")});
$('.item_fullscreen_hide').click(function() { $('.item_fullscreen').hide(); $('#item_loader').empty(); console.log("post closed")});
