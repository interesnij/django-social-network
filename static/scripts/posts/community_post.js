on('#ajax', 'click', '#c_ucm_post_repost_btn', function() {
  repost_constructor(this,
                     "/posts/repost/c_u_post_repost/",
                     "Репост записи на стену сделан",
                     "/posts/repost/c_c_post_repost/",
                     "Репост записи в сообщества сделан",
                     "/posts/repost/c_m_post_repost/",
                     "Репост записи в сообщения сделан")
});

on('#ajax', 'click', '#community_article_add', function() {
  var pk = this.getAttribute('data-pk');
  open_fullscreen("/article/c_article_window/" + pk + "/", document.getElementById("create_loader"))
});

on('#ajax', 'click', '#c_add_post_btn', function() {
  form_data = new FormData(document.forms.new_community_post);
  form_post = document.querySelector("#c_add_post_form");
  lenta_load = form_post.parentElement.parentElement.querySelector(".list_pk");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/posts/community_progs/add_post/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    form_post.querySelector('.id_text').value = "";
    clear_attach_block();
    list = form_post.parentElement.parentElement.querySelector(".tab_active");
    list_name = list.innerHTML;
    list_pk = list.getAttribute("list-pk");
    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    (new_post.querySelector('.span1').classList.contains(list_pk) && new_post.querySelector(".card")) ? (lenta_load.querySelector(".list_pk").prepend(new_post),
                                       toast_info('Запись опубликована'),
                                       lenta_load.querySelector(".post_empty") ? lenta_load.querySelector(".post_empty").style.display = "none" : null)
                                     : toast_info('Запись опубликована');
  }};

  link_.send(form_data);
});

on('#ajax', 'click', '#c_add_offer_post', function() {
  form_post = document.body.querySelector("#admin_offer_post");
  form_data = new FormData(form_post);

  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/posts/community_progs/add_offer_post/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    form_post.querySelector('.id_text').value = "";
    clear_attach_block();

    elem = link_.responseText;
    document.body.querySelector(".user_draft_list") ? (toast_info("Запись предложена"),
                                                       value = document.body.querySelector(".user_draft_count").innerHTML,
                                                       value = value*1,
                                                       value += 1,
                                                       document.body.querySelector(".user_draft_count").innerHTML = value)
    : (document.body.querySelector(".draft_post_container").innerHTML = '<div class="card mt-3 user_draft_list"><div class="card-header"><a href="/communities/user_draft/' + pk + '/" class="ajax"><div class="media"><div class="media-body"><h4 class="content-color-primary mb-0">Предложенные записи</h4></div><span class="user_draft_count">1</span></div></a></div></div>',
    toast_info("Запись предложена"))
  }};
  link_.send(form_data);
});

on('#ajax', 'click', '#c_add_post_list_btn', function() {
  form = document.body.querySelector("#post_list_form");
  form_data = new FormData(form);
  pk = form.getAttribute("data-pk");
  if (!form.querySelector("#id_name").value){form.querySelector("#id_name").style.border = "1px #FF0000 solid";toast_error("Название - обязательное поле!"); return
  } else if (!form.querySelector("#id_order").value){form.querySelector("#id_order").style.border = "1px #FF0000 solid";toast_error("Выберите порядковый номер!"); return
  } else { this.disabled = true }
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/posts/community_progs/add_list/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    date_list = document.body.querySelector(".date-list");
    list = date_list.querySelectorAll(".list");
    for (var i = 0; i < list.length; i++) {list[i].classList.remove("tab_active");list[i].classList.add("pointer", "c_post_list_change");};

    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    post_stream = document.body.querySelector(".post_stream");
    post_stream.innerHTML = '';
    post_stream.innerHTML = '<div class="card mb-3 post_empty centered"><div class="card-body"><svg fill="currentColor" class="thumb_big svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path fill="currentColor" d="M22 13h-8v-2h8v2zm0-6h-8v2h8V7zm-8 10h8v-2h-8v2zm-2-8v6c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V9c0-1.1.9-2 2-2h6c1.1 0 2 .9 2 2zm-1.5 6l-2.25-3-1.75 2.26-1.25-1.51L3.5 15h7z"/></svg></div><h6 style="margin: 20px;">Пока записей нет...</h6></div>';
    name = form.querySelector("#id_name").value;
    li = document.createElement("li");
    li.classList.add("date", "list", "tab_active");
    li.setAttribute("list-pk", new_post.querySelector(".list_pk").getAttribute("list-pk"));

    div = document.createElement("div");div.classList.add("media");_div = document.createElement("div");_div.classList.add("media-body");h6 = document.createElement("h6");h6.classList.add("mb-0");h6.innerHTML = name;_div.append(h6); div.append(_div);document.body.querySelector(".date-list").prepend(div);
    close_create_window()
  }};

  link_.send(form_data);
});

