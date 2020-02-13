/*!
   fullscreen open scripts for user
  */
$('#ajax').on('click', '.u_article_detail', function() {item = $(this).parents(".infinite-item");pk = item.attr("user-id");uuid = item.attr("item-id"); $('#article_loader').html('').load("/article/detail/" + pk + "/" + uuid + "/"); $('.article_fullscreen').show().addClass("article_open_100");console.log("article user open")});
$('#ajax').on('click', '.fullscreen', function() {item = $(this).parents(".infinite-item");pk = item.attr("user-id");uuid = item.attr("item-id");$('#item_loader').html('').load("/users/detail/item/" + pk + "/" + uuid + "/"); $('.item_fullscreen').show();console.log("item user open")});

$('#ajax').on('click', '.u_photo_detail', function() {photo = $(this); photo_id = photo.data("id"); user_uuid = photo.data("uuid");$('#photo_loader').html('').load("/gallery/load/photo/" + photo_id + "/" + user_uuid + "/");$('.photo_fullscreen').show();console.log("user photo open")});
$('#ajax').on('click', '.u_album_photo_detail', function() {photo = $(this); pk = photo.data("pk"); uuid = photo.parent().data("uuid"); uuid2 = photo.parent().data("uuid2");$('#photo_loader').html('').load("/gallery/load/u_photo/" + pk + "/" + uuid + "/" + uuid2 + "/");$('.photo_fullscreen').show();console.log("user album photo open")});

$('.goods-container').on('click', '.u_good_detail', function() {good = $(this);good_id = good.data("id");user_uuid = good.data("uuid");$('#good_loader').html('').load("/goods/user/good/" + good_id + "/" + user_uuid + "/");$('.good_fullscreen').show();console.log("user good open")});

$('#ajax').on('click', '.u_all_likes', function() {var btn = $(this); item = $(this).parents('.infinite-item');pk = item.attr("user-id");uuid = item.attr("item-id");$('#votes_loader').html('').load("/window/all_user_like/" + uuid + "/" + pk + "/"); $('.votes_fullscreen').show();console.log("likes user open")});
$('#ajax').on('click', '.u_all_dislikes', function() {var btn = $(this); item = $(this).parents('.infinite-item');pk = item.attr("user-id");uuid = item.attr("item-id");$('#votes_loader').html('').load("/window/all_user_dislike/" + uuid + "/" + pk + "/"); $('.votes_fullscreen').show();console.log("dislikes user open")});
$('#ajax').on('click', '.u_all_reposts', function() {var btn = $(this); item = $(this).parents('.infinite-item');pk = item.attr("user-id");uuid = item.attr("item-id");$('#votes_loader').html('').load("/window/all_user_reposts/" + uuid + "/" + pk + "/"); $('.votes_fullscreen').show();console.log("reposts user open")});


/*!
   fullscreen open scripts for community
  */
  $('#ajax').on('click', '.c_article_detail', function() {item = $(this).parent();pk = item.attr("community-id");uuid = item.attr("item-id"); $('#article_loader').html('').load("/article/read/" + pk + "/" + uuid + "/"); $('.article_fullscreen').show();console.log("article community open")});
  $('#ajax').on('click', '.c_fullscreen', function() {item = $(this).parent();pk = item.attr("community-id");uuid = item.attr("item-id");$('#item_loader').html('').load("/communities/item/" + pk + "/" + uuid + "/"); $('.item_fullscreen').show();console.log("item community open")});

  $('#ajax').on('click', '.show_staff_window', function() {btn = $(this).parents(".list-group-item");pk = btn.data("pk");uuid = btn.data("uuid");$('#load_staff_window').html('').load("/communities/manage/staff_window/" + pk + "/" + uuid + "/");$('.manage_window_fullscreen').show();console.log("community staff open");});

  $('#ajax').on('click', '.c_all_likes', function() {var btn = $(this); item = $(this).parents('.infinite-item');pk = item.attr("community-id");uuid = item.attr("item-id");$('#votes_loader').html('').load("/window/all_community_like/" + uuid + "/" + pk + "/"); $('.votes_fullscreen').show();console.log("likes community open")});
  $('#ajax').on('click', '.c_all_dislikes', function() {var btn = $(this); item = $(this).parents('.infinite-item');pk = item.attr("community-id");uuid = item.attr("item-id");$('#votes_loader').html('').load("/window/all_community_dislike/" + uuid + "/" + pk + "/"); $('.votes_fullscreen').show();console.log("dislikes community open")});
  $('#ajax').on('click', '.c_all_reposts', function() {var btn = $(this); item = $(this).parents('.infinite-item');pk = item.attr("community-id");uuid = item.attr("item-id");$('#votes_loader').html('').load("/window/all_community_reposts/" + uuid + "/" + pk + "/"); $('.votes_fullscreen').show();console.log("reposts community open")});


  /*!
     fullscreen close scripts
    */
  $('.photo_fullscreen_hide').click(function() { $('.photo_fullscreen').hide(); $('#photo_loader').empty();console.log("photo closed") });
  $('.votes_fullscreen_hide').click(function() { $('.votes_fullscreen').hide(); $('#votes_loader').empty();console.log("votes closed") });
  $('.article_fullscreen_hide').click(function() {$('.article_fullscreen').hide(); $('#article_loader').empty();console.log("user article closed")});
  $('.item_fullscreen_hide').click(function() { $('.item_fullscreen').hide(); $('#item_loader').empty(); console.log("user post closed")});
  $('.community_fullscreen_hide').click(function() {$('.community_fullscreen').hide();$('#community_loader').empty(); console.log("community post closed")});
  $('.community_manage_fullscreen_hide').click(function() {$('.manage_window_fullscreen').hide();$('#load_staff_window').empty();console.log("staff community closed")});
  $('.photo_fullscreen_hide').click(function() {$('.photo_fullscreen').hide();$('#photo_loader').empty();console.log("community add closed")});
  $('.good_fullscreen_hide').click(function() {$('.good_add_fullscreen').hide();$('#good_add_loader').empty();console.log("good closed")});
