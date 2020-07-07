on('#ajax', 'click', '#article_add', function() {
  var pk = this.getAttribute('data-pk');
  open_fullscreen("/article/u_article_window/" + pk + "/", document.getElementById("create_loader"));
  //setTimeout(function() { CKEDITOR.replace('id_content'); CKEDITOR.instances.id_content.updateElement(); }, 1000);
});

on('#ajax', 'click', '#form_post_btn', function() {
  form_data = new FormData(document.forms.new_post);
  form_post = document.querySelector("#form_post");
  lenta_load = form_post.parentElement.nextElementSibling;
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/posts/add_post/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    form_post.querySelector('.id_text').value = "";
    clear_attach_block();

    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    new_post.querySelector(".card") ? (lenta_load.querySelector(".stream").prepend(new_post),
                                       toast_info("Запись опубликована"),
                                       lenta_load.querySelector(".post_empty") ? lenta_load.querySelector(".post_empty").style.display = "none" : null)
                                    :  toast_error("Нужно написать или прикрепить что-нибудь!");
  }};

  link_.send(form_data);
});

on('#ajax', 'click', '#article_post', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  form_data = new FormData(document.forms.new_post);
  form_post = document.querySelector("#user_article_form");
  CKEDITOR.instances.id_content.updateElement();
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/article/add_user/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    response = new_post.querySelector(".card");
    document.querySelector(".stream").prepend(response)
    document.querySelector(".post_empty") ? lenta_load.querySelector(".post_empty").style.display = "none" : null;
  }};

  link_.send(form_data);
});

on('#ajax', 'click', '.u_itemComment', function() {
  form = this.parentElement.parentElement.parentElement;
  send_comment(form, form.parentElement.previousElementSibling, '/posts/user/post-comment/');
});

on('#ajax', 'click', '.u_replyItemComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  block = form.parentElement.parentElement.querySelector(".stream_reply_comments");
  send_comment(form, block.parentElement, '/posts/user/reply-comment/')
  form.parentElement.style.display = "none";
  block.classList.add("replies_open");
});

on('#ajax', 'click', '.u_replyParentItemComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  block = form.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  send_comment(form, block, '/posts/user/reply-comment/')
  form.parentElement.style.display = "none";
  block.classList.add("replies_open");
});

/*!
   item post scripts for user
  */
on('#ajax', 'click', '.u_post_remove', function() {
  item = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("data-uuid");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/posts/user/delete/" + uuid + "/", true );

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    item.style.display = "none";
    document.querySelector(".item_fullscreen").style.display = "none";
    p = document.createElement("div");
    p.classList.add("card", "mb-3");
    p.style.padding = "20px";
    p.style.display =  "block";

    p.innerHTML = "Запись удалена. <span class='u_post_abort_remove' style='cursor:pointer' data-uuid='" + uuid + "'>Восстановить</span>";
    item.parentElement.insertBefore(p, item);
    item.style.display = "none";
  }};

  link.send( );
});


on('#ajax', 'click', '.u_post_abort_remove', function() {
  item = this.parentElement.nextElementSibling;
  item.style.display = "block";
  uuid = this.getAttribute("data-uuid");
  block = this.parentElement;
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/posts/user/abort_delete/" + uuid + "/", true );

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    block.remove();
  }};

  link.send();
});

on('#ajax', 'click', '.u_post_fixed', function() {
  send_change(this, "/posts/user/fixed/", "u_post_unfixed", "Открепить")
})
on('#ajax', 'click', '.u_post_unfixed', function() {
  send_change(this, "/posts/user/unfixed/", "u_post_fixed", "Закрепить")
})

