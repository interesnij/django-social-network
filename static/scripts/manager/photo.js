
on('#ajax', 'click', '.photo_delete_window', function() {
  _this = this;
  if(_this.parentElement.classList.contains("btn_console")){
    div = _this.parentElement.parentElement.parentElement.parentElement;
    uuid = _this.parentElement.parentElement.parentElement.parentElement.getAttribute("data-uuid");
    list = document.querySelectorAll('.pag');
    for (var i = 0; i < list.length; i++) {
      list[i].classList.remove("changed");
    }
    div.classList.add("changed")
  }else if (_this.parentElement.parentElement.parentElement.parentElement.getAttribute){
    uuid = _this.parentElement.parentElement.parentElement.parentElement.getAttribute("data-uuid");
    _this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.classList.add("manager_removed")
  }
  loader = document.getElementById("create_loader");
  open_fullscreen("/managers/progs_photo/delete_window/" + uuid, loader)
})

on('#ajax', 'click', '.create_photo_delete_btn', function() {
  var moderation_container, container_object
  _this = this;
  form_data = new FormData(document.querySelector("#photo_delete_form"));
  form_post = document.querySelector("#photo_delete_form");
  if (document.body.querySelector(".changed")){
    div = document.body.querySelector(".changed");
    uuid = div.getAttribute("data-uuid");
    moderation_container = document.body.querySelector("#moderation_photo_container");
  } else if (_this.getAttribute){
    document.querySelector(".photo_fullscreen").style.display = "none";
    document.getElementById("photo_loader").innerHTML="";
  }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/managers/progs_photo/create_delete/" + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Фото удалено!");
    document.querySelector(".worker_fullscreen").style.display = "none";
    document.getElementById("worker_loader").innerHTML="";
    div.remove();
    try{
    if (container_object && !container_object.querySelector(".card")){
      container_object.innerHTML = '<div class="card mb-3 post_empty centered"><div class="card-body"><svg fill="currentColor" class="thumb_big svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path fill="currentColor" d="M22 13h-8v-2h8v2zm0-6h-8v2h8V7zm-8 10h8v-2h-8v2zm-2-8v6c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V9c0-1.1.9-2 2-2h6c1.1 0 2 .9 2 2zm-1.5 6l-2.25-3-1.75 2.26-1.25-1.51L3.5 15h7z"/></svg></div><h6 style="margin: 20px;text-align: center;"> Пока ничего нет...</h6></div>'
    } else if (moderation_container && !moderation_container.querySelector(".pag")){
      moderation_container.innerHTML = '<div class="card mb-3 post_empty centered"><div class="card-body"><svg fill="currentColor" class="thumb_big svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path fill="currentColor" d="M22 13h-8v-2h8v2zm0-6h-8v2h8V7zm-8 10h8v-2h-8v2zm-2-8v6c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V9c0-1.1.9-2 2-2h6c1.1 0 2 .9 2 2zm-1.5 6l-2.25-3-1.75 2.26-1.25-1.51L3.5 15h7z"/></svg></div><h6 style="margin: 20px;text-align: center;"> Жалоб пока нет...</h6></div>'
    }} catch { null }
  }};
  link_.send(form_data);
});

on('#ajax', 'click', '.photo_unverify', function() {
  div = this.parentElement.parentElement.parentElement.parentElement;
  post_uuid = div.getAttribute("data-uuid");
  obj_pk = div.getAttribute("data-pk");
  penalty_container = document.body.querySelector("#penalty_photo_container");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/managers/progs_photo/unverify/" + post_uuid + "/" + obj_pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Верификация отменена!");
    div.remove();
    if (!document.body.querySelector(".pag")){
      penalty_container.innerHTML = '<div class="card mb-3 post_empty centered"><div class="card-body"><svg fill="currentColor" class="thumb_big svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path fill="currentColor" d="M22 13h-8v-2h8v2zm0-6h-8v2h8V7zm-8 10h8v-2h-8v2zm-2-8v6c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V9c0-1.1.9-2 2-2h6c1.1 0 2 .9 2 2zm-1.5 6l-2.25-3-1.75 2.26-1.25-1.51L3.5 15h7z"/></svg></div><h6 style="margin: 20px;text-align: center;"> Штраф-лист пуст...</h6></div>'
    }
  }};
  link_.send();
});

