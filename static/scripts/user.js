
on('#ajax', 'click', '.color_change', function() {
  var span = this;
  var color = this.getAttribute('data-color');
  var input = span.querySelector(".custom-control-input");
  var list = document.querySelector(".theme-color");
  var link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/users/progs/color/" + color + "/", true );
  link_.send();
  link_.onreadystatechange = function () {
  if ( link_.readyState == 4 && link_.status == 200 ) {
    var uncheck=document.getElementsByTagName('input');
    for(var i=0;i<uncheck.length;i++)
    {uncheck[i].checked=false;}
    input.checked = true;
    addStyleSheets("/static/styles/color/" + color + ".css");
  }
};
});

on('#ajax', 'click', '#holder_article_image', function() {
  img = this.previousElementSibling.querySelector("#id_g_image")
  get_image_priview(this, img);
});

on('#ajax', 'click', '.user_claim', function() {
  this.parentElement.classList.remove("show");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  loader = document.getElementById("create_loader");
  open_fullscreen("/managers/progs_user/claim_window/" + pk, loader)
})
on('#ajax', 'click', '.create_user_claim_btn', function() {
  form_data = new FormData(document.querySelector("#user_claim_form"));
  form_post = document.querySelector("#user_claim_form");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/managers/progs_user/create_claim/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Жалоба отправлена!");
    document.querySelector(".create_fullscreen").style.display = "none";
    document.getElementById("create_loader").innerHTML="";
  }};
  link_.send(form_data);
});

on('#ajax', 'click', '.post_claim', function() {
  this.parentElement.classList.remove("show");
  uuid = _this.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute("data-uuid");
  loader = document.getElementById("create_loader");
  open_fullscreen("/managers/progs_post/claim_window/" + uuid, loader)
})
on('#ajax', 'click', '.create_post_claim_btn', function() {
  form_data = new FormData(document.querySelector("#post_claim_form"));
  form_post = document.querySelector("#post_claim_form");
  uuid = _this.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute("data-uuid");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/managers/progs_post/create_claim/" + uuid + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Жалоба отправлена!");
    document.querySelector(".create_fullscreen").style.display = "none";
    document.getElementById("create_loader").innerHTML="";
  }};
  link_.send(form_data);
});
