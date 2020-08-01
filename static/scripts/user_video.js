

on('#ajax', 'click', '.user_video_list_create_window', function(e) {
  e.preventDefault();
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  loader = document.getElementById("create_loader");
  open_fullscreen("/video/user/create_list_window/" + pk + "/", loader)
});
on('#ajax', 'click', '.user_video_create_window', function(e) {
  e.preventDefault();
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  loader = document.getElementById("create_loader");
  open_fullscreen("/video/user/create_video_window/" + pk + "/", loader);
  var list = loader.querySelectorAll('select');
  var count = list.length;
  for(i=0; i<count; i++) {
    list[i].classList.add("form-control")
  }
});

on('#ajax', 'click', '.user_video_create_attach', function(e) {
  e.preventDefault();
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  loader = document.getElementById("create_loader");
  open_fullscreen("/video/user/create_video_attach_window/" + pk + "/", loader);
  var list = loader.querySelectorAll('select');
  var count = list.length;
  for(i=0; i<count; i++) {
    list[i].classList.add("form-control")
  }
});


function get_video_info(){
  info_video = document.body.querySelector("#info_video");
  my_playlist = document.body.querySelector("#my_playlist");
  videos = my_playlist.querySelectorAll('.video_playlist_li');
  video_id = video_player.getVideoId();
  uuid = videos[video_id].getAttribute("data-video-uuid");
  if (info_video.innerHTML == "" || info_video.getAttribute("data-uuid") != uuid){
    pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
    list_load(info_video, "/video/user/detail/" + pk + "/" + uuid + "/");
    info_video.setAttribute("data-uuid", uuid);
    console.log("Воспроизводится ролик № : " + video_id)
  }
}

function video_onPlay(){
    get_video_info()
    music_player.pause();

  }
on('#ajax', 'click', '.u_video_list_detail', function() {
  var uuid, pk, loader;
  counter = this.getAttribute('video-counter');
  parent = this.parentElement;
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  uuid = document.body.querySelector(".pk_saver").getAttribute("album-uuid");
  loader = document.getElementById("video_loader");
  open_fullscreen("/video/user/list/" + pk + "/" + uuid + "/", loader);
  video_saver = document.body.querySelector("#video_id_saver");
  video_player_id = video_saver.getAttribute('data-video');
  video_saver.setAttribute('data-video', video_player_id + "a");
  setTimeout(function() {
    load_video_playlist(video_player_id + "a", counter);
    video_player.addListener(FWDUVPlayer.READY, onReady);
    function onReady(){
    console.log("video player ready");
    setTimeout(function() {video_player.playVideo(counter)}, 1000);
    get_video_info()
    }
  }, 500);
});

on('body', 'click', '.video_fullscreen_resize', function() {
  video_window = document.querySelector(".video_fullscreen");
  video_window.classList.add("video_fullscreen_resized", "draggable");
  document.body.querySelector(".video_btn_big").style.display = "none";
  document.body.querySelector(".video_btn_small").style.display = "block";
  get_resize_screen();
  dragElement(document.querySelector(".draggable"));

});
on('body', 'click', '.video_fullscreen_normal', function() {
  video_window = document.querySelector(".video_fullscreen");
  video_window.style.top = "0"; video_window.style.left = "auto";
  video_window.classList.remove("video_fullscreen_resized", "draggable");
  document.body.querySelector(".video_btn_small").style.display = "none";
  document.body.querySelector(".video_btn_big").style.display = "block";
  get_normal_screen()
});

on('#ajax', 'click', '.user_video_list_create', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  uuid = document.body.querySelector(".pk_saver").getAttribute("album-uuid");
  loader = document.getElementById("create_loader");
  open_fullscreen("/video/user/create_video_list_window/" + pk + "/" + uuid + "/", loader)
});

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
  link_.open( 'POST', "/video/user_progs/create_video_in_list/" + pk + "/" + uuid + "/", true );

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

on('#ajax', 'click', '#create_video_list_btn', function() {
  form = document.body.querySelector("#video_list_create");
  form_data = new FormData(form);
  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { null }
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'POST', "/video/progs/create_list/" + pk + "/", true );
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        elem_ = document.createElement('span');
        elem_.innerHTML = ajax_link.responseText;
        ajax = elem_.querySelector("#reload_block");
        rtr = document.getElementById('ajax');
        rtr.innerHTML = ajax.innerHTML;
        window.scrollTo(0,0);
        document.title = elem_.querySelector('title').innerHTML;

        uuid = rtr.querySelector(".pk_saver").getAttribute("album-uuid");
        window.history.pushState(null, "vfgffgfgf", '/users/' + pk + '/video/' + uuid + '/');
        toast_info("Список видео создан!")
      }
    }
    ajax_link.send(form_data);
});

on('body', 'click', '#video_holder', function() {
ggg = this;
img = this.previousElementSibling.querySelector("#id_image");
get_image_priview(ggg, img)
});
