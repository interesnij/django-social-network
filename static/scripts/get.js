on('body', 'click', '.menu_drop', function() {var block = this.nextElementSibling;block.classList.toggle("show");});

on('body', 'click', '#add_multi_comments_photos', function(event) {
  this.previousElementSibling.click();
})

on('body', 'click', '.ajax', function(event) {
  event.preventDefault();
  var url = this.getAttribute('href');
  if (url != window.location.pathname){
    ajax_get_reload(url);
  }
})

on('#ajax', 'click', '.photo_preview_delete', function() {
  parent = this.parentElement;
  block = parent.parentElement;
  parent.remove();
  block.querySelector(".photo") ? null : block.querySelector(".photo_input").parentElement.remove();

  try{ remove_file_dropdown(); is_full_dropdown()} catch { remove_file_attach(), is_full_attach()}
});
on('#ajax', 'click', '.video_preview_delete', function() {
  parent = this.parentElement;
  block = parent.parentElement;
  parent.remove();
  block.querySelector(".video") ? null : block.querySelector(".video_input").parentElement.remove();
  try{ remove_file_dropdown(); is_full_dropdown()} catch { remove_file_attach(), is_full_attach()}
});
on('#ajax', 'click', '.music_preview_delete', function() {
  parent = this.parentElement;
  block = parent.parentElement;
  parent.remove();
  block.querySelector(".music") ? null : block.querySelector(".music_input").parentElement.remove();
  try{ remove_file_dropdown(); is_full_dropdown()} catch { remove_file_attach(), is_full_attach()}
});
on('#ajax', 'click', '.good_preview_delete', function() {
  parent = this.parentElement;
  block = parent.parentElement;
  parent.remove();
  block.querySelector(".good") ? null : block.querySelector(".good_input").parentElement.remove();
  try{ remove_file_dropdown(); is_full_dropdown()} catch { remove_file_attach(), is_full_attach()}
});
on('#ajax', 'click', '.article_preview_delete', function() {
  parent = this.parentElement;
  block = parent.parentElement;
  parent.remove();
  block.querySelector(".article") ? null : block.querySelector(".article_input").parentElement.remove();
  try{ remove_file_dropdown(); is_full_dropdown()} catch { remove_file_attach(), is_full_attach()}
});
//window.addEventListener('popstate', function (e) {window.history.go(-1);});

on('body', 'click', '.next_item', function(event) {
  event.preventDefault();
  var url = this.getAttribute('href');
  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', url, true );
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        elem_ = document.createElement('span');
        elem_.innerHTML = ajax_link.responseText;
        rtr = document.getElementById('item_loader');
        rtr.innerHTML = elem_.innerHTML;
      }
    }
    ajax_link.send();
})
on('body', 'click', '.prev_item', function(event) {
  event.preventDefault();
  var url = this.getAttribute('href');
  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', url, true );
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        elem_ = document.createElement('span');
        elem_.innerHTML = ajax_link.responseText;
        rtr = document.getElementById('item_loader');
        rtr.innerHTML = elem_.innerHTML;
      }
    }
    ajax_link.send();
})

on('body', 'click', '.next_photo', function(event) {
  event.preventDefault();
  var url = this.getAttribute('href');
  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', url, true );
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        elem_ = document.createElement('span');
        elem_.innerHTML = ajax_link.responseText;
        rtr = document.getElementById('photo_loader');
        rtr.innerHTML = elem_.innerHTML;
      }
    }
    ajax_link.send();
})
on('body', 'click', '.prev_photo', function(event) {
  event.preventDefault();
  var url = this.getAttribute('href');
  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', url, true );
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        elem_ = document.createElement('span');
        elem_.innerHTML = ajax_link.responseText;
        rtr = document.getElementById('photo_loader');
        rtr.innerHTML = elem_.innerHTML;
      }
    }
    ajax_link.send();
})

on('#ajax', 'click', '.item_stat_f', function() {
  var parent, pk, uuid, loader
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = parent.getAttribute("item-uuid");
  loader = document.getElementById("stat_loader");
  open_fullscreen("/stat/item/" + uuid + "/", loader)
});

