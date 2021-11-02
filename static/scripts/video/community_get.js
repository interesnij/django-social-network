on('#ajax', 'click', '.c_video_list_add', function() {
  loader = document.getElementById("create_loader");
  create_fullscreen("/video/community_progs/add_list/" + document.body.querySelector(".pk_saver").getAttribute('data-pk') + "/", "worker_fullscreen");
});
on('#ajax', 'click', '.c_video_add', function() {
  create_fullscreen("/video/community_progs/create_video/", "item_fullscreen");
});
on('#ajax', 'click', '.copy_community_video_list', function() {
  on_off_list_in_collections(this, "/video/community_progs/add_list_in_collections/", "uncopy_community_video_list", "copy_community_video_list", "Удалить")
});
on('#ajax', 'click', '.uncopy_community_video_list', function() {
  on_off_list_in_collections(this, "/video/community_progs/remove_list_from_collections/", "copy_community_video_list", "uncopy_community_video_list", "Добавить")
});

on('#ajax', 'click', '.c_ucm_video_list_repost', function() {
  parent = this.parentElement.parentElement.parentElement;
  parent.getAttribute("data-pk") ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  parent.getAttribute("data-uuid") ? uuid = parent.getAttribute('data-uuid') : uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid');
  create_fullscreen("/video/repost/c_ucm_video_list_window/" + pk + "/" + uuid + "/", "worker_fullscreen");
  clear_attach_block();
});
on('#ajax', 'click', '.c_ucm_video_repost', function() {
  parent = this.parentElement;
  track_pk = parent.getAttribute("data-pk");
  parent.getAttribute('data-pk') ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  create_fullscreen("/video/repost/c_ucm_video_window/" + pk + "/" + track_pk + "/", "worker_fullscreen");
  clear_attach_block();
});
on('#ajax', 'click', '.c_ucm_video_list_repost', function() {
  parent = this.parentElement;
  parent.getAttribute("data-pk") ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  parent.getAttribute("data-uuid") ? uuid = parent.getAttribute('data-uuid') : uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid');
  create_fullscreen("/video/repost/c_ucm_video_list_window/" + pk + "/" + uuid + "/", "worker_fullscreen");
  clear_attach_block();
});

on('#ajax', 'click', '.с_video_list_create', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  create_fullscreen("/video/community_progs/add_list/" + pk + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.c_video_list_edit', function() {
  uuid = this.parentElement.parentElement.getAttribute('data-uuid');
  create_fullscreen("/video/community_progs/edit_list/" + uuid + "/", "worker_fullscreen");
});

on('#video_loader', 'click', '.c_all_video_likes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  create_fullscreen("/video/window/all_community_like/" + uuid + "/", "worker_fullscreen");
});
on('#video_loader', 'click', '.c_all_video_dislikes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  create_fullscreen("/video/window/all_community_dislike/" + uuid + "/", "worker_fullscreen");
});

on('#video_loader', 'click', '.c_all_video_comment_likes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  create_fullscreen("/video/window/all_community_comment_like/" + pk + "/", "worker_fullscreen");
});
on('#video_loader', 'click', '.c_all_video_comment_dislikes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  create_fullscreen("/video/window/all_community_comment_dislike/" + pk + "/", "worker_fullscreen");
});

on('#video_loader', 'click', '.c_all_video_reposts', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  create_fullscreen("/video/window/all_community_reposts/" + uuid + "/", "worker_fullscreen");
});
