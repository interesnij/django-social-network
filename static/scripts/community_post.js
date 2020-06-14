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
  form_data = new FormData(document.forms.new_post);
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
    new_post.querySelector(".card") ? (lenta_load.querySelector("#community_stream").prepend(new_post.querySelector(".card")),
                                       toast_info("Запись опубликована"),
                                       lenta_load.querySelector(".post_empty") ? lenta_load.querySelector(".post_empty").style.display = "none" : null)
                                    :  toast_error("Нужно написать или прикрепить что-нибудь!");
  }};

  link_.send(form_data);
});
