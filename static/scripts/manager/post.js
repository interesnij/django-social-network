on('#ajax', 'click', '.post_suspend', function() {
  _this = this;
  if (_this.parentElement.parentElement.parentElement.parentElement.getAttribute){
    uuid = _this.parentElement.parentElement.parentElement.parentElement.getAttribute("data-uuid");
  }else if(_this.parentElement.classList.contains("btn_console")){
    li = _this.parentElement.parentElement.parentElement.parentElement;
    pk = li.getAttribute("user-pk");
    list = document.querySelectorAll('.pag');
    for (var i = 0; i < list.length; i++) {
      list[i].classList.remove("changed");
    }
    li.classList.add("changed")
  }
  loader = document.getElementById("create_loader");
  open_fullscreen("/managers/progs_post/suspend_window/" + uuid, loader)
})
on('#ajax', 'click', '.post_manage_delete', function() {
  _this = this;
  if (_this.parentElement.parentElement.parentElement.parentElement.getAttribute){
    uuid = _this.parentElement.parentElement.parentElement.parentElement.getAttribute("data-uuid");
  }else if(_this.parentElement.classList.contains("btn_console")){
    li = _this.parentElement.parentElement.parentElement.parentElement;
    pk = li.getAttribute("user-pk");
    list = document.querySelectorAll('.pag');
    for (var i = 0; i < list.length; i++) {
      list[i].classList.remove("changed");
    }
    li.classList.add("changed")
  }
  loader = document.getElementById("create_loader");
  open_fullscreen("/managers/progs_post/delete_window/" + uuid, loader)
})

on('#ajax', 'click', '.create_post_suspend_btn', function() {
  form_data = new FormData(document.querySelector("#post_suspend_form"));
  form_post = document.querySelector("#post_suspend_form");
  if (_this.parentElement.parentElement.parentElement.parentElement.getAttribute){
    uuid = _this.parentElement.parentElement.parentElement.parentElement.getAttribute("data-uuid");
  }else if (document.body.querySelector(".changed")){
    li = document.body.querySelector(".changed");
    pk = li.getAttribute("data-uuid");
  }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/managers/progs_post/create_suspension/" + uuid + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Пост заморожен!");
    document.querySelector(".create_fullscreen").style.display = "none";
    document.getElementById("create_loader").innerHTML="";
  //  if (document.body.querySelector(".pk_saver")) {
  //    this_page_reload('/users/' + pk + '/')
  //  }else if (li.querySelector(".btn_console")){
  //    li.remove();
  //  }
  }};
  link_.send(form_data);
});
on('#ajax', 'click', '.create_post_delete_btn', function() {
  parent = this.parentElement;
  form_data = new FormData(document.querySelector("#post_delete_form"));
  form_post = document.querySelector("#post_delete_form");
  if (_this.getAttribute){
    uuid = _this.getAttribute("data-uuid");
  }else if (document.body.querySelector(".changed")){
    li = document.body.querySelector(".changed");
    pk = li.getAttribute("data-uuid");
  }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/managers/progs_post/create_delete/" + uuid + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Пост удален!");
    document.querySelector(".create_fullscreen").style.display = "none";
    document.getElementById("create_loader").innerHTML="";
  //  if (document.body.querySelector(".pk_saver")) {
  //    this_page_reload('/users/' + pk + '/')
  //  }else if (li.querySelector(".btn_console")){
  //    li.remove();
  //  }
  }};

  link_.send(form_data);
});

on('#ajax', 'click', '.post_unverify', function() {
  li = this.parentElement.parentElement.parentElement;
  post_uuid = li.getAttribute("data-uuid");
  obj_pk = li.getAttribute("data-pk");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/managers/progs_post/unverify/" + post_uuid + "/" + obj_pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Верификация отменена!");
    li.style.display = "none";
  }};

  link_.send();
});

on('#ajax', 'click', '.remove_post_suspend', function() {
  li = this.parentElement.parentElement.parentElement;
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
on('#ajax', 'click', '.remove_user_delete', function() {
  li = this.parentElement.parentElement.parentElement;
  uuid = li.getAttribute("data-uuid");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/managers/progs_post/delete_block/" + uuid + "/", true );

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
