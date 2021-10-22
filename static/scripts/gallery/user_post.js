// скрипты галереи для пользователя

on('#ajax', 'click', '.u_add_photo_list', function(e) {
  _this = this;
  parent = this.parentElement.parentElement.parentElement;
  uuid = parent.getAttribute("data-uuid");
  var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/gallery/user_progs/add_list/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
    if ( link.readyState == 4 && link.status == 200 ) {
      _this.innerHTML = "";
      _this.classList.add("u_remove_photo_list");
      _this.classList.remove("u_add_photo_list")
      _this.innerHTML = 'Удалить'
  }};
  link.send( null );
});
on('body', 'click', '.u_photo_list_remove', function() {
  media_list_delete(this, "/gallery/user_progs/delete_list/", "u_photo_list_remove", "u_photo_list_abort_remove")
});
on('body', 'click', '.u_photo_list_abort_remove', function() {
  media_list_recover(this, "/gallery/user_progs/restore_list/", "u_photo_list_abort_remove", "u_photo_list_remove")
});

on('#ajax', 'click', '#u_edit_photo_list_btn', function() {
  media_list_edit(this, "/gallery/user_progs/edit_list/")
});

on('#ajax', 'click', '#u_create_photo_list_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }
  post_and_load_object_page(form, "/gallery/user_progs/add_list/", "/users/", "/list/");
});

on('#ajax', 'click', '#u_ucm_photo_repost_btn', function() {
  repost_constructor(this,
                     "/gallery/repost/u_u_photo_repost/",
                     "Репост фотографии на стену сделан",
                     "/gallery/repost/u_c_photo_repost/",
                     "Репост фотографии в сообщества сделан",
                     "/gallery/repost/u_m_photo_repost/",
                     "Репост фотографии в сообщения сделан")
});

on('#ajax', 'click', '#u_ucm_photo_list_repost_btn', function() {
  repost_constructor(this,
                     "/gallery/repost/u_u_photo_list_repost/",
                     "Репост фотоальбома на стену сделан",
                     "/gallery/repost/u_c_photo_list_repost/",
                     "Репост фотоальбома в сообщества сделан",
                     "/gallery/repost/u_m_photo_list_repost/",
                     "Репост фотоальбома в сообщения сделан")
});

on('#ajax', 'click', '.u_photo_comment_edit', function() {
  get_edit_comment_form(this, "/gallery/user_progs/edit_comment/")
});

on('#ajax', 'click', '.u_photo_edit_comment_btn', function() {
  post_edit_comment_form(this, "/gallery/user_progs/edit_comment/")
});

on('#ajax', 'click', '.u_photo_off_comment', function() {
  send_photo_change(this, "/gallery/user_progs/off_comment/", "u_photo_on_comment", "Вкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".load_photo_comments").style.display = "none"
});
on('#ajax', 'click', '.u_photo_on_comment', function() {
  send_photo_change(this, "/gallery/user_progs/on_comment/", "u_photo_off_comment", "Выкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".load_photo_comments").style.display = "unset"
});

on('#ajax', 'click', '.u_photo_comment_delete', function() {
  comment_delete(this, "/gallery/user_progs/delete_comment/", "u_photo_comment_restore")
});
on('#ajax', 'click', '.u_photo_comment_restore', function() {
  comment_restore(this, "/gallery/user_progs/restore_comment/")
});

on('#ajax', 'click', '.u_photo_off_private', function() {
  send_photo_change(this, "/gallery/user_progs/off_private/", "u_photo_on_private", "Вкл. приватность")
});
on('#ajax', 'click', '.u_photo_on_private', function() {
  send_photo_change(this, "/gallery/user_progs/on_private/", "u_photo_off_private", "Выкл. приватность")
});

on('#ajax', 'click', '.u_photo_edit', function() {
  this.parentElement.nextElementSibling.style.display = "block"
});

on('#ajax', 'click', '.u_photo_description', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form.querySelector(".u_photo_description_form"));
  uuid = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute("data-uuid");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/user_progs/description/" + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {

    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    form.previousElementSibling.innerHTML = new_post.innerHTML + '<br><br><span class="u_photo_edit pointer">Редактировать</span>';
    form.style.display = "none";
    form.querySelector('#id_description').value = new_post.innerHTML;
  }}
  link_.send(form_data);
});

