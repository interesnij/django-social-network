
on('#ajax', 'click', '.c_video_add', function() {
  create_fullscreen("/video/community_progs/create_video/", "item_fullscreen");
});
on('#ajax', 'click', '.copy_community_video_list', function() {
  on_off_list_in_collections(this, "/video/community_progs/add_list_in_collections/", "uncopy_community_video_list", "copy_community_video_list", "Удалить")
});
on('#ajax', 'click', '.uncopy_community_video_list', function() {
  on_off_list_in_collections(this, "/video/community_progs/remove_list_from_collections/", "copy_community_video_list", "uncopy_community_video_list", "Добавить")
});
