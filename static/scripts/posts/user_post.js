on('#ajax', 'click', '#u_ucm_post_repost_btn', function() {
  repost_constructor(this,
                     "/posts/repost/u_u_post_repost/",
                     "Репост записи на стену сделан",
                     "/posts/repost/u_c_post_repost/",
                     "Репост записи в сообщества сделан",
                     "/posts/repost/u_m_post_repost/",
                     "Репост записи в сообщения сделан")
});

on('body', 'click', '.photo_attach_list_remove', function() {
  block = this.parentElement.parentElement;
  if (block.parentElement.classList.contains("attach_block")){
    remove_file_attach(), is_full_attach()
  } else if (block.classList.contains("comment_attach_block")){
    remove_file_dropdown(); is_full_dropdown()
  } else if (block.classList.contains("message_attach_block")){
    remove_file_message_attach(); is_full_message_attach()
  }
  block.remove();
});

on('#ajax', 'click', '#u_add_article', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  create_fullscreen("/article/u_article_window/" + pk + "/", "item_fullscreen");
});

on('#ajax', 'click', '#u_add_post_btn', function() {
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
  link_.open( 'POST', "/posts/user_progs/add_post/" + pk + "/", true );
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
    main_container = document.body.querySelector(".main-container");
    add_list_in_all_stat("created_user_post",new_post.querySelector(".pag").getAttribute("data-pk"),main_container.getAttribute("data-type"),main_container.getAttribute("data-pk"))
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

on('#ajax', 'click', '#u_edit_post_btn', function() {
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
  $input.value = form_post.querySelector(".smile_supported").innerHTML;
  form_post.append($input);
  form_data = new FormData(form_post);
  block = form_post.parentElement.parentElement;
  pk = block.getAttribute("data-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/posts/user_progs/edit_post/" + pk + "/", true );
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
    block.append(new_post.querySelector(".card-footer"));
    main_container = document.body.querySelector(".main-container");
    add_list_in_all_stat("edited_user_post",pk,main_container.getAttribute("data-type"),main_container.getAttribute("data-pk"));

  }};

  link_.send(form_data);
});

on('#ajax', 'click', '.u_add_post_in_list', function() {
  add_item_in_list(this, '/posts/user_progs/copy_post_in_list/', "u_add_post_in_list", "u_remove_post_from_list")
});
on('#ajax', 'click', '.u_remove_post_from_list', function() {
  remove_item_from_list(this, '/posts/user_progs/uncopy_post_from_list/', "u_remove_post_from_list", "u_add_post_in_list")
});

on('#ajax', 'click', '#u_add_post_list_btn', function() {
  form = this.parentElement.parentElement.parentElement
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){form.querySelector("#id_name").style.border = "1px #FF0000 solid";toast_error("Название - обязательное поле!"); return
  } else { this.disabled = true }
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/posts/user_progs/add_list/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    date_list = document.body.querySelector(".date-list");
    list = date_list.querySelectorAll(".list");
    for (var i = 0; i < list.length; i++) {list[i].classList.remove("active");list[i].classList.add("pointer", "post_list_change");};

    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    post_stream = document.body.querySelector(".span_list_pk");
    post_stream.innerHTML = '';
    post_stream.innerHTML = '<div class="card mb-3 items_empty centered"><div class="card-body"><svg fill="currentColor" class="thumb_big svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path fill="currentColor" d="M22 13h-8v-2h8v2zm0-6h-8v2h8V7zm-8 10h8v-2h-8v2zm-2-8v6c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V9c0-1.1.9-2 2-2h6c1.1 0 2 .9 2 2zm-1.5 6l-2.25-3-1.75 2.26-1.25-1.51L3.5 15h7z"/></svg></div><h6 style="margin: 20px;">Пока записей нет...</h6></div>';
    name = form.querySelector("#id_name").value;
    li = document.createElement("li");
    li.classList.add("date", "list", "active");
    new_pk = new_post.querySelector(".span_list_pk").getAttribute("list-pk");
    li.setAttribute("list-pk", new_pk);

    div = document.createElement("div");
    div.classList.add("media");
    _div = document.createElement("div");
    _div.classList.add("media-body");
    h6 = document.createElement("h6");
    h6.classList.add("mb-0");
    h6.innerHTML = name;
    _div.append(h6);
    div.append(_div);
    document.body.querySelector(".date-list").prepend(div);
    close_work_fullscreen();
    main_container = document.body.querySelector(".main-container");
    add_list_in_all_stat("created_user_post_list",new_pk,main_container.getAttribute("data-type"),main_container.getAttribute("data-pk"))
  }};

  link_.send(form_data);
});

