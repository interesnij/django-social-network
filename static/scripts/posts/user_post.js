on('#ajax', 'click', '#article_add', function() {
  var pk = this.getAttribute('data-pk');
  open_fullscreen("/article/u_article_window/" + pk + "/", document.getElementById("create_loader"));
  //setTimeout(function() { CKEDITOR.replace('id_content'); CKEDITOR.instances.id_content.updateElement(); }, 1000);
});

on('#ajax', 'click', '#form_post_btn', function() {
  form_data = new FormData(document.forms.new_post);
  form_post = document.querySelector("#form_post");
  lenta_load = form_post.parentElement.nextElementSibling;
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/posts/user_progs/add_post/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    form_post.querySelector('.id_text').value = "";
    clear_attach_block();

    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    new_post.querySelector(".card") ? (lenta_load.querySelector(".stream").prepend(new_post),
                                       toast_info("Запись опубликована"),
                                       lenta_load.querySelector(".post_empty") ? lenta_load.querySelector(".post_empty").style.display = "none" : null)
                                    :  toast_error("Нужно написать или прикрепить что-нибудь!");
  }};

  link_.send(form_data);
});

on('#ajax', 'click', '#u_ucm_post_repost_btn', function() {
  form_post = document.body.querySelector("#u_uсm_post_repost_form");
  form_data = new FormData(form_post);
  uuid = this.getAttribute("data-uuid");
  pk = this.getAttribute("data-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );

  if (form_post.querySelector('#repost_radio_wall').checked) {
    link_.open( 'POST', "/posts/repost/u_u_post_repost/" + pk + "/" + uuid + "/", true );
    link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link_.send(form_data);
    toast_info("Репост записи на стену сделан")
  }

  else if(form_post.querySelector('#repost_radio_community').checked){
    staff_communities = form_post.querySelector("#id_staff_communities");
    selectedOptions = staff_communities.selectedOptions;
    val = false;
    for (var i = 0; i < selectedOptions.length; i++) {if(selectedOptions[i].value) {val = true}}
    if(val){
      link_.open( 'POST', "/posts/repost/u_c_post_repost/" + pk + "/" + uuid + "/", true );
      link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      link_.send(form_data);
      toast_info("Репост записи в сообщества сделан")
    }else{toast_error("Выберите сообщества для репоста")}
  }

  else if(form_post.querySelector('#repost_radio_message').checked){
    user_connections = form_post.querySelector("#id_user_connections");
    selectedOptions = user_connections.selectedOptions;
    val = false;
    for (var i = 0; i < selectedOptions.length; i++) {if(selectedOptions[i].value) {val = true}}
    if(val){
      link_.open( 'POST', "/posts/repost/u_m_post_repost/" + pk + "/" + uuid + "/", true );
      link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      link_.send(form_data);
      toast_info("Репост записи в сообщения сделан")
    }else{toast_error("Выберите пользователя для репоста")}
  };

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    document.querySelector(".votes_fullscreen").style.display = "none";
    document.getElementById("votes_loader").innerHTML="";
  }}
});

on('#ajax', 'click', '#article_post', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  form_data = new FormData(document.forms.new_post);
  form_post = document.querySelector("#user_article_form");
  CKEDITOR.instances.id_content.updateElement();
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/article/add_user/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    response = new_post.querySelector(".card");
    document.querySelector(".stream").prepend(response)
    document.querySelector(".post_empty") ? lenta_load.querySelector(".post_empty").style.display = "none" : null;
  }};

  link_.send(form_data);
});

on('#ajax', 'click', '.u_itemComment', function() {
  form = this.parentElement.parentElement.parentElement;
  send_comment(form, form.parentElement.previousElementSibling, '/posts/user_progs/post-comment/');
});

on('#ajax', 'click', '.u_replyItemComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  block = form.parentElement.parentElement.querySelector(".stream_reply_comments");
  send_comment(form, block, '/posts/user_progs/reply-comment/')
  form.parentElement.style.display = "none";
  block.classList.add("replies_open");
});

