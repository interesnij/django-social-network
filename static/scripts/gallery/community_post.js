
// скрипты галереи для сообщества

on('#ajax', 'click', '#c_create_album_btn', function() {
  form = document.body.querySelector("#c_create_album_form");
  form_data = new FormData(form);
  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { null }
  post_and_load_object_page(form, "/gallery/community_progs/add_album/", "/communities/", "/album/");
});

on('#ajax', 'click', '#c_edit_album_btn', function() {
  form = document.body.querySelector("#c_edit_album_form");
  form_data = new FormData(form);
  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { null }
  pk = form.getAttribute("data-pk");
  uuid = form.getAttribute("data-uuid")

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/community_progs/edit_album/" + pk + "/" + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    title = form.querySelector('#id_title').value;
    description = form.querySelector('#id_description').value;

    album = document.body.querySelector(".album_active");
    album.querySelector("h6").innerHTML = title;
    album.querySelector(".albom_description").innerHTML = description;
    album.classList.remove("album_active");
    document.querySelector(".create_fullscreen").style.display = "none";
    document.getElementById("create_loader").innerHTML="";
  }}
  link_.send(form_data);
});


on('#ajax', 'click', '#c_ucm_photo_repost_btn', function() {
  form_post = document.body.querySelector("#c_uсm_photo_repost_form");
  form_data = new FormData(form_post);
  uuid = this.getAttribute("data-uuid");
  pk = this.getAttribute("data-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  if (form_post.querySelector('#repost_radio_wall').checked) {
    link_.open( 'POST', "/gallery/repost/c_u_photo_repost/" + pk + "/" + uuid + "/", true );
    link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link_.send(form_data);
    toast_info("Репост фотографии на стену сделан")
  }
  else if(form_post.querySelector('#repost_radio_community').checked){
    staff_communities = form_post.querySelector("#id_staff_communities");
    selectedOptions = staff_communities.selectedOptions;
    val = false;
    for (var i = 0; i < selectedOptions.length; i++) {if(selectedOptions[i].value) {val = true}}
    if(val){
      link_.open( 'POST', "/gallery/repost/c_c_photo_repost/" + pk + "/" + uuid + "/", true );
      link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      link_.send(form_data);
      toast_info("Репост фотографии в сообщества сделан")
    }else{toast_error("Выберите сообщества для репоста")}
  }

  else if(form_post.querySelector('#repost_radio_message').checked){
    user_connections = form_post.querySelector("#id_user_connections");
    selectedOptions = user_connections.selectedOptions;
    val = false;
    for (var i = 0; i < selectedOptions.length; i++) {if(selectedOptions[i].value) {val = true}}
    if(val){
      link_.open( 'POST', "/gallery/repost/c_m_photo_repost/" + pk + "/" + uuid + "/", true );
      link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      link_.send(form_data);
      toast_info("Репост фотографии в сообщения сделан")
    }else{toast_error("Выберите пользователя для репоста")}
  };

  link_.onreadystatechange = function () {
    if ( this.readyState == 4 && this.status == 200 ) {
      document.querySelector(".votes_fullscreen").style.display = "none";
      document.getElementById("votes_loader").innerHTML="";
    }}
});

