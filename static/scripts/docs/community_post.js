on('#ajax', 'click', '#c_ucm_doc_repost_btn', function() {
  repost_constructor(this,
                     "/docs/repost/c_u_doc_repost/",
                     "Репост документа на стену сделан",
                     "/docs/repost/c_c_doc_repost/",
                     "Репост документа в сообщества сделан",
                     "/docs/repost/c_m_doc_repost/",
                     "Репост документа в сообщения сделан")
});
on('#ajax', 'click', '#c_ucm_doc_list_repost_btn', function() {
  repost_constructor(this,
                     "/docs/repost/c_u_doc_list_repost/",
                     "Репост списка документов на стену сделан",
                     "/docs/repost/c_c_doc_list_repost/",
                     "Репост списка документов в сообщества сделан",
                     "/docs/repost/c_m_doc_list_repost/",
                     "Репост списка документов в сообщения сделан")
});

on('#ajax', 'click', '.c_doc_add', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  create_fullscreen("/docs/community_progs/create_doc/" + pk + "/", "worker_fullscreen");
});

on('body', 'click', '.c_doc_remove', function() {
  saver = this.parentElement.parentElement.parentElement;
  pk = saver.getAttribute("data-pk")
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/docs/community_progs/delete_doc/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    div = document.createElement("div");
    div.classList.add("col-md-6", "col-sm-12");
    div.style.padding = "20px";
    div.style.display =  "block";
    div.innerHTML = "Документ удален. <span class='c_doc_restore pointer underline' data-pk='" + pk + "'>Восстановить</span>";
    item = saver.parentElement.parentElement.parentElement;
    item.style.display = "none"; item.parentElement.insertBefore(div, item);
    main_container = document.body.querySelector(".main-container");
    add_list_in_all_stat("deleted_community_doc",pk,main_container.getAttribute("data-type"),main_container.getAttribute("data-pk"))
  }};
  link.send();
});
on('body', 'click', '.c_doc_restore', function() {
  pk = this.getAttribute("data-pk");
  block = this.parentElement; next = block.nextElementSibling;
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/docs/community_progs/restore_doc/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    block.remove();
    next.style.display = "block";
    main_container = document.body.querySelector(".main-container");
    add_list_in_all_stat("restored_community_doc",pk,main_container.getAttribute("data-type"),main_container.getAttribute("data-pk"))
  }};
  link.send();
});

on('#ajax', 'click', '.c_add_doc_in_list', function() {
  add_item_in_list(this, '/docs/community_progs/copy_doc_in_list/', "c_add_doc_in_list", "c_remove_doc_from_list")
});
on('#ajax', 'click', '.c_remove_photo_from_list', function() {
  remove_item_from_list(this, '/docs/community_progs/uncopy_doc_from_list/', "c_remove_doc_from_list", "c_add_doc_in_list")
});

on('#ajax', 'click', '#c_create_doc_list_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }
  post_and_load_object_page(form, "/docs/community_progs/add_list/", "/communities/", "/doc_list/", "added_community_doc_list");
});

on('#ajax', 'click', '#c_create_doc_btn', function() {
  form = document.querySelector("#c_doc_create");
  form_data = new FormData(form);

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
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/docs/community_progs/create_doc/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    list = document.body.querySelector("#id_list");
    span1 = response.querySelector('.span1')
    if (span1.classList.contains(document.body.querySelector(".uuid_saver").getAttribute("data-uuid"))){
      container = document.body.querySelector(".is_paginate");
      container.insertAdjacentHTML('afterBegin', response.innerHTML);
      container.querySelector(".items_empty") ? container.querySelector(".items_empty").style.display = "none" : null;
      toast_info("Документ создан!")
    };
    close_work_fullscreen();
    main_container = document.body.querySelector(".main-container");
    add_list_in_all_stat("created_community_doc",pk,main_container.getAttribute("data-type"),main_container.getAttribute("data-pk"))
  }};

  link_.send(form_data);
});

on('#ajax', 'click', '#c_edit_doc_list_btn', function() {
  media_list_edit(this, "/docs/community_progs/edit_list/", "edited_community_doc_list")
});

on('body', 'click', '.c_doc_list_remove', function() {
  media_list_delete(this, "/docs/community_progs/delete_list/", "c_doc_list_remove", "c_doc_list_abort_remove", "deleted_community_doc_list")
});
on('body', 'click', '.c_doc_list_abort_remove', function() {
  media_list_recover(this, "/docs/community_progs/restore_list/", "c_doc_list_abort_remove", "c_doc_list_remove", "recover_community_doc_list")
});