on('#ajax', 'click', '#u_edit_post_list_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }
  pk = form.getAttribute("data-pk");

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'POST', "/posts/user_progs/edit_list/" + pk + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        name = form.querySelector('#id_name').value;
        title = document.body.querySelector( '[list-pk=' + '"' + pk + '"' + ']' );
        title.querySelector(".list_name").innerHTML = name;
        close_work_fullscreen();
        toast_success("Список изменен");
        main_container = document.body.querySelector(".main-container");
        add_list_in_all_stat("edited_user_post_list",pk,main_container.getAttribute("data-type"),main_container.getAttribute("data-pk"));
      }
    }
    ajax_link.send(form_data);
});

on('#ajax', 'click', '.u_delete_post_list', function() {
  _this = this;
  list_pk = _this.parentElement.parentElement.getAttribute("data-uuid");
  block = _this.parentElement.nextElementSibling;

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', "/posts/user_progs/delete_list/" + list_pk + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        block.style.display = "none";
        _this.innerHTML = "Отменить удаление";
        _this.classList.remove("u_delete_post_list");
        _this.classList.add("u_restore_post_list", "mb-5");
        toast_success("Список удален");
        main_container = document.body.querySelector(".main-container");
        add_list_in_all_stat("deleted_user_post_list",list_pk,main_container.getAttribute("data-type"),main_container.getAttribute("data-pk"));
      }
    }
    ajax_link.send();
});
on('#ajax', 'click', '.u_restore_post_list', function() {
  _this = this;
  list_pk = _this.parentElement.parentElement.getAttribute("data-uuid");
  block = _this.parentElement.nextElementSibling;

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', "/posts/user_progs/restore_list/" + list_pk + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        block.style.display = "block";
        _this.innerHTML = "удалить список";
        _this.classList.remove("u_restore_post_list", "mb-5");
        _this.classList.add("u_delete_post_list");
        toast_success("Список восстановлен");
        main_container = document.body.querySelector(".main-container");
        add_list_in_all_stat("restored_user_post_list",list_pk,main_container.getAttribute("data-type"),main_container.getAttribute("data-pk"));
      }
    }
    ajax_link.send();
});

on('#ajax', 'click', '.u_post_comment_edit', function() {
  get_edit_comment_form(this, "/posts/user_progs/edit_comment/")
});

on('#ajax', 'click', '.u_post_edit_comment_btn', function() {
  post_edit_comment_form(this, "/posts/user_progs/edit_comment/")
});

/*!
   item post scripts for user
  */
on('#ajax', 'click', '.u_post_remove', function() {
  item = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = item.getAttribute("data-pk");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/posts/user_progs/delete/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    p = document.createElement("div");
    p.classList.add("card", "mb-3");
    p.style.padding = "20px";
    p.innerHTML = "<span class='u_post_restore pointer' data-pk='" + pk + "'>Запись удалена. <span class='underline'>Восстановить</span></span>";
    !document.querySelector(".post_detail") ? (item.parentElement.insertBefore(p, item), item.style.display = "none")
    : (document.querySelector(".item_fullscreen").style.display = "none",
    block = document.body.querySelector(".post_stream"),
    item = block.querySelector( '[data-pk=' + '"' + pk + '"' + ']' ),
    item.style.display = "none",
    p.style.display =  "block",
    item.parentElement.insertBefore(p, item));
    main_container = document.body.querySelector(".main-container");
    add_list_in_all_stat("deleted_user_post",pk,main_container.getAttribute("data-type"),main_container.getAttribute("data-pk"));
  }};

  link.send( );
});