on('#ajax', 'click', '#c_edit_post_list_btn', function() {
  form = document.body.querySelector("#post_list_form");
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else if (!form.querySelector("#id_order").value){
    form.querySelector("#id_order").style.border = "1px #FF0000 solid";
    toast_error("Выберите порядковый номер!");
  } else { this.disabled = true }
  pk = form.getAttribute("data-pk");
  list_pk = form.getAttribute("list-pk");

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'POST', "/posts/community_progs/edit_list/" + pk + "/" + list_pk + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        name = form.querySelector('#id_name').value;
        title = document.body.querySelector( '[list-pk=' + '"' + list_pk + '"' + ']' );
        title.querySelector(".list_name").innerHTML = name;
        close_create_window();
        toast_success("Список изменен")
      }
    }
    ajax_link.send(form_data);
});

on('#ajax', 'click', '.c_delete_post_list', function() {
  _this = this;
  list_pk = _this.parentElement.parentElement.getAttribute("list-pk");
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk')
  block = _this.parentElement.nextElementSibling;

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', "/posts/community_progs/delete_list/" + pk + "/" + list_pk + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        block.style.display = "none";
        _this.innerHTML = "Отменить удаление";
        _this.classList.remove("c_delete_post_list");
        _this.classList.add("c_abort_delete_post_list", "mb-5");
        toast_success("Список удален");
      }
    }
    ajax_link.send();
});
on('#ajax', 'click', '.c_abort_delete_post_list', function() {
  _this = this;
  list_pk = _this.parentElement.parentElement.getAttribute("list-pk");
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk')
  block = _this.parentElement.nextElementSibling;

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', "/posts/community_progs/abort_delete_list/" + pk + "/" + list_pk + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        block.style.display = "block";
        _this.innerHTML = "удалить список";
        _this.classList.remove("c_abort_delete_post_list", "mb-5");
        _this.classList.add("c_delete_post_list");
        toast_success("Список восстановлен");
      }
    }
    ajax_link.send();
});

on('#ajax', 'click', '.c_itemComment', function() {
  form = this.parentElement.parentElement.parentElement;
  send_comment(form, form.parentElement.previousElementSibling, '/posts/community_progs/post-comment/');
});

on('#ajax', 'click', '.c_replyItemComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  block = form.parentElement.parentElement.querySelector(".stream_reply_comments");
  send_comment(form, block, '/posts/community_progs/reply-comment/')
  form.parentElement.style.display = "none";
  block.classList.add("replies_open")
});

on('#ajax', 'click', '.c_replyParentItemComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  block = form.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  send_comment(form, block.parentElement, '/posts/community_progs/reply-comment/')
  form.parentElement.style.display = "none";
  block.classList.add("replies_open")
});

on('#ajax', 'click', '.c_post_comment_delete', function() {
  comment_delete(this, "/posts/community_progs/delete_comment/", "c_post_comment_abort_remove")
})
on('#ajax', 'click', '.c_post_comment_abort_remove', function() {
  comment_abort_delete(this, "/posts/community_progs/abort_delete_comment/")
});
on('#ajax', 'click', '.c_post_wall_comment_delete', function() {
  comment_wall_delete(this, "/posts/community_progs/delete_wall_comment/", "c_post_comment_abort_remove")
})

on('#ajax', 'click', '.c_post_wall_comment_abort_remove', function() {
  comment_wall_abort_delete(this, "/posts/community_progs/abort_delete_wall_comment/")
});

on('#ajax', 'click', '.c_like', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("data-uuid");
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = item.getAttribute('data-pk');
  send_like(item, "/posts/votes/community_like/" + uuid + "/" + pk + "/");
  like_reload(this.nextElementSibling, this.nextElementSibling.nextElementSibling.nextElementSibling, "c_all_posts_likes");
});
on('#ajax', 'click', '.c_dislike', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("data-uuid");
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = item.getAttribute('data-pk');
  send_dislike(item, "/posts/votes/community_dislike/" + uuid + "/" + pk + "/");
  dislike_reload(this.previousElementSibling, this.nextElementSibling, "c_all_posts_dislikes");
});
on('#ajax', 'click', '.c_like2', function() {
  _this = this;
  item = _this.parentElement;
  comment_pk = item.getAttribute("data-pk");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_like(item, "/posts/votes/community_comment/" + comment_pk + "/" + pk + "/like/");
  like_reload(this.nextElementSibling, this.nextElementSibling.nextElementSibling.nextElementSibling, "c_all_posts_comment_likes")
});
on('#ajax', 'click', '.c_dislike2', function() {
  _this = this;
  item = _this.parentElement;
  comment_pk = item.getAttribute("data-pk");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_dislike(item, "/posts/votes/community_comment/" + comment_pk + "/" + pk + "/dislike/");
  dislike_reload(this.previousElementSibling, this.nextElementSibling, "c_all_posts_comment_dislikes")
});

