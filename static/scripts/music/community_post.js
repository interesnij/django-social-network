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

on('#ajax', 'click', '.c_add_track_in_list', function() {
  _this = this;
  parent = _this.parentElement;
  uuid = parent.getAttribute("data-uuid");
  pk = _this.parentElement.parentElement.parentElement.parentElement.getAttribute("data-pk");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', '/music/community_progs/c_add_track_in_list/' + pk + "/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    list = parent.querySelector(".c_add_track_in_list");
    list.style.paddingLeft = "14px";
    list.classList.add("c_remove_track_in_list");
    list.classList.remove("c_add_track_in_list");
    span = document.createElement("span");
    span.innerHTML = '<svg fill="currentColor" style="width:15px;height:15px;" class="svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg> ';
    list.prepend(span)
  }};
  link.send( null );
})
on('#ajax', 'click', '.c_remove_track_in_list', function() {
  _this = this;
  parent = _this.parentElement;
  uuid = parent.getAttribute("data-uuid");
  pk = _this.parentElement.parentElement.parentElement.parentElement.getAttribute("data-pk");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', '/music/community_progs/c_remove_track_in_list/' + pk + "/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    list = parent.querySelector(".c_remove_track_in_list");
    list.style.paddingLeft = "30px";
    list.classList.add("c_add_track_in_list");
    list.classList.remove("c_remove_track_in_list");
    list.querySelector("svg").remove();
  }};
  link.send( null );
})

on('#ajax', 'click', '#c_soundcloud_set_create_btn', function() {
  this.disabled = true;
  form = document.body.querySelector("#c_soundcloud_set_create_form");
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else if (!form.querySelector("#id_permalink").value){
    form.querySelector("#id_permalink").style.border = "1px #FF0000 solid";
    toast_error("Ссылка - обязательное поле!");
  } else {this.disabled = true}
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'POST', "/music/community_progs/create_soundcloud_set/" + pk + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        elem_ = document.createElement('span');
        elem_.innerHTML = ajax_link.responseText;
        ajax = elem_.querySelector("#reload_block");
        rtr = document.getElementById('ajax');
        rtr.innerHTML = ajax.innerHTML;
        window.scrollTo(0,0);
        document.title = elem_.querySelector('title').innerHTML;

        uuid = rtr.querySelector(".pk_saver").getAttribute("data-uuid");
        window.history.pushState(null, "vfgffgfgf", '/communities/' + pk + '/music_list/' + uuid + '/');
      }
    }
    ajax_link.send(form_data);
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
      _this.innerHTML = '<svg fill="currentColor" class="svg_default" style="width: 17px;" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg>'
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
      _this.innerHTML = '<svg fill="currentColor" class="svg_default" style="width: 17px;" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg>'
  }};
  link.send( null );
});

on('#ajax', 'click', '#c_soundcloud_set_btn', function() {
  this.disabled = true;
  form = document.body.querySelector("#c_soundcloud_set_form");
  form_data = new FormData(form);
  if (!form.querySelector("#id_permalink").value){
    form.querySelector("#id_permalink").style.border = "1px #FF0000 solid";
    toast_error("Ссылка - обязательное поле!");
  } else {this.disabled = true}
  saver = document.body.querySelector(".pk_saver");
  pk = saver.getAttribute("data-pk");
  uuid = saver.getAttribute("data-uuid");

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'POST', "/music/community_progs/soundcloud_set/" + pk + "/" + uuid + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        close_create_window();
        this_page_reload(document.location.href);
      }
    }
    ajax_link.send(form_data);
})

on('#ajax', 'click', '#с_create_music_list_btn', function() {
  form = document.body.querySelector("#с_music_list_create");
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'POST', "/music/community_progs/create_list/" + pk + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        elem_ = document.createElement('span');
        elem_.innerHTML = ajax_link.responseText;
        ajax = elem_.querySelector("#reload_block");
        rtr = document.getElementById('ajax');
        rtr.innerHTML = ajax.innerHTML;
        window.scrollTo(0,0);
        document.title = elem_.querySelector('title').innerHTML;

        uuid = rtr.querySelector(".pk_saver").getAttribute("data-uuid");
        window.history.pushState(null, "vfgffgfgf", '/communities/' + pk + '/music_list/' + uuid + '/');
      }
    }
    ajax_link.send(form_data);
});

on('#ajax', 'click', '#c_edit_playlist_btn', function() {
  form = document.body.querySelector("#c_edit_playlist_form");
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }

  pk = form.getAttribute("data-pk");
  uuid = form.getAttribute("data-uuid");

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'POST', "/music/community_progs/edit_list/" + pk + "/" + uuid + "/", true );
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

on('#ajax', 'click', '.c_music_list_delete', function() {
  saver = document.querySelector(".pk_saver");
  pk = saver.getAttribute("data-pk");
  uuid = saver.getAttribute("data-uuid");

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', "/music/community_progs/delete_list/" + pk + "/" + uuid + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        this_page_reload("/communities/" + pk + "/music_list/" + uuid + "/")
      }
    }
    ajax_link.send();
});

on('#ajax', 'click', '.c_music_list_recover', function() {
  _this = this;
  saver = document.querySelector(".pk_saver");
  pk = saver.getAttribute("data-pk");
  uuid = saver.getAttribute("data-uuid");

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', "/music/community_progs/abort_delete_list/" + pk + "/" + uuid + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        this_page_reload("/communities/" + pk + "/music_list/" + uuid + "/")
      }
    }
    ajax_link.send();
});