on('#ajax', 'click', '.article_fullscreen_hide', function() {document.querySelector(".article_fullscreen").style.display = "none";document.getElementById("article_loader").innerHTML=""});
on('#ajax', 'click', '.photo_fullscreen_hide', function() {document.querySelector(".photo_fullscreen").style.display = "none";document.getElementById("photo_loader").innerHTML=""});
on('#ajax', 'click', '.votes_fullscreen_hide', function() {document.querySelector(".votes_fullscreen").style.display = "none";document.getElementById("votes_loader").innerHTML=""});
on('#ajax', 'click', '.item_fullscreen_hide', function() {document.querySelector(".item_fullscreen").style.display = "none";document.getElementById("item_loader").innerHTML=""});
on('#ajax', 'click', '.community_fullscreen_hide', function() {document.querySelector(".community_fullscreen").style.display = "none";document.getElementById("community_loader").innerHTML=""});
on('#ajax', 'click', '.community_manage_fullscreen_hide', function() {document.querySelector(".manage_window_fullscreen").style.display = "none";document.getElementById("load_staff_window").innerHTML=""});
on('#ajax', 'click', '.good_fullscreen_hide', function() {document.querySelector(".good_fullscreen").style.display = "none";document.getElementById("good_loader").innerHTML=""});
on('#ajax', 'click', '.stat_fullscreen_hide', function() {document.querySelector(".stat_fullscreen").style.display = "none";document.getElementById("stat_loader").innerHTML=""});
on('body', 'click', '.video_fullscreen_hide', function() {document.querySelector(".video_fullscreen").style.display = "none";document.getElementById("video_loader").innerHTML=""});
on('body', 'click', '.small_video_fullscreen_hide', function() {
  document.querySelector(".video_fullscreen").style.display = "none";
  video_window = document.querySelector(".video_fullscreen");
  video_window.classList.remove("video_fullscreen_resized", "draggable");
  document.body.querySelector(".video_btn_small").style.display = "none";
  document.body.querySelector(".video_btn_big").style.display = "block";
  document.getElementById("video_loader").innerHTML=""
});
on('body', 'click', '.create_fullscreen_hide', function() {document.querySelector(".create_fullscreen").style.display = "none";document.getElementById("create_loader").innerHTML=""});

// END FULLSCREENS //
//--------------------------------------------------------------------//

on('#ajax', 'click', '.show_replies', function() {
  this.nextElementSibling.classList.toggle('replies_open');
});

on('#ajax', 'click', '.reply_comment', function() {
  var objectUser = this.previousElementSibling.innerHTML;
  var form = this.nextElementSibling.querySelector(".text-comment");
  form.value = objectUser + ', ';
  this.nextElementSibling.style.display = "block";
  form.focus();
})

on('#ajax', 'click', '.comment_image', function() {
  var uuid, pk, loader;
  pk = this.getAttribute('photo-pk');
  uuid = this.getAttribute('data-uuid');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/load/comment/" + pk + "/" + uuid + "/", loader)
});


on('#ajax', 'click', '.comment_photo', function() {
  this.classList.add("current_file_dropdown");
  document.body.querySelector(".attach_block") ? (attach_block = document.body.querySelector(".attach_block"), attach_block.innerHTML = "", attach_block.classList.remove("attach_block")) : null;
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/img_comment_load/', loader)
});
on('#ajax', 'click', '.comment_video', function() {
  this.classList.add("current_file_dropdown");
  clear_attach_block();
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/video_load/', loader)
});
on('#ajax', 'click', '.comment_music', function() {
  this.classList.add("current_file_dropdown");
  clear_attach_block();
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/music_load/', loader)
});
on('#ajax', 'click', '.comment_good', function() {
  this.classList.add("current_file_dropdown");
  clear_attach_block();
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/good_load/', loader)
});
on('#ajax', 'click', '.comment_article', function() {
  this.classList.add("current_file_dropdown");
  clear_attach_block();
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/article_load/', loader)
});

on('#ajax', 'click', '.select_photo', function() {
  this.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/img_load/', loader)
});
on('#ajax', 'click', '.select_video', function() {
  this.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/video_load/', loader)
});
on('#ajax', 'click', '.select_music', function() {
  this.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/music_load/', loader)
});
on('#ajax', 'click', '.select_good', function() {
  this.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/good_load/', loader)
});
on('#ajax', 'click', '.select_article', function() {
  this.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/article_load/', loader)
});

on('#ajax', 'click', '.delete_thumb', function(e) {
  e.preventDefault();
  this.nextElementSibling.remove();
  block = document.createElement("div");
  this.parentElement.innerHTML = "<h4>Изображение</h4><i>(обязательно)</i>";
  this.remove();
})


on('#ajax', 'change', '#photo_add_comment_attach', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  form_data = new FormData(document.body.querySelector("#add_comment_photos"));
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/user/add_comment_photo/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;

    dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
    photo_comment_upload_attach(response, dropdown);
    }
    document.querySelector(".create_fullscreen").style.display = "none";
    document.getElementById("create_loader").innerHTML="";
  }
  link_.send(form_data);
});

