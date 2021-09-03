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
  loader = document.getElementById("create_loader");
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk')
  open_fullscreen("/music/user_progs/add_list/" + pk + "/", loader)
});

on('#ajax', 'click', '.u_soundcloud_set_create', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen("/music/user_progs/souncloud_create_list_window/", loader)
});

on('#ajax', 'click', '.u_soundcloud_set_list', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen("/music/user_progs/souncloud_list_window/" + this.parentElement.parentElement.getAttribute('data-uuid') + "/", loader)
});
on('#ajax', 'click', '.u_music_list_create_window', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen("/music/user_progs/create_list_window/", loader)
});
on('#ajax', 'click', '.u_playlist_edit', function() {
  uuid = this.parentElement.parentElement.getAttribute('data-uuid');
  loader = document.getElementById("create_loader");
  open_fullscreen("/music/user_progs/edit_list/" + uuid + "/", loader)
});

on('#ajax', 'click', '.load_music_list', function() {
  parent = this.parentElement.parentElement.parentElement;
  loader = document.getElementById("item_loader");
  open_fullscreen("/music/load_list/" + parent.getAttribute("playlist-pk") + "/", loader)
});

on('#ajax', 'click', '.u_ucm_music_repost', function() {
  parent = this.parentElement;
  track_pk = parent.getAttribute("data-pk");
  parent.getAttribute('user-pk') ? pk = parent.getAttribute('user-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/music/repost/u_ucm_music_window/" + pk + "/" + track_pk + "/", loader);
  clear_attach_block();
})
on('#ajax', 'click', '.u_ucm_music_list_repost', function() {
  parent = this.parentElement.parentElement.parentElement;
  parent.getAttribute("data-pk") ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  parent.getAttribute("data-uuid") ? uuid = parent.getAttribute('data-uuid') : uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/music/repost/u_ucm_list_window/" + pk + "/" + uuid + "/", loader);
  clear_attach_block();
})

on('#ajax', 'click', '.u_track_add', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen("/music/user_progs/add_track/", loader)
});