on('#ajax', 'click', '.remove_photo_delete', function() {
  div = this.parentElement.parentElement.parentElement.parentElement;
  uuid = div.getAttribute("data-uuid");
  penalty_container = document.body.querySelector("#penalty_photo_container");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/managers/progs_photo/delete_delete/" + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Фото восстановлено!");
    div.remove();
    if (penalty_container){
      !penalty_container.querySelector(".pag") ? penalty_container.innerHTML = '<div class="card mb-3 post_empty centered"><div class="card-body"><svg fill="currentColor" class="thumb_big svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path fill="currentColor" d="M22 13h-8v-2h8v2zm0-6h-8v2h8V7zm-8 10h8v-2h-8v2zm-2-8v6c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V9c0-1.1.9-2 2-2h6c1.1 0 2 .9 2 2zm-1.5 6l-2.25-3-1.75 2.26-1.25-1.51L3.5 15h7z"/></svg></div><h6 style="margin: 20px;text-align: center;"> Штраф-лист пуст...</h6></div>' : null
    }
  }};
  link_.send();
});

on('#ajax', 'click', '.photo_rejected', function() {
  div = this.parentElement.parentElement.parentElement.parentElement;
  uuid = div.getAttribute("data-uuid");
  moderation_container = document.body.querySelector("#moderation_photo_container");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/managers/progs_photo/create_rejected/" + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Жалобы на фото удалены!");
    div.remove();
    if (!moderation_container.querySelector(".card")){
      moderation_container.innerHTML = '<div class="card mb-3 post_empty centered"><div class="card-body"><svg fill="currentColor" class="thumb_big svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path fill="currentColor" d="M22 13h-8v-2h8v2zm0-6h-8v2h8V7zm-8 10h8v-2h-8v2zm-2-8v6c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V9c0-1.1.9-2 2-2h6c1.1 0 2 .9 2 2zm-1.5 6l-2.25-3-1.75 2.26-1.25-1.51L3.5 15h7z"/></svg></div><h6 style="margin: 20px;text-align: center;"> Пока ничего нет...</h6></div>'
    }
  }};

  link_.send();
});

/////////////////////////////////////////////////////////////
on('#ajax', 'click', '.photo_comment_delete_window', function() {
  _this = this;
  if(_this.parentElement.classList.contains("btn_console")){
    div = _this.parentElement.parentElement.parentElement.parentElement;
    pk = div.getAttribute("data-pk");
    list = document.querySelectorAll('.pag');
    for (var i = 0; i < list.length; i++) {
      list[i].classList.remove("changed");
    }
    div.classList.add("changed")
  }else if (_this.parentElement.parentElement.getAttribute){
    pk = _this.parentElement.parentElement.getAttribute("data-pk");
  }
  loader = document.getElementById("worker_loader");
  open_fullscreen("/managers/progs_photo/delete_comment_window/" + pk, loader)
})

