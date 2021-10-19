on('#ajax', 'click', '#u_ucm_good_repost_btn', function() {
  repost_constructor(this,
                     "/goods/repost/u_u_good_repost/",
                     "Репост товара на стену сделан",
                     "/goods/repost/u_c_good_repost/",
                     "Репост товара в сообщества сделан",
                     "/goods/repost/u_m_good_repost/",
                     "Репост товара в сообщения сделан")
});
on('#ajax', 'click', '#u_ucm_good_list_repost_btn', function() {
  repost_constructor(this,
                     "/goods/repost/u_u_good_list_repost/",
                     "Репост списка товаров на стену сделан",
                     "/goods/repost/u_c_good_list_repost/",
                     "Репост списка товаров в сообщества сделан",
                     "/goods/repost/u_m_good_list_repost/",
                     "Репост списка товаров в сообщения сделан")
});

on('#ajax', 'click', '.u_add_good_in_list', function() {
  add_item_in_list(this, '/goods/user_progs/add_good_in_list/', "u_add_good_in_list", "u_remove_good_from_list")
})
on('#ajax', 'click', '.u_remove_good_from_list', function() {
  remove_item_from_list(this, '/goods/user_progs/remove_good_from_list/', "u_remove_good_from_list", "u_add_good_in_list")
})

on('#ajax', 'click', '.u_add_good_list', function(e) {
  _this = this;
  parent = this.parentElement.parentElement.parentElement;
  uuid = parent.getAttribute("data-uuid");
  var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/goods/user_progs/add_list/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
    if ( link.readyState == 4 && link.status == 200 ) {
      _this.innerHTML = "";
      _this.classList.add("u_remove_good_list");
      _this.classList.remove("u_add_good_list")
      _this.innerHTML = '<svg fill="#ffffff" style="width: 17px;" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"></path><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"></path></svg>'
  }};
  link.send( null );
});
on('#ajax', 'click', '.u_remove_good_list', function(e) {
  _this = this;
  parent = this.parentElement.parentElement.parentElement;
  uuid = parent.getAttribute("data-uuid");
  var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/goods/user_progs/remove_list/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
    if ( link.readyState == 4 && link.status == 200 ) {
      _this.innerHTML = "";
      _this.classList.add("u_add_good_list");
      _this.classList.remove("u_remove_good_list")
      _this.innerHTML = '<svg fill="#ffffff" style="width: 17px;" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg>'
  }};
  link.send( null );
});

on('#ajax', 'change', '.goods_category', function() {
  var val = this.value;
  if (val == '') {
    document.getElementById('subcat').innerHTML = "";
  } else {
    var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    link.open( 'GET', "/goods/progs/cat/" + val + "/", true );
    link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link.onreadystatechange = function () {
      if ( link.readyState == 4 ) {
          if ( link.status == 200 ) {
              var sub = document.getElementById("subcat");
              sub.innerHTML = link.responseText;
          }
      }
  };
  link.send( null );
  };
});

function good_gallery(loader){
  thumb_list = loader.querySelectorAll(".thumb_list li");
  thumb = loader.querySelector(".big_img");
  thumb_list.forEach((item) => {
    item.addEventListener("mouseover", function () {
    image = item.children[0].src;
      thumb.src = image;
    });
  });
}

on('#ajax', 'click', '.u_good_comment_edit', function() {
  get_edit_comment_form(this, "/goods/user_progs/edit_comment/")
});

on('#ajax', 'click', '.u_good_edit_comment_btn', function() {
  post_edit_comment_form(this, "/goods/user_progs/edit_comment/")
});

on('#ajax', 'click', '.u_good_comment_delete', function() {
  comment_delete(this, "/goods/user_progs/delete_comment/", "u_good_comment_restore")
})
on('#ajax', 'click', '.u_good_comment_restore', function() {
  comment_restore(this, "/goods/user_progs/restore_comment/")
});

on('#ajax', 'click', '.u_good_off_private', function() {
  send_good_change(this, "/goods/user_progs/off_private/", "u_good_on_private", "Вкл. приватность")
})
on('#ajax', 'click', '.u_good_on_private', function() {
  send_good_change(this, "/goods/user_progs/on_private/", "u_good_off_private", "Выкл. приватность")
})

on('#ajax', 'click', '.u_good_edit', function() {
  this.parentElement.nextElementSibling.style.display = "block"
})

