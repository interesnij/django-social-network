on('#ajax', 'click', '#u_ucm_music_repost_btn', function() {
  repost_constructor(this,
                     "/music/repost/u_u_music_repost/",
                     "Репост аудиозаписи на стену сделан",
                     "/music/repost/u_c_music_repost/",
                     "Репост аудиозаписи в сообщества сделан",
                     "/music/repost/u_m_music_repost/",
                     "Репост аудиозаписи в сообщения сделан")
});
on('#ajax', 'click', '#u_ucm_music_list_repost_btn', function() {
  repost_constructor(this,
                     "/music/repost/u_u_music_list_repost/",
                     "Репост плейлиста на стену сделан",
                     "/music/repost/u_c_music_list_repost/",
                     "Репост плейлиста в сообщества сделан",
                     "/music/repost/u_m_music_list_repost/",
                     "Репост плейлиста в сообщения сделан")
});

on('body', 'click', '.u_track_edit', function() {
  parent = this.parentElement.parentElement.parentElement;
  blocks = document.body.querySelectorAll('.col-sm-12');
  for (var i = 0; i < blocks.length; i++) {blocks[i].classList.remove("edited_track")}

  parent.parentElement.parentElement.parentElement.classList.add("edited_track")
  create_fullscreen("/music/user_progs/edit_track/" + parent.getAttribute("data-pk") +"/", "item_fullscreen");
});

on('body', 'click', '#u_create_track_btn', function() {
  _this = this;
  form = _this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");

  lists = form.querySelector("#id_list");
  selectedOptions = lists.selectedOptions;
  val = false;
  for (var i = 0; i < selectedOptions.length; i++) {
    if(selectedOptions[i].value) {val = true}
  }

  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!")
  } else if (!val){
    form.querySelector("#id_list").style.border = "1px #FF0000 solid";
    toast_error("Выберите список!")
  }
  else if (!form.querySelector("#id_file").value){
    form.querySelector("#id_file").style.border = "1px #FF0000 solid";
    toast_error("Загрузите аудиозапись!")
  } else { _this.disabled = true }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/music/user_progs/create_track/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    document.body.querySelector(".pk_saver").getAttribute("data-uuid") ? (
      uuid = document.body.querySelector(".pk_saver").getAttribute("data-uuid"),
      check_span1(response.querySelector('.span1'), uuid, response.innerHTML),
      document.body.querySelector(".items_empty") ? document.body.querySelector(".items_empty").style.display = "none" : null) : get_preview(response, "track");
    toast_info("Аудиозапись создана!")
    close_work_fullscreen();
  }};

  link_.send(form_data);
});

on('body', 'click', '#u_edit_track_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  pk = form.getAttribute("data-pk");
  form_data = new FormData(form);

  lists = form.querySelector("#id_list");
  selectedOptions = lists.selectedOptions;
  val = false;
  for (var i = 0; i < selectedOptions.length; i++) {
    if(selectedOptions[i].value) {val = true}
  }

  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!")
  } else if (!val){
    form.querySelector("#id_list").style.border = "1px #FF0000 solid";
    toast_error("Выберите список!")
  }
  else if (!form.querySelector("#id_file").value){
    form.querySelector("#id_file").style.border = "1px #FF0000 solid";
    toast_error("Загрузите аудиозапись!")
  } else { this.disabled = true }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/music/user_progs/edit_track/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Аудиозапись изменена!")
    close_work_fullscreen();
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    track = document.body.querySelector(".edited_track");
    track.innerHTML = response.querySelector(".pag").innerHTML;
  }};

  link_.send(form_data);
});

on('body', 'click', '.u_track_remove', function() {
  saver = this.parentElement.parentElement.parentElement;
  pk = saver.getAttribute("data-pk")
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/music/user_progs/delete_track/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    div = document.createElement("div");
    div.classList.add("col-md-6", "col-sm-12");
    div.style.padding = "20px";
    div.style.display =  "block";
    div.innerHTML = "Аудиозапись удалена. <span class='u_track_restore pointer underline' data-pk='" + pk + "'>Восстановить</span>";
    item = saver.parentElement.parentElement.parentElement;
    item.style.display = "none"; item.parentElement.insertBefore(div, item)
  }};
  link.send( );
});
on('body', 'click', '.u_track_restore', function() {
  pk = this.getAttribute("data-pk");
  block = this.parentElement; next = block.nextElementSibling;
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/music/user_progs/restore_track/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    block.remove();
    next.style.display = "block";
  }};
  link.send();
});

on('#ajax', 'click', '.u_add_track_in_list', function() {
  add_item_in_list(this, '/music/user_progs/copy_track_in_list/', "u_add_track_in_list", "u_remove_track_from_list")
});
on('#ajax', 'click', '.u_remove_track_from_list', function() {
  remove_item_from_list(this, '/music/user_progs/uncopy_track_from_list/', "u_remove_track_from_list", "u_add_track_in_list")
});

on('#ajax', 'click', '#u_create_music_list_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }
  post_and_load_object_page(form, "/music/user_progs/add_list/", "/users/", "/music_list/", "added_user_music_list")
});

on('#ajax', 'click', '.u_remove_music_list', function(e) {
  _this = this;
  parent = this.parentElement.parentElement.parentElement;
  uuid = parent.getAttribute("data-uuid");
  var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/music/user_progs/remove_list/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
    if ( link.readyState == 4 && link.status == 200 ) {
      _this.innerHTML = "";
      _this.classList.add("u_add_music_list");
      _this.classList.remove("u_remove_music_list")
      _this.innerHTML = '<svg fill="currentColor" class="svg_default" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg>'
  }};
  link.send( null );
});

on('#ajax', 'click', '#u_edit_playlist_btn', function() {
  media_list_edit(this, "/music/user_progs/edit_list/", "edited_user_music_list")
});

on('body', 'click', '.u_playlist_remove', function() {
  media_list_delete(this, "/music/user_progs/delete_list/", "u_playlist_remove", "u_playlist_abort_remove", "deleted_user_music_list")
});
on('body', 'click', '.u_playlist_abort_remove', function() {
  media_list_recover(this, "/music/user_progs/restore_list/", "u_playlist_abort_remove", "u_playlist_remove", "restored_user_music_list")
});