on('#ajax', 'click', '.u_replyParentItemComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  block = form.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  send_comment(form, block.parentElement, '/posts/user_progs/reply-comment/')
  form.parentElement.style.display = "none";
  block.classList.add("replies_open");
});

/*!
   item post scripts for user
  */
on('#ajax', 'click', '.u_post_remove', function() {
  item = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("data-uuid");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/posts/user_progs/delete/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    p = document.createElement("div");
    p.classList.add("card", "mb-3");
    p.style.padding = "20px";
    p.style.display =  "block";
    p.innerHTML = "Запись удалена. <span class='u_post_abort_remove pointer' data-uuid='" + uuid + "'>Восстановить</span>";
    !document.querySelector(".post_detail") ? (item.parentElement.insertBefore(p, item), item.style.display = "none")
    : (document.querySelector(".item_fullscreen").style.display = "none",
    block = document.body.querySelector(".post_container"),
    item = block.querySelector( '[data-uuid=' + '"' + uuid + '"' + ']' ),
    item.parentElement.insertBefore(p, item),
    item.style.display = "none")
  }};

  link.send( );
});
on('#ajax', 'click', '.u_post_wall_remove', function() {
  item = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("data-uuid");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/posts/user_progs/wall_delete/" + pk + "/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    p = document.createElement("div");
    p.classList.add("card", "mb-3");
    p.style.padding = "20px";
    p.style.display =  "block";
    p.innerHTML = "Запись удалена. <span class='u_post_wall_abort_remove pointer' data-uuid='" + uuid + "'>Восстановить</span>";
    !document.querySelector(".post_detail") ? (item.parentElement.insertBefore(p, item), item.style.display = "none")
    : (document.querySelector(".item_fullscreen").style.display = "none",
    block = document.body.querySelector(".post_container"),
    item = block.querySelector( '[data-uuid=' + '"' + uuid + '"' + ']' ),
    item.parentElement.insertBefore(p, item),
    item.style.display = "none")
  }};

  link.send( );
});

on('#ajax', 'click', '.u_post_abort_remove', function() {
  item = this.parentElement.nextElementSibling;
  item.style.display = "block";
  uuid = this.getAttribute("data-uuid");
  block = this.parentElement;
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/posts/user_progs/abort_delete/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    block.remove();
  }};
  link.send();
});
on('#ajax', 'click', '.u_post_wall_abort_remove', function() {
  item = this.parentElement.nextElementSibling;
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  item.style.display = "block";
  uuid = this.getAttribute("data-uuid");
  block = this.parentElement;
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/posts/user_progs/wall_abort_delete/" + pk + "/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    block.remove();
  }};
  link.send();
});

on('#ajax', 'click', '.u_post_fixed', function() {
  send_change(this, "/posts/user_progs/fixed/", "u_post_unfixed", "Открепить")
})
on('#ajax', 'click', '.u_post_unfixed', function() {
  send_change(this, "/posts/user_progs/unfixed/", "u_post_fixed", "Закрепить")
})