on('#ajax', 'click', '.u_good_off_votes', function() {
  send_good_change(this, "/goods/user_progs/off_votes/", "u_good_on_votes", "Вкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "none";
  post.querySelector(".dislike").style.display = "none";
})
on('#ajax', 'click', '.u_good_on_votes', function() {
  send_good_change(this, "/goods/user_progs/on_votes/", "u_good_off_votes", "Выкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "unset";
  post.querySelector(".dislike").style.display = "unset";
})
on('#ajax', 'click', '.u_good_hide', function() {
  send_good_change(this, "/goods/user_progs/hide/", "u_good_unhide", "Товар не виден");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
})
on('#ajax', 'click', '.u_good_unhide', function() {
  send_good_change(this, "/goods/user_progs/unhide/", "u_good_hide", "Товар виден");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
})

on('#ajax', 'click', '.user_good_remove', function() {
  send_good_change(this, "/goods/user_progs/delete/", "user_good_restore", "Отмена");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  this.parentElement.parentElement.nextElementSibling.style.display = "none";
  post.querySelector(".order-2").style.display = "none";
  post.querySelector(".card").style.opacity = "0.5";
  this.style.color = "#FF0000";
})
on('#ajax', 'click', '.user_good_restore', function() {
  send_good_change(this, "/goods/user_progs/restore/", "user_good_remove", "Удалить");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  this.parentElement.parentElement.nextElementSibling.style.display = "unset";
  post.querySelector(".order-2").style.display = "unset";
  post.querySelector(".card").style.opacity = "1";
})

on('#ajax', 'click', '.u_good_like', function() {
  block = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = block.getAttribute("data-pk");
  good_pk = block.getAttribute("good-pk");
  send_like(block, "/goods/votes/user_like/" + good_pk + "/" + pk + "/");
  like_reload(this.nextElementSibling, this.nextElementSibling.nextElementSibling.nextElementSibling, "u_all_good_likes");
});
on('#ajax', 'click', '.u_good_dislike', function() {
  block = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = block.getAttribute("data-pk");
  good_pk = block.getAttribute("good-pk");
  send_dislike(block, "/goods/votes/user_dislike/" + good_pk + "/" + pk + "/");
  dislike_reload(this.previousElementSibling, this.nextElementSibling, "u_all_good_dislikes");
});
on('#ajax', 'click', '.u_good_like2', function() {
  _this = this;
  good = _this.parentElement;
  comment_pk = good.getAttribute("data-pk");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_like(good, "/goods/votes/user_comment/" + comment_pk + "/" + pk + "/like/");
  like_reload(this.nextElementSibling, this.nextElementSibling.nextElementSibling.nextElementSibling, "u_all_good_comment_likes")
});
on('#ajax', 'click', '.u_good_dislike2', function() {
  _this = this;
  good = _this.parentElement;
  comment_pk = good.getAttribute("data-pk");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_dislike(good, "/goods/votes/user_comment/" + comment_pk + "/" + pk + "/dislike/");
  dislike_reload(this.previousElementSibling, this.nextElementSibling, "u_all_good_comment_dislikes")
});


on('#ajax', 'click', '#good_image', function() {
  img = this.previousElementSibling.querySelector("#id_image")
  get_image_priview(this, img);
});
on('#ajax', 'click', '#good_image2', function() {
  img = this.previousElementSibling.querySelector(".image")
  get_image_priview(this, img);
});
on('#ajax', 'click', '#good_image3', function() {
  img = this.previousElementSibling.querySelector(".image")
  get_image_priview(this, img);
});
on('#ajax', 'click', '#good_image4', function() {
  img = this.previousElementSibling.querySelector(".image")
  get_image_priview(this, img);
});
on('#ajax', 'click', '#good_image5', function() {
  img = this.previousElementSibling.querySelector(".image")
  get_image_priview(this, img);
});
on('#ajax', 'click', '.u_good_add', function() {
  create_fullscreen('/goods/user_progs/add/' + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/", "item_fullscreen");
});

on('#ajax', 'click', '#u_add_good_btn', function() {
  form_post = document.body.querySelector("#u_add_good_form");
  form_data = new FormData(form_post);
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");

  lists = form_post.querySelector("#id_list");
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
    form_post.querySelector("#id_list").style.border = "1px #FF0000 solid";
    toast_error("Выберите альбом!");
    return
  } else {this.disabled = true}
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/goods/user_progs/add/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    new_good = document.createElement("div");
    new_good.innerHTML = elem;
    good = new_good.querySelector(".u_good_detail");
    data_pk = good.getAttribute('good-pk');
    data_uuid = good.getAttribute('good-uuid');
    src = good.querySelector("img").getAttribute('src');
    title = good.querySelector(".good_title").innerHTML;

    if (document.body.querySelector(".current_file_dropdown")){
      check_good_in_block(document.body.querySelector(".current_file_dropdown").parentElement.parentElement.parentElement.previousElementSibling, _this, pk) ? null : (good_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, media_block, pk))
    } else if (document.body.querySelector(".attach_block")){
      check_good_in_block(document.body.querySelector(".attach_block"), _this, pk) ? null : (good_post_attach(document.body.querySelector(".attach_block"), media_block, pk))
    } else if (document.body.querySelector(".message_attach_block")){
      check_good_in_block(document.body.querySelector(".message_attach_block"), _this, pk) ? null : (good_message_attach(document.body.querySelector(".message_attach_block"), media_block, pk))
    }
    else {
      uuid = document.body.querySelector(".pk_saver").getAttribute("data-uuid");
      span1 = new_good.querySelector('.span1')
      if (span1.classList.contains(data_pk)){
        container = document.body.querySelector(".is_paginate");
        container.insertAdjacentHTML('afterBegin', new_good.innerHTML);
        container.querySelector(".items_empty") ? container.querySelector(".items_empty").style.display = "none" : null;
      }
  };
  close_fullscreen();
  toast_info("Товар создан!")
  }};
  link_.send(form_data);
});

