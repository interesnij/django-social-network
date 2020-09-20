on('#ajax', 'click', '#c_ucm_doc_repost_btn', function() {
  form_post = document.body.querySelector("#c_uсm_doc_repost_form");
  form_data = new FormData(form_post);
  doc_pk = this.getAttribute("doc-pk");
  pk = this.getAttribute("data-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );

  if (form_post.querySelector('#repost_radio_wall').checked) {
    link_.open( 'POST', "/docs/repost/c_u_doc_repost/" + pk + "/" + doc_pk + "/", true );
    link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link_.send(form_data);
    toast_info("Репост документа на стену сделан")
  }

  else if(form_post.querySelector('#repost_radio_community').checked){
    staff_communities = form_post.querySelector("#id_staff_communities");
    selectedOptions = staff_communities.selectedOptions;
    val = false;
    for (var i = 0; i < selectedOptions.length; i++) {if(selectedOptions[i].value) {val = true}}
    if(val){
      link_.open( 'POST', "/docs/repost/c_c_doc_repost/" + pk + "/" + doc_pk + "/", true );
      link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      link_.send(form_data);
      toast_info("Репост документа в сообщества сделан")
    }else{toast_error("Выберите сообщества для репоста")}
  }

  else if(form_post.querySelector('#repost_radio_message').checked){
    user_connections = form_post.querySelector("#id_user_connections");
    selectedOptions = user_connections.selectedOptions;
    val = false;
    for (var i = 0; i < selectedOptions.length; i++) {if(selectedOptions[i].value) {val = true}}
    if(val){
      link_.open( 'POST', "/docs/repost/c_m_doc_repost/" + pk + "/" + doc_pk + "/", true );
      link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      link_.send(form_data);
      toast_info("Репост документа в сообщения сделан")
    }else{toast_error("Выберите пользователя для репоста")}
  };

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    document.querySelector(".votes_fullscreen").style.display = "none";
    document.getElementById("votes_loader").innerHTML="";
  }}
});

on('#ajax', 'click', '#c_ucm_doc_list_repost_btn', function() {
  form_post = document.body.querySelector("#c_uсm_doc_list_repost_form");
  form_data = new FormData(form_post);
  uuid = this.getAttribute("data-uuid");
  pk = this.getAttribute("data-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );

  if (form_post.querySelector('#repost_radio_wall').checked) {
    link_.open( 'POST', "/docs/repost/c_u_doc_list_repost/" + pk + "/" + uuid + "/", true );
    link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link_.send(form_data);
    toast_info("Репост списка документов на стену сделан")
  }

  else if(form_post.querySelector('#repost_radio_community').checked){
    staff_communities = form_post.querySelector("#id_staff_communities");
    selectedOptions = staff_communities.selectedOptions;
    val = false;
    for (var i = 0; i < selectedOptions.length; i++) {if(selectedOptions[i].value) {val = true}}
    if(val){
      link_.open( 'POST', "/docs/repost/c_c_doc_list_repost/" + pk + "/" + uuid + "/", true );
      link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      link_.send(form_data);
      toast_info("Репост списка документов в сообщества сделан")
    }else{toast_error("Выберите сообщества для репоста")}
  }

  else if(form_post.querySelector('#repost_radio_message').checked){
    user_connections = form_post.querySelector("#id_user_connections");
    selectedOptions = user_connections.selectedOptions;
    val = false;
    for (var i = 0; i < selectedOptions.length; i++) {if(selectedOptions[i].value) {val = true}}
    if(val){
      link_.open( 'POST', "/docs/repost/c_m_doc_list_repost/" + pk + "/" + uuid + "/", true );
      link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      link_.send(form_data);
      toast_info("Репост списка документов в сообщения сделан")
    }else{toast_error("Выберите пользователя для репоста")}
  };

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    document.querySelector(".votes_fullscreen").style.display = "none";
    document.getElementById("votes_loader").innerHTML="";
  }}
});

on('#ajax', 'click', '.c_doc_add', function(e) {
  block = this.parentElement;
  pk = block.parentElement.getAttribute("data-pk");
  uuid = document.body.querySelector(".pk_saver").getAttribute("data-uuid");
  var _link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  _link.open( 'GET', "/docs/community_progs/c_add_doc/" + pk + "/" + uuid + "/", true );
  _link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  _link.onreadystatechange = function () {
    if ( _link.readyState == 4 && _link.status == 200 ) {
      block.innerHTML = "";
      block.innerHTML = "<span class='c_doc_remove btn_default pointer' title='Удалить'><svg fill='currentColor' style='width:22px;height:22px;' class='svg_default'><path fill='none' d='M0 0h24v24H0z'/><path d='M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z'/></svg></span>"
  }};
  _link.send( null );
});

