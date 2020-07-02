on('#ajax', 'click', '.user_suspend', function() {
  this.parentElement.classList.remove("show");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  loader = document.getElementById("create_loader");
  open_fullscreen("/managers/progs_user/suspend_window/" + pk, loader)
})
on('#ajax', 'click', '.user_blocker', function() {
  this.parentElement.classList.remove("show");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  loader = document.getElementById("create_loader");
  open_fullscreen("/managers/progs_user/block_window/" + pk, loader)
})
on('#ajax', 'click', '.user_warning_banner', function() {
  this.parentElement.classList.remove("show");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  loader = document.getElementById("create_loader");
  open_fullscreen("/managers/progs_user/warning_banner_window/" + pk, loader)
})

on('#ajax', 'click', '.create_user_suspend_btn', function() {
  form_data = new FormData(document.querySelector("#user_suspend_form"));
  form_post = document.querySelector("#user_suspend_form");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/managers/progs_user/create_suspension/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Аккаунт приостановлен!");
    document.querySelector(".create_fullscreen").style.display = "none";
    document.getElementById("create_loader").innerHTML="";
  }};

  link_.send(form_data);
});
on('#ajax', 'click', '.create_user_blocker_btn', function() {
  form_data = new FormData(document.querySelector("#user_blocker_form"));
  form_post = document.querySelector("#user_blocker_form");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/managers/progs_user/create_block/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Аккаунт заблокирован!");
    document.querySelector(".create_fullscreen").style.display = "none";
    document.getElementById("create_loader").innerHTML="";
  }};

  link_.send(form_data);
});
on('#ajax', 'click', '.create_user_warning_banner_btn', function() {
  form_data = new FormData(document.querySelector("#user_warning_banner_form"));
  form_post = document.querySelector("#user_warning_banner_form");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/managers/progs_user/create_warning_banner/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Предупреждающий баннер применен!");
    document.querySelector(".create_fullscreen").style.display = "none";
    document.getElementById("create_loader").innerHTML="";
  }};

  link_.send(form_data);
});