on('#ajax', 'click', '.u_post_restore', function() {
  item = this.parentElement.nextElementSibling;
  pk = this.getAttribute("data-pk");
  block = this.parentElement;
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/posts/user_progs/restore/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    block.remove();
    item.style.display = "block";
    main_container = document.body.querySelector(".main-container");
    add_list_in_all_stat("restored_user_post",pk,main_container.getAttribute("data-type"),main_container.getAttribute("data-pk"));
  }};
  link.send();
});

on('#ajax', 'click', '.u_post_fixed', function() {
  item = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = item.getAttribute("data-pk");
  send_change(this, "/posts/user_progs/fixed/", "u_post_unfixed", "Открепить");
  main_container = document.body.querySelector(".main-container");
  add_list_in_all_stat("fixed_user_post",pk,main_container.getAttribute("data-type"),main_container.getAttribute("data-pk"));
});
on('#ajax', 'click', '.u_post_unfixed', function() {
  item = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = item.getAttribute("data-pk");
  send_change(this, "/posts/user_progs/unfixed/", "u_post_fixed", "Закрепить");
  main_container = document.body.querySelector(".main-container");
  add_list_in_all_stat("unfixed_user_post",pk,main_container.getAttribute("data-type"),main_container.getAttribute("data-pk"));
});