on('#ajax', 'click', '#с_ucm_photo_album_repost_btn', function() {
  form_post = document.body.querySelector("#с_uсm_photo_album_repost_form");
  form_data = new FormData(form_post);
  uuid = this.getAttribute("data-uuid");
  pk = this.getAttribute("data-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );

  if (form_post.querySelector('#repost_radio_wall').checked) {
    link_.open( 'POST', "/gallery/repost/с_u_photo_album_repost/" + pk + "/" + uuid + "/", true );
    link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link_.send(form_data);
    toast_info("Репост фотоальбома на стену сделан")
  }

  else if(form_post.querySelector('#repost_radio_community').checked){
    staff_communities = form_post.querySelector("#id_staff_communities");
    selectedOptions = staff_communities.selectedOptions;
    val = false;
    for (var i = 0; i < selectedOptions.length; i++) {if(selectedOptions[i].value) {val = true}}
    if(val){
      link_.open( 'POST', "/gallery/repost/с_c_photo_album_repost/" + pk + "/" + uuid + "/", true );
      link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      link_.send(form_data);
      toast_info("Репост фотоальбома в сообщества сделан")
    }else{toast_error("Выберите сообщества для репоста")}
  }

  else if(form_post.querySelector('#repost_radio_message').checked){
    user_connections = form_post.querySelector("#id_user_connections");
    selectedOptions = user_connections.selectedOptions;
    val = false;
    for (var i = 0; i < selectedOptions.length; i++) {if(selectedOptions[i].value) {val = true}}
    if(val){
      link_.open( 'POST', "/gallery/repost/с_m_photo_album_repost/" + pk + "/" + uuid + "/", true );
      link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      link_.send(form_data);
      toast_info("Репост фотоальбома в сообщения сделан")
    }else{toast_error("Выберите пользователя для репоста")}
  };

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    document.querySelector(".votes_fullscreen").style.display = "none";
    document.getElementById("votes_loader").innerHTML="";
  }}
});

on('#ajax', 'click', '.c_photoComment', function() {
  form = this.parentElement.parentElement.parentElement;
  send_comment(form, form.parentElement.previousElementSibling, '/gallery/community_progs/post-comment/');
});

on('#ajax', 'click', '.c_replyPhotoComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  block = form.parentElement.parentElement.querySelector(".stream_reply_comments");
  send_comment(form, block, '/gallery/community_progs/reply-comment/')
  form.parentElement.style.display = "none";
  block.classList.add("replies_open")
});

on('#ajax', 'click', '.c_replyParentPhotoComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  block = form.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  send_comment(form, block.parentElement, '/gallery/community_progs/reply-comment/')
  form.parentElement.style.display = "none";
  block.classList.add("replies_open")
});

on('#ajax', 'click', '.c_photo_off_comment', function() {
  send_photo_change(this, "/gallery/community_progs/off_comment/", "c_photo_on_comment", "Вкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".c_photo_comments").style.display = "none"
})
on('#ajax', 'click', '.c_photo_on_comment', function() {
  send_photo_change(this, "/gallery/community_progs/on_comment/", "c_photo_off_comment", "Выкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".c_photo_comments").style.display = "unset"
})

on('#ajax', 'click', '.c_photo_comment_delete', function() {
  comment_delete(this, "/gallery/community_progs/delete_comment/", "c_photo_comment_abort_remove")
})
on('#ajax', 'click', '.c_photo_comment_abort_remove', function() {
  comment_abort_delete(this, "/gallery/community_progs/abort_delete_comment/")
});


on('#ajax', 'click', '.u_photo_off_private', function() {
  send_photo_change(this, "/gallery/community_progs/off_private/", "c_photo_on_private", "Вкл. приватность")
})
on('#ajax', 'click', '.c_photo_on_private', function() {
  send_photo_change(this, "/gallery/community_progs/on_private/", "c_photo_off_private", "Выкл. приватность")
})

on('#ajax', 'click', '.c_photo_edit', function() {
  this.parentElement.nextElementSibling.style.display = "block"
})

on('#ajax', 'click', '.c_photo_description', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form.querySelector(".c_photo_description_form"));
  uuid = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute("data-uuid");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/community_progs/description/" + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {

    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    form.previousElementSibling.innerHTML = new_post.innerHTML + '<br><br><span class="c_photo_edit pointer">Редактировать</span>';
    form.style.display = "none";
    form.querySelector('#id_description').value = new_post.innerHTML;
  }}
  link_.send(form_data);
});

