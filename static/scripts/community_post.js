on('#ajax', 'click', '.user_community_create_window', function(e) {
  e.preventDefault();
  pk = this.getAttribute("data-pk");
  loader = document.getElementById("create_loader");
  open_fullscreen("/communities/progs/create_community_window/" + pk + "/", loader)
});

on('#ajax', 'click', '#add_community_btn', function() {
  form = document.querySelector("#add_community_form");
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else if (!form.querySelector("#sub_category").value){
    form.querySelector("#sub_category").style.border = "1px #FF0000 solid";
    toast_error("Тематика - обязательное поле!")
  } else {toast_info("Сообщество создано!")};
  create_reload_page(form, "/communities/progs/add/", '/communities/')
});

on('#ajax', 'change', '#sub_category', function() {
  var val = this.value;
  if (val == '') {
    document.getElementById('subcat').innerHTML = "";
  } else {
    var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    link.open( 'GET', "/communities/progs/cat/" + val + "/", true );
    link.onreadystatechange = function () {
      if ( link.readyState == 4 ) {
          if ( link.status == 200 ) {
              var sub = document.getElementById("subcat");
              sub.innerHTML = link.responseText;
          }
      }
  };
  link.send( null );
  };
});


on('#ajax', 'click', '#c_add_post', function() {
  form_data = new FormData(document.forms.new_community_post);
  form_post = document.querySelector("#commnity_post");
  lenta_load = form_post.parentElement.nextElementSibling;
  pk = document.body.querySelector(".pk_saver").getAttribute("community-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/posts/add_post_community/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    form_post.querySelector('.id_text').value = "";
    clear_attach_block();

    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    new_post.querySelector(".card") ? (lenta_load.querySelector("#community_stream").prepend(new_post),
                                       toast_info("Запись опубликована"),
                                       lenta_load.querySelector(".post_empty") ? lenta_load.querySelector(".post_empty").style.display = "none" : null)
                                    :  toast_error("Нужно написать или прикрепить что-нибудь!");
  }};

  link_.send(form_data);
});

on('#ajax', 'click', '.c_itemComment', function() {
  form = this.parentElement.parentElement.parentElement;
  send_comment(form, form.parentElement.previousElementSibling, '/posts/community/post-comment/');
});

on('#ajax', 'click', '.c_replyItemComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  send_comment(form, form.parentElement.parentElement.querySelector(".stream_reply_comments"), '/posts/community/reply-comment/')
  form.parentElement.style.display = "none";
});

on('#ajax', 'click', '.c_replyParentItemComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  send_comment(form, form.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement, '/posts/community/reply-comment/')
  form.parentElement.style.display = "none";
});

on('#ajax', 'click', '.c_like', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("item-uuid");
  pk = document.body.querySelector(".pk_saver").getAttribute("community-pk");
  send_like(item, "/posts/votes/community_like/" + uuid + "/" + pk + "/");
  vote_reload("/posts/item_window/c_like_window/" + uuid + "/", "/posts/item_window/u_dislike_window/" + uuid + "/", this.nextElementSibling, this.nextElementSibling.nextElementSibling.nextElementSibling)
});
on('#ajax', 'click', '.c_dislike', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  uuid = item.getAttribute("item-uuid");
  pk = document.body.querySelector(".pk_saver").getAttribute("community-pk");
  send_dislike(item, "/posts/votes/community_dislike/" + uuid + "/" + pk + "/");
  vote_reload("/posts/item_window/c_like_window/" + uuid + "/", "/posts/item_window/u_dislike_window/" + uuid + "/", this.previousElementSibling, this.nextElementSibling)
});
on('#ajax', 'click', '.c_like2', function() {
  _this = this;
  item = _this.parentElement;
  comment_pk = item.getAttribute("data-pk");
  pk = document.body.querySelector(".pk_saver").getAttribute("community-pk");
  send_like(item, "/posts/votes/community_comment/" + comment_pk + "/" + pk + "/like/");
  vote_reload("/posts/item_window/c_comment_like_window/" + comment_pk + "/", "/posts/item_window/u_comment_dislike_window/" + comment_pk + "/", _this.nextElementSibling, _this.nextElementSibling.nextElementSibling.nextElementSibling)
});
on('#ajax', 'click', '.c_dislike2', function() {
  _this = this;
  item = _this.parentElement;
  comment_pk = item.getAttribute("data-pk");
  pk = document.body.querySelector(".pk_saver").getAttribute("community-pk");
  send_dislike(item, "/posts/votes/community_comment/" + comment_pk + "/" + pk + "/dislike/");
  vote_reload("/posts/item_window/c_comment_like_window/" + comment_pk + "/", "/posts/item_window/u_comment_dislike_window/" + comment_pk + "/", _this.previousElementSibling, _this.nextElementSibling)
});

on('body', 'click', '#community_avatar_btn', function(event) {
  this.previousElementSibling.click();
})
on('#ajax', 'change', '#community_avatar_upload', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("community-pk");
  form_data = new FormData(document.body.querySelector("#add_community_avatar"));
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/community/add_avatar/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    document.body.querySelector(".avatar_figure").innerHTML = "";
    img = response.querySelector("img");
    document.body.querySelector(".avatar_figure").append(img);
    }
  }
  link_.send(form_data);
})
