on('#ajax', 'click', '.u_photoComment', function() {
  form = this.parentElement.parentElement.parentElement;
  send_comment(form, form.parentElement.previousElementSibling, '/gallery/user_progs/post-comment/');
});

on('#ajax', 'click', '.u_replyPostComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  send_comment(form, form.parentElement.parentElement.querySelector(".stream_reply_comments"), '/gallery/user_progs/reply-comment/')
  form.parentElement.style.display = "none";
});

on('#ajax', 'click', '.u_replyParentPostComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  send_comment(form, form.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement, '/gallery/user_progs/reply-comment/')
  form.parentElement.style.display = "none";
});

on('#ajax', 'click', '.u_photo_off_comment', function() {
  send_photo_change(this, "/gallery/user_progs/off_comment/", "u_photo_on_comment", "Вкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".u_photo_comments").style.display = "none"
})
on('#ajax', 'click', '.u_photo_on_comment', function() {
  send_photo_change(this, "/gallery/user_progs/on_comment/", "u_photo_off_comment", "Выкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".u_photo_comments").style.display = "unset"
})

on('#ajax', 'click', '.u_photo_off_private', function() {
  send_photo_change(this, "/gallery/user_progs/off_private/", "u_photo_on_private", "Вкл. приватность")
})
on('#ajax', 'click', '.u_photo_on_private', function() {
  send_photo_change(this, "/gallery/user_progs/on_private/", "u_photo_off_private", "Выкл. приватность")
})

on('#ajax', 'click', '.u_photo_edit', function() {
  this.parentElement.nextElementSibling.style.display = "block"
})

on('#ajax', 'click', '.u_photo_description', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form.querySelector(".u_photo_description_form"));
  uuid = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute("data-uuid");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/user_progs/description/" + uuid + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {

    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    form.previousElementSibling.innerHTML = new_post.innerHTML + '<br><br><span style="cursor:pointer" class="u_photo_edit">Редактировать</span>';
    form.style.display = "none";
    form.querySelector('#id_description').value = new_post.innerHTML;
  }}
  link_.send(form_data);
});

on('#ajax', 'click', '.u_photo_off_votes', function() {
  send_photo_change(this, "/gallery/user_progs/off_votes/", "u_photo_on_votes", "Вкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "none";
  post.querySelector(".dislike").style.display = "none";
})
on('#ajax', 'click', '.u_photo_on_votes', function() {
  send_photo_change(this, "/gallery/user_progs/on_votes/", "u_photo_off_votes", "Выкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "unset";
  post.querySelector(".dislike").style.display = "unset";
})

on('#ajax', 'click', '.user_photo_remove', function() {
  send_photo_change(this, "/gallery/user_progs/delete/", "user_photo_abort_remove", "Отмена");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  this.parentElement.parentElement.nextElementSibling.style.display = "none";
  post.querySelector(".order-2").style.display = "none";
  post.querySelector(".card").style.opacity = "0.5";
  this.style.color = "#FF0000";
})
on('#ajax', 'click', '.user_photo_abort_remove', function() {
  send_photo_change(this, "/gallery/user_progs/abort_delete/", "user_photo_remove", "Удалить");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  this.parentElement.parentElement.nextElementSibling.style.display = "unset";
  post.querySelector(".order-2").style.display = "unset";
  post.querySelector(".card").style.opacity = "1";
})

on('#ajax', 'click', '.u_photo_like', function() {
  photo = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = photo.getAttribute("data-uuid");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_like(photo, "/gallery/votes/user_like/" + uuid + "/" + pk + "/");
  vote_reload("/gallery/photo_window/u_like_window/" + uuid + "/", "/gallery/photo_window/u_dislike_window/" + uuid + "/", this.nextElementSibling, this.nextElementSibling.nextElementSibling.nextElementSibling)
});
on('#ajax', 'click', '.u_photo_dislike', function() {
  photo = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = photo.getAttribute("data-uuid");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_dislike(photo, "/gallery/votes/user_dislike/" + uuid + "/" + pk + "/");
  vote_reload("/gallery/photo_window/u_like_window/" + uuid + "/", "/gallery/photo_window/u_dislike_window/" + uuid + "/", this.previousElementSibling, this.nextElementSibling)
});
on('#ajax', 'click', '.u_photo_dislike2', function() {
  _this = this;
  photo = _this.parentElement;
  comment_pk = photo.getAttribute("data-pk");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_like(photo, "/gallery/votes/user_comment/" + comment_pk + "/" + pk + "/like/");
  vote_reload("/gallery/photo_window/u_comment_like_window/" + comment_pk + "/", "/gallery/photo_window/u_comment_dislike_window/" + comment_pk + "/", _this.nextElementSibling, _this.nextElementSibling.nextElementSibling.nextElementSibling)
});
on('#ajax', 'click', '.u_photo_dislike2', function() {
  _this = this;
  photo = _this.parentElement;
  comment_pk = photo.getAttribute("data-pk");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_dislike(photo, "/gallery/votes/user_comment/" + comment_pk + "/" + pk + "/dislike/");
  vote_reload("/gallery/photo_window/u_comment_like_window/" + comment_pk + "/", "/gallery/photo_window/u_comment_dislike_window/" + comment_pk + "/", _this.previousElementSibling, _this.nextElementSibling)
});

on('body', 'click', '#u_add_multi_photos', function(event) {
  this.previousElementSibling.click();
})

on('#ajax', 'change', '#u_gallery_photo_add', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  form_data = new FormData(document.body.querySelector("#add_photos"));
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/user/add_photo/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    photo_list = response.querySelector("#photos_container");
    response.innerHTML = photo_list.innerHTML;
    document.body.querySelector("#photos_container").prepend(response);
  }}
  link_.send(form_data);
});

on('#ajax', 'change', '#u_gallery_album_photo_add', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  uuid = document.body.querySelector(".pk_saver").getAttribute("album-uuid");
  form_data = new FormData(document.body.querySelector("#add_photos"));
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/user/add_album_photo/" + pk + "/" + uuid + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    photo_list = document.createElement("div");
    response.innerHTML = elem;
    photo_list.innerHTML = response.querySelector("#photos_container").innerHTML;
    photo_list.classList.add("row");
    photo_list.style.marginLeft = "0";
    photo_list.style.marginRight = "0";
    document.body.querySelector("#photos_container").prepend(photo_list);
  }}
  link_.send(form_data);
});