on('#ajax', 'click', '.u_post_off_comment', function() {
  send_change(this, "/posts/user_progs/off_comment/", "u_post_on_comment", "Вкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".load_post_comments") ? post.querySelector(".load_post_comments").style.display = "none"
  : post.querySelector(".u_news_item_comments").style.display = "none";
  main_container = document.body.querySelector(".main-container");
  add_list_in_all_stat("off_comment_user_post",post.getAttribute("data-pk"),main_container.getAttribute("data-type"),main_container.getAttribute("data-pk"));
})
on('#ajax', 'click', '.u_post_on_comment', function() {
  send_change(this, "/posts/user_progs/on_comment/", "u_post_off_comment", "Выкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".load_post_comments") ? post.querySelector(".load_post_comments").style.display = "unset"
  : post.querySelector(".u_news_item_comments").style.display = "unset";
  main_container = document.body.querySelector(".main-container");
  add_list_in_all_stat("on_comment_user_post",post.getAttribute("data-pk"),main_container.getAttribute("data-type"),main_container.getAttribute("data-pk"));
});

on('#ajax', 'click', '.u_post_off_votes', function() {
  send_change(this, "/posts/user_progs/off_votes/", "u_post_on_votes", "Вкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "none";
  post.querySelector(".dislike").style.display = "none";
  main_container = document.body.querySelector(".main-container");
  add_list_in_all_stat("off_votes_user_post",post.getAttribute("data-pk"),main_container.getAttribute("data-type"),main_container.getAttribute("data-pk"));
});
on('#ajax', 'click', '.u_post_on_votes', function() {
  send_change(this, "/posts/user_progs/on_votes/", "u_post_off_votes", "Выкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "unset";
  post.querySelector(".dislike").style.display = "unset";
  main_container = document.body.querySelector(".main-container");
  add_list_in_all_stat("on_votes_user_post",post.getAttribute("data-pk"),main_container.getAttribute("data-type"),main_container.getAttribute("data-pk"));
});

on('#ajax', 'click', '.u_like', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  item_pk = item.getAttribute("data-pk");
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = item.getAttribute('data-pk');
  send_like(item, "/posts/votes/user_like/" + item_pk + "/" + pk + "/");
  like_reload(this.nextElementSibling, this.nextElementSibling.nextElementSibling.nextElementSibling, "u_all_posts_likes");
  main_container = document.body.querySelector(".main-container");
  add_list_in_all_stat("like_user_post",item_pk,main_container.getAttribute("data-type"),main_container.getAttribute("data-pk"));
});
on('#ajax', 'click', '.u_dislike', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  item_pk = item.getAttribute("data-pk");
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = item.getAttribute('data-pk');
  send_dislike(item, "/posts/votes/user_dislike/" + item_pk + "/" + pk + "/");
  dislike_reload(this.previousElementSibling, this.nextElementSibling, "u_all_posts_dislikes");
  main_container = document.body.querySelector(".main-container");
  add_list_in_all_stat("dislike_user_post",item_pk,main_container.getAttribute("data-type"),main_container.getAttribute("data-pk"));
});

on('#ajax', 'click', '.u_like2', function() {
  _this = this;
  item = _this.parentElement;
  comment_pk = item.getAttribute("data-pk");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_like(item, "/posts/votes/user_comment/" + comment_pk + "/" + pk + "/like/");
  like_reload(this.nextElementSibling, this.nextElementSibling.nextElementSibling.nextElementSibling, "u_all_posts_comment_likes")
  main_container = document.body.querySelector(".main-container");
  add_list_in_all_stat("like_user_post_comment",comment_pk,main_container.getAttribute("data-type"),main_container.getAttribute("data-pk"));
});
on('#ajax', 'click', '.u_dislike2', function() {
  _this = this;
  item = _this.parentElement;
  comment_pk = item.getAttribute("data-pk");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_dislike(item, "/posts/votes/user_comment/" + comment_pk + "/" + pk + "/dislike/");
  dislike_reload(this.previousElementSibling, this.nextElementSibling, "u_all_posts_comment_dislikes");
  main_container = document.body.querySelector(".main-container");
  add_list_in_all_stat("dislike_user_post_comment",comment_pk,main_container.getAttribute("data-type"),main_container.getAttribute("data-pk"));
});

on('#ajax', 'click', '.u_post_comment_delete', function() {
  comment_delete(this, "/posts/user_progs/delete_comment/", "u_post_comment_restore")
});

on('#ajax', 'click', '.u_post_comment_restore', function() {
  comment_restore(this, "/posts/user_progs/restore_comment/")
});

on('#ajax', 'change', '#u_photo_post_attach', function() {
  form = this.parentElement;
  form_data = new FormData(form);
  input = form.querySelector(".upload_for_post_attach")
  if (input.files.length > 10) {
      toast_error("Не больше 10 фотографий");
      return;
  }
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/user_progs/add_attach_photo/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    photo_list = response.querySelectorAll(".pag");
    if (document.body.querySelector(".attach_block")){
      block = document.body.querySelector(".attach_block");
      photo_post_upload_attach(photo_list, block);
    } else if (document.body.querySelector(".message_attach_block")){
      block = document.body.querySelector(".message_attach_block");
      photo_message_upload_attach(photo_list, block);
    }
    }
    close_work_fullscreen();
  }
  link_.send(form_data);
});

on('#ajax', 'change', '#u_photo_post_comment_attach', function() {
  form = document.body.querySelector("#add_comment_photos");
  form_data = new FormData(form);
  input = form.querySelector("#u_photo_post_comment_attach")
  if (input.files.length > 2) {
      toast_error("Не больше 2 фотографий");
      return;
  }
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/user_progs/add_attach_photo/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    photo_list = response.querySelectorAll(".pag");
    photo_comment_upload_attach(photo_list, document.body.querySelector(".current_file_dropdown").parentElement.parentElement, photo_list.length);
    }
    close_work_fullscreen();
  }
  link_.send(form_data);
});