on('#ajax', 'click', '.c_doc_remove', function(e) {
  block = this.parentElement;
  pk = block.parentElement.getAttribute("data-pk");
  uuid = document.body.querySelector(".pk_saver").getAttribute("data-uuid");
  var _link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  _link.open( 'GET', "/docs/community_progs/c_remove_doc/" + pk + "/" + uuid + "/", true );
  _link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  _link.onreadystatechange = function () {
    if ( _link.readyState == 4 && _link.status == 200 ) {
      block.innerHTML = "";
      block.innerHTML = "<span class='c_doc_add btn_default pointer' title='Добавить'><svg fill='currentColor' style='width:22px;height:22px;' class='svg_default'><path d='M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z'/><path d='M0 0h24v24H0z' fill='none'/></svg></span>"
  }};
  _link.send( null );
});

on('#ajax', 'click', '.c_add_doc_in_list', function() {
  _this = this;
  parent = _this.parentElement;
  uuid = parent.getAttribute("data-uuid");
  pk = _this.parentElement.parentElement.parentElement.parentElement.getAttribute("data-pk");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', '/docs/community_progs/c_add_doc_in_list/' + pk + "/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    list = parent.querySelector(".c_add_doc_in_list");
    list.style.paddingLeft = "14px";
    list.classList.add("c_remove_doc_in_list");
    list.classList.remove("c_add_doc_in_list");
    span = document.createElement("span");
    span.innerHTML = '<svg fill="currentColor" style="width:15px;height:15px;" class="svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg> ';
    list.prepend(span)
  }};
  link.send( null );
})
on('#ajax', 'click', '.c_remove_doc_in_list', function() {
  _this = this;
  parent = _this.parentElement;
  uuid = parent.getAttribute("data-uuid");
  pk = _this.parentElement.parentElement.parentElement.parentElement.getAttribute("data-pk");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', '/docs/community_progs/c_remove_doc_in_list/' + pk + "/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    list = parent.querySelector(".c_remove_doc_in_list");
    list.style.paddingLeft = "30px";
    list.classList.add("c_add_doc_in_list");
    list.classList.remove("c_remove_doc_in_list");
    list.querySelector("svg").remove();
  }};
  link.send( null );
})

on('#ajax', 'click', '#c_create_doc_list_btn', function() {
  form = document.body.querySelector("#c_doc_list_create");
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { null }
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'POST', "/docs/community_progs/create_list/" + pk + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        elem_ = document.createElement('span');
        elem_.innerHTML = ajax_link.responseText;
        ajax = elem_.querySelector("#reload_block");
        rtr = document.getElementById('ajax');
        rtr.innerHTML = ajax.innerHTML;
        window.scrollTo(0,0);
        document.title = elem_.querySelector('title').innerHTML;

        uuid = rtr.querySelector(".pk_saver").getAttribute("data-uuid");
        window.history.pushState(null, "vfgffgfgf", '/communities/' + pk + "/" + 'doc_list/' + uuid + '/');
      }
    }
    ajax_link.send(form_data);
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
  uuid = document.body.querySelector(".pk_saver").getAttribute("data-uuid");
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
    if (span1.classList.contains(uuid)){
      container = document.body.querySelector(".community_block_paginate");
      container.insertAdjacentHTML('afterBegin', response.innerHTML);
      container.querySelector(".doc_empty") ? container.querySelector(".doc_empty").style.display = "none" : null;
      toast_info("Документ создан!")
    } else{
      toast_info("Документ создан!")
    }
    document.querySelector(".create_fullscreen").style.display = "none";
    document.getElementById("create_loader").innerHTML="";
  }};

  link_.send(form_data);
});

on('#ajax', 'click', '#c_edit_doc_list_btn', function() {
  form = document.body.querySelector("#c_edit_doc_list_form");
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }

  pk = form.getAttribute("data-pk");
  uuid = form.getAttribute("data-uuid");

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'POST', "/docs/community_progs/edit_list/" + pk + "/" + uuid + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        name = form.querySelector('#id_name').value;
        document.body.querySelector(".list_name").innerHTML = name;
        document.querySelector(".create_fullscreen").style.display = "none";
        document.getElementById("create_loader").innerHTML="";
        toast_success("Список документов изменен")
      }
    }
    ajax_link.send(form_data);
});

on('#ajax', 'click', '.c_doc_list_delete', function() {
  saver = document.querySelector(".pk_saver");
  pk = saver.getAttribute("data-pk");
  uuid = saver.getAttribute("data-uuid");

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', "/docs/community_progs/delete_list/" + pk + "/" + uuid + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        this_page_reload("/communities/" + pk + "/doc_list/" + uuid)
      }
    }
    ajax_link.send();
});

on('#ajax', 'click', '.c_doc_list_recover', function() {
  saver = document.querySelector(".pk_saver");
  pk = saver.getAttribute("data-pk");
  uuid = saver.getAttribute("data-uuid");

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', "/docs/community_progs/abort_delete_list/" + pk + "/" + uuid + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        this_page_reload("/communities/" + pk + "/doc_list/" + uuid)
      }
    }
    ajax_link.send();
});
