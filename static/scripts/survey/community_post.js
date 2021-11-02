on('#ajax', 'click', '#c_add_survey_btn', function() {
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
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/survey/community_progs/add/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    _new = document.createElement("div");
    _new.innerHTML = elem;

    if (document.querySelector(".attach_block")){
      check_good_in_block(document.body.querySelector(".attach_block"), _this, pk) ? null : (good_post_attach(document.body.querySelector(".attach_block"), media_block, pk))
    } else if (document.querySelector(".message_attach_block")){
      check_good_in_block(document.body.querySelector(".message_attach_block"), _this, pk) ? null : (good_message_attach(document.body.querySelector(".message_attach_block"), media_block, pk))
    }
    else {
        container = document.body.querySelector(".is_paginate");
        container.insertAdjacentHTML('afterBegin', _new.innerHTML);
        container.querySelector(".items_empty") ? container.querySelector(".items_empty").style.display = "none" : null;
  }
  close_work_fullscreen();
  toast_info("Товар создан!");
  }};
  link_.send(form_data);
});

on('#ajax', 'click', '#c_edit_survey_list_btn', function() {
  media_list_edit(this, "/gallery/community_progs/edit_list/", "edited_community_survey_list")
});

on('body', 'click', '.c_survey_list_remove', function() {
  media_list_delete(this, "/survey/community_progs/delete_list/", "c_survey_list_remove", "c_survey_list_abort_remove", "removed_community_survey_list")
});
on('body', 'click', '.c_survey_list_abort_remove', function() {
  media_list_recover(this, "/survey/community_progs/restore_list/", "c_survey_list_abort_remove", "c_survey_list_remove", "restored_community_survey_list")
});
