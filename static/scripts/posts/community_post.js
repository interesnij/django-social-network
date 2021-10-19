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
  pk = this.getAttribute('data-pk');
  create_fullscreen("/article/c_article_window/" + pk + "/", "item_fullscreen");
});

on('#ajax', 'click', '#c_add_post_btn', function() {
  form_post = this.parentElement.parentElement.parentElement.parentElement;
  text_val = form_post.querySelector(".smile_supported");
  _val = format_text(text_val);
  _text = _val.innerHTML;
  if (_text.replace(/<(?!img)\/?[a-z][^>]*(>|$)/gi, "").trim() == "" && form_post.querySelector(".files_0")) {
    toast_error("Напишите или прикрепите что-нибудь"); return
  };

  $input = document.createElement("input");
  $input.setAttribute("name", "text");
  $input.setAttribute("type", "hidden");
  $input.classList.add("input_text");
  $input.value = _text;
  form_post.append($input);
  form_data = new FormData(form_post);

  lenta_load = form_post.parentElement.nextElementSibling.nextElementSibling;
  pk = form_post.parentElement.parentElement.getAttribute("data-uuid");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/posts/community_progs/add_post/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    clear_attach_block();

    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    drops = form_post.querySelectorAll(".dropdown-menu");
    form_post.querySelector(".input_text").remove();
    form_post.querySelector(".smile_supported").innerHTML = "";
    for (var i = 0; i < drops.length; i++){drops[i].classList.remove("show")}
    lenta_load.insertAdjacentHTML('afterBegin', new_post.innerHTML);
    toast_info('Запись опубликована');
    lenta_load.querySelector(".items_empty") ? lenta_load.querySelector(".items_empty").style.display = "none" : null;
  } else {
        new_post = document.createElement("span");
        new_post.innerHTML = link_.responseText;
        if (new_post.querySelector(".exception_value")){
          text = new_post.querySelector(".exception_value").innerHTML;
          toast_info(text)
        }
    }
  };

  link_.send(form_data);
});

on('#ajax', 'click', '#c_edit_post_btn', function() {
  form_post = this.parentElement.parentElement.parentElement.parentElement;
  text_val = form_post.querySelector(".smile_supported");
  _text = text_val.innerHTML;
  format_text(text_val);
  if (_text.replace(/<(?!br)(?!img)\/?[a-z][^>]*(>|$)/gi, "").trim() == "" && !form_post.querySelector(".files_0")) {
    toast_error("Напишите или прикрепите что-нибудь")
  };

  $input = document.createElement("input");
  $input.setAttribute("name", "text");
  $input.setAttribute("type", "hidden");
  $input.classList.add("input_text");
  $input.value = form_post.querySelector(".smile_supported").innerHTML;
  form_post.append($input);
  form_data = new FormData(form_post);
  block = form_post.parentElement.parentElement;

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/posts/community_progs/edit_post/" + block.getAttribute("data-uuid") + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    clear_attach_block();
    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    form_post.parentElement.remove();
    block.querySelector(".fullscreen") ? block.querySelector(".fullscreen").remove() : null;
    block.querySelector(".attach_container") ? block.querySelector(".attach_container").remove() : null;
    block.querySelector(".card-footer").remove()
    if (new_post.querySelector(".fullscreen")) {
      block.append(new_post.querySelector(".fullscreen"))
    }
    if (new_post.querySelector(".attach_container")) {
      block.append(new_post.querySelector(".attach_container"))
    };
    block.append(new_post.querySelector(".card-footer"))

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
    drops = form_post.querySelectorAll(".dropdown-menu");
    for (var i = 0; i < drops.length; i++){drops[i].classList.remove("show")}
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

on('#ajax', 'click', '.c_add_post_in_list', function() {
  add_item_in_list(this, '/posts/community_progs/add_post_in_list/', "c_add_post_in_list", "c_remove_post_from_list")
})
on('#ajax', 'click', '.c_remove_post_from_list', function() {
  remove_item_from_list(this, '/posts/community_progs/remove_post_from_list/', "c_remove_post_from_list", "c_add_post_in_list")
})

on('#ajax', 'click', '#c_add_post_list_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  pk = form.getAttribute("data-pk");
  if (!form.querySelector("#id_name").value){form.querySelector("#id_name").style.border = "1px #FF0000 solid";toast_error("Название - обязательное поле!"); return
  } else { this.disabled = true }
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/posts/community_progs/add_list/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    date_list = document.body.querySelector(".date-list");
    list = date_list.querySelectorAll(".list");
    for (var i = 0; i < list.length; i++) {list[i].classList.remove("tab_active");list[i].classList.add("pointer", "c_post_list_change");};
    date_list.querySelector(".is_main_post_list").classList.remove("tab_active");
    date_list.querySelector(".is_main_post_list").classList.add("pointer", "u_posts_change");

    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    post_stream = document.body.querySelector(".list_pk");
    post_stream.innerHTML = '';
    post_stream.innerHTML = '<div class="card mb-3 items_empty centered"><div class="card-body"><svg fill="currentColor" class="thumb_big svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path fill="currentColor" d="M22 13h-8v-2h8v2zm0-6h-8v2h8V7zm-8 10h8v-2h-8v2zm-2-8v6c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V9c0-1.1.9-2 2-2h6c1.1 0 2 .9 2 2zm-1.5 6l-2.25-3-1.75 2.26-1.25-1.51L3.5 15h7z"/></svg></div><h6 style="margin: 20px;">Пока записей нет...</h6></div>';
    name = form.querySelector("#id_name").value;
    li = document.createElement("li");
    li.classList.add("date", "list", "tab_active");
    li.setAttribute("list-pk", new_post.querySelector(".list_pk").getAttribute("list-pk"));

    div = document.createElement("div");div.classList.add("media");_div = document.createElement("div");_div.classList.add("media-body");h6 = document.createElement("h6");h6.classList.add("mb-0");h6.innerHTML = name;_div.append(h6); div.append(_div);document.body.querySelector(".date-list").prepend(div);
    close_fullscreen();
  }};

  link_.send(form_data);
});