on('#ajax', 'click', '.u_post_off_comment', function() {
  send_change(this, "/posts/user/off_comment/", "u_post_on_comment", "Вкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".u_item_comments").style.display = "none"
})
on('#ajax', 'click', '.u_post_on_comment', function() {
  send_change(this, "/posts/user/on_comment/", "u_post_off_comment", "Выкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".u_item_comments").style.display = "unset"
})

on('#ajax', 'click', '.u_post_off_votes', function() {
  send_change(this, "/posts/user/off_votes/", "u_post_on_votes", "Вкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "none";
  post.querySelector(".dislike").style.display = "none";
})
on('#ajax', 'click', '.u_post_on_votes', function() {
  send_change(this, "/posts/user/on_votes/", "u_post_off_votes", "Выкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "unset";
  post.querySelector(".dislike").style.display = "unset";
})

on('#ajax', 'click', '.u_like', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("data-uuid");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_like(item, "/posts/votes/user_like/" + uuid + "/" + pk + "/");
  vote_reload("/posts/item_window/u_like_window/" + uuid + "/", "/posts/item_window/u_dislike_window/" + uuid + "/", this.nextElementSibling, this.nextElementSibling.nextElementSibling.nextElementSibling)
});
on('#ajax', 'click', '.u_dislike', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("data-uuid");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_dislike(item, "/posts/votes/user_dislike/" + uuid + "/" + pk + "/");
  vote_reload("/posts/item_window/u_like_window/" + uuid + "/", "/posts/item_window/u_dislike_window/" + uuid + "/", this.previousElementSibling, this.nextElementSibling)
});
on('#ajax', 'click', '.u_like2', function() {
  _this = this;
  item = _this.parentElement;
  comment_pk = item.getAttribute("data-pk");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_like(item, "/posts/votes/user_comment/" + comment_pk + "/" + pk + "/like/");
  vote_reload("/posts/item_window/u_comment_like_window/" + comment_pk + "/", "/posts/item_window/u_comment_dislike_window/" + comment_pk + "/", _this.nextElementSibling, _this.nextElementSibling.nextElementSibling.nextElementSibling)
});
on('#ajax', 'click', '.u_dislike2', function() {
  _this = this;
  item = _this.parentElement;
  comment_pk = item.getAttribute("data-pk");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_dislike(item, "/posts/votes/user_comment/" + comment_pk + "/" + pk + "/dislike/");
  vote_reload("/posts/item_window/u_comment_like_window/" + comment_pk + "/", "/posts/item_window/u_comment_dislike_window/" + comment_pk + "/", _this.previousElementSibling, _this.nextElementSibling)
});


on('#ajax', 'change', '#photo_add_post_attach', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  form_data = new FormData(document.body.querySelector("#add_photos"));
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/user/add_comment_photo/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    photo_list = response.querySelectorAll(".u_photo_detail");

    block = document.body.querySelector(".attach_block");
    block_divs = block.querySelectorAll("div");
    block_divs_length = photo_list.length;

    photo_post_upload_attach(photo_list, block, block_divs_length);
    }
    document.querySelector(".create_fullscreen").style.display = "none";
    document.getElementById("create_loader").innerHTML="";
  }
  link_.send(form_data);
});

on('#ajax', 'click', '.photo_load_several', function() {
  _this = this.previousElementSibling.querySelector("img");
  if (document.body.querySelector(".current_file_dropdown")){
    photo_comment_attach(_this, document.body.querySelector(".current_file_dropdown").parentElement.parentElement)
  } else if (document.body.querySelector(".attach_block")){
    photo_post_attach(_this, document.body.querySelector(".attach_block"))
  }
  this.classList.add("active_svg");
});
on('#ajax', 'click', '.photo_load_one', function() {
  _this = this;
  if (document.body.querySelector(".current_file_dropdown")){
    photo_comment_attach(_this, document.body.querySelector(".current_file_dropdown").parentElement.parentElement)
  } else if (document.body.querySelector(".attach_block")){
    photo_post_attach(_this, document.body.querySelector(".attach_block"))
  }
  document.querySelector(".create_fullscreen").style.display = "none";
  document.getElementById("create_loader").innerHTML="";
});

