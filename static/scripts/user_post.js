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

  link__ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link__.open( 'GET', "/user/fixed/" + uuid + "/", true );

  link__.onreadystatechange = function () {
  if ( link__.readyState == 4 && link__.status == 200 ) {
    new_span = document.createElement("span");
    new_span.classList.add("dropdown-item", "item_user_unfixed");
    new_span.innerHTML = "Открепить";
    parent.innerHTML = "";
    parent.append(new_span)
  }};
  link__.send( null );
});

on('#ajax', 'click', '.item_user_unfixed', function() {
  item = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("item-uuid");
  parent = this.parentElement;

  link__ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link__.open( 'GET', "/user/unfixed/" + uuid + "/", true );

  link__.onreadystatechange = function () {
  if ( link__.readyState == 4 && link__.status == 200 ) {
    new_span = document.createElement("span");
    new_span.classList.add("dropdown-item", "item_user_fixed");
    new_span.innerHTML = "Закрепить";
    parent.innerHTML = "";
    parent.append(new_span)
  }};
  link__.send( null );
});


on('#ajax', 'click', '.item_user_off_comment', function() {
  item = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("item-uuid");
  parent = this.parentElement;
  comment_btn = item.querySelector(".u_item_comments");
  comment_block = item.querySelector(".u_load_comments");

  link__ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link__.open( 'GET', "/user/off_comment/" + uuid + "/", true );

  link__.onreadystatechange = function () {
  if ( link__.readyState == 4 && link__.status == 200 ) {
    new_span = document.createElement("span");
    new_span.classList.add("dropdown-item", "item_user_on_comment");
    new_span.innerHTML = "Включить комментарии";
    parent.innerHTML = "";
    parent.append(new_span);
    comment_btn.style.display = "none";
    comment_block.style.display = "none"
  }};
  link__.send( null );
});

on('#ajax', 'click', '.item_user_on_comment', function() {
  item = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("item-uuid");
  parent = this.parentElement;
  comment_btn = item.querySelector(".u_item_comments");
  comment_block = item.querySelector(".u_load_comments");

  link__ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link__.open( 'GET', "/user/on_comment/" + uuid + "/", true );
  link__.onreadystatechange = function () {
  if ( link__.readyState == 4 && link__.status == 200 ) {
    new_span = document.createElement("span");
    new_span.classList.add("dropdown-item", "item_user_off_comment");
    new_span.innerHTML = "Выключить комментарии";
    parent.innerHTML = "";
    parent.append(new_span);
    comment_btn.style.display = "inline-block";
    comment_block.style.display = "block"
  }};
  link__.send( null );
});
$("body").on('click', '.u_like', function() {
  $.ajax({
    url: "/votes/user_like/" + uuid + "/" + pk + "/",
    type: 'POST',
    data: {'obj': pk},
    success: function(json){
      like.find("[data-count='like']").text(json.like_count);
      like.toggleClass('btn_success btn_default');
      like.next().html('').load("/window/u_like_window/" + uuid + "/" + pk + "/");
      dislike.find("[data-count='dislike']").text(json.dislike_count);
      dislike.removeClass('btn_danger').addClass("btn_default");
      dislike.next().html('').load("/window/u_dislike_window/" + uuid + "/" + pk + "/")
}
});
});

on('#ajax', 'click', '.u_like', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("item-uuid");
  pk = item.parentElement.getAttribute("user-pk");
  dislike = this.nextElementSibling.nextElementSibling;
  like_block = this.nextElementSibling;
  dislike_block = this.nextElementSibling.nextElementSibling.nextElementSibling;

  link__ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link__.overrideMimeType("application/json");
  link__.open( 'GET', "/votes/user_like/" + uuid + "/" + pk + "/", true );

  link__.onreadystatechange = function () {
  if ( link__.readyState == 4 && link__.status == 200 ) {
    jsonResponse = JSON.parse(link__.responseText);
    likes_count = item.querySelector(".likes_count");
    dislikes_count = item.querySelector(".dislikes_count");
    likes_count.innerHTML = jsonResponse.like_count;
    dislikes_count.innerHTML = jsonResponse.dislike_count;
    item.querySelector(".u_like").classList.toggle("btn_success", "btn_default");
    item.querySelector(".u_dislike").classList.add("btn_default").remove("btn_danger");

    like_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    like_link.open( 'GET', "/item_window/u_like_window/" + uuid + "/" + pk + "/", true );
    like_link.onreadystatechange = function () {
    if ( like_link.readyState == 4 && like_link.status == 200 ) {
      span_1 = document.createElement("span");
      span_1.innerHTML = like_link.responseText;
      like_block.innerHTML = "";
      like_block.append(span_1);
    }}
    like_link.send( null );

    dislike_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    dislike_link.open( 'GET', "/item_window/u_dislike_window/" + uuid + "/" + pk + "/", true );
    dislike_link.onreadystatechange = function () {
    if ( dislike_link.readyState == 4 && like_link.status == 200 ) {
      span_2 = document.createElement("span");
      span_2.innerHTML = dislike_link.responseText;
      dislike_block.innerHTML = "";
      dislike_block.append(span_2);
    }}
    dislike_link.send( null );

  }};
  link__.send( null );
});