on('#ajax', 'click', '#u_create_good_list_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!"); return
  } else { this.disabled = true }
  post_and_load_object_page(form, "/goods/user_progs/add_list/", "/users/", "/goods_list/")
});

on('#ajax', 'click', '#u_edit_good_list_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }
  uuid = form.getAttribute("data-uuid");

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'POST', "/goods/user_progs/edit_list/" + uuid + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        name = form.querySelector('#id_name').value;
        document.body.querySelector(".list_name").innerHTML = name;
        close_fullscreen();
        toast_success("Список товаров изменен")
      }
    }
    ajax_link.send(form_data);
});

on('body', 'click', '.u_good_list_remove', function() {
  media_list_delete(this, "/goods/user_progs/delete_list/", "u_good_list_remove", "u_good_list_abort_remove")
});
on('body', 'click', '.u_good_list_abort_remove', function() {
  media_list_recover(this, "/goods/user_progs/restore_list/", "u_good_list_abort_remove", "u_good_list_remove")
});

on('#ajax', 'click', '.mob_u_good_off_comment', function() {
  send_mob_good_change(this, "/goods/user_progs/off_comment/", "mob_u_good_on_comment", "Вкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".load_good_comments").style.display = "none"
})
on('#ajax', 'click', '.mob_u_good_on_comment', function() {
  send_mob_good_change(this, "/goods/user_progs/on_comment/", "mob_u_good_off_comment", "Выкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".load_good_comments").style.display = "unset"
})
on('#ajax', 'click', '.mob_u_good_off_votes', function() {
  send_mob_good_change(this, "/goods/user_progs/off_votes/", "mob_u_good_on_votes", "Вкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "none";
  post.querySelector(".dislike").style.display = "none";
})
on('#ajax', 'click', '.mob_u_good_on_votes', function() {
  send_mob_good_change(this, "/goods/user_progs/on_votes/", "mob_u_good_off_votes", "Выкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "unset";
  post.querySelector(".dislike").style.display = "unset";
})
on('#ajax', 'click', '.mob_u_good_hide', function() {
  send_mob_good_change(this, "/goods/user_progs/hide/", "mob_u_good_unhide", "Товар не виден");
})
on('#ajax', 'click', '.mob_u_good_unhide', function() {
  send_mob_good_change(this, "/goods/user_progs/unhide/", "mob_u_good_hide", "Товар виден");
})
on('#ajax', 'click', '.mob_user_good_remove', function() {
  send_mob_good_change(this, "/goods/user_progs/delete/", "mob_user_good_restore", "Отмена");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".good_card").style.display = "none";
  post.querySelector(".card").style.opacity = "0.5";
  this.style.color = "#FF0000";
})
on('#ajax', 'click', '.mob_user_good_restore', function() {
  send_mob_good_change(this, "/goods/user_progs/restore/", "mob_user_good_remove", "Удалить");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".good_card").style.display = "unset";
  post.querySelector(".card").style.opacity = "1";
})