on('body', 'click', '#community_avatar_btn', function(event) {
  this.previousElementSibling.click();
})
on('#ajax', 'change', '#community_avatar_upload', function() {
  parent = this.parentElement;
  post_with_pk_and_reload(parent, "/gallery/community_progs/add_avatar/")
})

on('#ajax', 'click', '.c_post_fixed', function() {
  send_change(this, "/posts/community_progs/fixed/", "c_post_unfixed", "Открепить")
})
on('#ajax', 'click', '.c_post_unfixed', function() {
  send_change(this, "/posts/community_progs/unfixed/", "c_post_fixed", "Закрепить")
})

on('#ajax', 'click', '.c_post_off_comment', function() {
  send_change(this, "/posts/community_progs/off_comment/", "c_post_on_comment", "Вкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".c_item_comments") ? post.querySelector(".c_item_comments").style.display = "unset"
  : post.querySelector(".c_news_item_comments").style.display = "none"
})
on('#ajax', 'click', '.c_post_on_comment', function() {
  send_change(this, "/posts/community_progs/on_comment/", "c_post_off_comment", "Выкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".c_item_comments") ? post.querySelector(".c_item_comments").style.display = "unset"
  : post.querySelector(".c_news_item_comments").style.display = "unset"
})

on('#ajax', 'click', '.c_post_off_votes', function() {
  send_change(this, "/posts/community_progs/off_votes/", "c_post_on_votes", "Вкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "none";
  post.querySelector(".dislike").style.display = "none";
})
on('#ajax', 'click', '.c_post_on_votes', function() {
  send_change(this, "/posts/community_progs/on_votes/", "c_post_off_votes", "Выкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "unset";
  post.querySelector(".dislike").style.display = "unset";
})

on('#ajax', 'click', '.c_post_remove', function() {
  item = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("data-uuid");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/posts/community_progs/delete/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    p = document.createElement("div");
    p.classList.add("card", "mb-3");
    p.style.padding = "20px";
    p.style.display =  "block";
    p.innerHTML = "Запись удалена. <span class='c_post_abort_remove pointer' data-uuid='" + uuid + "'>Восстановить</span>";
    !document.querySelector(".post_detail") ? (item.parentElement.insertBefore(p, item), item.style.display = "none")
    : (document.querySelector(".item_fullscreen").style.display = "none",
    block = document.body.querySelector(".post_container"),
    item = block.querySelector( '[data-uuid=' + '"' + uuid + '"' + ']' ),
    item.parentElement.insertBefore(p, item),
    item.style.display = "none")
  }};

  link.send( );
});

on('#ajax', 'click', '.c_post_wall_remove', function() {
  item = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("data-uuid");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/posts/community_progs/wall_delete/" + pk + "/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    p = document.createElement("div");
    p.classList.add("card", "mb-3");
    p.style.padding = "20px";
    p.style.display =  "block";
    p.innerHTML = "Запись удалена. <span class='c_post_wall_abort_remove pointer' data-uuid='" + uuid + "'>Восстановить</span>";
    !document.querySelector(".post_detail") ? (item.parentElement.insertBefore(p, item), item.style.display = "none")
    : (document.querySelector(".item_fullscreen").style.display = "none",
    block = document.body.querySelector(".post_container"),
    item = block.querySelector( '[data-uuid=' + '"' + uuid + '"' + ']' ),
    item.parentElement.insertBefore(p, item),
    item.style.display = "none")
  }};

  link.send( );
});


on('#ajax', 'click', '.c_post_abort_remove', function() {
  item = this.parentElement.nextElementSibling;
  item.style.display = "block";
  uuid = this.getAttribute("data-uuid");
  block = this.parentElement;
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/posts/community_progs/abort_delete/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    block.remove();
  }};

  link.send();
});

on('#ajax', 'click', '.c_post_wall_abort_remove', function() {
  item = this.parentElement.nextElementSibling;
  item.style.display = "block";
  uuid = this.getAttribute("data-uuid");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  block = this.parentElement;
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/posts/community_progs/wall_abort_delete/" + pk + "/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    block.remove();
  }};

  link.send();
});


on('body', 'click', '#c_multi_photos', function(event) {
  this.previousElementSibling.click();
})

on('#ajax', 'change', '#c_photo_post_attach', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  form_data = new FormData(document.body.querySelector("#add_photos"));
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/community_progs/add_attach_photo/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    photo_list = response.querySelectorAll(".c_photo_detail");

    photo_post_upload_attach(response.querySelectorAll(".c_photo_detail"), document.body.querySelector(".attach_block"), photo_list.length);
    }
    close_create_window();
  }
  link_.send(form_data);
});

on('#ajax', 'change', '#c_photo_post_comment_attach', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  form_data = new FormData(document.body.querySelector("#add_photos"));
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/community_progs/add_comment_photo/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    photo_comment_attach(response.querySelectorAll(".c_photo_detail"), dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement, photo_list.length);
    }
    close_create_window();
  }
  link_.send(form_data);
});
