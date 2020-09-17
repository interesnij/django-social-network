on('#ajax', 'click', '.u_ucm_video_repost', function() {
  parent = this.parentElement;
  track_pk = parent.getAttribute("data-pk");
  parent.getAttribute('data-pk') ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/video/repost/u_ucm_video_window/" + pk + "/" + track_pk + "/", loader);
  clear_attach_block();
})
on('#ajax', 'click', '.u_ucm_video_list_repost', function() {
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

on('#ajax', 'click', '.u_video_list_detail', function() {
  video_pk = this.getAttribute("video-pk");
  counter = this.getAttribute('video-counter') - 1;
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = this.getAttribute('data-pk');
  this.parentElement.parentElement.getAttribute("data-uuid") ? uuid = this.parentElement.parentElement.getAttribute("data-uuid") : uuid = document.body.querySelector(".pk_saver").getAttribute("data-uuid");
  play_video_list("/video/user/list/" + pk + "/" + uuid + "/", counter, pk, video_pk)
});

on('#ajax', 'click', '.u_post_video', function() {
  uuid = this.getAttribute('data-uuid');
  pk = this.getAttribute("data-pk");
  video_pk = this.getAttribute("video-pk");
  counter = this.getAttribute('video-counter') - 1;
  play_video_list("/video/user/list_post/" + pk + "/" + uuid + "/", counter, pk, video_pk)
});

on('#ajax', 'click', '.u_play_comment_video', function() {
  comment_pk = this.getAttribute("comment-pk");
  pk = this.getAttribute("data-pk");
  video_pk = this.getAttribute("video-pk");
  counter = this.getAttribute('video-counter') - 1;
  play_video_list("/video/user/list_post_comment/" + pk + "/" + comment_pk + "/", counter, pk, video_pk);
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
