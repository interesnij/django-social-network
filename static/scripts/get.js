/*!
   fullscreen open scripts for user
  */
$('#ajax').on('click', '.u_article_detail', function() {item = $(this).parents(".infinite-item");pk = item.attr("user-id");uuid = item.attr("item-id"); $('#article_loader').html('').load("/article/detail/" + pk + "/" + uuid + "/"); $('.article_fullscreen').show().addClass("article_open_100");console.log("article user open")});
$('#ajax').on('click', '.fullscreen', function() {item = $(this).parents(".infinite-item");pk = item.attr("user-id");uuid = item.attr("item-id");$('#item_loader').html('').load("/users/detail/item/" + pk + "/" + uuid + "/"); $('.item_fullscreen').show();console.log("item user open")});
$('#ajax').on('click', '.avatar_detail', function() {photo = $(this);photo_id = photo.data("id");user_uuid = photo.data("uuid");$('#photo_loader').html('').load("/gallery/load/avatar_detail/" + photo_id + "/" + user_uuid + "/");$('.photo_fullscreen').show();});
$('#ajax').on('click', '.u_photo_detail', function() {photo = $(this); photo_id = photo.data("id"); user_uuid = photo.data("uuid");$('#photo_loader').html('').load("/gallery/load/photo/" + photo_id + "/" + user_uuid + "/");$('.photo_fullscreen').show();console.log("user photo open")});
$('#ajax').on('click', '.u_album_photo_detail', function() {photo = $(this); pk = photo.data("pk"); uuid = photo.parent().data("uuid"); uuid2 = photo.parent().data("uuid2");$('#photo_loader').html('').load("/gallery/load/u_photo/" + pk + "/" + uuid + "/" + uuid2 + "/");$('.photo_fullscreen').show();console.log("user album photo open")});

$('.goods-container').on('click', '.u_good_detail', function() {good = $(this);good_id = good.data("id");user_uuid = good.data("uuid");$('#good_loader').html('').load("/goods/user/good/" + good_id + "/" + user_uuid + "/");$('.good_fullscreen').show();console.log("user good open")});

$('#ajax').on('click', '.u_all_likes', function() {var btn = $(this); item = $(this).parents('.infinite-item');pk = item.attr("user-id");uuid = item.attr("item-id");$('#votes_loader').html('').load("/window/all_user_like/" + uuid + "/" + pk + "/"); $('.votes_fullscreen').show();console.log("likes user open")});
$('#ajax').on('click', '.u_all_dislikes', function() {var btn = $(this); item = $(this).parents('.infinite-item');pk = item.attr("user-id");uuid = item.attr("item-id");$('#votes_loader').html('').load("/window/all_user_dislike/" + uuid + "/" + pk + "/"); $('.votes_fullscreen').show();console.log("dislikes user open")});
$('#ajax').on('click', '.u_all_reposts', function() {var btn = $(this); item = $(this).parents('.infinite-item');pk = item.attr("user-id");uuid = item.attr("item-id");$('#votes_loader').html('').load("/window/all_user_reposts/" + uuid + "/" + pk + "/"); $('.votes_fullscreen').show();console.log("reposts user open")});


