on('#ajax', 'click', '#u_ucm_video_repost_btn', function() {
  form_post = document.body.querySelector("#u_uсm_video_repost_form");
  form_data = new FormData(form_post);
  track_pk = this.getAttribute("track-pk");
  pk = this.getAttribute("data-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );

  if (form_post.querySelector('#repost_radio_wall').checked) {
    link_.open( 'POST', "/video/repost/u_u_video_repost/" + pk + "/" + track_pk + "/", true );
    link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link_.send(form_data);
    toast_info("Репост видеозаписи на стену сделан")
  }

  else if(form_post.querySelector('#repost_radio_community').checked){
    staff_communities = form_post.querySelector("#id_staff_communities");
    selectedOptions = staff_communities.selectedOptions;
    val = false;
    for (var i = 0; i < selectedOptions.length; i++) {if(selectedOptions[i].value) {val = true}}
    if(val){
      link_.open( 'POST', "/video/repost/u_c_video_repost/" + pk + "/" + track_pk + "/", true );
      link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      link_.send(form_data);
      toast_info("Репост видеозаписи в сообщества сделан")
    }else{toast_error("Выберите сообщества для репоста")}
  }

  else if(form_post.querySelector('#repost_radio_message').checked){
    user_connections = form_post.querySelector("#id_user_connections");
    selectedOptions = user_connections.selectedOptions;
    val = false;
    for (var i = 0; i < selectedOptions.length; i++) {if(selectedOptions[i].value) {val = true}}
    if(val){
      link_.open( 'POST', "/video/repost/u_m_video_repost/" + pk + "/" + track_pk + "/", true );
      link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      link_.send(form_data);
      toast_info("Репост видеозаписи в сообщения сделан")
    }else{toast_error("Выберите пользователя для репоста")}
  };

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    document.querySelector(".votes_fullscreen").style.display = "none";
    document.getElementById("votes_loader").innerHTML="";
  }}
});


on('#ajax', 'click', '#u_ucm_video_album_repost_btn', function() {
  form_post = document.body.querySelector("#u_uсm_video_album_repost_form");
  form_data = new FormData(form_post);
  uuid = this.getAttribute("data-uuid");
  pk = this.getAttribute("data-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );

  if (form_post.querySelector('#repost_radio_wall').checked) {
    link_.open( 'POST', "/video/repost/u_u_video_album_repost/" + pk + "/" + uuid + "/", true );
    link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link_.send(form_data);
    toast_info("Репост видеоальбома на стену сделан")
  }

  else if(form_post.querySelector('#repost_radio_community').checked){
    staff_communities = form_post.querySelector("#id_staff_communities");
    selectedOptions = staff_communities.selectedOptions;
    val = false;
    for (var i = 0; i < selectedOptions.length; i++) {if(selectedOptions[i].value) {val = true}}
    if(val){
      link_.open( 'POST', "/video/repost/u_c_video_album_repost/" + pk + "/" + uuid + "/", true );
      link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      link_.send(form_data);
      toast_info("Репост видеоальбома в сообщества сделан")
    }else{toast_error("Выберите сообщества для репоста")}
  }

  else if(form_post.querySelector('#repost_radio_message').checked){
    user_connections = form_post.querySelector("#id_user_connections");
    selectedOptions = user_connections.selectedOptions;
    val = false;
    for (var i = 0; i < selectedOptions.length; i++) {if(selectedOptions[i].value) {val = true}}
    if(val){
      link_.open( 'POST', "/video/repost/u_m_video_album_repost/" + pk + "/" + uuid + "/", true );
      link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      link_.send(form_data);
      toast_info("Репост видеоальбома в сообщения сделан")
    }else{toast_error("Выберите пользователя для репоста")}
  };

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    document.querySelector(".votes_fullscreen").style.display = "none";
    document.getElementById("votes_loader").innerHTML="";
  }}
});

on('#ajax', 'click', '.u_video_create_window', function(e) {
  e.preventDefault();
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  loader = document.getElementById("create_loader");
  open_fullscreen("/video/user/create_video_window/" + pk + "/", loader);
  var list = loader.querySelectorAll('select');
  var count = list.length;
  for(i=0; i<count; i++) {
    list[i].classList.add("form-control")
  }
});