on('#ajax', 'click', '.u_post_off_comment', function() {
  send_change(this, "/posts/user_progs/off_comment/", "u_post_on_comment", "Вкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".u_item_comments") ? post.querySelector(".u_item_comments").style.display = "none"
  : post.querySelector(".u_news_item_comments").style.display = "none"
})
on('#ajax', 'click', '.u_post_on_comment', function() {
  send_change(this, "/posts/user_progs/on_comment/", "u_post_off_comment", "Выкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".u_item_comments") ? post.querySelector(".u_item_comments").style.display = "unset"
  : post.querySelector(".u_news_item_comments").style.display = "unset"
})

on('#ajax', 'click', '.u_post_off_votes', function() {
  send_change(this, "/posts/user_progs/off_votes/", "u_post_on_votes", "Вкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "none";
  post.querySelector(".dislike").style.display = "none";
})
on('#ajax', 'click', '.u_post_on_votes', function() {
  send_change(this, "/posts/user_progs/on_votes/", "u_post_off_votes", "Выкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "unset";
  post.querySelector(".dislike").style.display = "unset";
})

on('#ajax', 'click', '.u_like', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("data-uuid");
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = item.getAttribute('data-pk');
  send_like(item, "/posts/votes/user_like/" + uuid + "/" + pk + "/");
  like_reload(this.nextElementSibling, this.nextElementSibling.nextElementSibling.nextElementSibling, "u_all_posts_likes");
});
on('#ajax', 'click', '.u_dislike', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("data-uuid");
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = item.getAttribute('data-pk');
  send_dislike(item, "/posts/votes/user_dislike/" + uuid + "/" + pk + "/");
  dislike_reload(this.previousElementSibling, this.nextElementSibling, "u_all_posts_dislikes");
});

on('#ajax', 'click', '.u_like2', function() {
  _this = this;
  item = _this.parentElement;
  comment_pk = item.getAttribute("data-pk");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_like(item, "/posts/votes/user_comment/" + comment_pk + "/" + pk + "/like/");
  like_reload(this.nextElementSibling, this.nextElementSibling.nextElementSibling.nextElementSibling, "u_all_posts_comment_likes")
});
on('#ajax', 'click', '.u_dislike2', function() {
  _this = this;
  item = _this.parentElement;
  comment_pk = item.getAttribute("data-pk");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_dislike(item, "/posts/votes/user_comment/" + comment_pk + "/" + pk + "/dislike/");
  dislike_reload(this.previousElementSibling, this.nextElementSibling, "u_all_posts_comment_dislikes")
});

on('#ajax', 'click', '.u_post_comment_delete', function() {
  comment_delete(this, "/posts/user_progs/delete_comment/", "u_post_comment_abort_remove")
})

on('#ajax', 'click', '.u_post_comment_abort_remove', function() {
  comment_abort_delete(this, "/posts/user_progs/abort_delete_comment/")
});

on('#ajax', 'click', '.u_post_wall_comment_delete', function() {
  comment_wall_delete(this, "/posts/user_progs/delete_wall_comment/", "u_post_comment_abort_remove")
})

on('#ajax', 'click', '.u_post_wall_comment_abort_remove', function() {
  comment_wall_abort_delete(this, "/posts/user_progs/abort_delete_wall_comment/")
});

on('#ajax', 'change', '#u_photo_post_attach', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  form = document.body.querySelector("#add_photos");
  form_data = new FormData(form);
  input = form.querySelector("#u_photo_post_comment_attach")
  if (input.files.length > 10) {
      toast_error("Не больше 10 фотографий");
      return;
  }
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/user_progs/add_comment_photo/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    photo_list = response.querySelectorAll(".u_photo_detail");

    block = document.body.querySelector(".attach_block");
    block_divs = block.querySelectorAll("div");
    block_divs_length = photo_list.length;

    photo_post_upload_attach(photo_list, block, block_divs_length);
    }
    document.querySelector(".create_fullscreen").style.display = "none";
    document.getElementById("create_loader").innerHTML="";
  }
  link_.send(form_data);
});

function onSelect(e) {
    if (e.files.length > 5) {
        alert("Only 5 files accepted.");
        e.preventDefault();
    }
}
on('#ajax', 'change', '#u_photo_post_comment_attach', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  form = document.body.querySelector("#add_comment_photos");
  form_data = new FormData(form);
  input = form.querySelector("#u_photo_post_comment_attach")
  if (input.files.length > 2) {
      toast_error("Не больше 2 фотографий");
      return;
  }
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/user_progs/add_comment_photo/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    photo_list = response.querySelectorAll(".u_photo_detail");
    photo_comment_upload_attach(photo_list, document.body.querySelector(".current_file_dropdown").parentElement.parentElement, photo_list.length);
    }
    document.querySelector(".create_fullscreen").style.display = "none";
    document.getElementById("create_loader").innerHTML="";
  }
  link_.send(form_data);
});

