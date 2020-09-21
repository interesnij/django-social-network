

on('#ajax', 'click', '.c_good_add_attach', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("create_loader");
  open_fullscreen('/goods/community_progs/add_attach/' + pk + '/', loader);
});

on('#ajax', 'click', '.c_goodComment', function() {
  form = this.parentElement.parentElement.parentElement;
  send_comment(form, form.parentElement.previousElementSibling, '/goods/community_progs/post-comment/');
});

on('#ajax', 'click', '.c_replyGoodComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  block = form.parentElement.parentElement.querySelector(".stream_reply_comments");
  send_comment(form, block, '/goods/community_progs/reply-comment/')
  form.parentElement.style.display = "none";
  block.classList.add("replies_open")
});

on('#ajax', 'click', '.c_replyParentGoodComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  block = form.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  send_comment(form, block.parentElement, '/goods/community_progs/reply-comment/')
  form.parentElement.style.display = "none";
  block.classList.add("replies_open")
});

on('#ajax', 'click', '.c_good_off_comment', function() {
  send_good_change(this, "/goods/community_progs/off_comment/", "c_good_on_comment", "Вкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".c_good_comments").style.display = "none"
})
on('#ajax', 'click', '.c_good_on_comment', function() {
  send_good_change(this, "/goods/community_progs/on_comment/", "c_good_off_comment", "Выкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".c_good_comments").style.display = "unset"
})

on('#ajax', 'click', '.c_good_comment_delete', function() {
  comment_delete(this, "/goods/community_progs/delete_comment/", "c_good_comment_abort_remove")
})
on('#ajax', 'click', '.c_good_comment_abort_remove', function() {
  comment_abort_delete(this, "/goods/community_progs/abort_delete_comment/")
});


on('#ajax', 'click', '.c_good_add', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("create_loader");
  open_fullscreen('/goods/community_progs/add/' + pk + '/', loader)
});

on('#ajax', 'click', '.u_good_off_private', function() {
  send_good_change(this, "/goods/community_progs/off_private/", "c_good_on_private", "Вкл. приватность")
})
on('#ajax', 'click', '.c_good_on_private', function() {
  send_good_change(this, "/goods/community_progs/on_private/", "c_good_off_private", "Выкл. приватность")
})

on('#ajax', 'click', '.c_good_off_votes', function() {
  send_good_change(this, "/goods/community_progs/off_votes/", "c_good_on_votes", "Вкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "none";
  post.querySelector(".dislike").style.display = "none";
})
on('#ajax', 'click', '.c_good_on_votes', function() {
  send_good_change(this, "/goods/community_progs/on_votes/", "c_good_off_votes", "Выкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "unset";
  post.querySelector(".dislike").style.display = "unset";
})
on('#ajax', 'click', '.c_good_hide', function() {
  send_good_change(this, "/goods/community_progs/hide/", "u_good_unhide", "Товар не виден");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
})
on('#ajax', 'click', '.c_good_unhide', function() {
  send_good_change(this, "/goods/community_progs/unhide/", "u_good_hide", "Товар виден");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
})

on('#ajax', 'click', '.community_good_remove', function() {
  send_good_change(this, "/goods/community_progs/delete/", "community_good_abort_remove", "Отмена");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  this.parentElement.parentElement.nextElementSibling.style.display = "none";
  post.querySelector(".order-2").style.display = "none";
  post.querySelector(".card").style.opacity = "0.5";
  this.style.color = "#FF0000";
})
on('#ajax', 'click', '.community_good_abort_remove', function() {
  send_good_change(this, "/goods/community_progs/abort_delete/", "community_good_remove", "Удалить");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  this.parentElement.parentElement.nextElementSibling.style.display = "unset";
  post.querySelector(".order-2").style.display = "unset";
  post.querySelector(".card").style.opacity = "1";
})

on('#ajax', 'click', '.c_good_like', function() {
  good = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = document.body.querySelector(".data_display").getAttribute("data-uuid");
  pk = document.body.querySelector(".data_display").getAttribute("data-pk");
  send_like(good, "/goods/votes/community_like/" + uuid + "/" + pk + "/");
  like_reload(this.nextElementSibling, this.nextElementSibling.nextElementSibling.nextElementSibling, "c_all_good_likes");
});
on('#ajax', 'click', '.c_good_dislike', function() {
  good = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = document.body.querySelector(".data_display").getAttribute("data-uuid");
  pk = document.body.querySelector(".data_display").getAttribute("data-pk");
  send_dislike(good, "/goods/votes/community_dislike/" + uuid + "/" + pk + "/");
  dislike_reload(this.previousElementSibling, this.nextElementSibling, "c_all_good_dislikes");
});
on('#ajax', 'click', '.c_good_like2', function() {
  _this = this;
  good = _this.parentElement;
  comment_pk = good.getAttribute("data-pk");
  good.getAttribute('data-pk') ? pk = good.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  send_like(good, "/goods/votes/community_comment/" + comment_pk + "/" + pk + "/like/");
  like_reload(this.nextElementSibling, this.nextElementSibling.nextElementSibling.nextElementSibling, "c_all_good_comment_likes")
}); 
on('#ajax', 'click', '.c_good_dislike2', function() {
  _this = this;
  good = _this.parentElement;
  comment_pk = good.getAttribute("data-pk");
  good.getAttribute('data-pk') ? pk = good.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  send_dislike(good, "/goods/votes/community_comment/" + comment_pk + "/" + pk + "/dislike/");
  dislike_reload(this.previousElementSibling, this.nextElementSibling, "c_all_good_comment_dislikes")
});

on('#ajax', 'click', '#c_add_good_btn', function() {
  form_post = document.body.querySelector("#c_add_good_form");
  form_data = new FormData(form_post);

  lists = form_post.querySelector("#id_album");
  selectedOptions = lists.selectedOptions;
  val = false;
  for (var i = 0; i < selectedOptions.length; i++) {
    if(selectedOptions[i].value) {val = true}
  }
  if (!document.body.querySelector("#id_title").value){
    document.body.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else if (!document.body.querySelector("#category").value){
    document.body.querySelector("#category").style.border = "1px #FF0000 solid";
    toast_error("Категория - обязательное поле!")
  } else if (!document.body.querySelector("#id_description").value){
    document.body.querySelector("#id_description").style.border = "1px #FF0000 solid";
    toast_error("Описание товара - обязательное поле!");
  } else if (!document.body.querySelector("#id_image").value){
    document.body.querySelector("#good_image").style.border = "1px #FF0000 solid !important";
    toast_error("Фотография на обложку обязательна!")
  } else if (!val){
    form_post.querySelector("#id_album").style.border = "1px #FF0000 solid";
    toast_error("Выберите альбом!");
    return
  } else {this.disabled = true}

  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/goods/community_progs/add/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    new_good = document.createElement("div");
    new_good.innerHTML = elem;
    if (document.querySelector(".current_file_dropdown")){
      dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
      is_full_dropdown();
      img_block = dropdown.parentElement.previousElementSibling;
      data_pk = new_good.querySelector(".new_image").getAttribute('good-pk');

      if (img_block.querySelector( '[good-pk=' + '"' + data_pk + '"]' )){
        new_good.setAttribute("tooltip", "Товар уже выбран");
        new_good.setAttribute("flow", "up");
        return
      };
      new_good.classList.add("attach_toggle");
      title = new_good.querySelector(".good_title").innerHTML;
      if (!img_block.querySelector(".select_good1")){
        div = create_preview_good("select_good1", new_good.querySelector(".img").getAttribute('data-src'), data_pk, title)
      } else if (!img_block.querySelector(".select_good2")){
        div = create_preview_good("select_good2", new_good.querySelector(".img").getAttribute('data-src'), data_pk, title)
      }
      img_block.append(div);
      img_block.querySelector(".good_input") ? null : ($good_input = document.createElement("span"), $good_input.innerHTML = '<input type="hidden" class="good_input" name="good" value="1">', img_block.append($good_input));

      add_file_dropdown()
      is_full_dropdown();

    } else if (document.querySelector(".attach_block")){
      block = document.body.querySelector(".attach_block");
      is_full_attach();
      data_pk = new_good.querySelector(".new_image").getAttribute('good-pk');
      title = new_good.querySelector(".good_title").innerHTML;

      if (block.querySelector( '[good-pk=' + '"' + data_pk + '"]' )){
        new_good.setAttribute("tooltip", "Товар уже выбран");
        new_good.setAttribute("flow", "up");
        return
      };
      new_good.classList.add("attach_toggle");
      if (!block.querySelector(".good_input")){div = create_preview_good("select_good1", new_good.querySelector(".img").getAttribute('data-src'), data_pk, title)}
      else if (!block.querySelector(".select_good2")){div = create_preview_good("select_good2", new_good.querySelector(".img").getAttribute('data-src'), data_pk, title)}
      else if (!block.querySelector(".select_good3")){div = create_preview_good("select_good3", new_good.querySelector(".img").getAttribute('data-src'), data_pk, title)}
      else if (!block.querySelector(".select_good4")){div = create_preview_good("select_good4", new_good.querySelector(".img").getAttribute('data-src'), data_pk, title)}
      else if (!block.querySelector(".select_good5")){div = create_preview_good("select_good5", new_good.querySelector(".img").getAttribute('data-src'), data_pk, title)}
      else if (!block.querySelector(".select_good6")){div = create_preview_good("select_good6", new_good.querySelector(".img").getAttribute('data-src'), data_pk, title)}
      else if (!block.querySelector(".select_good7")){div = create_preview_good("select_good7", new_good.querySelector(".img").getAttribute('data-src'), data_pk, title)}
      else if (!block.querySelector(".select_good8")){div = create_preview_good("select_good8", new_good.querySelector(".img").getAttribute('data-src'), data_pk, title)}
      else if (!block.querySelector(".select_good9")){div = create_preview_good("select_good9", new_good.querySelector(".img").getAttribute('data-src'), data_pk, title)}
      else if (!block.querySelector(".select_good10")){div = create_preview_good("select_good10", new_good.querySelector(".img").getAttribute('data-src'), data_pk, title)}
    block.append(div);
    block.querySelector(".good_input") ? null : ($good_input = document.createElement("span"), $good_input.innerHTML = '<input type="hidden" class="good_input" name="good" value="1">', block.append($good_input));

    add_file_attach()
    is_full_attach();
    }
    else {
      uuid = document.body.querySelector(".pk_saver").getAttribute("data-uuid");
      span1 = new_good.querySelector('.span1')
      if (span1.classList.contains(uuid)){
        container = document.body.querySelector("#community_goods_container");
        container.insertAdjacentHTML('afterBegin', new_good.innerHTML);
        container.querySelector(".goods_empty") ? container.querySelector(".goods_empty").style.display = "none" : null;
        toast_info("Товар создан!")
      } else{
        toast_info("Товар создан!")
      }
  }
  document.querySelector(".create_fullscreen").style.display = "none";
  document.getElementById("create_loader").innerHTML="";
  toast_info("Товар создан!")
  }};
  link_.send(form_data);
});

on('#ajax', 'click', '#с_ucm_good_repost_btn', function() {
  form_post = document.body.querySelector("#с_uсm_good_repost_form");
  form_data = new FormData(form_post);
  good_pk = container.getAttribute('good-pk');
  pk = this.getAttribute("data-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );

  if (form_post.querySelector('#repost_radio_wall').checked) {
    link_.open( 'POST', "/goods/repost/с_u_good_repost/" + pk + "/" + good_pk + "/", true );
    link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link_.send(form_data);
    toast_info("Репост товара на стену сделан")
  }

  else if(form_post.querySelector('#repost_radio_community').checked){
    staff_communities = form_post.querySelector("#id_staff_communities");
    selectedOptions = staff_communities.selectedOptions;
    val = false;
    for (var i = 0; i < selectedOptions.length; i++) {if(selectedOptions[i].value) {val = true}}
    if(val){
      link_.open( 'POST', "/goods/repost/с_c_good_repost/" + pk + "/" + uuid + "/", true );
      link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      link_.send(form_data);
      toast_info("Репост товара в сообщества сделан")
    }else{toast_error("Выберите сообщества для репоста")}
  }

  else if(form_post.querySelector('#repost_radio_message').checked){
    user_connections = form_post.querySelector("#id_user_connections");
    selectedOptions = user_connections.selectedOptions;
    val = false;
    for (var i = 0; i < selectedOptions.length; i++) {if(selectedOptions[i].value) {val = true}}
    if(val){
      link_.open( 'POST', "/goods/repost/с_m_good_repost/" + pk + "/" + good_pk + "/", true );
      link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      link_.send(form_data);
      toast_info("Репост товара в сообщения сделан")
    }else{toast_error("Выберите пользователя для репоста")}
  };

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    document.querySelector(".votes_fullscreen").style.display = "none";
    document.getElementById("votes_loader").innerHTML="";
  }}
});
on('#ajax', 'click', '#c_ucm_good_list_repost_btn', function() {
  form_post = document.body.querySelector("#c_uсm_good_list_repost_form");
  form_data = new FormData(form_post);
  uuid = this.getAttribute("data-uuid");
  pk = this.getAttribute("data-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );

  if (form_post.querySelector('#repost_radio_wall').checked) {
    link_.open( 'POST', "/goods/repost/c_u_good_list_repost/" + pk + "/" + uuid + "/", true );
    link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link_.send(form_data);
    toast_info("Репост списка товаров на стену сделан")
  }

  else if(form_post.querySelector('#repost_radio_community').checked){
    staff_communities = form_post.querySelector("#id_staff_communities");
    selectedOptions = staff_communities.selectedOptions;
    val = false;
    for (var i = 0; i < selectedOptions.length; i++) {if(selectedOptions[i].value) {val = true}}
    if(val){
      link_.open( 'POST', "/goods/repost/c_c_good_list_repost/" + pk + "/" + uuid + "/", true );
      link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      link_.send(form_data);
      toast_info("Репост списка товаров в сообщества сделан")
    }else{toast_error("Выберите сообщества для репоста")}
  }

  else if(form_post.querySelector('#repost_radio_message').checked){
    user_connections = form_post.querySelector("#id_user_connections");
    selectedOptions = user_connections.selectedOptions;
    val = false;
    for (var i = 0; i < selectedOptions.length; i++) {if(selectedOptions[i].value) {val = true}}
    if(val){
      link_.open( 'POST', "/goods/repost/c_m_good_list_repost/" + pk + "/" + uuid + "/", true );
      link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      link_.send(form_data);
      toast_info("Репост списка товаров в сообщения сделан")
    }else{toast_error("Выберите пользователя для репоста")}
  };

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    document.querySelector(".votes_fullscreen").style.display = "none";
    document.getElementById("votes_loader").innerHTML="";
  }}
});

