on('#ajax', 'click', '.user_claim', function() {
  this.parentElement.classList.remove("show");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  create_fullscreen("/managers/progs_user/claim_window/" + pk + "/", "worker_fullscreen");
});
on('#ajax', 'click', '.create_user_claim_btn', function() {
  form_data = new FormData(document.querySelector("#user_claim_form"));
  form_post = document.querySelector("#user_claim_form");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/managers/progs_user/create_claim/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Жалоба отправлена!");
    document.querySelector(".worker_fullscreen").style.display = "none";
    document.getElementById("worker_loader").innerHTML="";
  }};
  link_.send(form_data);
});

on('#ajax', 'click', '.post_claim', function() {
  uuid = this.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute("data-uuid");
  create_fullscreen("/managers/progs_post/claim_window/" + uuid + "/", "worker_fullscreen");
});
on('#ajax', 'click', '.create_post_claim_btn', function() {
  uuid = this.getAttribute("data-uuid");
  form_data = new FormData(document.querySelector("#post_claim_form"));
  form_post = document.querySelector("#post_claim_form");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/managers/progs_post/create_claim/" + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Жалоба отправлена!");
    document.querySelector(".worker_fullscreen").style.display = "none";
    document.getElementById("worker_loader").innerHTML="";
  }};
  link_.send(form_data);
});

on('#ajax', 'click', '.post_comment_claim', function() {
  pk = this.parentElement.parentElement.getAttribute("data-pk");
  create_fullscreen("/managers/progs_post/claim_comment_window/" + pk + "/", "worker_fullscreen");
});
on('#ajax', 'click', '.create_post_comment_claim_btn', function() {
  pk = this.getAttribute("data-pk");
  form_data = new FormData(document.querySelector("#post_comment_claim_form"));
  form_post = document.querySelector("#post_comment_claim_form");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/managers/progs_post/comment_create_claim/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Жалоба отправлена!");
    document.querySelector(".worker_fullscreen").style.display = "none";
    document.getElementById("worker_loader").innerHTML="";
  }};
  link_.send(form_data);
});