on('#ajax', 'click', '.create_video_attach_btn', function() {
  form_data = new FormData(document.querySelector("#create_video_form"));
  user_pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/video/progs/create_video_attach/" + user_pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem_ = document.createElement('div');
    elem_.innerHTML = link_.responseText;

      dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
      video_comment_attach(elem_.querySelector("img"), dropdown);

      document.querySelector(".create_fullscreen").style.display = "none";
      document.getElementById("create_loader").innerHTML="";
  }};

  link_.send(form_data);
});

on('#ajax', 'click', '.video_load_one', function() {
  _this = this;
  if (document.body.querySelector(".current_file_dropdown")){
    video_comment_attach(_this, document.body.querySelector(".current_file_dropdown").parentElement.parentElement)
  } else if (document.body.querySelector(".attach_block")){
    video_post_attach(_this, document.body.querySelector(".attach_block"))
  }
  document.querySelector(".create_fullscreen").style.display = "none";
  document.getElementById("create_loader").innerHTML="";
});
on('#ajax', 'click', '.video_load_several', function() {
  _this = this.previousElementSibling.querySelector("img");
  if (document.body.querySelector(".current_file_dropdown")){
    video_comment_attach(_this, document.body.querySelector(".current_file_dropdown").parentElement.parentElement)
  } else if (document.body.querySelector(".attach_block")){
    video_post_attach(_this, document.body.querySelector(".attach_block"))
  }
  this.classList.add("active_svg");
});

on('#ajax', 'click', '.music_load_one', function() {
  _this = this;
  if (document.body.querySelector(".current_file_dropdown")){
    music_comment_attach(_this, document.body.querySelector(".current_file_dropdown").parentElement.parentElement)
  } else if (document.body.querySelector(".attach_block")){
    music_post_attach(_this, document.body.querySelector(".attach_block"))
  }
  document.querySelector(".create_fullscreen").style.display = "none";
  document.getElementById("create_loader").innerHTML="";
});
on('#ajax', 'click', '.music_load_several', function() {
  _this = this.previousElementSibling;
  if (document.body.querySelector(".current_file_dropdown")){
    music_comment_attach(_this, document.body.querySelector(".current_file_dropdown").parentElement.parentElement)
  } else if (document.body.querySelector(".attach_block")){
    music_post_attach(_this, document.body.querySelector(".attach_block"))
  }
  this.classList.add("active_svg");
});

on('#ajax', 'click', '.good_load_one', function() {
  _this = this;
  if (document.body.querySelector(".current_file_dropdown")){
    good_comment_attach(_this, document.body.querySelector(".current_file_dropdown").parentElement.parentElement)
  } else if (document.body.querySelector(".attach_block")){
    good_post_attach(_this, document.body.querySelector(".attach_block"))
  }
  document.querySelector(".create_fullscreen").style.display = "none";
  document.getElementById("create_loader").innerHTML="";
});
on('#ajax', 'click', '.good_load_several', function() {
  _this = this.previousElementSibling;
  if (document.body.querySelector(".current_file_dropdown")){
    good_comment_attach(_this, document.body.querySelector(".current_file_dropdown").parentElement.parentElement)
  } else if (document.body.querySelector(".attach_block")){
    good_post_attach(_this, document.body.querySelector(".attach_block"))
  }
  this.classList.add("active_svg");
});

on('#ajax', 'click', '.article_load_one', function() {
  _this = this;
  if (document.body.querySelector(".current_file_dropdown")){
    article_comment_attach(_this, document.body.querySelector(".current_file_dropdown").parentElement.parentElement)
  } else if (document.body.querySelector(".attach_block")){
    article_post_attach(_this, document.body.querySelector(".attach_block"))
  }
  document.querySelector(".create_fullscreen").style.display = "none";
  document.getElementById("create_loader").innerHTML="";
});
on('#ajax', 'click', '.article_load_several', function() {
  _this = this.previousElementSibling;
  if (document.body.querySelector(".current_file_dropdown")){
    article_comment_attach(_this, document.body.querySelector(".current_file_dropdown").parentElement.parentElement)
  } else if (document.body.querySelector(".attach_block")){
    article_post_attach(_this, document.body.querySelector(".attach_block"))
  }
  this.classList.add("active_svg");
});
