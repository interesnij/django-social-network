on('#ajax', 'click', '.copy_community_good_list', function() {
  on_off_list_in_collections(this, "/goods/community_progs/add_list_in_collections/", "uncopy_community_good_list", "copy_community_good_list", "Удалить")
});
on('#ajax', 'click', '.uncopy_community_good_list', function() {
  on_off_list_in_collections(this, "/goods/community_progs/remove_list_from_collections/", "copy_community_good_list", "uncopy_community_good_list", "Добавить")
});