on('#ajax', 'click', '.photo_load_several', function() {
  previous = this.previousElementSibling
  _this = previous.querySelector("img");
  photo_pk = previous.getAttribute('photo-pk');
  user_pk = previous.getAttribute('data-pk');
  src = _this.parentElement.getAttribute("data-href");
  if (document.body.querySelector(".current_file_dropdown")){
    check_photo_in_block(document.body.querySelector(".current_file_dropdown").parentElement.parentElement.parentElement.parentElement.previousElementSibling, _this, photo_pk) ? null : (photo_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, photo_pk, user_pk, src), this.classList.add("active_svg"))
  } else if (document.body.querySelector(".attach_block")){
    check_photo_in_block(document.body.querySelector(".attach_block"), _this, photo_pk) ? null : (photo_post_attach(document.body.querySelector(".attach_block"), photo_pk, user_pk, src), this.classList.add("active_svg"))
  } else if (document.body.querySelector(".message_attach_block")){
    check_photo_in_block(document.body.querySelector(".message_attach_block"), _this, photo_pk) ? null : (photo_message_attach(document.body.querySelector(".message_attach_block"), photo_pk, user_pk, src), this.classList.add("active_svg"), show_message_form_send_btn())
  }
});

on('#ajax', 'click', '.photo_load_one', function() {
  _this = this;
  photo_pk = _this.parentElement.getAttribute('photo-pk');
  user_pk = _this.parentElement.getAttribute('data-pk');
  src = _this.parentElement.getAttribute("data-href");
  if (document.body.querySelector(".current_file_dropdown")){
    check_photo_in_block(document.body.querySelector(".current_file_dropdown").parentElement.parentElement.parentElement.parentElement.previousElementSibling, _this, photo_pk) ? null : (photo_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, photo_pk, user_pk, src), close_work_fullscreen())
  } else if (document.body.querySelector(".attach_block")){
    check_photo_in_block(document.body.querySelector(".attach_block"), _this, photo_pk) ? null : (photo_post_attach(document.body.querySelector(".attach_block"), photo_pk, user_pk, src), close_work_fullscreen())
  } else if (document.body.querySelector(".message_attach_block")){
    check_photo_in_block(document.body.querySelector(".message_attach_block"), _this, photo_pk) ? null : (close_work_fullscreen(), photo_message_attach(document.body.querySelector(".message_attach_block"), photo_pk, user_pk, src))
  }
});

on('#ajax', 'click', '.u_create_video_attach_btn', function() {
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

    close_work_fullscreen();
  }};

  link_.send(form_data);
});

