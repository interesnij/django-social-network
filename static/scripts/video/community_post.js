on('#ajax', 'click', '#c_ucm_video_repost_btn', function() {
  repost_constructor(this,
                     "/video/repost/c_u_video_repost/",
                     "Репост видеозаписи на стену сделан",
                     "/video/repost/c_c_video_repost/",
                     "Репост видеозаписи в сообщества сделан",
                     "/video/repost/c_m_video_repost/",
                     "Репост видеозаписи в сообщения сделан")
});
on('#ajax', 'click', '#c_ucm_video_list_repost_btn', function() {
  repost_constructor(this,
                     "/video/repost/c_u_video_list_repost/",
                     "Репост видеоальбома на стену сделан",
                     "/video/repost/c_c_video_list_repost/",
                     "Репост видеоальбома в сообщества сделан",
                     "/video/repost/c_m_video_list_repost/",
                     "Репост видеоальбома в сообщения сделан")
});

on('#ajax', 'click', '.c_video_comment_edit', function() {
  get_edit_comment_form(this, "/video/community_progs/edit_comment/")
});

on('#ajax', 'click', '.c_video_edit_comment_btn', function() {
  post_edit_comment_form(this, "/video/community_progs/edit_comment/")
});

on('#video_loader', 'click', '.c_video_off_comment', function() {
  send_photo_change(this, "/video/community_progs/off_comment/", "c_video_on_comment", "Вкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".load_video_comments").style.display = "none"
})
on('#video_loader', 'click', '.c_video_on_comment', function() {
  send_photo_change(this, "/video/community_progs/on_comment/", "c_video_off_comment", "Выкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".load_video_comments").style.display = "unset"
})

on('#video_loader', 'click', '.c_video_comment_delete', function() {
  comment_delete(this, "/video/community_progs/delete_comment/", "c_video_comment_restore")
})
on('#video_loader', 'click', '.c_video_comment_restore', function() {
  comment_restore(this, "/video/community_progs/restore_comment/")
});


on('#video_loader', 'click', '.u_video_off_private', function() {
  send_photo_change(this, "/video/community_progs/off_private/", "c_video_on_private", "Вкл. приватность")
})
on('#video_loader', 'click', '.c_video_on_private', function() {
  send_photo_change(this, "/video/community_progs/on_private/", "c_video_off_private", "Выкл. приватность")
})

on('#video_loader', 'click', '.c_video_off_votes', function() {
  send_photo_change(this, "/video/community_progs/off_votes/", "c_video_on_votes", "Вкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "none";
  post.querySelector(".dislike").style.display = "none";
})
on('#video_loader', 'click', '.c_video_on_votes', function() {
  send_photo_change(this, "/video/community_progs/on_votes/", "c_video_off_votes", "Выкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "unset";
  post.querySelector(".dislike").style.display = "unset";
})

on('body', 'click', '.community_video_remove', function() {
  send_photo_change(this, "/video/community_progs/delete/", "community_video_restore", "Отмена");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  this.parentElement.parentElement.nextElementSibling.style.display = "none";
  post.querySelector(".order-2").style.display = "none";
  post.querySelector(".card").style.opacity = "0.5";
  this.style.color = "#FF0000";
})
on('body', 'click', '.community_video_restore', function() {
  send_photo_change(this, "/video/community_progs/restore/", "community_video_remove", "Удалить");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  this.parentElement.parentElement.nextElementSibling.style.display = "unset";
  post.querySelector(".order-2").style.display = "unset";
  post.querySelector(".card").style.opacity = "1";
})

on('#video_loader', 'click', '.c_video_like', function() {
  video = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = document.body.querySelector(".data_display").getAttribute("data-uuid");
  pk = document.body.querySelector(".data_display").getAttribute("data-pk");
  send_like(video, "/video/votes/community_like/" + uuid + "/" + pk + "/");
  like_reload(this.nextElementSibling, this.nextElementSibling.nextElementSibling.nextElementSibling, "u_all_video_likes");
});
on('#video_loader', 'click', '.c_video_dislike', function() {
  video = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = document.body.querySelector(".data_display").getAttribute("data-uuid");
  pk = document.body.querySelector(".data_display").getAttribute("data-pk");
  send_dislike(video, "/video/votes/community_dislike/" + uuid + "/" + pk + "/");
  dislike_reload(this.previousElementSibling, this.nextElementSibling, "u_all_video_dislikes");
});
on('#video_loader', 'click', '.c_video_like2', function() {
  _this = this;
  video = _this.parentElement;
  comment_pk = video.getAttribute("data-pk");
  send_like(video, "/video/votes/community_comment/" + comment_pk + "/like/");
  like_reload(this.nextElementSibling, this.nextElementSibling.nextElementSibling.nextElementSibling, "u_all_video_comment_likes")
});
on('#video_loader', 'click', '.c_video_dislike2', function() {
  _this = this;
  video = _this.parentElement;
  comment_pk = video.getAttribute("data-pk");
  send_dislike(video, "/video/votes/community_comment/" + comment_pk + "/" + "/dislike/");
  dislike_reload(this.previousElementSibling, this.nextElementSibling, "u_all_video_comment_dislikes")
});

on('#ajax', 'click', '#c_add_video_list_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }
  post_and_load_object_page(form, "/video/community_progs/add_list/", "/communities/", "/video_list/");
});

on('#ajax', 'click', '#c_edit_video_list_btn', function() {
  media_list_edit(this, "/video/community_progs/edit_list/")
});

on('body', 'click', '.c_video_list_remove', function() {
  media_list_delete(this, "/video/community_progs/delete_list/", "c_video_list_remove", "c_video_list_abort_remove")
});
on('body', 'click', '.c_video_list_abort_remove', function() {
  media_list_recover(this, "/video/community_progs/restore_list/", "c_video_list_abort_remove", "c_video_list_remove")
});

on('#ajax', 'click', '.c_video_create_window', function(e) {
  e.preventDefault();
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  create_fullscreen("/video/community_progs/create_video/" + pk + "/", "item_fullscreen");
});

on('#ajax', 'click', '.c_add_video_in_list', function() {
  add_item_in_list(this, '/video/community_progs/add_video_in_list/', "c_add_video_in_list", "c_remove_video_from_list")
})
on('#ajax', 'click', '.c_remove_video_from_list', function() {
  remove_item_from_list(this, '/video/community_progs/remove_video_from_list/', "c_remove_video_from_list", "c_add_video_in_list")
})
