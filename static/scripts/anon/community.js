/*!
   fullscreen's script of community
  */
$('#ajax').on('click', '.article_detail', function() {var item = $(this); var item_id = item.data("id");$('#article_loader').html('').load("/article/detail/" + item_id); $('.article_fullscreen').show();});
$('#ajax').on('click', '.c_fullscreen', function() {var item = $(this); var pk = item.data("pk"); var uuid = item.data("uuid");$('#item_loader').html('').load("/communities/item/" + pk + "/" + uuid + "/"); $('.item_fullscreen').show();});
$('#ajax').on('click', '.c_all_likes', function() {var btn = $(this); item = $(this).parents('.interaction'); var pk = item.data("pk"); var uuid = item.data("uuid");$('#votes_loader').html('').load("/window/all_community_like/" + uuid + "/" + pk + "/"); $('.votes_fullscreen').show();});
$('#ajax').on('click', '.c_all_dislikes', function() {var btn = $(this); item = $(this).parents('.interaction'); var pk = item.data("pk"); var uuid = item.data("uuid");$('#votes_loader').html('').load("/window/all_community_dislike/" + uuid + "/" + pk + "/"); $('.votes_fullscreen').show();});
$('#ajax').on('click', '.c_all_reposts', function() {var btn = $(this); item = $(this).parents('.interaction'); var pk = item.data("pk"); var uuid = item.data("uuid");$('#votes_loader').html('').load("/window/all_community_reposts/" + uuid + "/" + pk + "/"); $('.votes_fullscreen').show();});

$('#ajax').on('click', '.photo_fullscreen_hide', function() { $('.photo_fullscreen').hide(); $('#photo_loader').empty(); });
$('#ajax').on('click', '.item_fullscreen_hide', function() { $('.item_fullscreen').hide(); $('#item_loader').empty(); });
$('#ajax').on('click', '.votes_fullscreen_hide', function() { $('.votes_fullscreen').hide(); $('#votes_loader').empty(); });
$('#ajax').on('click', '.article_fullscreen_hide', function() {$('.article_fullscreen').hide(); $('#article_loader').empty();});


/*!
   get comment script of community
  */
$('#ajax').on('click', '.c_comment.comments_close', function() {var btn = $(this); var item = btn.closest(".infinite-item"); var uuid = item.attr("item-id"); var pk = btn.data('pk'); var container = item.find(".load_comments");$.ajax({url: "/community/comment/" + uuid + "/" + pk + "/", data: {'uuid': uuid}, cache: false,beforeSend: function() {item.find(".load_comments").html("<span style='display:flex;justify-content: center;'><img src='/static/images/loading.gif'></span>");},success:function(data){container.html(data.comments);btn.addClass("comments_open").removeClass("comments_close");}}); return false;});

$('#ajax').on('click', '.c_comment.comments_open', function() {var btn = $(this); var item = btn.closest(".infinite-item"); var container = item.find(".load_comments");container.empty(); btn.removeClass('comments_open').addClass("comments_close");});
