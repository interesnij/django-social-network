on('#ajax', 'click', '.u_copy_playlist', function() {
  on_off_list_in_collections(this, "/music/user_progs/add_list_in_collections/", "u_uncopy_playlist", "u_copy_playlist", "Удалить")
});
on('#ajax', 'click', '.u_uncopy_playlist', function() {
  on_off_list_in_collections(this, "/music/user_progs/remove_list_from_collections/", "u_copy_playlist", "u_uncopy_playlist", "Добавить")
});

on('#ajax', 'click', '.load_profile_playlist', function() {
  profile_list_block_load(this, ".load_block", "/music_list/", "load_profile_playlist");
});

on('#ajax', 'click', '.load_attach_playlist', function() {
  profile_list_block_attach(this, ".load_block", "/u_music_list_load/", "load_attach_playlist");
});

on('#ajax', 'click', '.u_playlist_add', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk')
  create_fullscreen("/music/user_progs/add_list/" + pk + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.u_soundcloud_set_create', function() {
  create_fullscreen("/music/user_progs/souncloud_create_list_window/", "worker_fullscreen");
});

on('#ajax', 'click', '.u_soundcloud_set_list', function() {
  create_fullscreen("/music/user_progs/souncloud_list_window/" + this.parentElement.parentElement.getAttribute('data-uuid') + "/", "worker_fullscreen");
});
on('#ajax', 'click', '.u_music_list_create_window', function() {
  create_fullscreen("/music/user_progs/create_list_window/", "worker_fullscreen");
});
on('#ajax', 'click', '.u_playlist_edit', function() {
  uuid = this.parentElement.parentElement.getAttribute('data-uuid');
  create_fullscreen("/music/user_progs/edit_list/" + uuid + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.load_music_list', function() {
  card = this.parentElement.parentElement.parentElement;
  playlist_pk = card.getAttribute("playlist-pk");
  owner_pk = card.getAttribute("owner-pk");

  create_fullscreen("/music/load_list/" + playlist_pk + "/", "item_fullscreen");
  window.history.pushState(null, "vfgffgfgf", window.location.href + "?key=wall&owner_id=" + owner_pk + "&playlist=" + playlist_pk);
});

on('#ajax', 'click', '.u_ucm_music_repost', function() {
  parent = this.parentElement;
  track_pk = parent.getAttribute("data-pk");
  parent.getAttribute('user-pk') ? pk = parent.getAttribute('user-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  create_fullscreen("/music/repost/u_ucm_music_window/" + pk + "/" + track_pk + "/", "worker_fullscreen");
  clear_attach_block();
});
on('#ajax', 'click', '.u_ucm_music_list_repost', function() {
  parent = this.parentElement.parentElement.parentElement;
  parent.getAttribute("data-pk") ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  parent.getAttribute("data-uuid") ? uuid = parent.getAttribute('data-uuid') : uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid');
  create_fullscreen("/music/repost/u_ucm_list_window/" + pk + "/" + uuid + "/", "worker_fullscreen");
  clear_attach_block();
});

on('#ajax', 'click', '.u_track_add', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  create_fullscreen("/music/user_progs/create_track/" + pk + "/", "worker_fullscreen");
});
