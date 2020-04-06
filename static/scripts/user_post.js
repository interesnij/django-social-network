
on('#ajax', 'click', '#form_post_btn', function() {
  var form_post, form_data, lenta_load, pk, link_, elem, new_post;

  form_data = new FormData(document.forms.new_post);
  form_post = document.querySelector("#form_post");
  lenta_load = form_post.parentElement.nextElementSibling;
  pk = lenta_load.querySelector(".stream").getAttribute("user-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/posts/add_post/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    document.querySelector('#id_text').value = "";
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
    if (request.responseText.indexOf("Нужно ввести") != -1){
      error = form_post.querySelector("#user_post_error");
      error.append(response);
      setTimeout(error.innerHTML = "", 4000);
    }else{
      lenta_load.querySelector(".stream").prepend(response)
    }
    lenta_load.querySelector(".stream").prepend(response)
    lenta_load.querySelector(".post_empty") ? lenta_load.querySelector(".post_empty").style.display = "none" : console.log("post_empty не обнаружен");
  }};

  link_.send(form_data);
});


on('#ajax', 'click', '.u_itemComment', function() {
  var form, form_comment, pk, link_, elem, new_post;
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
  var form, form_comment, pk, link_, elem, new_post;
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
  var form, form_comment, pk, link_, elem, new_post;
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
