on('#ajax', 'click', '#u_ucm_doc_repost_btn', function() {
  repost_constructor(this,
                     "/docs/repost/u_u_doc_repost/",
                     "Репост документа на стену сделан",
                     "/docs/repost/u_c_doc_repost/",
                     "Репост документа в сообщества сделан",
                     "/docs/repost/u_m_doc_repost/",
                     "Репост документа в сообщения сделан")
});
on('#ajax', 'click', '#u_ucm_doc_list_repost_btn', function() {
  repost_constructor(this,
                     "/docs/repost/u_u_doc_list_repost/",
                     "Репост списка документов на стену сделан",
                     "/docs/repost/u_c_doc_list_repost/",
                     "Репост списка документов в сообщества сделан",
                     "/docs/repost/u_m_doc_list_repost/",
                     "Репост списка документов в сообщения сделан")
});

on('#ajax', 'click', '.u_add_doc_list', function(e) {
  _this = this;
  parent = this.parentElement.parentElement.parentElement;
  uuid = parent.getAttribute("data-uuid");
  var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/docs/user_progs/add_list/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
    if ( link.readyState == 4 && link.status == 200 ) {
      _this.innerHTML = "";
      _this.classList.add("u_remove_doc_list");
      _this.classList.remove("u_add_doc_list")
      _this.innerHTML = '<svg fill="currentColor" class="svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg>'
  }};
  link.send( null );
});

on('body', 'click', '.u_doc_remove', function() {
  saver = this.parentElement.parentElement.parentElement;
  pk = saver.getAttribute("data-pk")
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/docs/user_progs/delete_doc/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    div = document.createElement("div");
    div.classList.add("col-sm-12");
    div.style.padding = "20px";
    div.style.display =  "block";
    div.innerHTML = "Документ удален. <span class='u_doc_restore pointer underline' data-pk='" + pk + "'>Восстановить</span>";
    item = saver.parentElement.parentElement.parentElement;
    item.style.display = "none"; item.parentElement.insertBefore(div, item)
  }};
  link.send( );
});
on('body', 'click', '.u_doc_restore', function() {
  pk = this.getAttribute("data-pk");
  block = this.parentElement; next = block.nextElementSibling;
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/docs/user_progs/restore_doc/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    block.remove();
    next.style.display = "block";
  }};
  link.send();
});

on('#ajax', 'click', '.u_add_doc_in_list', function() {
  add_item_in_list(this, '/docs/user_progs/add_doc_in_list/', "u_add_doc_in_list", "u_remove_doc_from_list")
});
on('#ajax', 'click', '.u_remove_doc_from_list', function() {
  remove_item_from_list(this, '/docs/user_progs/remove_doc_from_list/', "u_remove_doc_from_list", "u_add_doc_in_list")
});

on('#ajax', 'click', '#u_create_doc_btn', function() {
  form = document.querySelector("#u_doc_create");
  form_data = new FormData(form);
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");

  lists = form.querySelector("#id_list");
  selectedOptions = lists.selectedOptions;
  val = false;
  for (var i = 0; i < selectedOptions.length; i++) {
    if(selectedOptions[i].value) {val = true}
  }

  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!")
  } else if (!val){
    form.querySelector("#id_list").style.border = "1px #FF0000 solid";
    toast_error("Выберите список!")
  }
  else if (!form.querySelector("#id_file").value){
    form.querySelector("#id_file").style.border = "1px #FF0000 solid";
    toast_error("Загрузите документ!")
  } else { this.disabled = true }
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/docs/user_progs/create_doc/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    span1 = response.querySelector('.span1')
    if (span1.classList.contains(document.body.querySelector(".uuid_saver").getAttribute("data-uuid"))){
      container = document.body.querySelector(".is_paginate");
      container.insertAdjacentHTML('afterBegin', response.innerHTML);
      container.querySelector(".items_empty") ? container.querySelector(".items_empty").style.display = "none" : null;
      toast_info("Документ создан!")
    };
    toast_info("Документ создан!");
    close_fullscreen();
  }};

  link_.send(form_data);
});

on('#ajax', 'click', '#u_create_doc_list_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }
  post_and_load_object_page(form, "/docs/user_progs/add_list/", "/users/", "/doc_list/");
});

on('#ajax', 'click', '#u_edit_doc_list_btn', function() {
  media_list_edit(this, "/docs/user_progs/edit_list/")
});

on('body', 'click', '.u_doc_list_remove', function() {
  media_list_delete(this, "/docs/user_progs/delete_list/", "u_doc_list_remove", "u_doc_list_abort_remove")
});
on('body', 'click', '.u_doc_list_abort_remove', function() {
  media_list_recover(this, "/docs/user_progs/restore_list/", "u_doc_list_abort_remove", "u_doc_list_remove")
});