on('#ajax', 'click', '.video_load_one', function() {
  _this = this;
  pk = _this.getAttribute('video-pk');
  counter = _this.getAttribute('video-counter');
  src = _this.getAttribute('src');
  if (document.body.querySelector(".current_file_dropdown")){
    check_video_in_block(document.body.querySelector(".current_file_dropdown").parentElement.parentElement.parentElement.parentElement.previousElementSibling, _this, pk) ? null : (video_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, pk, counter, src), close_work_fullscreen())
  } else if (document.body.querySelector(".attach_block")){
    check_video_in_block(document.body.querySelector(".attach_block"), _this, pk) ? null : (video_post_attach(document.body.querySelector(".attach_block"), pk, counter, src), close_work_fullscreen())
  } else if (document.body.querySelector(".message_attach_block")){
    check_video_in_block(document.body.querySelector(".message_attach_block"), _this, pk) ? null : (video_message_attach(document.body.querySelector(".message_attach_block"), pk, counter, src), close_work_fullscreen(), show_message_form_send_btn())
  }
});
on('#ajax', 'click', '.video_load_several', function() {
  previous = this.previousElementSibling
  _this = previous.querySelector("img");
  pk = _this.getAttribute('video-pk');
  counter = _this.getAttribute('video-counter');
  src = _this.getAttribute('src');
  if (document.body.querySelector(".current_file_dropdown")){
    check_video_in_block(document.body.querySelector(".current_file_dropdown").parentElement.parentElement.parentElement.parentElement.previousElementSibling, _this, pk) ? null : (video_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, pk, counter, src), this.classList.add("active_svg"))
  } else if (document.body.querySelector(".attach_block")){
    check_video_in_block(document.body.querySelector(".attach_block"), _this, pk) ? null : (video_post_attach(document.body.querySelector(".attach_block"), pk, counter, src), this.classList.add("active_svg"))
  } else if (document.body.querySelector(".message_attach_block")){
    check_video_in_block(document.body.querySelector(".message_attach_block"), _this, pk) ? null : (video_message_attach(document.body.querySelector(".message_attach_block"), pk, counter, src), this.classList.add("active_svg"), show_message_form_send_btn())
  }
});
on('body', 'click', '.video_attach_list', function() {
  _this = this;
  name = _this.parentElement.querySelector(".list_name").innerHTML;
  pk = _this.getAttribute('data-pk');
  count = _this.parentElement.querySelector(".count").innerHTML;
  if (document.body.querySelector(".current_file_dropdown")){
    check_video_list_in_block(document.body.querySelector(".current_file_dropdown").parentElement.parentElement.parentElement.parentElement.previousElementSibling, _this, pk) ? null : (video_list_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, name, pk, count), close_work_fullscreen())
  } else if (document.body.querySelector(".attach_block")){
    check_video_list_in_block(document.body.querySelector(".attach_block"), _this, pk) ? null : (video_list_post_attach(document.body.querySelector(".attach_block"), name, pk, count), close_work_fullscreen())
  } else if (document.body.querySelector(".message_attach_block")){
    check_video_list_in_block(document.body.querySelector(".message_attach_block"), _this, pk) ? null : (video_list_message_attach(document.body.querySelector(".message_attach_block"), name, pk, count), close_work_fullscreen())
  }
});

on('#ajax', 'click', '.music_load_one', function() {
  _this = this;
  pk = _this.getAttribute('music-pk');
  counter = _this.getAttribute('music-counter');
  _this.querySelector("img") ? src = _this.querySelector("img").getAttribute('src') : src = '/static/images/no_track_img.jpg'
  if (document.body.querySelector(".current_file_dropdown")){
    check_music_in_block(document.body.querySelector(".current_file_dropdown").parentElement.parentElement.parentElement.parentElement.previousElementSibling, _this, counter) ? null : (music_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, pk, counter, src), close_work_fullscreen())
  } else if (document.body.querySelector(".attach_block")){
    check_music_in_block(document.body.querySelector(".attach_block"), _this, counter) ? null : (music_post_attach(document.body.querySelector(".attach_block"), pk, counter, src), close_work_fullscreen())
  } else if (document.body.querySelector(".message_attach_block")){
    check_music_in_block(document.body.querySelector(".message_attach_block"), _this, counter) ? null : (music_message_attach(document.body.querySelector(".message_attach_block"), pk, counter, src), close_work_fullscreen(), show_message_form_send_btn())
  }
  close_work_fullscreen();
});
on('#ajax', 'click', '.music_load_several', function() {
  _this = this.previousElementSibling
  pk = _this.getAttribute('music-pk');
  counter = _this.getAttribute('music-counter');
  _this.querySelector("img") ? src = _this.querySelector("img").getAttribute('src') : src = '/static/images/no_track_img.jpg'
  if (document.body.querySelector(".current_file_dropdown")){
    check_music_in_block(document.body.querySelector(".current_file_dropdown").parentElement.parentElement.parentElement.parentElement.previousElementSibling, _this, counter) ? null : (music_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, pk, counter, src), this.classList.add("active_svg"))
  } else if (document.body.querySelector(".attach_block")){
    check_music_in_block(document.body.querySelector(".attach_block"), _this, counter) ? null : (music_post_attach(document.body.querySelector(".attach_block"), pk, counter, src), this.classList.add("active_svg"))
  } else if (document.body.querySelector(".message_attach_block")){
    check_music_in_block(document.body.querySelector(".message_attach_block"), _this, counter) ? null : (music_message_attach(document.body.querySelector(".message_attach_block"), pk, counter, src), this.classList.add("active_svg"), show_message_form_send_btn())
  }
});
on('body', 'click', '.music_attach_list', function() {
  _this = this;
  name = _this.parentElement.querySelector(".list_name").innerHTML;
  pk = _this.getAttribute('data-pk');
  count = _this.parentElement.querySelector(".count").innerHTML;
  if (document.body.querySelector(".current_file_dropdown")){
    check_playlist_in_block(document.body.querySelector(".current_file_dropdown").parentElement.parentElement.parentElement.parentElement.previousElementSibling, _this, pk) ? null : (playlist_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, name, pk, count), close_work_fullscreen())
  } else if (document.body.querySelector(".attach_block")){
    check_playlist_in_block(document.body.querySelector(".attach_block"), _this, pk) ? null : (playlist_post_attach(document.body.querySelector(".attach_block"), name, pk, count), close_work_fullscreen())
  } else if (document.body.querySelector(".message_attach_block")){
    check_playlist_in_block(document.body.querySelector(".message_attach_block"), _this, pk) ? null : (playlist_message_attach(document.body.querySelector(".message_attach_block"), name, pk, count), close_work_fullscreen())
  }
});

