
// скрипты галереи для сообщества

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
    form.previousElementSibling.innerHTML = new_post.innerHTML + '<br><br><span style="cursor:pointer" class="c_photo_edit">Редактировать</span>';
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
  photo = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = document.body.querySelector(".data_display").getAttribute("data-uuid");
  pk = document.body.querySelector(".data_display").getAttribute("data-pk");
  send_like(photo, "/gallery/votes/community_like/" + uuid + "/" + pk + "/");
  vote_reload("/gallery/window/c_like_window/" + uuid + "/", "/gallery/window/c_dislike_window/" + uuid + "/", this.nextElementSibling, this.nextElementSibling.nextElementSibling.nextElementSibling)
});
on('#ajax', 'click', '.c_photo_dislike', function() {
  photo = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = document.body.querySelector(".data_display").getAttribute("data-uuid");
  pk = document.body.querySelector(".data_display").getAttribute("data-pk");
  send_dislike(photo, "/gallery/votes/community_dislike/" + uuid + "/" + pk + "/");
  vote_reload("/gallery/window/c_like_window/" + uuid + "/", "/gallery/window/c_dislike_window/" + uuid + "/", this.previousElementSibling, this.nextElementSibling)
});
on('#ajax', 'click', '.c_photo_like2', function() {
  _this = this;
  photo = _this.parentElement;
  comment_pk = photo.getAttribute("data-pk");
  send_like(photo, "/gallery/votes/community_comment/" + comment_pk + "/like/");
  vote_reload("/gallery/window/c_comment_like_window/" + comment_pk + "/", "/gallery/window/c_comment_dislike_window/" + comment_pk + "/", _this.nextElementSibling, _this.nextElementSibling.nextElementSibling.nextElementSibling)
});
on('#ajax', 'click', '.c_photo_dislike2', function() {
  _this = this;
  photo = _this.parentElement;
  comment_pk = photo.getAttribute("data-pk");
  send_dislike(photo, "/gallery/votes/community_comment/" + comment_pk + "/" + "/dislike/");
  vote_reload("/gallery/window/c_comment_like_window/" + comment_pk + "/", "/gallery/window/c_comment_dislike_window/" + comment_pk + "/", _this.previousElementSibling, _this.nextElementSibling)
});

on('body', 'click', '#c_add_multi_photos', function(event) {
  this.previousElementSibling.click();
})

on('#ajax', 'change', '#c_gallery_photo_add', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  form_data = new FormData(document.body.querySelector("#c_add_photos"));
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/community/add_photo/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    photo_list = response.querySelector("#c_photos_container");
    response.innerHTML = photo_list.innerHTML;
    response.classList.add("row");
    response.style.marginLeft = "0";
    response.style.marginRight = "0";
    document.body.querySelector("#c_photos_container").prepend(response);
    document.body.querySelector(".post_empty") ? document.body.querySelector(".post_empty").style.display = "none" : null
  }}
  link_.send(form_data);
});

on('#ajax', 'change', '#c_gallery_album_photo_add', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  uuid = document.body.querySelector(".pk_saver").getAttribute("data-uuid");
  form_data = new FormData(document.body.querySelector("#c_add_photos"));
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/community/add_album_photo/" + pk + "/" + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    photo_list = document.createElement("div");
    response.innerHTML = elem;
    photo_list.innerHTML = response.querySelector("#c_photos_container").innerHTML;
    photo_list.classList.add("row");
    photo_list.style.marginLeft = "0";
    photo_list.style.marginRight = "0";
    document.body.querySelector(".post_empty") ? document.body.querySelector(".post_empty").style.display = "none" : null
    document.body.querySelector("#c_photos_container").prepend(photo_list);
  }}
  link_.send(form_data);
});
