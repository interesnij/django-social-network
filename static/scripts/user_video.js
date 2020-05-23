on('#ajax', 'click', '.user_video_list_create_window', function(e) {
  e.preventDefault();
  pk = this.getAttribute("data-pk");
  loader = document.getElementById("create_loader");
  open_fullscreen("/video/user/create_list_window/" + pk + "/", loader)
});
on('#ajax', 'click', '.user_video_create_window', function(e) {
  e.preventDefault();
  pk = this.getAttribute("data-pk");
  loader = document.getElementById("create_loader");
  open_fullscreen("/video/user/create_video_window/" + pk + "/", loader);
  var list = loader.querySelectorAll('select');
  var count = list.length;
  for(i=0; i<count; i++) {
    list[i].classList.add("form-control")
  }
});

on('#ajax', 'click', '.u_video_detail', function() {
  var uuid, pk, loader;
  counter = this.getAttribute('data-counter');
  parent = this.parentElement.parentElement;
  pk = parent.getAttribute('data-pk');
  loader = document.getElementById("video_loader");
  open_fullscreen("/video/user/basic_list/" + pk + "/", loader);
  video_saver = document.body.querySelector("#video_id_saver");
  video_player_id = video_saver.getAttribute('data-video');
  video_saver.setAttribute('data-video', video_player_id + "a");
  setTimeout(function() {
    load_video_playlist(video_player_id + "a", counter);
    video_player.addListener(FWDUVPlayer.READY, onReady);
    function onReady(){
    console.log("video player ready");
    video_player.addListener(FWDUVPlayer.PLAY, video_onPlay);
    setTimeout(function() {video_player.playVideo(counter);video_player.play()}, 1000);
    }
  }, 500);
});
function video_onPlay(){
    console.log("Воспроизводится ролик № : " + video_player.getVideoId());
    music_player.pause()
  }
on('#ajax', 'click', '.u_video_list_detail', function() {
  var uuid, pk, loader;
  counter = this.getAttribute('data-counter');
  parent = this.parentElement.parentElement;
  pk = parent.getAttribute('data-pk');
  uuid = parent.getAttribute('data-uuid');
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
    setTimeout(function() {video_player.playVideo(counter);video_player.play()}, 1000);
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
  var parent, pk, uuid, loader
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = parent.getAttribute("item-uuid");
  loader = document.getElementById("stat_loader");
  open_fullscreen("/stat/item/" + uuid + "/", loader)
});

on('body', 'click', '#create_video_album_btn', function() {
  _this = this;
  pk = _this.getAttribute("data-pk");
  form_data = new FormData(document.querySelector("#create_video_album"));
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'POST', "/video/progs/create_list/", true );

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    console.log("vse ok")
    }};
  link.send(form_data);
})


on('#ajax', 'click', '#create_video_btn', function() {
  form_data = new FormData(document.querySelector("#create_video_form"));
  pk = this.getAttribute("data-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/video/progs/create_video/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem_ = document.createElement('span');
    elem_.innerHTML = link_.responseText;
    container = document.body.querySelector("#video_playlist");
    row = container.querySelector(".row");
    container.prepend(row);
  }};

  link_.send(form_data);
});

on('#ajax', 'click', '#create_video_list_btn', function() {
  form_data = new FormData(document.querySelector("#video_list_create"));
  pk = this.getAttribute("data-pk");
  uuid = this.getAttribute("data-uuid");
  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'POST', "/video/progs/create_list/" + pk + "/", true );
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        elem_ = document.createElement('span');
        elem_.innerHTML = ajax_link.responseText;
        ajax = elem_.querySelector("#reload_block");
        rtr = document.getElementById('ajax');
        rtr.innerHTML = ajax.innerHTML;
        uuid = rtr.querySelector(".uuid_saver").getAttribute("albom-uuid");
        window.scrollTo(0,0);
        document.title = elem_.querySelector('title').innerHTML;
        Index.initLink();
      }
    }
    ajax_link.send(form_data);
    window.history.pushState({route: '/users/video_list/' + pk + '/' + uuid + '/'}, "network", 'users/video_list/' + pk + '/' + uuid + '/');
});

on('body', 'click', '#video_holder', function() {
entrou = false;
ggg = this;
img = this.previousElementSibling.querySelector("#id_image");
img.click();

img.onchange = function() {
  if (!entrou) {imgPath = img.value;
    extn = imgPath.substring(imgPath.lastIndexOf(".") + 1).toLowerCase();
  if (extn == "gif" || extn == "png" || extn == "jpg" || extn == "jpeg")
  {if (typeof FileReader != "undefined") {
    ggg.innerHTML = "";
    reader = new FileReader();
    reader.onload = function(e) {
      $img = document.createElement("img");
      $img.id = "targetImageCrop";
      $img.src = e.target.result;
      $img.class = "thumb-image";
      ggg.append($img);

      };
      reader.readAsDataURL(img.files[0]);
    }
  } else { this.value = null; }
} entrou = true;
setTimeout(function() { entrou = false; }, 1000);
}});