$('.add_board_hide').on('click', function() {$('#for_settings').hide();});
$('#images_upload').on('click', function() {$('#for_images_upload').show();});
$('#settings').on('click', function() {$('#for_settings').show();});
$('#gallery').on('click', function() {$('#for_gallery').show();});
$('#doc').on('click', function() {$('#for_doc').show();});
$('#good').on('click', function() {$('#for_good').show();});
$('#question').on('click', function() {$('#for_question').show();});
/*!
   fullscreen open scripts for community
  */
  $('#ajax').on('click', '.c_article_detail', function() {item = $(this).parent();pk = item.attr("community-id");uuid = item.attr("item-id"); $('#article_loader').html('').load("/article/read/" + pk + "/" + uuid + "/"); $('.article_fullscreen').show();console.log("article community open")});
  $('#ajax').on('click', '.c_fullscreen', function() {item = $(this).parent();pk = item.attr("community-id");uuid = item.attr("item-id");$('#item_loader').html('').load("/communities/item/" + pk + "/" + uuid + "/"); $('.item_fullscreen').show();console.log("item community open")});

  $('#ajax').on('click', '.show_staff_window', function() {btn = $(this).parents(".list-group-item");pk = btn.data("pk");uuid = btn.data("uuid");$('#load_staff_window').html('').load("/communities/manage/staff_window/" + pk + "/" + uuid + "/");$('.manage_window_fullscreen').show();console.log("community staff open");});

  $('body').on('click', '.c_all_likes', function() {var btn = $(this); item = $(this).parents('.infinite-item');pk = item.attr("community-id");uuid = item.attr("item-id");$('#votes_loader').html('').load("/window/all_community_like/" + uuid + "/" + pk + "/"); $('.votes_fullscreen').show();console.log("likes community open")});
  $('body').on('click', '.c_all_dislikes', function() {var btn = $(this); item = $(this).parents('.infinite-item');pk = item.attr("community-id");uuid = item.attr("item-id");$('#votes_loader').html('').load("/window/all_community_dislike/" + uuid + "/" + pk + "/"); $('.votes_fullscreen').show();console.log("dislikes community open")});
  $('body').on('click', '.c_all_reposts', function() {var btn = $(this); item = $(this).parents('.infinite-item');pk = item.attr("community-id");uuid = item.attr("item-id");$('#votes_loader').html('').load("/window/all_community_reposts/" + uuid + "/" + pk + "/"); $('.votes_fullscreen').show();console.log("reposts community open")});
  $('#ajax').on('click', '#good_add', function() {$('#good_add_loader').html('').load("{% url 'good_add_community' pk=user.pk %}");$('.good_add_fullscreen').show();})
  $('#ajax').on('click', '.community_add', function() {$('#community_loader').html('').load("/communities/add/progs/");$('.community_fullscreen').show();console.log("add community open")})
  $('#ajax').on('click', '#community_article_add', function() {btn = $(this);pk = btn.data('pk');$('#article_loader').html('').load("/article/add_community/" + pk + "/");$('.article_fullscreen').show();console.log("add community article open")})
  $('#ajax').on('click', '#article_add', function() {$('#article_loader').html('').load("{% url 'article_add_user' pk=user.pk %}"); $('.article_fullscreen').show();})
  $('#ajax').on('click', '.u_photos_add', function() { $('#photos_add_window').show();console.log("user photos add open")})
  $('#ajax').on('click', '.u_albums_add', function() {user = $(this);user_id = user.data("uuid"); $('#photo_add_loader').html('').load("/gallery/user/add_album/" + user_id + "/"); $('.photofullscreen').show();console.log("user album photos add open")})
  $('body').on('click', '.u_photo_edit', function() {$('#block_description_form').show();console.log("user description photo open");});
  $("#u_albums_add").click(function() {$('#photos_add_window').show();console.log("user photo form open")})
  $("#u_albums_add").click(function() {user = $(this);user_id = user.data("uuid");$('#photo_add_loader').html('').load("/gallery/user/add_album/" + user_id + "/");$('.photo_fullscreen').show();console.log("user album add open")})
  /*!
     fullscreen close scripts
    */
  $('.photo_fullscreen_hide').click(function() { $('.photo_fullscreen').hide(); $('#photo_loader').empty();console.log("photo closed") });
  $('.votes_fullscreen_hide').click(function() { $('.votes_fullscreen').hide(); $('#votes_loader').empty();console.log("votes closed") });
  $('.article_fullscreen_hide').click(function() {$('.article_fullscreen').hide(); $('#article_loader').empty();console.log("user article closed")});
  $('.item_fullscreen_hide').click(function() { $('.item_fullscreen').hide(); $('#item_loader').empty(); console.log("user post closed")});
  $('.community_fullscreen_hide').click(function() {$('.community_fullscreen').hide();$('#community_loader').empty(); console.log("community post closed")});
  $('.community_manage_fullscreen_hide').click(function() {$('.manage_window_fullscreen').hide();$('#load_staff_window').empty();console.log("staff community closed")});
  $('.good_fullscreen_hide').click(function() {$('.good_add_fullscreen').hide();$('#good_add_loader').empty();console.log("good closed")});


  /*!
     comments scripts
    */