on('#ajax', 'click', '.create_photo_comment_delete_btn', function() {
  var container_object, moderation_container
  _this = this;
  form_data = new FormData(document.querySelector("#photo_comment_delete_form"));
  form_post = document.querySelector("#photo_comment_delete_form");
  if (document.body.querySelector(".changed")){
    div = document.body.querySelector(".changed");
    pk = div.getAttribute("data-pk");
    moderation_container = document.body.querySelector("#moderation_photo_comment_container");
  } else if (_this.getAttribute){
    div = _this;
    pk = div.getAttribute("data-pk");
    container_object = document.body.querySelector(".comments_block_container");
  }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/managers/progs_photo/comment_create_delete/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Комментарий удален!");
    document.querySelector(".worker_fullscreen").style.display = "none";
    document.getElementById("worker_loader").innerHTML="";
    if (container_object){
      comment_pk = container_object.querySelector( '[data-pk=' + '"' + pk + '"' + ']' );
      comment = comment_pk.parentElement.parentElement;
      comment.remove()
    } else if (moderation_container){
      div.remove();
      !moderation_container.querySelector(".pag") ?
      moderation_container.innerHTML = '<div class="card mb-3 post_empty centered"><div class="card-body"><svg fill="currentColor" class="thumb_big svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path fill="currentColor" d="M22 13h-8v-2h8v2zm0-6h-8v2h8V7zm-8 10h8v-2h-8v2zm-2-8v6c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V9c0-1.1.9-2 2-2h6c1.1 0 2 .9 2 2zm-1.5 6l-2.25-3-1.75 2.26-1.25-1.51L3.5 15h7z"/></svg></div><h6 style="margin: 20px;text-align: center;"> Жалоб пока нет...</h6></div>' : null
    }
  }};
  link_.send(form_data);
});
on('#ajax', 'click', '.photo_comment_unverify', function() {
  div = this.parentElement.parentElement.parentElement.parentElement;
  comment_pk = div.getAttribute("comment-pk");
  obj_pk = div.getAttribute("obj-pk");
  penalty_container = document.body.querySelector("#penalty_photo_comment_container");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/managers/progs_photo/comment_unverify/" + comment_pk + "/" + obj_pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Верификация отменена!");
    div.remove();
    if (!document.body.querySelector(".pag")){
      penalty_container.innerHTML = '<div class="card mb-3 post_empty centered"><div class="card-body"><svg fill="currentColor" class="thumb_big svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path fill="currentColor" d="M22 13h-8v-2h8v2zm0-6h-8v2h8V7zm-8 10h8v-2h-8v2zm-2-8v6c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V9c0-1.1.9-2 2-2h6c1.1 0 2 .9 2 2zm-1.5 6l-2.25-3-1.75 2.26-1.25-1.51L3.5 15h7z"/></svg></div><h6 style="margin: 20px;text-align: center;"> Штраф-лист пуст...</h6></div>'
    }
  }};
  link_.send();
});
on('#ajax', 'click', '.remove_photo_comment_delete', function() {
  div = this.parentElement.parentElement.parentElement.parentElement;
  comment_pk = div.getAttribute("comment-pk");
  penalty_container = document.body.querySelector("#penalty_photo_comment_container");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/managers/progs_photo/comment_delete_delete/" + comment_pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Сообщение восстановлено!");
    div.remove();
    if (penalty_container){
      !penalty_container.querySelector(".pag") ? penalty_container.innerHTML = '<div class="card mb-3 post_empty centered"><div class="card-body"><svg fill="currentColor" class="thumb_big svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path fill="currentColor" d="M22 13h-8v-2h8v2zm0-6h-8v2h8V7zm-8 10h8v-2h-8v2zm-2-8v6c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V9c0-1.1.9-2 2-2h6c1.1 0 2 .9 2 2zm-1.5 6l-2.25-3-1.75 2.26-1.25-1.51L3.5 15h7z"/></svg></div><h6 style="margin: 20px;text-align: center;"> Штраф-лист пуст...</h6></div>' : null
    }
  }};
  link_.send();
});
on('#ajax', 'click', '.photo_comment_rejected', function() {

  div = this.parentElement.parentElement.parentElement.parentElement;
  comment_pk = div.getAttribute("data-pk");
  moderation_container = document.body.querySelector("#moderation_photo_comment_container");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/managers/progs_photo/comment_create_rejected/" + comment_pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Жалобы на комментарий удалены!");
    div.remove();
    if (!moderation_container.querySelector(".pag")){
      moderation_container.innerHTML = '<div class="card mb-3 post_empty centered"><div class="card-body"><svg fill="currentColor" class="thumb_big svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path fill="currentColor" d="M22 13h-8v-2h8v2zm0-6h-8v2h8V7zm-8 10h8v-2h-8v2zm-2-8v6c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V9c0-1.1.9-2 2-2h6c1.1 0 2 .9 2 2zm-1.5 6l-2.25-3-1.75 2.26-1.25-1.51L3.5 15h7z"/></svg></div><h6 style="margin: 20px;text-align: center;"> Пока ничего нет...</h6></div>'
    }
  }};

  link_.send();
});
