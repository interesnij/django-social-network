on('#ajax', 'click', '.copy_user_music_list', function() {
  on_off_list_in_collections(this, "/music/user_progs/add_list_in_collections/", "uncopy_user_music_list", "copy_user_music_list", "Удалить")
});
on('#ajax', 'click', '.uncopy_user_music_list', function() {
  on_off_list_in_collections(this, "/music/user_progs/remove_list_from_collections/", "copy_user_music_list", "uncopy_user_music_list", "Добавить")
});

on('#ajax', 'click', '.load_profile_playlist', function() {
  profile_list_block_load(this, ".load_block", "/music_list/", "load_profile_playlist");
});

on('#ajax', 'click', '.load_attach_playlist', function() {
  profile_list_block_attach(this, ".load_block", "/u_music_list_load/", "load_attach_playlist");
});

on('#ajax', 'click', '.load_music_list', function() {
  card = this.parentElement.parentElement.parentElement;
  playlist_pk = card.getAttribute("playlist-pk");
  owner_pk = card.getAttribute("owner-pk");

  create_fullscreen("/music/load_list/" + playlist_pk + "/", "item_fullscreen");
  window.history.pushState(null, "vfgffgfgf", window.location.href + "?key=wall&owner_id=" + owner_pk + "&playlist=" + playlist_pk);
});

on('#ajax', 'click', '.u_track_add', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  create_fullscreen("/music/user_progs/create_track/" + pk + "/", "worker_fullscreen");
});
