on('#ajax', 'click', '.copy_community_music_list', function() {
  on_off_list_in_collections(this, "/music/community_progs/add_list_in_collections/", "uncopy_community_music_list", "copy_community_music_list", "Удалить")
});
on('#ajax', 'click', '.uncopy_community_music_list', function() {
  on_off_list_in_collections(this, "/music/community_progs/remove_list_from_collections/", "copy_community_music_list", "uncopy_community_music_list", "Добавить")
});

on('#ajax', 'click', '.c_track_add', function() {
  create_fullscreen("/music/community_progs/add_track/", "worker_fullscreen");
});
