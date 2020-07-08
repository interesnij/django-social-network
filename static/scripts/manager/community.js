on('#ajax', 'click', '.community_suspend', function() {
  _this = this;
  if (document.body.querySelector(".pk_saver")){
    this.parentElement.classList.remove("show");
    pk = document.body.querySelector(".pk_saver").getAttribute("community-pk")
  }else if(_this.parentElement.classList.contains("btn_console")){
    li = _this.parentElement.parentElement.parentElement.parentElement;
    pk = li.getAttribute("community-pk");
    list = document.querySelectorAll('.pag');
    for (var i = 0; i < list.length; i++) {
      list[i].classList.remove("changed");
    }
    li.classList.add("changed")
  }
  loader = document.getElementById("worker_loader");
  open_fullscreen("/managers/progs_community/suspend_window/" + pk, loader)
})
on('#ajax', 'click', '.community_blocker', function() {
  _this = this;
  if (document.body.querySelector(".pk_saver")){
    this.parentElement.classList.remove("show");
    pk = document.body.querySelector(".pk_saver").getAttribute("community-pk")
  }else if(_this.parentElement.classList.contains("btn_console")){
    li = _this.parentElement.parentElement.parentElement.parentElement;
    pk = li.getAttribute("community-pk");
    list = document.querySelectorAll('.pag');
    for (var i = 0; i < list.length; i++) {
      list[i].classList.remove("changed");
    }
    li.classList.add("changed")
  }
  loader = document.getElementById("worker_loader");
  open_fullscreen("/managers/progs_community/block_window/" + pk, loader)
})
on('#ajax', 'click', '.community_warning_banner', function() {
  _this = this;
  if (document.body.querySelector(".pk_saver")){
    this.parentElement.classList.remove("show");
    pk = document.body.querySelector(".pk_saver").getAttribute("community-pk")
  }else if(_this.parentElement.classList.contains("btn_console")){
    li = _this.parentElement.parentElement.parentElement.parentElement;
    pk = li.getAttribute("community-pk");
    list = document.querySelectorAll('.pag');
    for (var i = 0; i < list.length; i++) {
      list[i].classList.remove("changed");
    }
    li.classList.add("changed")
  }
  loader = document.getElementById("worker_loader");
  open_fullscreen("/managers/progs_community/warning_banner_window/" + pk, loader)
})

on('#ajax', 'click', '.create_community_suspend_btn', function() {
  form_data = new FormData(document.querySelector("#community_suspend_form"));
  form_post = document.querySelector("#community_suspend_form");
  if (document.body.querySelector(".pk_saver")){
    pk = document.body.querySelector(".pk_saver").getAttribute("community-pk")
  }else if (document.body.querySelector(".changed")){
    li = document.body.querySelector(".changed");
    pk = li.getAttribute("community-pk");
  }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/managers/progs_community/create_suspension/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Сообщество приостановлено!");
    document.querySelector(".worker_fullscreen").style.display = "none";
    document.getElementById("worker_loader").innerHTML="";
    if (document.body.querySelector(".pk_saver")) {
      this_page_reload('/communities/' + pk + '/')
    }else if (li.querySelector(".btn_console")){
      li.remove();
    }
  }};

  link_.send(form_data);
});
on('#ajax', 'click', '.create_community_blocker_btn', function() {
  parent = this.parentElement;
  form_data = new FormData(document.querySelector("#community_blocker_form"));
  form_post = document.querySelector("#community_blocker_form");
  if (document.body.querySelector(".pk_saver")){
    pk = document.body.querySelector(".pk_saver").getAttribute("community-pk")
  }else if (document.body.querySelector(".changed")){
    li = document.body.querySelector(".changed");
    pk = li.getAttribute("community-pk");
  }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/managers/progs_community/create_block/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Сообщество заблокировано!");
    document.querySelector(".worker_fullscreen").style.display = "none";
    document.getElementById("worker_loader").innerHTML="";
    if (document.body.querySelector(".pk_saver")) {
      this_page_reload('/communities/' + pk + '/')
    }else if (li.querySelector(".btn_console")){
      li.remove();
    }
  }};

  link_.send(form_data);
});
on('#ajax', 'click', '.create_community_warning_banner_btn', function() {
  parent = this.parentElement;
  form_data = new FormData(document.querySelector("#community_warning_banner_form"));
  form_post = document.querySelector("#community_warning_banner_form");
  if (document.body.querySelector(".pk_saver")){
    pk = document.body.querySelector(".pk_saver").getAttribute("community-pk")
  }else if (document.body.querySelector(".changed")) {
    li = document.body.querySelector(".changed");
    pk = li.getAttribute("community-pk");
  }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/managers/progs_community/create_warning_banner/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Предупреждающий баннер применен!");
    document.querySelector(".worker_fullscreen").style.display = "none";
    document.getElementById("worker_loader").innerHTML="";
    if (document.body.querySelector(".pk_saver")) {
      this_page_reload('/communities/' + pk + '/')
    }else if (li.querySelector(".btn_console")){
      li.remove();
    }
  }};

  link_.send(form_data);
});

on('#ajax', 'click', '.community_unverify', function() {
  li = this.parentElement.parentElement.parentElement;
  community_pk = li.getAttribute("community-pk");
  obj_pk = li.getAttribute("data-pk");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/managers/progs_community/unverify/" + community_pk + "/" + obj_pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Верификация отменена!");
    li.style.display = "none";
  }};

  link_.send();
});

on('#ajax', 'click', '.remove_community_suspend', function() {
  li = this.parentElement.parentElement.parentElement;
  pk = li.getAttribute("community-pk");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/managers/community_user/delete_suspension/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Приостановка отменена!");
    li.style.display = "none";
  }};

  link_.send();
});
on('#ajax', 'click', '.remove_community_bloсk', function() {
  li = this.parentElement.parentElement.parentElement;
  pk = li.getAttribute("community-pk");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/managers/progs_community/delete_block/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Сообщество разблокировано!");
    li.style.display = "none";
  }};

  link_.send();
});
on('#ajax', 'click', '.remove_community_warning_banner', function() {
  li = this.parentElement.parentElement.parentElement;
  pk = li.getAttribute("community-pk");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/managers/progs_community/delete_warning_banner/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Предупреждающий баннер убран!");
    li.style.display = "none";
  }};

  link_.send();
});

on('#ajax', 'click', '.community_rejected', function() {
  li = this.parentElement.parentElement.parentElement.parentElement;
  pk = li.getAttribute("user-pk");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/managers/progs_community/create_rejected/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Жалобы на сообщество удалены!");
    li.style.display = "none";
  }};

  link_.send();
});