on('#ajax', 'click', '.c_photo_off_votes', function() {
  send_photo_change(this, "/gallery/community_progs/off_votes/", "c_photo_on_votes", "Вкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "none";
  post.querySelector(".dislike").style.display = "none";
})
on('#ajax', 'click', '.c_photo_on_votes', function() {
  send_photo_change(this, "/gallery/community_progs/on_votes/", "c_photo_off_votes", "Выкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "unset";
  post.querySelector(".dislike").style.display = "unset";
})

on('#ajax', 'click', '.community_photo_remove', function() {
  send_photo_change(this, "/gallery/community_progs/delete/", "community_photo_abort_remove", "Отмена");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  this.parentElement.parentElement.nextElementSibling.style.display = "none";
  post.querySelector(".order-2").style.display = "none";
  post.querySelector(".card").style.opacity = "0.5";
  this.style.color = "#FF0000";
})
on('#ajax', 'click', '.community_photo_abort_remove', function() {
  send_photo_change(this, "/gallery/community_progs/abort_delete/", "community_photo_remove", "Удалить");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  this.parentElement.parentElement.nextElementSibling.style.display = "unset";
  post.querySelector(".order-2").style.display = "unset";
  post.querySelector(".card").style.opacity = "1";
})

on('#ajax', 'click', '.c_photo_like', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = parent.getAttribute("data-uuid");
  pk = parent.getAttribute("data-pk");
  send_like(parent, "/gallery/votes/community_like/" + uuid + "/" + pk + "/");
  like_reload(this.nextElementSibling, this.nextElementSibling.nextElementSibling.nextElementSibling, "c_all_photo_likes");
});
on('#ajax', 'click', '.c_photo_dislike', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = parent.getAttribute("data-uuid");
  pk = parent.getAttribute("data-pk");
  send_dislike(parent, "/gallery/votes/community_dislike/" + uuid + "/" + pk + "/");
  dislike_reload(this.previousElementSibling, this.nextElementSibling, "c_all_photo_dislikes");
});
on('#ajax', 'click', '.c_photo_like2', function() {
  _this = this;
  photo = _this.parentElement;
  comment_pk = photo.getAttribute("data-pk");
  pk = document.body.querySelector(".data_display").getAttribute("data-pk");
  send_like(photo, "/gallery/votes/community_comment/" + comment_pk + "/" + pk + "/like/");
  like_reload(this.nextElementSibling, this.nextElementSibling.nextElementSibling.nextElementSibling, "u_all_photo_comment_likes")
});
on('#ajax', 'click', '.c_photo_dislike2', function() {
  _this = this;
  photo = _this.parentElement;
  comment_pk = photo.getAttribute("data-pk");
  pk = document.body.querySelector(".data_display").getAttribute("data-pk");
  send_dislike(photo, "/gallery/votes/community_comment/" + comment_pk + "/" + pk + "/dislike/");
  dislike_reload(this.previousElementSibling, this.nextElementSibling, "u_all_photo_comment_dislikes")
});

on('body', 'click', '#c_add_multi_photos', function(event) {
  this.previousElementSibling.click();
})

on('#ajax', 'change', '#c_gallery_photo_add', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  form_data = new FormData(document.body.querySelector("#c_add_photos"));
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/community_progs/add_photo/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    document.body.querySelector("#c_photos_container").insertAdjacentHTML('afterBegin', response.innerHTML);
    document.body.querySelector(".post_empty") ? document.body.querySelector(".post_empty").style.display = "none" : null
  }}
  link_.send(form_data);
});

on('#ajax', 'change', '#c_gallery_album_photo_add', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  uuid = document.body.querySelector(".pk_saver").getAttribute("data-uuid");
  form_data = new FormData(document.body.querySelector("#c_add_photos"));
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/community_progs/add_album_photo/" + pk + "/" + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    photo_list = document.createElement("div");
    response.innerHTML = elem;
    document.body.querySelector("#c_album_photos_container").insertAdjacentHTML('afterBegin', response.innerHTML);
    document.body.querySelector(".post_empty") ? document.body.querySelector(".post_empty").style.display = "none" : null
  }}
  link_.send(form_data);
});