$('body').on('click', '.show_replies', function() { var element = $(this); element.next().toggleClass('replies_open');console.log("show comment replies") });

$('body').on('click', '.comment_image', function() {photo = $(this);pk = photo.data("id");uuid = photo.data("uuid");$('#photo_loader').html('').load("/gallery/load/comment/" + pk + "/" + uuid + "/"); $('.photo_fullscreen').show();console.log("show user photos for select image")});

$('body').on('click', '.upload_photo', function() {
  btn = $(this); img_block = btn.parent().parent().prev();
  if (!img_block.empty()){img_block.empty()};
  img_block.append('<span class="close_upload_block" title="Закрыть панель загрузки фото"><svg fill="currentColor" style="width:15px" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span><div class="col-lg-6 col-md-6"><a href="#" style="display:none" class="delete_thumb1">Удалить</a><input class="file1 hide_image" type="file" name="photo" accept="image/*" id="id_item_comment_photo"><div class="comment_photo1"><h4 class="svg_default"><svg width="35" height="35" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/>+<path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg></h4></div></div><div class="col-lg-6 col-md-6"><a href="#" style="display:none" class="delete_thumb1">Удалить</a><input class="file2 hide_image" type="file" name="photo2" accept="image/*" id="id_item_comment_photo2"><div class="comment_photo2"><h4 class="svg_default"><svg width="35" height="35" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">+<path d="M0 0h24v24H0z" fill="none"/><path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg></h4></div></div>');img_block.show();console.log("load comment upload block")});

$('body').on('click', '.comment_photo1', function() {img = $(this);entrou = false;imageLoader = img.prev();imageLoader.click();$(imageLoader).on("change", function() {if (!entrou) {imgPath = $(this)[0].value;extn = imgPath.substring(imgPath.lastIndexOf(".") + 1).toLowerCase();if (extn == "gif" || extn == "png" || extn == "jpg" || extn == "jpeg") {if (typeof FileReader != "undefined") {image_holder = $(img); image_holder.empty();reader = new FileReader();reader.onload = function(e) { $img = $("<img />", { id: "targetImageCrop", src: e.target.result, class: "thumb-image" }).appendTo(image_holder); }; image_holder.show(); reader.readAsDataURL($(this)[0].files[0]);} } else { this.value = null; } } entrou = true; setTimeout(function() { entrou = false; }, 1000); img.prev().prev().show();console.log("upload comment image 1")});});

$('body').on('click', '.comment_photo2', function() {img = $(this);entrou = false;imageLoader = img.prev();imageLoader.click();$(imageLoader).on("change", function() {if (!entrou) {imgPath = $(this)[0].value;extn = imgPath.substring(imgPath.lastIndexOf(".") + 1).toLowerCase();if (extn == "gif" || extn == "png" || extn == "jpg" || extn == "jpeg") {if (typeof FileReader != "undefined") {image_holder = $(img); image_holder.empty();reader = new FileReader();reader.onload = function(e) { $img = $("<img />", { id: "targetImageCrop", src: e.target.result, class: "thumb-image" }).appendTo(image_holder); }; image_holder.show(); reader.readAsDataURL($(this)[0].files[0]);} } else { this.value = null; } } entrou = true; setTimeout(function() { entrou = false; }, 1000); img.prev().prev().show();console.log("upload comment image 2")});});

$('body').on('click', '.close_upload_block', function() {$(this).parent().empty();console.log("comment upload block closed")});
$('body').on('click', '.delete_thumb1', function(e) {e.preventDefault(); var a = $(this); a.parent().empty().append('<a href="#" style="display:none" class="delete_thumb1">Удалить</a><input class="file1 hide_image" type="file" name="photo" accept="image/*" id="id_item_comment_photo"><div class="comment_photo1"><h4 class="svg_default"><svg width="35" height="35" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none" /><path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z" /></svg></h4></div>');console.log("comment image deleted")});

