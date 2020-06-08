

on('#ajax', 'click', '#form_post_btn', function() {
  form_data = new FormData(document.forms.new_post);
  form_post = document.querySelector("#form_post");
  lenta_load = form_post.parentElement.nextElementSibling;
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/posts/add_post/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    try{document.querySelector('#id_text').value = "";}catch{ null };

    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    response = new_post.querySelector(".card");
    if (link_.responseText.indexOf("Нужно") != -1){
      error = form_post.querySelector("#user_post_error");
      error.append(link_.responseText);

    }else{
      lenta_load.querySelector(".stream").prepend(response)
    }
    lenta_load.querySelector(".post_empty") ? lenta_load.querySelector(".post_empty").style.display = "none" : null;
  }toast_error("Нужно написать или прикрепить что-нибудь!")};

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
  send_comment(form, form.parentElement.previousElementSibling, '/user/post-comment/');
  toast_success("Комментарий опубликован!")
});

on('#ajax', 'click', '.success_toast', function() {
  toast_success("Комментарий опубликован!")
});
on('#ajax', 'click', '.error_toast', function() {
  toast_error("Комментарий опубликован!")
});
on('#ajax', 'click', '.info_toast', function() {
  toast_info("Комментарий опубликован!")
});
on('#ajax', 'click', '.warning_toast', function() {
  toast_warning("Комментарий опубликован!")
});

on('#ajax', 'click', '.u_replyComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  send_comment(form, form.parentElement.parentElement.querySelector(".stream_reply_comments"), '/user/reply-comment/')
  form.parentElement.style.display = "none";
});

on('#ajax', 'click', '.u_replyParentComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  send_comment(form, form.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement, '/user/reply-comment/')
  form.parentElement.style.display = "none";
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


function send_change(span, _link, new_class, html){
  parent = span.parentElement;
  item = span.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("item-uuid");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', _link + uuid + "/", true );
  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    new_span = document.createElement("span");
    new_span.classList.add(new_class, "dropdown-item");
    new_span.innerHTML = html;
    parent.innerHTML = "";
    parent.append(new_span);
  }};
  link.send( null );
}

on('#ajax', 'click', '.item_user_fixed', function() {
  send_change(this, "/user/fixed/", "item_user_unfixed", "Открепить")
})
on('#ajax', 'click', '.item_user_unfixed', function() {
  send_change(this, "/user/unfixed/", "item_user_fixed", "Закрепить")
})

on('#ajax', 'click', '.item_user_off_comment', function() {
  send_change(this, "/user/off_comment/", "item_user_on_comment", "Включить комментарии")
})
on('#ajax', 'click', '.item_user_on_comment', function() {
  send_change(this, "/user/on_comment/", "item_user_off_comment", "Выключить комментарии")
})

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

on('#ajax', 'click', '#holder_article_image', function() {
  img = this.previousElementSibling.querySelector("#id_g_image")
  get_image_priview(this, img);
});
