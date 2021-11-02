on('#ajax', 'click', '#u_add_survey_btn', function() {
  form_post = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form_post);

  answers = form_post.querySelector("#answers_container");
  selectedOptions = answers.querySelectorAll(".answer");
  val = false;
  for (var i = 0; i < selectedOptions.length; i++) {
    if(selectedOptions[i].value) {val = true}
  }
  if (!document.body.querySelector("#id_title").value){
    document.body.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else if (!val){
    for (var i = 0; i < selectedOptions.length; i++) {selectedOptions[i].style.border = "1px #FF0000 solid"};
    toast_error("Напишите варианты ответов!");
    return
  } else {this.disabled = true}
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/survey/user_progs/add/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    _new = document.createElement("div");
    _new.innerHTML = elem;
    if (document.querySelector(".attach_block")){
      document.body.querySelector(".attach_block").append(_new.querySelector(".load_pag"));
      add_file_attach();
      is_full_attach();
    } else if (document.querySelector(".message_attach_block")){
      document.body.querySelector(".message_attach_block").append(_new.querySelector(".load_pag"));
      add_file_attach();
      is_full_attach();
    }
    else {
        container = document.body.querySelector(".is_paginate");
        container.insertAdjacentHTML('afterBegin', _new.innerHTML);
        container.querySelector(".items_empty") ? container.querySelector(".items_empty").style.display = "none" : null;
  };
  close_work_fullscreen();
  toast_info("Опрос создан!")
  }};
  link_.send(form_data);
});

on('#ajax', 'click', '#u_edit_survey_list_btn', function() {
  media_list_edit(this, "/survey/user_progs/edit_list/", "edited_user_survey_list")
});

on('body', 'click', '.u_survey_list_remove', function() {
  media_list_delete(this, "/survey/user_progs/delete_list/", "u_survey_list_remove", "u_survey_list_abort_remove", "removed_user_survey_list")
});
on('body', 'click', '.u_survey_list_abort_remove', function() {
  media_list_recover(this, "/survey/user_progs/restore_list/", "u_survey_list_abort_remove", "u_survey_list_remove", "restored_user_survey_list")
});