$("body").on('click', '.reply_comment', function() {var reply_comment_form = $(this); var objectUser = reply_comment_form.prev().text().trim(); var form = reply_comment_form.next().find(".text-comment"); form.val(objectUser + ', '); reply_comment_form.next().show(); form.focus();console.log("load comment replies form")})

$('body').on('click', '.select_photo', function() {uuid = $(this).data("uuid");$('#photo_loader').html("").load("/users/load/img_load/" + uuid + "/"); $('.photo_fullscreen').show();console.log("select image for comment form")});

$('body').on('click', '.c_item_repost', function() {item = $(this).parents('.infinite-item');item_id = item.attr("item-id"); $('#user_item_pk').html(item_id);});
/*!
   community comments scripts
  */
  $('body').on('click', '.c_comment.comments_close', function() {var btn = $(this); var item = btn.closest(".infinite-item"); var uuid = item.attr("item-id"); var pk = item.attr("community-id"); var container = item.find(".load_comments");$.ajax({url: "/community/comment/" + uuid + "/" + pk + "/", data: {'uuid': uuid}, cache: false,beforeSend: function() {item.find(".load_comments").html("<span style='display:flex;justify-content: center;'><img src='/static/images/loading.gif'></span>");},success:function(data){container.html(data.comments);btn.addClass("comments_open").removeClass("comments_close");console.log("show comments community")}}); return false;});

  $('body').on('click', '.c_comment.comments_open', function() {var btn = $(this); var item = btn.closest(".infinite-item"); var container = item.find(".load_comments");container.empty(); btn.removeClass('comments_open').addClass("comments_close");console.log("hide comments community")});


/*!
   user comments scripts
  */
  $('body').on('click', '.u_comment.comments_close', function() {btn = $(this);item = btn.closest(".infinite-item");uuid = item.attr("item-id");pk = item.attr("user-id");container = item.find(".load_comments");$.ajax({url: "/user/comment/" + uuid + "/" + pk + "/", data: {'uuid': uuid}, cache: false,beforeSend: function() { item.find(".load_comments").html("<span style='display:flex;justify-content: center;'><img src='/static/images/loading.gif'></span>"); },success: function(data) {   container.html(data.comments);btn.addClass("comments_open").removeClass("comments_close");console.log("show comments")}}); return false;});
  $('body').on('click', '.u_comment.comments_open', function() {btn = $(this);item = btn.closest(".infinite-item");container = item.find(".load_comments");container.empty();btn.removeClass('comments_open').addClass("comments_close");console.log("hide comments");});


/*!
   Infinite scripts
  */
  var goods_infinite = new Waypoint.Infinite({
      element: $('.goods-container')[0], onBeforePageLoad: function() { $('.load').show(); }, onAfterPageLoad: function($items) { $('.load').hide(); }
  });
  var lenta = new Waypoint.Infinite({
      element: $('.lenta-container')[0], onBeforePageLoad: function() { $('.items-load').show(); }, onAfterPageLoad: function($items) { $('.items-load').hide(); }
  });
  var infinite = new Waypoint.Infinite({
      element: $('.communities_manage_container')[0], onBeforePageLoad: function() { $('.c_load').show(); }, onAfterPageLoad: function($items) { $('.c_load').hide(); }
  });
  var infinite = new Waypoint.Infinite({
      element: $('.communities_container')[0], onBeforePageLoad: function() { $('.communities_load').show(); }, onAfterPageLoad: function($items) { $('.communities_load').hide(); }
  });

  
  /*!
       music scripts for user
    */
$('body').on('click', '.jp-playlist-current .track_item', function() {track = $(this); li = track.parents('.infinite-item'); track_id = li.data('counter');my_playlist_stop(track_id); li.addClass("playlist_pause");});
