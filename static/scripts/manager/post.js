on('#ajax', 'click', '.post_suspend_window', function() {
  _this = this;
  if(_this.parentElement.classList.contains("btn_console")){
    div = _this.parentElement.parentElement.parentElement.parentElement;
    uuid = _this.parentElement.parentElement.parentElement.parentElement.getAttribute("data-uuid");
    list = document.querySelectorAll('.pag');
    for (var i = 0; i < list.length; i++) {
      list[i].classList.remove("changed");
    }
    div.classList.add("changed")
  }else if (_this.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute){
    uuid = _this.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute("data-uuid");
  }
  loader = document.getElementById("create_loader");
  open_fullscreen("/managers/progs_post/suspend_window/" + uuid, loader)
})
on('#ajax', 'click', '.post_delete_window', function() {
  _this = this;
  if(_this.parentElement.classList.contains("btn_console")){
    div = _this.parentElement.parentElement.parentElement.parentElement;
    uuid = _this.parentElement.parentElement.parentElement.parentElement.getAttribute("data-uuid");
    list = document.querySelectorAll('.pag');
    for (var i = 0; i < list.length; i++) {
      list[i].classList.remove("changed");
    }
    div.classList.add("changed")
  }else if (_this.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute){
    uuid = _this.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute("data-uuid");
  }
  loader = document.getElementById("create_loader");
  open_fullscreen("/managers/progs_post/delete_window/" + uuid, loader)
})

on('#ajax', 'click', '.create_post_suspend_btn', function() {
  _this = this;
  form_data = new FormData(document.querySelector("#post_suspend_form"));
  form_post = document.querySelector("#post_suspend_form");
  if (document.body.querySelector(".changed")){
    div = document.body.querySelector(".changed");
    pk = div.getAttribute("data-uuid");
  } else if (_this.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute){
    div = _this.parentElement.parentElement.parentElement.parentElement.parentElement;
    pk = div.getAttribute("data-uuid");
  }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/managers/progs_post/create_suspension/" + uuid + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Пост заморожен!");
    document.querySelector(".create_fullscreen").style.display = "none";
    document.getElementById("create_loader").innerHTML="";
    div.remove();
  }};
  link_.send(form_data);
});
on('#ajax', 'click', '.create_post_delete_btn', function() {
  _this = this;
  form_data = new FormData(document.querySelector("#post_delete_form"));
  form_post = document.querySelector("#post_delete_form");
  if (document.body.querySelector(".changed")){
    div = document.body.querySelector(".changed");
    pk = div.getAttribute("data-uuid");
  } else if (_this.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute){
    div = _this.parentElement.parentElement.parentElement.parentElement.parentElement;
    pk = div.getAttribute("data-uuid");
  }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/managers/progs_post/create_delete/" + uuid + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Пост удален!");
    document.querySelector(".create_fullscreen").style.display = "none";
    document.getElementById("create_loader").innerHTML="";
    div.remove();
  }};

  link_.send(form_data);
});

on('#ajax', 'click', '.post_unverify', function() {
  div = this.parentElement.parentElement.parentElement.parentElement;
  post_uuid = div.getAttribute("data-uuid");
  obj_pk = div.getAttribute("data-pk");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/managers/progs_post/unverify/" + post_uuid + "/" + obj_pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Верификация отменена!");
    div.style.display = "none";
  }};

  link_.send();
});

on('#ajax', 'click', '.remove_post_suspend', function() {
  li = this.parentElement.parentElement.parentElement.parentElement;
  uuid = li.getAttribute("data-uuid");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/managers/progs_post/delete_suspension/" + uuid + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Заморозка отменена!");
    li.style.display = "none";
  }};
  link_.send();
});
on('#ajax', 'click', '.remove_post_delete', function() {
  li = this.parentElement.parentElement.parentElement.parentElement;
  uuid = li.getAttribute("data-uuid");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/managers/progs_post/delete_delete/" + uuid + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Пост разблокирован!");
    li.style.display = "none";
  }};
  link_.send();
});

on('#ajax', 'click', '.post_rejected', function() {
  li = this.parentElement.parentElement.parentElement.parentElement;
  uuid = li.getAttribute("data-uuid");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/managers/progs_post/create_rejected/" + uuid + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Жалобы на запись удалены!");
    li.style.display = "none";
  }};

  link_.send();
});
