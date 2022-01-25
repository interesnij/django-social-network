on('#ajax', 'click', '#u_ucm_video_repost_btn', function() {
  repost_constructor(this,
                     "/video/repost/u_u_video_repost/",
                     "Репост видеозаписи на стену сделан",
                     "/video/repost/u_c_video_repost/",
                     "Репост видеозаписи в сообщества сделан",
                     "/video/repost/u_m_video_repost/",
                     "Репост видеозаписи в сообщения сделан")
});
on('#ajax', 'click', '#u_ucm_video_list_repost_btn', function() {
  repost_constructor(this,
                     "/video/repost/u_u_video_list_repost/",
                     "Репост видеоальбома на стену сделан",
                     "/video/repost/u_c_video_list_repost/",
                     "Репост видеоальбома в сообщества сделан",
                     "/video/repost/u_m_video_list_repost/",
                     "Репост видеоальбома в сообщения сделан")
});

on('#ajax', 'click', '.u_video_create_window', function(e) {
  e.preventDefault();
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  create_fullscreen("/video/user_progs/create_video/" + pk + "/", "item_fullscreen");
  open_fullscreen("/video/user_progs/create_video/" + pk + "/", loader);
});

on('#ajax', 'click', '.u_video_comment_edit', function() {
  get_edit_comment_form(this, "/video/user_progs/edit_comment/")
});

on('#ajax', 'click', '.u_video_edit_comment_btn', function() {
  post_edit_comment_form(this, "/video/user_progs/edit_comment/")
});

on('#video_loader', 'click', '.u_video_off_comment', function() {
  send_photo_change(this, "/video/user_progs/off_comment/", "u_video_on_comment", "Вкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".load_video_comments").style.display = "none"
});
on('#video_loader', 'click', '.u_video_on_comment', function() {
  send_photo_change(this, "/video/user_progs/on_comment/", "u_video_off_comment", "Выкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".load_video_comments").style.display = "unset"
});

on('#video_loader', 'click', '.u_video_comment_delete', function() {
  comment_delete(this, "/video/user_progs/delete_comment/", "u_video_comment_restore")
});
on('#video_loader', 'click', '.u_video_comment_restore', function() {
  comment_restore(this, "/video/user_progs/restore_comment/")
});

on('#ajax', 'click', '.u_video_edit', function() {
  this.parentElement.nextElementSibling.style.display = "block"
});

on('#video_loader', 'click', '.u_video_off_votes', function() {
  send_photo_change(this, "/video/user_progs/off_votes/", "u_video_on_votes", "Вкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "none";
  post.querySelector(".dislike").style.display = "none";
});
on('#video_loader', 'click', '.u_video_on_votes', function() {
  send_photo_change(this, "/video/user_progs/on_votes/", "u_video_off_votes", "Выкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "unset";
  post.querySelector(".dislike").style.display = "unset";
});

on('body', 'click', '.user_video_remove', function() {
  send_photo_change(this, "/video/user_progs/delete/", "user_video_restore", "Отмена");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  this.parentElement.parentElement.nextElementSibling.style.display = "none";
  post.querySelector(".order-2").style.display = "none";
  post.querySelector(".card").style.opacity = "0.5";
  this.style.color = "#FF0000";
});
on('body', 'click', '.user_video_restore', function() {
  send_photo_change(this, "/video/user_progs/restore/", "user_video_remove", "Удалить");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  this.parentElement.parentElement.nextElementSibling.style.display = "unset";
  post.querySelector(".order-2").style.display = "unset";
  post.querySelector(".card").style.opacity = "1";
});

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

on('#ajax', 'click', '#u_create_video_btn', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");

  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else if (!form.querySelector("#id_uri").value){
    form.querySelector("#id_uri").style.border = "1px #FF0000 solid";
    toast_error("Ссылка на видео - обязательное поле!")
  } else if (!form.querySelector("#id_image").value){
    form.querySelector("#video_holder").style.border = "1px #FF0000 solid";
    toast_error("Фотография на обложку обязательна!")
  } else if (!form.querySelector("#id_list").value){
    form.querySelector("#id_list").style.border = "1px #FF0000 solid";
    toast_error("Выберите список!")
  } else {this.disabled = true}

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/video/user_progs/create_video/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    span1 = response.querySelector('.span1');
    if (span1.classList.contains(document.body.querySelector(".uuid_saver").getAttribute("data-uuid"))){
      container = document.body.querySelector(".is_paginate");
      container.insertAdjacentHTML('afterBegin', response.innerHTML);
      container.querySelector(".items_empty") ? container.querySelector(".items_empty").style.display = "none" : null;
      toast_info("Видео создано!")
    } else{
      toast_info("Видео создано!")
    }
    close_work_fullscreen();
  } else {this.disabled = false}};
  link_.send(form_data);
});

on('#ajax', 'click', '#u_create_video_list_btn', function() {
  this.disabled = true;
  form = document.body.querySelector("#u_video_list_create");
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }
  post_and_load_object_page(form, "/video/user_progs/add_list/", "/users/", "/video_list/", "added_user_video_list")

});

on('#ajax', 'click', '#u_edit_video_list_btn', function() {
  media_list_edit(this, "/video/user_progs/edit_list/", "edited_user_video_list")
});

on('body', 'click', '.u_video_list_remove', function() {
  media_list_delete(this, "/video/user_progs/delete_list/", "u_video_list_remove", "u_video_list_abort_remove", "deleted_user_video_list")
});
on('body', 'click', '.u_video_list_abort_remove', function() {
  media_list_recover(this, "/video/user_progs/restore_list/", "u_video_list_abort_remove", "u_video_list_remove", "restored_community_video_list")
});