on('#ajax', 'click', '#c_edit_post_list_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
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
        close_fullscreen();
        toast_success("Список изменен")
      }
    }
    ajax_link.send(form_data);
});

on('#ajax', 'click', '.c_delete_post_list', function() {
  _this = this;
  list_pk = _this.parentElement.parentElement.getAttribute("data-uuid");
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
        _this.classList.add("c_restore_post_list", "mb-5");
        toast_success("Список удален");
      }
    }
    ajax_link.send();
});
on('#ajax', 'click', '.c_restore_post_list', function() {
  _this = this;
  list_pk = _this.parentElement.parentElement.getAttribute("data-uuid");
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk')
  block = _this.parentElement.nextElementSibling;

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', "/posts/community_progs/restore_list/" + pk + "/" + list_pk + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        block.style.display = "block";
        _this.innerHTML = "удалить список";
        _this.classList.remove("c_restore_post_list", "mb-5");
        _this.classList.add("c_delete_post_list");
        toast_success("Список восстановлен");
      }
    }
    ajax_link.send();
});

on('#ajax', 'click', '.c_post_comment_edit', function() {
  get_edit_comment_form(this, "/posts/community_progs/edit_comment/")
});

on('#ajax', 'click', '.c_post_edit_comment_btn', function() {
  post_edit_comment_form(this, "/posts/community_progs/edit_comment/")
});

on('#ajax', 'click', '.c_post_comment_delete', function() {
  comment_delete(this, "/posts/community_progs/delete_comment/", "c_post_comment_restore")
})
on('#ajax', 'click', '.c_post_comment_restore', function() {
  comment_restore(this, "/posts/community_progs/restore_comment/")
});
on('#ajax', 'click', '.c_post_owner_comment_delete', function() {
  comment_owner_delete(this, "/posts/community_progs/delete_owner_comment/", "c_post_owner_comment_restore")
})
on('#ajax', 'click', '.c_post_owner_comment_restore', function() {
  comment_owner_restore(this, "/posts/community_progs/restore_owner_comment/")
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
  post.querySelector(".load_post_comments") ? post.querySelector(".load_post_comments").style.display = "unset"
  : post.querySelector(".c_news_item_comments").style.display = "none"
});
on('#ajax', 'click', '.c_post_on_comment', function() {
  send_change(this, "/posts/community_progs/on_comment/", "c_post_off_comment", "Выкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".load_post_comments") ? post.querySelector(".load_post_comments").style.display = "unset"
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
    p.innerHTML = "<span class='c_post_restore pointer' data-uuid='" + uuid + "'>Запись удалена. <span class='underline'>Восстановить</span></span>";
    !document.querySelector(".post_detail") ? (item.parentElement.insertBefore(p, item), item.style.display = "none")
    : (document.querySelector(".item_fullscreen").style.display = "none",
    block = document.body.querySelector(".post_stream"),
    item = block.querySelector( '[data-uuid=' + '"' + uuid + '"' + ']' ),
    item.parentElement.insertBefore(p, item),
    item.style.display = "none",
    p.style.display =  "block")
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
    p.innerHTML = "Запись удалена. <span class='c_post_wall_restore pointer' data-uuid='" + uuid + "'>Восстановить</span>";
    !document.querySelector(".post_detail") ? (item.parentElement.insertBefore(p, item), item.style.display = "none")
    : (document.querySelector(".item_fullscreen").style.display = "none",
    block = document.body.querySelector(".post_stream"),
    item = block.querySelector( '[data-uuid=' + '"' + uuid + '"' + ']' ),
    item.parentElement.insertBefore(p, item),
    item.style.display = "none",
    p.style.display =  "block")
  }};

  link.send( );
});


on('#ajax', 'click', '.c_post_restore', function() {
  item = this.parentElement.nextElementSibling;
  uuid = this.getAttribute("data-uuid");
  block = this.parentElement;
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/posts/community_progs/restore/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    block.remove();
    item.style.display = "block";
  }};

  link.send();
});

on('#ajax', 'click', '.c_post_wall_restore', function() {
  item = this.parentElement.nextElementSibling;
  uuid = this.getAttribute("data-uuid");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  block = this.parentElement;
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/posts/community_progs/wall_restore/" + pk + "/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    block.remove();
    item.style.display = "block";
  }};

  link.send();
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
    close_fullscreen();
  }
  link_.send(form_data);
});
