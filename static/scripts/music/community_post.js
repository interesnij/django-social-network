on('#ajax', 'click', '#c_ucm_music_repost_btn', function() {
  repost_constructor(this,
                     "/music/repost/c_u_music_repost/",
                     "Репост аудиозаписи на стену сделан",
                     "/music/repost/c_c_music_repost/",
                     "Репост аудиозаписи в сообщества сделан",
                     "/music/repost/c_m_music_repost/",
                     "Репост аудиозаписи в сообщения сделан")
});
on('#ajax', 'click', '#c_ucm_music_list_repost_btn', function() {
  repost_constructor(this,
                     "/music/repost/c_u_music_list_repost/",
                     "Репост плейлиста на стену сделан",
                     "/music/repost/c_c_music_list_repost/",
                     "Репост плейлиста в сообщества сделан",
                     "/music/repost/c_m_music_list_repost/",
                     "Репост плейлиста в сообщения сделан")
});

on('#ajax', 'click', '#c_create_music_list_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }
  post_and_load_object_page(form, "/music/community_progs/add_list/", "/communities/", "/music_list/")
});

on('#ajax', 'click', '.c_add_track_in_list', function() {
  add_item_in_list(this, '/music/community_progs/add_track_in_list/', "c_add_track_in_list", "c_remove_track_from_list")
});
on('#ajax', 'click', '.c_remove_video_from_list', function() {
  remove_item_from_list(this, '/music/community_progs/remove_track_from_list/', "c_remove_track_from_list", "c_add_track_in_list")
});

on('#ajax', 'click', '#c_soundcloud_set_create_btn', function() {
  form = document.body.querySelector("#u_soundcloud_set_create_form");
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!"); return
  } else if (!form.querySelector("#id_permalink").value){
    form.querySelector("#id_permalink").style.border = "1px #FF0000 solid";
    toast_error("Ссылка - обязательное поле!"); return
  } else {this.disabled = true;}
  post_and_load_object_page(form, "/music/community_progs/create_soundcloud_set/", "/communities/", "/music_list/");
  get_document_opacity_1(document.body.querySelector(".main-container"));
});

on('#ajax', 'click', '.c_add_music_list', function(e) {
  _this = this;
  parent = this.parentElement.parentElement.parentElement;
  uuid = parent.getAttribute("data-uuid"); pk = parent.getAttribute("data-pk");
  var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/music/community_progs/add_list/" + pk + "/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
    if ( link.readyState == 4 && link.status == 200 ) {
      _this.innerHTML = "";
      _this.classList.add("c_remove_music_list");
      _this.classList.remove("c_add_music_list")
      _this.innerHTML = '<svg fill="currentColor" class="svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg>'
  }};
  link.send( null );
});
on('#ajax', 'click', '.c_remove_music_list', function(e) {
  _this = this;
  parent = this.parentElement.parentElement.parentElement;
  uuid = parent.getAttribute("data-uuid"); pk = parent.getAttribute("data-pk");
  var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/music/community_progs/remove_list/" + pk + "/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
    if ( link.readyState == 4 && link.status == 200 ) {
      _this.innerHTML = "";
      _this.classList.add("c_add_music_list");
      _this.classList.remove("c_remove_music_list")
      _this.innerHTML = '<svg fill="currentColor" class="svg_default" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg>'
  }};
  link.send( null );
});

on('#ajax', 'click', '#c_soundcloud_set_btn', function() {
  uuid = this.getAttribute("data-uuid");
  form = document.body.querySelector("#c_soundcloud_set_form");
  form_data = new FormData(form);
  if (!form.querySelector("#id_permalink").value){
    form.querySelector("#id_permalink").style.border = "1px #FF0000 solid";
    toast_error("Ссылка - обязательное поле!");
  };

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'POST', "/music/community_progs/soundcloud_set/" + uuid + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        this_page_reload(document.location.href);
      } else {this.disabled = false}
    }
    ajax_link.send(form_data);
})

on('#ajax', 'click', '#c_create_music_list_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }
  post_and_load_object_page(form, "/music/community_progs/add_list/", "/communities/", "/music_list/")
});

on('#ajax', 'click', '#c_edit_playlist_btn', function() {
  media_list_edit(this, "/music/community_progs/edit_list/")
});

on('body', 'click', '.c_playlist_remove', function() {
  media_list_delete(this, "/music/community_progs/delete_list/", "c_playlist_remove", "c_playlist_abort_remove")
});
on('body', 'click', '.c_playlist_abort_remove', function() {
  media_list_recover(this, "/music/community_progs/restore_list/", "c_playlist_abort_remove", "c_playlist_remove")
});

on('body', 'click', '#c_create_track_btn', function() {
  _this = this;
  form = _this.parentElement.parentElement.parentElement;
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
  } else { _this.disabled = true }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/music/community_progs/create_track/", true );
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

on('body', 'click', '#c_edit_track_btn', function() {
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
  link_.open( 'POST', "/music/community_progs/edit_track/" + pk + "/", true );
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

on('body', 'click', '.c_track_remove', function() {
  saver = this.parentElement.parentElement.parentElement;
  pk = saver.getAttribute("data-pk")
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/music/community_progs/delete_track/" + pk + "/", true );
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
on('body', 'click', '.c_track_restore', function() {
  pk = this.getAttribute("data-pk");
  block = this.parentElement; next = block.nextElementSibling;
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/music/community_progs/restore_track/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    block.remove();
    next.style.display = "block";
  }};
  link.send();
});
