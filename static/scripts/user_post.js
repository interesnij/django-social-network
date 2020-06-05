on('#ajax', 'change', '#photo_add_attach', function() {
   files = this.files;
   for(var a=0;a<files.length;a++)
   if (parseInt(files.length)>2){
      alert("You can only upload a maximum of 2 files");
    }
alert(files[a]);
});

on('#ajax', 'click', '#form_post_btn', function() {
  form_data = new FormData(document.forms.new_post);
  form_post = document.querySelector("#form_post");
  lenta_load = form_post.parentElement.nextElementSibling;
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");

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

on('#ajax', 'click', '#article_post', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  form_data = new FormData(document.forms.new_post);
  form_post = document.querySelector("#user_article_form");
  CKEDITOR.instances.id_content.updateElement();
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/article/add_user/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    response = new_post.querySelector(".card");
    document.querySelector(".stream").prepend(response)
    document.querySelector(".post_empty") ? lenta_load.querySelector(".post_empty").style.display = "none" : null;
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
    form.parentElement.previousElementSibling.append(response);
    form.querySelector(".img_block").innerHTML = "";
    form_dropdown = form.querySelector(".current_file_dropdown");
    form_dropdown.classList.remove("current_file_dropdown");
    form_dropdown.parentElement.parentElement.classList.remove("files_one", "files_two");
    form_dropdown.parentElement.parentElement.classList.add("files_null")
  }};

  link_.send(form_comment);
});

on('#ajax', 'click', '#holder_article_image', function() {
  img = this.previousElementSibling.querySelector("#id_g_image")
  get_image_priview(this, img);

});
on('#ajax', 'click', '.comment_photo1', function() {
  img = this.querySelector("#id_item_comment_photo");
  get_image_priview(this.querySelector("#photo"), img);
  is_full_dropdown();
});
on('#ajax', 'click', '.comment_photo2', function() {
  img = this.querySelector("#id_item_comment_photo2");
  get_image_priview(this.querySelector("#photo2"), img);
  is_full_dropdown();
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
    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    response = new_post.querySelector(".comment");
    reply_stream.append(response);
    reply_stream.classList.add("replies_open");

    form.querySelector(".img_block").innerHTML = "";
    form_dropdown = form.querySelector(".current_file_dropdown");
    form_dropdown.classList.remove("current_file_dropdown");
    form_dropdown.parentElement.parentElement.classList.remove("files_one", "files_two");
    form_dropdown.parentElement.parentElement.classList.add("files_null")
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
    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    response = new_post.querySelector(".comment");
    reply_stream.append(response);

    form.querySelector(".img_block").innerHTML = "";
    form_dropdown = form.querySelector(".current_file_dropdown");
    form_dropdown.classList.remove("current_file_dropdown");
    form_dropdown.parentElement.parentElement.classList.remove("files_one", "files_two");
    form_dropdown.parentElement.parentElement.classList.add("files_null")
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

on('#ajax', 'click', '.u_like', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("item-uuid");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_like(item, "/votes/user_like/" + uuid + "/" + pk + "/");
  vote_reload("/item_window/u_like_window/" + uuid + "/" + pk + "/", "/item_window/u_dislike_window/" + uuid + "/" + pk + "/", this.nextElementSibling, this.nextElementSibling.nextElementSibling.nextElementSibling)
});
on('#ajax', 'click', '.u_dislike', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("item-uuid");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_dislike(item, "/votes/user_dislike/" + uuid + "/" + pk + "/");
  vote_reload("/item_window/u_like_window/" + uuid + "/" + pk + "/", "/item_window/u_dislike_window/" + uuid + "/" + pk + "/", this.previousElementSibling, this.nextElementSibling)
});
on('#ajax', 'click', '.u_like2', function() {
  _this = this;
  item = _this.parentElement;
  comment_pk = item.getAttribute("data-pk");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_like(item, "/votes/user_comment/" + comment_pk + "/" + pk + "/like/");
  vote_reload("/item_window/u_comment_like_window/" + comment_pk + "/" + pk + "/", "/item_window/u_comment_dislike_window/" + comment_pk + "/" + pk + "/", _this.nextElementSibling, _this.nextElementSibling.nextElementSibling.nextElementSibling)
});
on('#ajax', 'click', '.u_dislike2', function() {
  _this = this;
  item = _this.parentElement;
  comment_pk = item.getAttribute("data-pk");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_dislike(item, "/votes/user_comment/" + comment_pk + "/" + pk + "/dislike/");
  vote_reload("/item_window/u_comment_like_window/" + comment_pk + "/" + pk + "/", "/item_window/u_comment_dislike_window/" + comment_pk + "/" + pk + "/", _this.previousElementSibling, _this.nextElementSibling)
});


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
