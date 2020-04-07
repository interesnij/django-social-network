on('#ajax', 'click', '#form_post_btn', function() {
  form_data = new FormData(document.forms.new_post);
  form_post = document.querySelector("#form_post");
  lenta_load = form_post.parentElement.nextElementSibling;
  pk = this.getAttribute("user-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/posts/add_post/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    try{document.querySelector('#id_text').value = "";}catch{console.log("text null")};
    document.querySelector('#for_images_upload').innerHTML = "";
    document.querySelector('#for_gallery').innerHTML = "";
    document.querySelector('#for_doc').innerHTML = "";
    document.querySelector('#for_good').innerHTML = "";
    document.querySelector('#for_question').innerHTML = "";
    document.querySelector('#for_settings').innerHTML = "";

    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    response = new_post.querySelector(".card");
    if (link_.responseText.indexOf("Нужно") != -1){
      error = form_post.querySelector("#user_post_error");
      error.append(link_.responseText);
      //setTimeout(error.innerHTML = "", 4000);
    }else{
      lenta_load.querySelector(".stream").prepend(response)
    }

    lenta_load.querySelector(".post_empty") ? lenta_load.querySelector(".post_empty").style.display = "none" : console.log("post_empty не обнаружен");
  }};

  link_.send(form_data);
});


on('#ajax', 'click', '.u_itemComment', function() {
  form = this.parentElement.parentElement.parentElement;
  form_comment = new FormData(form);
  upload_block = form.querySelector(".upload_block");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', '/user/post-comment/', true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    form.querySelector(".form-control-rounded").value="";
    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    response = new_post.querySelector(".comment");
    form.parentElement.previousElementSibling.append(response)
  }};

  link_.send(form_comment);
});

on('#ajax', 'click', '.u_replyComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  form_comment = new FormData(form);
  upload_block = form.parentElement.querySelector(".upload_block");
  reply_stream = form.parentElement.nextElementSibling.nextElementSibling;

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', '/user/reply-comment/', true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    form.querySelector(".form-control-rounded").value="";
    form.parentElement.style.display = "none";
    upload_block.innerHTML = "";
    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    response = new_post.querySelector(".comment");
    reply_stream.append(response);
    reply_stream.classList.add("replies_open");
  }};

  link_.send(form_comment);
});


on('#ajax', 'click', '.u_replyParentComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  form_comment = new FormData(form);
  upload_block = form.parentElement.querySelector(".upload_block");
  reply_stream = form.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', '/user/reply-comment/', true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    form.querySelector(".form-control-rounded").value="";
    form.parentElement.style.display = "none";
    upload_block.innerHTML = "";
    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    response = new_post.querySelector(".comment");
    reply_stream.append(response);
  }};

  link_.send(form_comment);
});


/*!
   item post scripts for user
  */
on('#ajax', 'click', '.item_user_remove', function() {
  item = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("item-uuid");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/user/delete/" + uuid + "/", true );

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    item.style.display = "none";
    document.querySelector(".item_fullscreen").style.display = "none";
    p = document.createElement("div");
    p.classList.add("card", "mb-4");
    p.style.padding = "20px";
    p.style.display =  "block";

    p.innerHTML = "Запись удалена. <span class='item_user_remove_abort' style='cursor:pointer' data-uuid='" + uuid + "'>Восстановить</span>";
    item.parentElement.insertBefore(p, item);
    item.style.display = "none";
  }};

  link.send( );
});

on('#ajax', 'click', '.item_user_remove_abort', function() {
  item = this.parentElement.nextElementSibling;
  item.style.display = "block";
  uuid = this.getAttribute("data-uuid");
  block = this.parentElement;
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/user/abort_delete/" + uuid + "/", true );

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    block.remove();
  }};

  link.send();
});

on('#ajax', 'click', '.item_user_fixed', function() {
  item = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("item-uuid");
  parent = this.parentElement;
  parent.innerHTML = "";
  response = "<span class='dropdown-item item_user_unfixed'>Открепить</span>";

  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/user/fixed/" + uuid + "/", true );

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {

  }};

  link.send();
  parent.innerHTML = response;
});

on('#ajax', 'click', '.item_user_unfixed', function() {
  item = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("item-uuid");
  parent = this.parentElement;
  response = "<span class='dropdown-item item_user_fixed'>Закрепить</span>";
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/user/unfixed/" + uuid + "/", true );

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    parent.innerHTML = "<span class='dropdown-item item_user_fixed'>Закрепить</span>";
  }};

  link.send();
});