on('#ajax', 'click', '.u_photo_off_votes', function() {
  send_photo_change(this, "/gallery/user_progs/off_votes/", "u_photo_on_votes", "Вкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "none";
  post.querySelector(".dislike").style.display = "none";
});
on('#ajax', 'click', '.u_photo_on_votes', function() {
  send_photo_change(this, "/gallery/user_progs/on_votes/", "u_photo_off_votes", "Выкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "unset";
  post.querySelector(".dislike").style.display = "unset";
});

on('#ajax', 'click', '.user_photo_remove', function() {
  send_photo_change(this, "/gallery/user_progs/delete/", "user_photo_restore", "Отмена");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  this.parentElement.parentElement.nextElementSibling.style.display = "none";
  post.querySelector(".order-2").style.display = "none";
  post.querySelector(".card").style.opacity = "0.5";
  this.style.color = "#FF0000";
});
on('#ajax', 'click', '.user_photo_restore', function() {
  send_photo_change(this, "/gallery/user_progs/restore/", "user_photo_remove", "Удалить");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  this.parentElement.parentElement.nextElementSibling.style.display = "unset";
  post.querySelector(".order-2").style.display = "unset";
  post.querySelector(".card").style.opacity = "1";
});

on('#ajax', 'click', '.u_photo_like', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = parent.getAttribute("data-uuid");
  pk = parent.getAttribute("data-pk");
  send_like(parent, "/gallery/votes/user_like/" + uuid + "/" + pk + "/");
  like_reload(this.nextElementSibling, this.nextElementSibling.nextElementSibling.nextElementSibling, "u_all_photo_likes");
});
on('#ajax', 'click', '.u_photo_dislike', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = parent.getAttribute("data-uuid");
  pk = parent.getAttribute("data-pk");
  send_dislike(parent, "/gallery/votes/user_dislike/" + uuid + "/" + pk + "/");
  dislike_reload(this.previousElementSibling, this.nextElementSibling, "u_all_photo_dislikes");
});
on('#ajax', 'click', '.u_photo_like2', function() {
  _this = this;
  photo = _this.parentElement;
  comment_pk = photo.getAttribute("data-pk");
  pk = document.body.querySelector(".data_display").getAttribute("data-pk");
  send_like(photo, "/gallery/votes/user_comment/" + comment_pk + "/" + pk + "/like/");
  like_reload(this.nextElementSibling, this.nextElementSibling.nextElementSibling.nextElementSibling, "u_all_photo_comment_likes")
});
on('#ajax', 'click', '.u_photo_dislike2', function() {
  _this = this;
  photo = _this.parentElement;
  comment_pk = photo.getAttribute("data-pk");
  pk = document.body.querySelector(".data_display").getAttribute("data-pk");
  send_dislike(photo, "/gallery/votes/user_comment/" + comment_pk + "/" + pk + "/dislike/");
  dislike_reload(this.previousElementSibling, this.nextElementSibling, "u_all_photo_comment_dislikes")
});

on('#ajax', 'change', '#u_gallery_photo_add', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  form_data = new FormData(document.body.querySelector("#add_photos"));
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/user_progs/add_photos_in_main_list/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    document.body.querySelector(".is_block_paginate").insertAdjacentHTML('afterBegin', response.innerHTML);
    document.body.querySelector(".items_empty") ? document.body.querySelector(".items_empty").style.display = "none" : null
  }}
  link_.send(form_data);
});