on('#ajax', 'click', '#c_create_good_list_btn', function() {
  form = document.body.querySelector("#c_good_list_create");
  form_data = new FormData(form);
  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true; }
  post_and_load_object_page(form, "/goods/community_progs/create_list/", "/communities/", "/goods_list/")
});


on('#ajax', 'click', '#c_edit_good_list_btn', function() {
  form = document.body.querySelector("#c_edit_good_list_form");
  form_data = new FormData(form);
  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }

  pk = form.getAttribute("data-pk");
  uuid = form.getAttribute("data-uuid");

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'POST', "/goods/community_progs/edit_album/" + pk + "/" + uuid + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        name = form.querySelector('#id_title').value;
        document.body.querySelector(".list_name").innerHTML = name;
        document.querySelector(".create_fullscreen").style.display = "none";
        document.getElementById("create_loader").innerHTML="";
        toast_success("Список товаров изменен")
      }
    }
    ajax_link.send(form_data);
});

on('#ajax', 'click', '.c_good_list_delete', function() {
  saver = document.querySelector(".pk_saver");
  pk = saver.getAttribute("data-pk");
  uuid = saver.getAttribute("data-uuid");

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', "/goods/community_progs/delete_album/" + pk + "/" + uuid + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        this_page_reload("/communities/" + pk + "/goods_list/" + uuid + "/")
      }
    }
    ajax_link.send();
});

on('#ajax', 'click', '.c_good_list_recover', function() {
  saver = document.querySelector(".pk_saver");
  pk = saver.getAttribute("data-pk");
  uuid = saver.getAttribute("data-uuid");

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', "/goods/community_progs/abort_delete_album/" + pk + "/" + uuid + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        this_page_reload("/communities/" + pk + "/goods_list/" + uuid + "/")
      }
    }
    ajax_link.send();
});