on('#ajax', 'click', '.doc_load_several', function() {
  _this = this.previousElementSibling;
  pk = _this.getAttribute('data-pk');
  media_block = _this.querySelector(".media-body")
  if (document.body.querySelector(".current_file_dropdown")){
    check_doc_in_block(document.body.querySelector(".current_file_dropdown").parentElement.parentElement.parentElement.parentElement.previousElementSibling, _this, pk) ? null : (doc_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, media_block, pk), this.classList.add("active_svg"))
  } else if (document.body.querySelector(".attach_block")){
    check_doc_in_block(document.body.querySelector(".attach_block"), _this, pk) ? null : (doc_post_attach(document.body.querySelector(".attach_block"), media_block, pk), this.classList.add("active_svg"))
  } else if (document.body.querySelector(".message_attach_block")){
    check_doc_in_block(document.body.querySelector(".message_attach_block"), _this, pk) ? null : (doc_message_attach(document.body.querySelector(".message_attach_block"), media_block, pk), this.classList.add("active_svg"), show_message_form_send_btn())
  }
});
on('body', 'click', '.doc_attach_list', function() {
  _this = this;
  name = _this.parentElement.querySelector(".list_name").innerHTML;
  pk = _this.getAttribute('data-pk');
  count = _this.parentElement.querySelector(".count").innerHTML;
  if (document.body.querySelector(".current_file_dropdown")){
    check_doc_list_in_block(document.body.querySelector(".current_file_dropdown").parentElement.parentElement.parentElement.parentElement.previousElementSibling, _this, pk) ? null : (doc_list_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, name, pk, count), close_work_fullscreen())
  } else if (document.body.querySelector(".attach_block")){
    check_doc_list_in_block(document.body.querySelector(".attach_block"), _this, pk) ? null : (doc_list_post_attach(document.body.querySelector(".attach_block"), name, pk, count), close_work_fullscreen())
  } else if (document.body.querySelector(".message_attach_block")){
    check_doc_list_in_block(document.body.querySelector(".message_attach_block"), _this, pk) ? null : (doc_list_message_attach(document.body.querySelector(".message_attach_block"), name, pk, count), close_work_fullscreen())
  }
});

on('#ajax', 'click', '.survey_attach_remove', function() {
  block = this.parentElement.parentElement;
  block.parentElement.nextElementSibling.querySelector(".attach_panel").style.display = "block";
  block.remove();
  remove_file_attach();
});