on('#ajax', 'change', '#u_gallery_list_photo_add', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  form = document.body.querySelector("#add_photos");
  form_data = new FormData(form);
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/user_progs/add_photos_in_photo_list/" + pk + "/" + form.getAttribute("data-uuid") + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    photo_list = document.createElement("div");
    response.innerHTML = elem;
    document.body.querySelector(".is_block_paginate").insertAdjacentHTML('afterBegin', response.innerHTML);
    document.body.querySelector(".items_empty") ? document.body.querySelector(".items_empty").style.display = "none" : null
  }}
  link_.send(form_data);
});

on('#ajax', 'change', '#user_avatar_upload', function() {
  parent = this.parentElement;
  post_with_pk_and_reload(parent, "/gallery/user_progs/add_avatar/")
});

on('#ajax', 'change', '#u_photo_attach', function() {
  if (this.files.length > 10) {
      toast_error("Не больше 10 фотографий");return
  }
  form_data = new FormData(this.parentElement);
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/user_progs/add_attach_photo/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    photo_list = response.querySelectorAll(".pag");
    photo_post_upload_attach(photo_list, document.body.querySelector(".attach_block"));
    }
    close_fullscreen();
  }
  link_.send(form_data);
});

on('#ajax', 'change', '#u_photo_comment_attach', function() {
  if (this.files.length > 2) {
      toast_error("Не больше 2 фотографий");return
  }
  form_data = new FormData(this.parentElement);
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/user_progs/add_attach_photo/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    photo_list = response.querySelectorAll(".pag");
    photo_comment_upload_attach(photo_list, document.body.querySelector(".current_file_dropdown").parentElement.parentElement);
    }
    close_fullscreen();
  }
  link_.send(form_data);
});

on('#ajax', 'click', '.u_add_photo_in_list', function() {
  add_item_in_list(this, '/gallery/user_progs/add_photo_in_list/', "u_add_photo_in_list", "u_remove_photo_from_list")
});
on('#ajax', 'click', '.u_remove_photo_from_list', function() {
  remove_item_from_list(this, '/gallery/user_progs/remove_photo_from_list/', "u_remove_photo_from_list", "u_add_photo_in_list")
});

on('#ajax', 'click', '.mob_u_photo_off_comment', function() {
  mob_send_change(this, "/gallery/user_progs/off_comment/", "mob_u_photo_on_comment", "Вкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".load_photo_comments").style.display = "none"
});
on('#ajax', 'click', '.mob_u_photo_on_comment', function() {
  mob_send_change(this, "/gallery/user_progs/on_comment/", "mob_u_photo_off_comment", "Выкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".load_photo_comments").style.display = "unset"
});
on('#ajax', 'click', '.mob_u_photo_off_private', function() {
  mob_send_change(this, "/gallery/user_progs/off_private/", "mob_u_photo_on_private", "Вкл. приватность")
});
on('#ajax', 'click', '.mob_u_photo_on_private', function() {
  mob_send_change(this, "/gallery/user_progs/on_private/", "mob_u_photo_off_private", "Выкл. приватность")
});
on('#ajax', 'click', '.mob_u_photo_off_votes', function() {
  mob_send_change(this, "/gallery/user_progs/off_votes/", "mob_u_photo_on_votes", "Вкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "none";
  post.querySelector(".dislike").style.display = "none";
});
on('#ajax', 'click', '.mob_u_photo_on_votes', function() {
  mob_send_change(this, "/gallery/user_progs/on_votes/", "mob_u_photo_off_votes", "Выкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "unset";
  post.querySelector(".dislike").style.display = "unset";
});
on('#ajax', 'click', '.mob_user_photo_remove', function() {
  mob_send_change(this, "/gallery/user_progs/delete/", "mob_user_photo_restore", "Отмена");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".content_block").style.display = "none";
  post.querySelector(".image_card").style.opacity = "0.5";
});
on('#ajax', 'click', '.mob_user_photo_restore', function() {
  mob_send_change(this, "/gallery/user_progs/restore/", "mob_user_photo_remove", "Удалить");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".content_block").style.display = "unset";
  post.querySelector(".image_card").style.opacity = "1";
});
