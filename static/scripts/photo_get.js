on('#ajax', 'click', '.u_album_photo_detail', function() {
  var container, uuid, uuid2, pk, loader;
  container = this.parentElement;
  uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid');
  uuid2 = container.getAttribute('data-uuid2');
  pk = this.getAttribute('photo-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/load/u_album_photo/" + pk + "/" + uuid + "/" + uuid2 + "/", loader)
});
on('#ajax', 'click', '.u_photo_detail', function() {
  var container, uuid, pk, loader;
  container = this.parentElement;
  uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid');
  pk = this.getAttribute('photo-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/load/u_photo/" + pk + "/" + uuid + "/", loader)
});
on('#ajax', 'click', '.u_photos_add', function() {
  document.querySelector('#photos_add_window').style.display =="none";
})

on('#ajax', 'click', '.u_albums_add', function() {
  var container, uuid, loader;
  container = this.parentElement;
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("create_loader");
  open_fullscreen("/gallery/user/add_album/" + pk + "/", loader)
});

on('#ajax', 'click', '.u_photo_edit', function() {
  document.querySelector('#block_description_form').style.display =="none";
})

on('#ajax', 'click', '#create_video_in_list_btn', function() {
  form = document.querySelector("#create_video_list_form");
  form_data = new FormData(form);

  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else if (!form.querySelector("#id_uri").value){
    form.querySelector("#id_uri").style.border = "1px #FF0000 solid";
    toast_error("Ссылка на видео - обязательное поле!")
  } else if (!form.querySelector("#id_image").value){
    form.querySelector("#video_holder").style.border = "1px #FF0000 solid";
    toast_error("Фотография на обложку обязательна!")
  }
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  uuid = document.body.querySelector(".pk_saver").getAttribute("album-uuid");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/video/progs/create_video_in_list/" + pk + "/" + uuid + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    album = document.body.querySelector("#id_album");
    if (album.value == pk){
      elem_ = document.createElement('div');
      elem_.innerHTML = link_.responseText;
      elem_.classList.add("col-12", "col-md-6", "u_video_list_detail");
      elem_.setAttribute("video-counter", "0");
      elem_.style.cursor = "pointer";
      container = document.body.querySelector(".movies_list_in_list");
      container.prepend(elem_);
      try{container.querySelector(".video_none").style.display = "none"}catch{null};
    }
    document.querySelector(".create_fullscreen").style.display = "none";
    document.getElementById("create_loader").innerHTML="";
    toast_info("Видеоролик создан!")
  }};

  link_.send(form_data);
});

on('#ajax', 'click', '#add_album', function() {
  form = document.body.querySelector("#form_album_add");
  form_data = new FormData(form);
  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { null }
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'POST', "/video/user/add_album/" + pk + "/", true );
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        elem_ = document.createElement('span');
        elem_.innerHTML = ajax_link.responseText;
        ajax = elem_.querySelector("#reload_block");
        rtr = document.getElementById('ajax');
        rtr.innerHTML = ajax.innerHTML;
        uuid = rtr.querySelector(".pk_saver").getAttribute("album-uuid");
        window.scrollTo(0,0);
        document.title = elem_.querySelector('title').innerHTML;
        window.history.pushState(null, "vfgffgfgf", '/gallery/user/album/' + pk + '/' + uuid + '/');
        toast_info("Альбом изображений создан!");
        list_load(block.querySelector("#album_photo_load"), rtr);
      }
    }
    ajax_link.send(form_data);
});
