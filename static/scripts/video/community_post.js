

on('#video_loader', 'click', '.c_video_off_comment', function() {
  send_photo_change(this, "/video/community_progs/off_comment/", "c_video_on_comment", "Вкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".load_video_comments").style.display = "none"
});
on('#video_loader', 'click', '.c_video_on_comment', function() {
  send_photo_change(this, "/video/community_progs/on_comment/", "c_video_off_comment", "Выкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".load_video_comments").style.display = "unset"
});


on('#video_loader', 'click', '.c_video_off_votes', function() {
  send_photo_change(this, "/video/community_progs/off_votes/", "c_video_on_votes", "Вкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "none";
  post.querySelector(".dislike").style.display = "none";
});
on('#video_loader', 'click', '.c_video_on_votes', function() {
  send_photo_change(this, "/video/community_progs/on_votes/", "c_video_off_votes", "Выкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "unset";
  post.querySelector(".dislike").style.display = "unset";
});

on('body', 'click', '.community_video_remove', function() {
  send_photo_change(this, "/video/community_progs/delete/", "community_video_restore", "Отмена");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  this.parentElement.parentElement.nextElementSibling.style.display = "none";
  post.querySelector(".order-2").style.display = "none";
  post.querySelector(".card").style.opacity = "0.5";
  this.style.color = "#FF0000";
});
on('body', 'click', '.community_video_restore', function() {
  send_photo_change(this, "/video/community_progs/restore/", "community_video_remove", "Удалить");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  this.parentElement.parentElement.nextElementSibling.style.display = "unset";
  post.querySelector(".order-2").style.display = "unset";
  post.querySelector(".card").style.opacity = "1";
});

on('#ajax', 'click', '#c_add_video_list_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }
  post_and_load_object_page(form, "/video/community_progs/add_list/", "/communities/", "/video_list/", "added_community_video_list");
});

on('#ajax', 'click', '#c_edit_video_list_btn', function() {
  media_list_edit(this, "/video/community_progs/edit_list/", "edited_community_video_list")
});

on('body', 'click', '.c_video_list_remove', function() {
  media_list_delete(this, "/video/community_progs/delete_list/", "c_video_list_remove", "c_video_list_abort_remove", "removed_community_video_list")
});
on('body', 'click', '.c_video_list_abort_remove', function() {
  media_list_recover(this, "/video/community_progs/restore_list/", "c_video_list_abort_remove", "c_video_list_remove", "restored_community_video_list")
});

on('#ajax', 'click', '.c_video_create_window', function(e) {
  e.preventDefault();
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  create_fullscreen("/video/community_progs/create_video/" + pk + "/", "item_fullscreen");
});