on('#ajax', 'click', '.photo_load_several', function() {
  _this = this.previousElementSibling.querySelector("img");
  if (document.body.querySelector(".current_file_dropdown")){
    photo_comment_attach(_this, document.body.querySelector(".current_file_dropdown").parentElement.parentElement)
  } else if (document.body.querySelector(".attach_block")){
    photo_post_attach(_this, document.body.querySelector(".attach_block"))
  }
  this.classList.add("active_svg");
});
on('#ajax', 'click', '.photo_load_one', function() {
  _this = this;
  if (document.body.querySelector(".current_file_dropdown")){
    photo_comment_attach(_this, document.body.querySelector(".current_file_dropdown").parentElement.parentElement)
  } else if (document.body.querySelector(".attach_block")){
    photo_post_attach(_this, document.body.querySelector(".attach_block"))
  }
  document.querySelector(".create_fullscreen").style.display = "none";
  document.getElementById("create_loader").innerHTML="";
});

on('#votes_loader', 'click', '.commmunty_load_one', function() {
  _this = this;
  block = _this.parentElement.parentElement.parentElement.parentElement;
  document.querySelector(".create_fullscreen")
  commmunity_form_selected(_this, block.querySelector(".selected_message_target_items"))
});
on('#votes_loader', 'click', '.chat_item_load_one', function() {
  _this = this;
  block = _this.parentElement.parentElement.parentElement.parentElement;
  document.querySelector(".create_fullscreen")
  chat_item_form_selected(_this, block.querySelector(".selected_message_target_items"))
});

on('#ajax', 'click', '.u_create_video_attach_btn', function() {
  form_data = new FormData(document.querySelector("#create_video_form"));
  user_pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/video/progs/create_video_attach/" + user_pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

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
on('#ajax', 'click', '.doc_load_several', function() {
  _this = this.previousElementSibling;
  if (document.body.querySelector(".current_file_dropdown")){
    doc_comment_attach(_this, document.body.querySelector(".current_file_dropdown").parentElement.parentElement)
  } else if (document.body.querySelector(".attach_block")){
    doc_post_attach(_this, document.body.querySelector(".attach_block"))
  }
  this.classList.add("active_svg");
});

on('#ajax', 'click', '.music_attach_playlist', function() {
  attach_list_for_post(this, "/music/get/playlist_preview/")
});
on('#ajax', 'click', '.photo_attach_album', function() {
  attach_list_for_post(this, "/gallery/user_progs/get_album_preview/")
});
on('#ajax', 'click', '.attach_video_album', function() {
  attach_list_for_post(this, "/video/user_progs/get_album_preview/")
});
on('#ajax', 'click', '.attach_doc_list', function() {
  attach_list_for_post(this, "/docs/user_progs/list_preview/")
});

on('#ajax', 'click', '.attach_good_album', function() {
  attach_list_for_post(this, "/goods/user_progs/get_album_preview/")
});

on('#ajax', 'click', '.music_attach_playlist_remove', function() {
  block = this.parentElement.parentElement.parentElement;
  block.parentElement.nextElementSibling.querySelector(".attach_panel").style.display = "block";
  block.nextElementSibling.remove();
  block.remove();
})
on('#ajax', 'click', '.doc_attach_list_remove', function() {
  block = this.parentElement.parentElement.parentElement;
  block.parentElement.nextElementSibling.querySelector(".attach_panel").style.display = "block";
  block.nextElementSibling.remove();
  block.remove();
})
on('#ajax', 'click', '.video_attach_album_remove', function() {
  block = this.parentElement.parentElement.parentElement;
  block.parentElement.nextElementSibling.querySelector(".attach_panel").style.display = "block";
  block.remove();
})
on('#ajax', 'click', '.good_attach_album_remove', function() {
  block = this.parentElement.parentElement.parentElement;
  block.parentElement.nextElementSibling.querySelector(".attach_panel").style.display = "block";
  block.remove();
})
on('#ajax', 'click', '.photo_attach_album_remove', function() {
  block = this.parentElement.parentElement.parentElement;
  block.parentElement.nextElementSibling.querySelector(".attach_panel").style.display = "block";
  block.remove();
})

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