on('#ajax', 'click', '.photo_load_several', function() {
  _this = this.previousElementSibling.querySelector("img");
  if (document.body.querySelector(".current_file_dropdown")){
    photo_comment_attach(_this, document.body.querySelector(".current_file_dropdown").parentElement.parentElement);
    console.log("photo_comment_attach")
  } else if (document.body.querySelector(".attach_block")){
    photo_post_attach(_this, document.body.querySelector(".attach_block")); console.log("photo_post_attach")
  }
  this.classList.add("active_svg");
});
on('#ajax', 'click', '.photo_load_one', function() {
  _this = this;
  if (document.body.querySelector(".current_file_dropdown")){
    photo_comment_attach(_this, document.body.querySelector(".current_file_dropdown").parentElement.parentElement);
    console.log("photo_comment_attach")
  } else if (document.body.querySelector(".attach_block")){
    photo_post_attach(_this, document.body.querySelector(".attach_block")); console.log("photo_post_attach")
  }
  document.querySelector(".create_fullscreen").style.display = "none";
  document.getElementById("create_loader").innerHTML="";
});

on('#ajax', 'click', '.create_video_attach_btn', function() {
  form_data = new FormData(document.querySelector("#create_video_form"));
  user_pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/video/progs/create_video_attach/" + user_pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem_ = document.createElement('div');
    elem_.innerHTML = link_.responseText;

      dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
      video_comment_attach(elem_.querySelector("img"), dropdown);

      document.querySelector(".create_fullscreen").style.display = "none";
      document.getElementById("create_loader").innerHTML="";
  }};

  link_.send(form_data);
});

on('#ajax', 'click', '.video_load_one', function() {
  _this = this;
  if (document.body.querySelector(".current_file_dropdown")){
    video_comment_attach(_this, document.body.querySelector(".current_file_dropdown").parentElement.parentElement)
  } else if (document.body.querySelector(".attach_block")){
    video_post_attach(_this, document.body.querySelector(".attach_block"))
  }
  document.querySelector(".create_fullscreen").style.display = "none";
  document.getElementById("create_loader").innerHTML="";
});
on('#ajax', 'click', '.video_load_several', function() {
  _this = this.previousElementSibling.querySelector("img");
  if (document.body.querySelector(".current_file_dropdown")){
    video_comment_attach(_this, document.body.querySelector(".current_file_dropdown").parentElement.parentElement)
  } else if (document.body.querySelector(".attach_block")){
    video_post_attach(_this, document.body.querySelector(".attach_block"))
  }
  this.classList.add("active_svg");
});

on('#ajax', 'click', '.music_load_one', function() {
  _this = this;
  if (document.body.querySelector(".current_file_dropdown")){
    music_comment_attach(_this, document.body.querySelector(".current_file_dropdown").parentElement.parentElement)
  } else if (document.body.querySelector(".attach_block")){
    music_post_attach(_this, document.body.querySelector(".attach_block"))
  }
  document.querySelector(".create_fullscreen").style.display = "none";
  document.getElementById("create_loader").innerHTML="";
});
on('#ajax', 'click', '.music_load_several', function() {
  _this = this.previousElementSibling;
  if (document.body.querySelector(".current_file_dropdown")){
    music_comment_attach(_this, document.body.querySelector(".current_file_dropdown").parentElement.parentElement)
  } else if (document.body.querySelector(".attach_block")){
    music_post_attach(_this, document.body.querySelector(".attach_block"))
  }
  this.classList.add("active_svg");
});

on('#ajax', 'click', '.good_load_one', function() {
  _this = this;
  if (document.body.querySelector(".current_file_dropdown")){
    good_comment_attach(_this, document.body.querySelector(".current_file_dropdown").parentElement.parentElement)
  } else if (document.body.querySelector(".attach_block")){
    good_post_attach(_this, document.body.querySelector(".attach_block"))
  }
  document.querySelector(".create_fullscreen").style.display = "none";
  document.getElementById("create_loader").innerHTML="";
});
on('#ajax', 'click', '.good_load_several', function() {
  _this = this.previousElementSibling;
  if (document.body.querySelector(".current_file_dropdown")){
    good_comment_attach(_this, document.body.querySelector(".current_file_dropdown").parentElement.parentElement)
  } else if (document.body.querySelector(".attach_block")){
    good_post_attach(_this, document.body.querySelector(".attach_block"))
  }
  this.classList.add("active_svg");
});

