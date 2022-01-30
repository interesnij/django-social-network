

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
