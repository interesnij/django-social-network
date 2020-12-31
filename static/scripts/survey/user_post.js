on('#ajax', 'click', '#u_add_survey_btn', function() {
  form_post = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form_post);

  ansvers = form_post.querySelector("#ansvers");
  selectedOptions = ansvers.selectedOptions;
  val = false;
  for (var i = 0; i < selectedOptions.length; i++) {
    if(selectedOptions[i].value) {val = true}
  }
  if (!document.body.querySelector("#id_title").value){
    document.body.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else if (!val){
    form_post.querySelector("#ansvers").style.border = "1px #FF0000 solid";
    toast_error("Напишите варианты ответов!");
    return
  } else {this.disabled = true}
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/goods/user_progs/add/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    _new = document.createElement("div");
    _new.innerHTML = elem;

    if (document.querySelector(".attach_block")){
      check_good_in_block(document.body.querySelector(".attach_block"), _this, pk) ? null : (good_post_attach(document.body.querySelector(".attach_block"), media_block, pk))
    } else if (document.querySector(".message_attach_block")){
      check_good_in_block(document.body.querySelector(".message_attach_block"), _this, pk) ? null : (good_message_attach(document.body.querySelector(".message_attach_block"), media_block, pk))
    }
    else {
        container = document.body.querySelector(".is_paginate");
        container.insertAdjacentHTML('afterBegin', _new.innerHTML);
        container.querySelector(".surveys_empty") ? container.querySelector(".surveys_empty").style.display = "none" : null;
        toast_info("Опрос создан!")
  }
  close_create_window();
  toast_info("Опрос создан!")
  }};
  link_.send(form_data);
});