on('#ajax', 'click', '.user_video_create_attach', function(e) {
  e.preventDefault();
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  loader = document.getElementById("create_loader");
  open_fullscreen("/video/user/create_video_attach_window/" + pk + "/", loader);
  var list = loader.querySelectorAll('select');
  var count = list.length;
  for(i=0; i<count; i++) {
    list[i].classList.add("form-control")
  }
});

on('#video_loader', 'click', '.u_videoComment', function() {
  form = this.parentElement.parentElement.parentElement;
  send_comment(form, form.parentElement.previousElementSibling, '/video/user_progs/post-comment/');
});

on('#video_loader', 'click', '.u_replyVideoComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  block = form.parentElement.parentElement.querySelector(".stream_reply_comments");
  send_comment(form, block, '/video/user_progs/reply-comment/')
  form.parentElement.style.display = "none";
  block.classList.add("replies_open")
});

on('#video_loader', 'click', '.u_replyParentVideoComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  block = form.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  send_comment(form, block.parentElement, '/video/user_progs/reply-comment/')
  form.parentElement.style.display = "none";
  block.classList.add("replies_open")
});

on('#video_loader', 'click', '.u_video_off_comment', function() {
  send_photo_change(this, "/video/user_progs/off_comment/", "u_video_on_comment", "Вкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".u_video_comments").style.display = "none"
})
on('#video_loader', 'click', '.u_video_on_comment', function() {
  send_photo_change(this, "/video/user_progs/on_comment/", "u_video_off_comment", "Выкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".u_video_comments").style.display = "unset"
})

on('#video_loader', 'click', '.u_video_comment_delete', function() {
  comment_delete(this, "/video/user_progs/delete_comment/", "u_video_comment_abort_remove")
})
on('#video_loader', 'click', '.u_video_comment_abort_remove', function() {
  comment_abort_delete(this, "/video/user_progs/abort_delete_comment/")
});

on('#video_loader', 'click', '.u_video_off_private', function() {
  send_photo_change(this, "/video/user_progs/off_private/", "u_video_on_private", "Вкл. приватность")
})
on('#video_loader', 'click', '.u_video_on_private', function() {
  send_photo_change(this, "/video/user_progs/on_private/", "u_video_off_private", "Выкл. приватность")
})

on('#ajax', 'click', '.u_video_edit', function() {
  this.parentElement.nextElementSibling.style.display = "block"
})

on('#video_loader', 'click', '.u_video_off_votes', function() {
  send_photo_change(this, "/video/user_progs/off_votes/", "u_video_on_votes", "Вкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "none";
  post.querySelector(".dislike").style.display = "none";
})
on('#video_loader', 'click', '.u_video_on_votes', function() {
  send_photo_change(this, "/video/user_progs/on_votes/", "u_video_off_votes", "Выкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "unset";
  post.querySelector(".dislike").style.display = "unset";
})

on('body', 'click', '.user_video_remove', function() {
  send_photo_change(this, "/video/user_progs/delete/", "user_video_abort_remove", "Отмена");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  this.parentElement.parentElement.nextElementSibling.style.display = "none";
  post.querySelector(".order-2").style.display = "none";
  post.querySelector(".card").style.opacity = "0.5";
  this.style.color = "#FF0000";
})
on('body', 'click', '.user_video_abort_remove', function() {
  send_photo_change(this, "/video/user_progs/abort_delete/", "user_video_remove", "Удалить");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  this.parentElement.parentElement.nextElementSibling.style.display = "unset";
  post.querySelector(".order-2").style.display = "unset";
  post.querySelector(".card").style.opacity = "1";
})

on('#video_loader', 'click', '.u_video_like', function() {
  video = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = video.getAttribute("data-uuid");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_like(video, "/video/votes/user_like/" + uuid + "/" + pk + "/");
  like_reload(this.nextElementSibling, this.nextElementSibling.nextElementSibling.nextElementSibling, "u_all_video_likes");
});
on('#video_loader', 'click', '.u_video_dislike', function() {
  video = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = video.getAttribute("data-uuid");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_dislike(video, "/video/votes/user_dislike/" + uuid + "/" + pk + "/");
  dislike_reload(this.previousElementSibling, this.nextElementSibling, "u_all_video_dislikes");
});
on('#video_loader', 'click', '.u_video_like2', function() {
  _this = this;
  video = _this.parentElement;
  comment_pk = video.getAttribute("data-pk");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_like(video, "/video/votes/user_comment/" + comment_pk + "/" + pk + "/like/");
  like_reload(this.nextElementSibling, this.nextElementSibling.nextElementSibling.nextElementSibling, "u_all_video_comment_likes")
});
on('#video_loader', 'click', '.u_video_dislike2', function() {
  _this = this;
  video = _this.parentElement;
  comment_pk = video.getAttribute("data-pk");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_dislike(video, "/video/votes/user_comment/" + comment_pk + "/" + pk + "/dislike/");
  dislike_reload(this.previousElementSibling, this.nextElementSibling, "u_all_video_comment_dislikes")
});

on('#ajax', 'click', '#u_create_video_btn', function() {
  form = document.querySelector("#u_create_video_form");
  form_data = new FormData(form);
  lists = form.querySelector("#id_album");
  selectedOptions = lists.selectedOptions;
  val = false;
  for (var i = 0; i < selectedOptions.length; i++) {
    if(selectedOptions[i].value) {val = true}
  }

  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else if (!form.querySelector("#id_uri").value){
    form.querySelector("#id_uri").style.border = "1px #FF0000 solid";
    toast_error("Ссылка на видео - обязательное поле!")
  } else if (!form.querySelector("#id_image").value){
    form.querySelector("#video_holder").style.border = "1px #FF0000 solid";
    toast_error("Фотография на обложку обязательна!")
  } else if (!val){
    form.querySelector("#id_album").style.border = "1px #FF0000 solid";
    toast_error("Выберите альбом!");
    return
  };

  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  uuid = document.body.querySelector(".pk_saver").getAttribute("data-uuid");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/video/user_progs/create_video/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    span1 = response.querySelector('.span1')
    if (span1.classList.contains(uuid)){
      container = document.body.querySelector(".profile_block_paginate");
      container.insertAdjacentHTML('afterBegin', response.innerHTML);
      container.querySelector(".video_none") ? container.querySelector(".video_none").style.display = "none" : null;
      toast_info("Видео создано!")
    } else{
      toast_info("Видео создано!")
    }
    document.querySelector(".create_fullscreen").style.display = "none";
    document.getElementById("create_loader").innerHTML="";
  }};

  link_.send(form_data);
});

on('#ajax', 'click', '#u_create_video_list_btn', function() {
  this.disabled = true;
  form = document.body.querySelector("#u_video_list_create");
  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { null }
  post_and_load_object_page(form, "/video/user_progs/create_list/", "/users/", "/video_list/")

});

on('#ajax', 'click', '#u_edit_video_list_btn', function() {
  form = document.body.querySelector("#u_edit_video_list_form");
  form_data = new FormData(form);
  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }

  pk = form.getAttribute("data-pk");
  uuid = form.getAttribute("data-uuid");

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'POST', "/video/user_progs/edit_list/" + pk + "/" + uuid + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        name = form.querySelector('#id_title').value;
        document.body.querySelector(".list_name").innerHTML = name;
        document.querySelector(".create_fullscreen").style.display = "none";
        document.getElementById("create_loader").innerHTML="";
        toast_success("Список видео изменен")
      }
    }
    ajax_link.send(form_data);
});

on('#ajax', 'click', '.u_video_list_delete', function() {
  saver = document.querySelector(".pk_saver");
  pk = saver.getAttribute("data-pk");
  uuid = saver.getAttribute("data-uuid");

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', "/video/user_progs/delete_list/" + pk + "/" + uuid + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        this_page_reload("/users/" + pk + "/video_list/" + uuid)
      }
    }
    ajax_link.send();
});

on('#ajax', 'click', '.u_video_list_recover', function() {
  saver = document.querySelector(".pk_saver");
  pk = saver.getAttribute("data-pk");
  uuid = saver.getAttribute("data-uuid");

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', "/video/user_progs/abort_delete_list/" + pk + "/" + uuid + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        this_page_reload("/users/" + pk + "/video_list/" + uuid)
      }
    }
    ajax_link.send();
});