on('#ajax', 'click', '.article_load_one', function() {
  _this = this;
  if (document.body.querySelector(".current_file_dropdown")){
    article_comment_attach(_this, document.body.querySelector(".current_file_dropdown").parentElement.parentElement)
  } else if (document.body.querySelector(".attach_block")){
    article_post_attach(_this, document.body.querySelector(".attach_block"))
  }
  document.querySelector(".create_fullscreen").style.display = "none";
  document.getElementById("create_loader").innerHTML="";
});
on('#ajax', 'click', '.article_load_several', function() {
  _this = this.previousElementSibling;
  if (document.body.querySelector(".current_file_dropdown")){
    article_comment_attach(_this, document.body.querySelector(".current_file_dropdown").parentElement.parentElement)
  } else if (document.body.querySelector(".attach_block")){
    article_post_attach(_this, document.body.querySelector(".attach_block"))
  }
  this.classList.add("active_svg");
});

on('#ajax', 'click', '.tag_item', function() {
  var track_id = this.parentElement.parentElement.getAttribute('music-counter');
  var tag_pk = document.querySelector(".tag_playlist").getAttribute('data-pk');
  if (!document.body.classList.contains("tag_" + tag_pk)){
    save_playlist("tag_" + tag_pk, '/music/manage/temp_tag/' + tag_pk, '/music/get/tag/' + tag_pk, track_id)
  }else{
    music_player.loadPlaylist(0);
    if (FWDMSP.LOAD_PLAYLIST_COMPLETE){
      console.log("Плейдист загружен!");
    setTimeout(function() {music_player.playSpecificTrack("tag_" + tag_pk, track_id)}, 50);
  }
  }
  });

on('#ajax', 'click', '.genre_item', function() {
  var track_id = this.parentElement.parentElement.getAttribute('music-counter');
  var genre_pk = document.querySelector(".genre_playlist").getAttribute('data-pk');
  if (!document.body.classList.contains("genre_" + genre_pk)){
    save_playlist("genre_" + genre_pk, '/music/manage/temp_genre/' + genre_pk, '/music/get/genre/' + genre_pk, track_id)
  }else{
    music_player.loadPlaylist(0);
    if (FWDMSP.LOAD_PLAYLIST_COMPLETE){
      console.log("Плейдист загружен!");
    setTimeout(function() {music_player.playSpecificTrack("genre_" + list_pk, track_id)}, 50);
  }
  }
});

on('#ajax', 'click', '.music_list_item', function() {
  var track_id = this.parentElement.parentElement.getAttribute('music-counter');
  var list_pk = document.querySelector(".music_playlist").getAttribute('data-pk');
  if (!document.body.classList.contains("list_" + list_pk)){
    save_playlist("list_" + list_pk, '/music/manage/temp_list/' + list_pk, '/music/get/list/' + list_pk, track_id)
  }else{
    music_player.loadPlaylist(0);
    if (FWDMSP.LOAD_PLAYLIST_COMPLETE){
      console.log("Плейлист загружен!");
    setTimeout(function() {music_player.playSpecificTrack("list_" + list_pk, track_id)}, 50);
  }
  }
});

on('#ajax', 'click', '.track_add', function(e) {
  block = this.parentElement;
  pk = block.parentElement.getAttribute("data-pk");
  var _link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  _link.open( 'GET', "/music/manage/add_track/" + pk, true );
  _link.onreadystatechange = function () {
    if ( _link.readyState == 4 && _link.status == 200 ) {
      block.innerHTML = "";
      block.innerHTML = "<span class='track_remove' title='Удалить'><svg xmlns='http://www.w3.org/2000/svg' fill='currentColor' style='width:22px;height:22px;' class='svg_default' viewBox='0 0 2424'><path fill='none' d='M0 0h24v24H0z'/><path d='M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z'/></svg></span>"
  }};
  _link.send( null );
});

on('#ajax', 'click', '.track_remove', function(e) {
  block = this.parentElement;
  pk = block.parentElement.getAttribute("data-pk");
  var _link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  _link.open( 'GET', "/music/manage/remove_track/" + pk, true );
  _link.onreadystatechange = function () {
    if ( _link.readyState == 4 && _link.status == 200 ) {
      block.innerHTML = "";
      block.innerHTML = "<span class='track_add' title='Добавить'><svg fill='currentColor' style='width:22px;height:22px;' class='svg_default' xmlns='http://www.w3.org/2000/svg' viewBox='0 024 24'><path d='M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z'/><path d='M0 0h24v24H0z' fill='none'/></svg></span>"
  }};
  _link.send( null );
});
