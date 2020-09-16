on('#ajax', 'click', '.u_ucm_video_repost', function() {
  parent = this.parentElement;
  track_pk = parent.getAttribute("data-pk");
  parent.getAttribute('data-pk') ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/video/repost/u_ucm_video_window/" + pk + "/" + track_pk + "/", loader);
  clear_attach_block();
})
on('#ajax', 'click', '.u_ucm_video_album_repost', function() {
  parent = this.parentElement;
  parent.getAttribute("data-pk") ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  parent.getAttribute("data-uuid") ? uuid = parent.getAttribute('data-uuid') : uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/video/repost/u_ucm_video_album_window/" + pk + "/" + uuid + "/", loader);
  clear_attach_block();
})

on('#video_loader', 'click', '.u_all_video_likes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/video/window/all_user_like/" + uuid + "/", loader)
});
on('#video_loader', 'click', '.u_all_video_dislikes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/video/window/all_user_dislike/" + uuid + "/", loader)
});

on('#video_loader', 'click', '.u_all_video_comment_likes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/video/window/all_user_comment_like/" + pk + "/", loader)
});
on('#video_loader', 'click', '.u_all_video_comment_dislikes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/video/window/all_user_comment_dislike/" + pk + "/", loader)
});

on('#video_loader', 'click', '.u_all_video_reposts', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/video/window/all_user_reposts/" + uuid + "/", loader)
});

on('#video_loader', 'click', '.u_video_comments', function() {
  clear_comment_dropdown();
  video_display = this.parentElement.parentElement.parentElement;
  pk = video_display.getAttribute("data-pk");
  uuid = video_display.getAttribute("data-uuid");
  url = "/video/user_progs/comment/" + uuid + "/" + pk + "/";
  list_load(video_display.nextElementSibling, url);
  this.classList.toggle("comments_open");
});


function get_video_info(pk){
  info_video = document.body.querySelector("#info_video");
  my_playlist = document.body.querySelector("#my_playlist");
  videos = my_playlist.querySelectorAll('.video_playlist_li');
  video_id = video_player.getVideoId();
  uuid = videos[video_id].getAttribute("data-video-uuid");
  if (info_video.innerHTML == "" || info_video.getAttribute("data-uuid") != uuid){
    list_load(info_video, "/video/user/info/" + pk + "/" + uuid + "/");
    info_video.setAttribute("data-uuid", uuid);
    console.log("Воспроизводится ролик № : " + video_id)
  }
}

on('#ajax', 'click', '.u_video_list_detail', function() {
  var uuid, pk, loader;
  counter = this.getAttribute('video-counter') - 1;
  parent = this.parentElement;
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = this.getAttribute('data-pk');
  parent.parentElement.getAttribute("data-uuid") ? uuid = parent.parentElement.getAttribute("data-uuid") : uuid = document.body.querySelector(".pk_saver").getAttribute("data-uuid");
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
    get_video_info(pk)
    }
  }, 500);
});

on('#ajax', 'click', '.u_post_video', function() {
  var uuid, pk, loader;
  parent = this.parentElement;
  counter = this.getAttribute('video-counter') - 1;
  document.body.querySelector(".pk_saver").getAttribute("data-uuid") ? uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid') : uuid = this.getAttribute('data-uuid');
  pk = this.getAttribute("data-pk");
  loader = document.getElementById("video_loader");
  open_fullscreen("/video/user/list_post/" + pk + "/" + uuid + "/", loader);
  video_saver = document.body.querySelector("#video_id_saver");
  video_player_id = video_saver.getAttribute('data-video');
  video_saver.setAttribute('data-video', video_player_id + "a");
  setTimeout(function() {
    load_video_playlist(video_player_id + "a", counter);
    video_player.addListener(FWDUVPlayer.READY, onReady);
    function onReady(){
    console.log("video player ready");
    setTimeout(function() {video_player.playVideo(counter)}, 1000);
    get_video_info(pk)
    }
  }, 500);
});

on('#ajax', 'click', '.u_play_comment_video', function() {
  counter = this.getAttribute('video-counter') - 1;
  comment_pk = this.getAttribute("comment-pk");
  pk = this.getAttribute("data-pk");
  loader = document.getElementById("video_loader");
  open_fullscreen("/video/user/list_post_comment/" + pk + "/" + uuid + "/", loader);
  video_saver = document.body.querySelector("#video_id_saver");
  video_player_id = video_saver.getAttribute('data-video');
  video_saver.setAttribute('data-video', video_player_id + "a");
  setTimeout(function() {
    load_video_playlist(video_player_id + "a", counter);
    video_player.addListener(FWDUVPlayer.READY, onReady);
    function onReady(){
    console.log("video player ready");
    setTimeout(function() {video_player.playVideo(counter)}, 1000);
    get_video_info(pk)
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

on('#ajax', 'click', '.u_video_list_create_window', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  loader = document.getElementById("create_loader");
  open_fullscreen("/video/user/create_list_window/" + pk + "/", loader)
});

on('#ajax', 'click', '.user_video_list_create', function() {
  pk_saver = document.body.querySelector(".pk_saver");
  pk = pk_saver.getAttribute("data-pk");
  uuid = pk_saver.getAttribute("album-uuid");
  loader = document.getElementById("create_loader");
  open_fullscreen("/video/user/create_video_list_window/" + pk + "/" + uuid + "/", loader)
});

on('body', 'click', '#video_holder', function() {
ggg = this;
img = this.previousElementSibling.querySelector("#id_image");
get_image_priview(ggg, img)
});
