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
  link_.open( 'POST', "/posts/user_progs/add_post/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

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
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

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
  send_comment(form, block, '/posts/user/reply-comment/')
  form.parentElement.style.display = "none";
  block.classList.add("replies_open");
});

on('#ajax', 'click', '.u_replyParentItemComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  block = form.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  send_comment(form, block.parentElement, '/posts/user/reply-comment/')
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
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    p = document.createElement("div");
    p.classList.add("card", "mb-3");
    p.style.padding = "20px";
    p.style.display =  "block";
    p.innerHTML = "Запись удалена. <span class='u_post_abort_remove pointer' data-uuid='" + uuid + "'>Восстановить</span>";
    !document.querySelector(".post_detail") ? (item.parentElement.insertBefore(p, item), item.style.display = "none")
    : (document.querySelector(".item_fullscreen").style.display = "none",
    block = document.body.querySelector(".post_container"),
    item = block.querySelector( '[data-uuid=' + '"' + uuid + '"' + ']' ),
    item.parentElement.insertBefore(p, item),
    item.style.display = "none")
  }};

  link.send( );
});
on('#ajax', 'click', '.u_post_wall_remove', function() {
  item = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("data-uuid");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/posts/user/wall_delete/" + pk + "/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    p = document.createElement("div");
    p.classList.add("card", "mb-3");
    p.style.padding = "20px";
    p.style.display =  "block";
    p.innerHTML = "Запись удалена. <span class='u_post_wall_abort_remove pointer' data-uuid='" + uuid + "'>Восстановить</span>";
    !document.querySelector(".post_detail") ? (item.parentElement.insertBefore(p, item), item.style.display = "none")
    : (document.querySelector(".item_fullscreen").style.display = "none",
    block = document.body.querySelector(".post_container"),
    item = block.querySelector( '[data-uuid=' + '"' + uuid + '"' + ']' ),
    item.parentElement.insertBefore(p, item),
    item.style.display = "none")
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
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    block.remove();
  }};
  link.send();
});
on('#ajax', 'click', '.u_post_wall_abort_remove', function() {
  item = this.parentElement.nextElementSibling;
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  item.style.display = "block";
  uuid = this.getAttribute("data-uuid");
  block = this.parentElement;
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/posts/user/wall_abort_delete/" + pk + "/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

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
  post.querySelector(".u_item_comments") ? post.querySelector(".u_item_comments").style.display = "none"
  : post.querySelector(".u_news_item_comments").style.display = "none"
})
on('#ajax', 'click', '.u_post_on_comment', function() {
  send_change(this, "/posts/user/on_comment/", "u_post_off_comment", "Выкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".u_item_comments") ? post.querySelector(".u_item_comments").style.display = "unset"
  : post.querySelector(".u_news_item_comments").style.display = "unset"
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

function like_block_create(_class, user_pk){
  userpic = document.body.querySelector(".userpic");
  userpic.querySelector("img") ? user_img = userpic.querySelector("img") : user_img = '<svg fill="currentColor" class="svg_default svg_default_50" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
  user_name = userpic.getAttribute("data-name");
  div = document.createElement("div");
  span1 = document.createElement("span");
  span1.classList.add(_class, "pointer");
  span1.innerHTML = "Одобрил 1 человек";
  span2 = document.createElement("span");
  span2.style.display = "flex";
  span2.innerHTML = '<a style="padding-right:10px" data-pk="' + user_pk + '"><figure style="margin: 0;" title="' + user_name + '">' + user_img + '</figure></a>';
  div.append(span1); div.append(span2);
  return div
}
function user_vote_thumb_create(user_pk){
  userpic = document.body.querySelector(".userpic");
  userpic.querySelector("img") ? user_img = userpic.querySelector("img").getAttribute("data-src") : user_img = '<svg fill="currentColor" class="svg_default svg_default_50" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
  user_name = userpic.getAttribute("data-name");
  a = document.createElement("a");
  a.style.paddingRight = "10px";
  a.setAttribute("data-pk", user_pk);
  $img = document.createElement("img");
  $img.setAttribute("data-src", user_img);
  a.innerHTML = '<figure style="margin: 0;" title="' + user_name + '">' + $img + '</figure>';
  return a
}
function like_reload(like_block, dislike_block, _class){
  user_pk = document.body.querySelector(".userpic").getAttribute("data-pk");
  if (!like_block.querySelector('figure')){
    console.log("создаем блок лайков");
    div = document.createElement("div");
    div.style.margin = "15px";
    div.innerHTML = like_block_create(_class, user_pk);
    like_block.append(div)
  }
  else if (like_block.querySelector( '[data-pk=' + '"' + user_pk + '"' + ']' )){
      if (!like_block.querySelector('figure')){
        like_block.innerHTML = ""
        console.log("удаляем блок лайков");
      } else {
        like_block.querySelector( '[data-pk=' + '"' + user_pk + '"' + ']' ).remove()
        value = like_block.querySelector('[data-count=like]').innerHTML;
        value = value*1;
        value -= 1;
        like_block.querySelector('[data-count=like]').innerHTML = value;
        console.log("удаляем пользователя из лайков");
      }
  }
  else {
      all_likes = like_block.querySelector('.pointer');
      a = document.createElement("a");
      a.innerHTML = user_vote_thumb_create(user_pk);
      all_likes.nextElementSibling.prepend(a);
      value = all_likes.querySelector('[data-count=like]').innerHTML;
      value = value*1;
      value += 1;
      all_likes.querySelector('[data-count=like]').innerHTML = value;
      console.log("создаем пользователя в лайках")
  }
  if (dislike_block.querySelector( '[data-pk=' + '"' + user_pk + '"' + ']' )){
    dislike_block.querySelector( '[data-pk=' + '"' + user_pk + '"' + ']' ).remove();
    value = dislike_block.querySelector('[data-count=dislike]').innerHTML;
    value = value*1;
    value -= 1;
    console.log("удаляем пользователя из дизлайков")
    if (!dislike_block.querySelector('figure')){
      dislike_block.innerHTML = ""
    }
  }
}

on('#ajax', 'click', '.u_like', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("data-uuid");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_like(item, "/posts/votes/user_like/" + uuid + "/" + pk + "/");
  like_reload(this.nextElementSibling, this.nextElementSibling.nextElementSibling.nextElementSibling, "u_all_posts_likes");
});
on('#ajax', 'click', '.u_dislike', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("data-uuid");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_dislike(item, "/posts/votes/user_dislike/" + uuid + "/" + pk + "/");
  dislike_reload(this.previousElementSibling, this.nextElementSibling);
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

on('#ajax', 'click', '.u_post_comment_delete', function() {
  comment_delete(this, "/posts/user/delete_comment/", "u_post_comment_abort_remove")
})

on('#ajax', 'click', '.u_post_comment_abort_remove', function() {
  comment_abort_delete(this, "/posts/user/abort_delete_comment/")
});

on('#ajax', 'click', '.u_post_wall_comment_delete', function() {
  comment_wall_delete(this, "/posts/user/delete_wall_comment/", "u_post_comment_abort_remove")
})

on('#ajax', 'click', '.u_post_wall_comment_abort_remove', function() {
  comment_wall_abort_delete(this, "/posts/user/abort_delete_wall_comment/")
});

on('#ajax', 'change', '#u_photo_post_attach', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  form_data = new FormData(document.body.querySelector("#add_photos"));
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/user/add_comment_photo/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

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
on('#ajax', 'change', '#u_photo_post_comment_attach', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  form_data = new FormData(document.body.querySelector("#add_comment_photos"));
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/user/add_comment_photo/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    photo_comment_attach(response.querySelectorAll(".u_photo_detail"), dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement, photo_list.length);
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
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

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
