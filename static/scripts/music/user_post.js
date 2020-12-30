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

on('#ajax', 'click', '.u_track_add', function(e) {
  block = this.parentElement;
  uuid = document.body.querySelector(".pk_saver").getAttribute("data-uuid");
  var _link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  _link.open( 'GET', "/music/user_progs/u_add_track/" + uuid + "/", true );
  _link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  _link.onreadystatechange = function () {
    if ( _link.readyState == 4 && _link.status == 200 ) {
      block.innerHTML = "";
      block.innerHTML = "<span class='u_track_remove btn_default pointer' title='Удалить'><svg fill='currentColor' style='width:22px;height:22px;' class='svg_default'><path fill='none' d='M0 0h24v24H0z'/><path d='M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z'/></svg></span>"
  }};
  _link.send( null );
});

on('#ajax', 'click', '.u_track_remove', function(e) {
  block = this.parentElement;
  uuid = document.body.querySelector(".pk_saver").getAttribute("data-uuid");
  var _link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  _link.open( 'GET', "/music/user_progs/u_remove_track/" + uuid + "/", true );
  _link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  _link.onreadystatechange = function () {
    if ( _link.readyState == 4 && _link.status == 200 ) {
      block.innerHTML = "";
      block.innerHTML = "<span class='u_track_add btn_default pointer' title='Добавить'><svg fill='currentColor' style='width:22px;height:22px;' class='svg_default'><path d='M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z'/><path d='M0 0h24v24H0z' fill='none'/></svg></span>"
  }};
  _link.send( null );
});

on('#ajax', 'click', '.u_add_track_in_list', function() {
  _this = this;
  parent = _this.parentElement;
  uuid = parent.getAttribute("data-uuid");
  pk = _this.parentElement.parentElement.parentElement.parentElement.getAttribute("data-pk");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', '/music/user_progs/u_add_track_in_list/' + pk + "/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    list = parent.querySelector(".u_add_track_in_list");
    list.style.paddingLeft = "14px";
    list.classList.add("u_remove_track_in_list");
    list.classList.remove("u_add_track_in_list");
    span = document.createElement("span");
    span.innerHTML = '<svg fill="currentColor" style="width:15px;height:15px;" class="svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg> ';
    list.prepend(span)
  }};
  link.send( null );
})
on('#ajax', 'click', '.u_remove_track_in_list', function() {
  _this = this;
  parent = _this.parentElement;
  uuid = parent.getAttribute("data-uuid");
  pk = _this.parentElement.parentElement.parentElement.parentElement.getAttribute("data-pk");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', '/music/user_progs/u_remove_track_in_list/' + pk + "/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    list = parent.querySelector(".u_remove_track_in_list");
    list.style.paddingLeft = "30px";
    list.classList.add("u_add_track_in_list");
    list.classList.remove("u_remove_track_in_list");
    list.querySelector("svg").remove();
  }};
  link.send( null );
})

on('#ajax', 'click', '#u_soundcloud_set_create_btn', function() {
  form = document.body.querySelector("#u_soundcloud_set_create_form");
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!"); return
  } else if (!form.querySelector("#id_permalink").value){
    form.querySelector("#id_permalink").style.border = "1px #FF0000 solid";
    toast_error("Ссылка - обязательное поле!"); return
  } else {this.disabled = true;}
  post_and_load_object_page(form, "/music/user_progs/create_soundcloud_set/", "/users/", "/music_list/")
});

on('#ajax', 'click', '#u_soundcloud_set_btn', function() {
  this.disabled = true;
  form = document.body.querySelector("#u_soundcloud_set_form");
  form_data = new FormData(form);
  if (!form.querySelector("#id_permalink").value){
    form.querySelector("#id_permalink").style.border = "1px #FF0000 solid";
    toast_error("Ссылка - обязательное поле!");
  } else {this.disabled = true}
  saver = document.body.querySelector(".pk_saver");
  uuid = saver.getAttribute("data-uuid");

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'POST', "/music/user_progs/soundcloud_set/" + uuid + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        close_create_window();
        this_page_reload(document.location.href);
      }
    }
    ajax_link.send(form_data);
});

on('#ajax', 'click', '#u_create_music_list_btn', function() {
  this.disabled = true;
  form = document.body.querySelector("#u_music_list_create");
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }
  post_and_load_object_page(form, "/music/user_progs/create_list/", "/users/", "/music_list/")
});


on('#ajax', 'click', '#u_edit_playlist_btn', function() {
  form = document.body.querySelector("#u_edit_playlist_form");
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }
  uuid = form.getAttribute("data-uuid");

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'POST', "/music/user_progs/edit_list/" + uuid + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        name = form.querySelector('#id_name').value;
        document.body.querySelector(".playlist_name").innerHTML = name;
        close_create_window();
        toast_success("Плейлист изменен")
      }
    }
    ajax_link.send(form_data);
});

on('#ajax', 'click', '.u_music_list_delete', function() {
  saver = document.querySelector(".pk_saver");
  pk = saver.getAttribute("data-pk");
  uuid = saver.getAttribute("data-uuid");

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', "/music/user_progs/delete_list/" + uuid + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        this_page_reload("/users/" + pk + "/music_list/" + uuid + "/")
      }
    }
    ajax_link.send();
});

on('#ajax', 'click', '.u_music_list_recover', function() {
  _this = this;
  saver = document.querySelector(".pk_saver");
  pk = saver.getAttribute("data-pk");
  uuid = saver.getAttribute("data-uuid");

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', "/music/user_progs/abort_delete_list/" + uuid + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        this_page_reload("/users/" + pk + "/music_list/" + uuid + "/")
      }
    }
    ajax_link.send();
});