on('#ajax', 'click', '.good_load_one', function() {
  _this = this;
  data_pk = _this.getAttribute('good-pk');
  data_uuid = _this.getAttribute('good-uuid');
  src = _this.querySelector("img").getAttribute('src');
  title = _this.querySelector(".good_title").innerHTML;

  if (document.body.querySelector(".current_file_dropdown")){
    check_good_in_block(document.body.querySelector(".current_file_dropdown").parentElement.parentElement.parentElement.parentElement.previousElementSibling, _this, data_pk) ? null : (good_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, src, data_pk, data_uuid, title), close_work_fullscreen())
  } else if (document.body.querySelector(".attach_block")){
    check_good_in_block(document.body.querySelector(".attach_block"), _this, data_pk) ? null : (good_post_attach(document.body.querySelector(".attach_block"), src, data_pk, data_uuid, title), close_work_fullscreen())
  } else if (document.body.querySelector(".message_attach_block")){
    check_good_in_block(document.body.querySelector(".message_attach_block"), _this, data_pk) ? null : (good_message_attach(document.body.querySelector(".message_attach_block"), src, data_pk, data_uuid, title), close_work_fullscreen(), show_message_form_send_btn())
  }
});
on('#ajax', 'click', '.good_load_several', function() {
  _this = this.previousElementSibling;
  data_pk = _this.getAttribute('good-pk');
  data_uuid = _this.getAttribute('good-uuid');
  src = _this.querySelector("img").getAttribute('src');
  title = _this.querySelector(".good_title").innerHTML;

  if (document.body.querySelector(".current_file_dropdown")){
    check_good_in_block(document.body.querySelector(".current_file_dropdown").parentElement.parentElement.parentElement.parentElement.previousElementSibling, _this, data_pk) ? null : (good_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, src, data_pk, data_uuid, title), this.classList.add("active_svg"))
  } else if (document.body.querySelector(".attach_block")){
    check_good_in_block(document.body.querySelector(".attach_block"), _this, data_pk) ? null : (good_post_attach(document.body.querySelector(".attach_block"), src, data_pk, data_uuid, title), this.classList.add("active_svg"))
  } else if (document.body.querySelector(".message_attach_block")){
    check_good_in_block(document.body.querySelector(".message_attach_block"), _this, data_pk) ? null : (good_message_attach(document.body.querySelector(".message_attach_block"), src, data_pk, data_uuid, title), this.classList.add("active_svg"), show_message_form_send_btn())
  }
});
on('body', 'click', '.good_attach_list', function() {
  _this = this;
  name = _this.parentElement.querySelector(".list_name").innerHTML;
  pk = _this.getAttribute('data-pk');
  count = _this.parentElement.querySelector(".count").innerHTML;
  if (document.body.querySelector(".current_file_dropdown")){
    check_good_list_in_block(document.body.querySelector(".current_file_dropdown").parentElement.parentElement.parentElement.parentElement.previousElementSibling, _this, pk) ? null : (good_list_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, name, pk, count), close_work_fullscreen())
  } else if (document.body.querySelector(".attach_block")){
    check_good_list_in_block(document.body.querySelector(".attach_block"), _this, pk) ? null : (good_list_post_attach(document.body.querySelector(".attach_block"), name, pk, count), close_work_fullscreen())
  } else if (document.body.querySelector(".message_attach_block")){
    check_good_list_in_block(document.body.querySelector(".message_attach_block"), _this, pk) ? null : (good_list_message_attach(document.body.querySelector(".message_attach_block"), name, pk, count), close_work_fullscreen())
  }
});

on('#ajax', 'click', '.commmunty_load_one', function() {
  _this = this;
  block = _this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  commmunity_form_selected(_this, block.querySelector("#selected_message_target_items"))
});
on('#ajax', 'click', '.chat_item_load_one', function() {
  _this = this;
  block = _this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  chat_item_form_selected(_this, block.querySelector("#selected_message_target_items"))
});
on('#ajax', 'click', '.chat_friends_load_one', function() {
  _this = this;
  block = this.parentElement.parentElement.nextElementSibling;
  chat_item_form_selected(_this, block)
});
