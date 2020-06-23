on('#ajax', 'click', '#community_article_add', function() {
  var pk = this.getAttribute('data-pk');
  open_fullscreen("/article/c_article_window/" + pk + "/", document.getElementById("create_loader"))
});

on('#ajax', 'click', '#c_add_post', function() {
  form_data = new FormData(document.forms.new_community_post);
  form_post = document.querySelector("#commnity_post");
  lenta_load = form_post.parentElement.nextElementSibling;
  pk = document.body.querySelector(".pk_saver").getAttribute("community-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/posts/add_post_community/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    form_post.querySelector('.id_text').value = "";
    clear_attach_block();

    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    new_post.querySelector(".card") ? (lenta_load.querySelector("#community_stream").prepend(new_post),
                                       toast_info("Запись опубликована"),
                                       lenta_load.querySelector(".post_empty") ? lenta_load.querySelector(".post_empty").style.display = "none" : null)
                                    :  toast_error("Нужно написать или прикрепить что-нибудь!");
  }};

  link_.send(form_data);
});

on('#ajax', 'click', '.c_itemComment', function() {
  form = this.parentElement.parentElement.parentElement;
  send_comment(form, form.parentElement.previousElementSibling, '/posts/community/post-comment/');
});

on('#ajax', 'click', '.c_replyItemComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  send_comment(form, form.parentElement.parentElement.querySelector(".stream_reply_comments"), '/posts/community/reply-comment/')
  form.parentElement.style.display = "none";
});

on('#ajax', 'click', '.c_replyParentItemComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  send_comment(form, form.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement, '/posts/community/reply-comment/')
  form.parentElement.style.display = "none";
});

on('#ajax', 'click', '.c_like', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("data-uuid");
  pk = document.body.querySelector(".pk_saver").getAttribute("community-pk");
  send_like(item, "/posts/votes/community_like/" + uuid + "/" + pk + "/");
  vote_reload("/posts/item_window/c_like_window/" + uuid + "/", "/posts/item_window/u_dislike_window/" + uuid + "/", this.nextElementSibling, this.nextElementSibling.nextElementSibling.nextElementSibling)
});
on('#ajax', 'click', '.c_dislike', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("data-uuid");
  pk = document.body.querySelector(".pk_saver").getAttribute("community-pk");
  send_dislike(item, "/posts/votes/community_dislike/" + uuid + "/" + pk + "/");
  vote_reload("/posts/item_window/c_like_window/" + uuid + "/", "/posts/item_window/u_dislike_window/" + uuid + "/", this.previousElementSibling, this.nextElementSibling)
});
on('#ajax', 'click', '.c_like2', function() {
  _this = this;
  item = _this.parentElement;
  comment_pk = item.getAttribute("data-pk");
  pk = document.body.querySelector(".pk_saver").getAttribute("community-pk");
  send_like(item, "/posts/votes/community_comment/" + comment_pk + "/" + pk + "/like/");
  vote_reload("/posts/item_window/c_comment_like_window/" + comment_pk + "/", "/posts/item_window/u_comment_dislike_window/" + comment_pk + "/", _this.nextElementSibling, _this.nextElementSibling.nextElementSibling.nextElementSibling)
});
on('#ajax', 'click', '.c_dislike2', function() {
  _this = this;
  item = _this.parentElement;
  comment_pk = item.getAttribute("data-pk");
  pk = document.body.querySelector(".pk_saver").getAttribute("community-pk");
  send_dislike(item, "/posts/votes/community_comment/" + comment_pk + "/" + pk + "/dislike/");
  vote_reload("/posts/item_window/c_comment_like_window/" + comment_pk + "/", "/posts/item_window/u_comment_dislike_window/" + comment_pk + "/", _this.previousElementSibling, _this.nextElementSibling)
});

on('body', 'click', '#community_avatar_btn', function(event) {
  this.previousElementSibling.click();
})
on('#ajax', 'change', '#community_avatar_upload', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("community-pk");
  form_data = new FormData(document.body.querySelector("#add_community_avatar"));
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/community/add_avatar/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    document.body.querySelector(".avatar_figure").innerHTML = "";
    img = response.querySelector("img");
    document.body.querySelector(".avatar_figure").append(img);
    }
  }
  link_.send(form_data);
})

on('#ajax', 'click', '.c_post_fixed', function() {
  send_change(this, "/posts/community/fixed/", "c_post_unfixed", "Открепить")
})
on('#ajax', 'click', '.c_post_unfixed', function() {
  send_change(this, "/posts/community/unfixed/", "c_post_fixed", "Закрепить")
})

on('#ajax', 'click', '.c_post_off_comment', function() {
  send_change(this, "/posts/community/off_comment/", "c_post_on_comment", "Вкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".c_item_comments").style.display = "none"
})
on('#ajax', 'click', '.c_post_on_comment', function() {
  send_change(this, "/posts/community/on_comment/", "c_post_off_comment", "Выкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".c_item_comments").style.display = "unset"
})

on('#ajax', 'click', '.c_post_off_votes', function() {
  send_change(this, "/posts/community/off_votes/", "c_post_on_votes", "Вкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "none";
  post.querySelector(".dislike").style.display = "none";
})
on('#ajax', 'click', '.c_post_on_votes', function() {
  send_change(this, "/posts/community/on_votes/", "c_post_off_votes", "Выкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "unset";
  post.querySelector(".dislike").style.display = "unset";
})

on('#ajax', 'click', '.c_post_remove', function() {
  item = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("data-uuid");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/posts/community/delete/" + uuid + "/", true );

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    item.style.display = "none";
    document.querySelector(".item_fullscreen").style.display = "none";
    p = document.createElement("div");
    p.classList.add("card", "mb-3");
    p.style.padding = "20px";
    p.style.display =  "block";

    p.innerHTML = "Запись удалена. <span class='c_post_abort_remove' style='cursor:pointer' data-uuid='" + uuid + "'>Восстановить</span>";
    item.parentElement.insertBefore(p, item);
    item.style.display = "none";
  }};

  link.send( );
});


on('#ajax', 'click', '.c_post_abort_remove', function() {
  item = this.parentElement.nextElementSibling;
  item.style.display = "block";
  uuid = this.getAttribute("data-uuid");
  block = this.parentElement;
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/posts/community/abort_delete/" + uuid + "/", true );

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    block.remove();
  }};

  link.send();
});
