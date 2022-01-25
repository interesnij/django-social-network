
on('body', 'click', '.c_photo_list_remove', function() {
  media_list_delete(this, "/gallery/community_progs/delete_list/", "c_photo_list_remove", "c_photo_list_abort_remove", "removed_community_photo_list")
});
on('body', 'click', '.c_photo_list_abort_remove', function() {
  media_list_recover(this, "/gallery/community_progs/restore_list/", "c_photo_list_abort_remove", "c_photo_list_remove", "restored_community_photo_list")
});

on('#ajax', 'click', '#c_edit_photo_list_btn', function() {
  media_list_edit(this, "/gallery/community_progs/edit_list/", "edited_community_photo_list")
});

on('#ajax', 'click', '#c_create_photo_list_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }
  post_and_load_object_page(form, "/gallery/community_progs/add_list/", "/communities/", "/list/", "added_community_photo_list");
});

on('#ajax', 'click', '#c_ucm_photo_repost_btn', function() {
  repost_constructor(this,
                     "/gallery/repost/c_u_photo_repost/",
                     "Репост фотографии на стену сделан",
                     "/gallery/repost/c_c_photo_repost/",
                     "Репост фотографии в сообщества сделан",
                     "/gallery/repost/c_m_photo_repost/",
                     "Репост фотографии в сообщения сделан")
});

on('#ajax', 'click', '#c_ucm_photo_list_repost_btn', function() {
  repost_constructor(this,
                     "/gallery/repost/c_u_photo_list_repost/",
                     "Репост фотоальбома на стену сделан",
                     "/gallery/repost/c_c_photo_list_repost/",
                     "Репост фотоальбома в сообщества сделан",
                     "/gallery/repost/c_m_photo_list_repost/",
                     "Репост фотоальбома в сообщения сделан")
});

on('#ajax', 'click', '.c_photo_comment_edit', function() {
  get_edit_comment_form(this, "/gallery/community_progs/edit_comment/")
});

on('#ajax', 'click', '.c_photo_edit_comment_btn', function() {
  post_edit_comment_form(this, "/gallery/community_progs/edit_comment/")
});

on('#ajax', 'click', '.c_photo_off_comment', function() {
  send_photo_change(this, "/gallery/community_progs/off_comment/", "c_photo_on_comment", "Вкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".load_photo_comments").style.display = "none"
})
on('#ajax', 'click', '.c_photo_on_comment', function() {
  send_photo_change(this, "/gallery/community_progs/on_comment/", "c_photo_off_comment", "Выкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".load_photo_comments").style.display = "unset"
});

on('#ajax', 'click', '.c_photo_comment_delete', function() {
  comment_delete(this, "/gallery/community_progs/delete_comment/", "c_photo_comment_restore")
});
on('#ajax', 'click', '.c_photo_comment_restore', function() {
  comment_restore(this, "/gallery/community_progs/restore_comment/")
});

on('#ajax', 'click', '.c_photo_edit', function() {
  this.parentElement.nextElementSibling.style.display = "block"
});

on('#ajax', 'click', '.c_photo_description', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form.querySelector(".c_photo_description_form"));
  data_display = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = data_display.getAttribute("data-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/community_progs/description/" + pk + "/", true );
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
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "none";
  post.querySelector(".dislike").style.display = "none";
});
on('#ajax', 'click', '.c_photo_on_votes', function() {
  send_photo_change(this, "/gallery/community_progs/on_votes/", "c_photo_off_votes", "Выкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "unset";
  post.querySelector(".dislike").style.display = "unset";
});

on('#ajax', 'click', '.community_photo_remove', function() {
  send_photo_change(this, "/gallery/community_progs/delete/", "community_photo_restore", "Отмена");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  this.parentElement.parentElement.nextElementSibling.style.display = "none";
  post.querySelector(".order-2").style.display = "none";
  post.querySelector(".card").style.opacity = "0.5";
  this.style.color = "#FF0000";
});
on('#ajax', 'click', '.community_photo_restore', function() {
  send_photo_change(this, "/gallery/community_progs/restore/", "community_photo_remove", "Удалить");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  this.parentElement.parentElement.nextElementSibling.style.display = "unset";
  post.querySelector(".order-2").style.display = "unset";
  post.querySelector(".card").style.opacity = "1";
});

on('#ajax', 'click', '.c_photo_like', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = parent.getAttribute("owner-pk");
  c_pk = parent.getAttribute("data-pk");
  send_like(parent, "/gallery/votes/community_like/" + pk + "/" + c_pk + "/");
  like_reload(this.nextElementSibling, this.nextElementSibling.nextElementSibling.nextElementSibling, "c_all_photo_likes");
});
on('#ajax', 'click', '.c_photo_dislike', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  photo_pk = parent.getAttribute("data-pk");
  pk = parent.getAttribute("owner-pk");
  send_dislike(parent, "/gallery/votes/community_dislike/" + photo_pk + "/" + pk + "/");
  dislike_reload(this.previousElementSibling, this.nextElementSibling, "c_all_photo_dislikes");
});

on('#ajax', 'click', '.mob_c_photo_off_comment', function() {
  mob_send_change(this, "/gallery/community_progs/off_comment/", "mob_c_photo_on_comment", "Вкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".load_photo_comments").style.display = "none"
});
on('#ajax', 'click', '.mob_c_photo_on_comment', function() {
  mob_send_change(this, "/gallery/community_progs/on_comment/", "mob_c_photo_off_comment", "Выкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".load_photo_comments").style.display = "unset"
});

on('#ajax', 'click', '.mob_c_photo_off_votes', function() {
  mob_send_change(this, "/gallery/community_progs/off_votes/", "mob_c_photo_on_votes", "Вкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "none";
  post.querySelector(".dislike").style.display = "none";
});
on('#ajax', 'click', '.mob_c_photo_on_votes', function() {
  mob_send_change(this, "/gallery/community_progs/on_votes/", "mob_c_photo_off_votes", "Выкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "unset";
  post.querySelector(".dislike").style.display = "unset";
});
on('#ajax', 'click', '.mob_community_photo_remove', function() {
  mob_send_change(this, "/gallery/community_progs/delete/", "mob_community_photo_restore", "Отмена");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".content_block").style.display = "none";
  post.querySelector(".image_card").style.opacity = "0.5";
});
on('#ajax', 'click', '.mob_community_photo_restore', function() {
  mob_send_change(this, "/gallery/community_progs/restore/", "mob_community_photo_remove", "Удалить");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".content_block").style.display = "unset";
  post.querySelector(".image_card").style.opacity = "1";
});
