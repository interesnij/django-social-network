on('#ajax', 'click', '.c_ucm_video_repost', function() {
  parent = this.parentElement;
  track_pk = parent.getAttribute("data-pk");
  parent.getAttribute('data-pk') ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/video/repost/c_ucm_video_window/" + pk + "/" + track_pk + "/", loader);
  clear_attach_block();
})
on('#ajax', 'click', '.c_ucm_video_list_repost', function() {
  parent = this.parentElement;
  parent.getAttribute("data-pk") ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  parent.getAttribute("data-uuid") ? uuid = parent.getAttribute('data-uuid') : uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/video/repost/c_ucm_video_album_window/" + pk + "/" + uuid + "/", loader);
  clear_attach_block();
})

on('#ajax', 'click', '.с_video_list_create_window', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  loader = document.getElementById("create_loader");
  open_fullscreen("/video/community_progs/create_list/" + pk + "/", loader)
});

on('#ajax', 'click', '.c_video_list_edit_window', function() {
  body = document.body.querySelector(".pk_saver");
  pk = body.getAttribute("data-pk");
  uuid = body.getAttribute("data-uuid");
  loader = document.getElementById("create_loader");
  open_fullscreen("/video/community_progs/edit_list/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.c_video_list_create_window', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  loader = document.getElementById("create_loader");
  open_fullscreen("/video/community/create_list_window/" + pk + "/", loader)
});

on('#video_loader', 'click', '.c_all_video_likes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/video/window/all_community_like/" + uuid + "/", loader)
});
on('#video_loader', 'click', '.c_all_video_dislikes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/video/window/all_community_dislike/" + uuid + "/", loader)
});

on('#video_loader', 'click', '.c_all_video_comment_likes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/video/window/all_community_comment_like/" + pk + "/", loader)
});
on('#video_loader', 'click', '.c_all_video_comment_dislikes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/video/window/all_community_comment_dislike/" + pk + "/", loader)
});

on('#video_loader', 'click', '.c_all_video_reposts', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/video/window/all_community_reposts/" + uuid + "/", loader)
});

on('#video_loader', 'click', '.c_video_comments', function() {
  clear_comment_dropdown();
  video_display = this.parentElement.parentElement.parentElement;
  pk = video_display.getAttribute("data-pk");
  uuid = video_display.getAttribute("data-uuid");
  url = "/video/community_progs/comment/" + uuid + "/" + pk + "/";
  list_load(data.querySelector(".c_load_comments"), url);
  this.classList.toggle("comments_open");
});
