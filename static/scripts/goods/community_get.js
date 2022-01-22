on('#ajax', 'click', '.copy_community_good_list', function() {
  on_off_list_in_collections(this, "/goods/community_progs/add_list_in_collections/", "uncopy_community_good_list", "copy_community_good_list", "Удалить")
});
on('#ajax', 'click', '.uncopy_community_good_list', function() {
  on_off_list_in_collections(this, "/goods/community_progs/remove_list_from_collections/", "copy_community_good_list", "uncopy_community_good_list", "Добавить")
});

on('#ajax', 'click', '.c_all_good_likes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  good_pk = container.getAttribute('good-pk');
  create_fullscreen("/goods/window/all_community_like/" + pk + "/" + good_pk + "/", "worker_fullscreen");
});
on('#ajax', 'click', '.c_all_good_dislikes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  good_pk = container.getAttribute('good-pk');
  create_fullscreen("/goods/window/all_community_dislike/" + pk + "/" + good_pk + "/", "worker_fullscreen");
});
on('#ajax', 'click', '.c_goods_list_create', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  create_fullscreen("/goods/community_progs/add_list/" + pk + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.c_good_list_add', function() {
  create_fullscreen("/goods/community_progs/add_list/" + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/", "worker_fullscreen");
});
on('#ajax', 'click', '.c_good_list_edit', function() {
  uuid = this.parentElement.parentElement.getAttribute('data-uuid');
  create_fullscreen("/goods/community_progs/edit_list/" + uuid + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.c_ucm_good_repost', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement
  pk = parent.getAttribute('data-pk');
  create_fullscreen("/goods/repost/c_ucm_good_window/" + pk + "/", "worker_fullscreen");
  clear_attach_block();
});
on('#ajax', 'click', '.c_ucm_good_list_repost', function() {
  parent = this.parentElement.parentElement;
  pk = parent.getAttribute('data-pk');
  create_fullscreen("/goods/repost/c_ucm_list_window/" + pk + "/", "worker_fullscreen");
  clear_attach_block();
});

on('#ajax', 'click', '.c_all_good_comment_likes', function() {12
  container = this.parentElement.parentElement.parentElement;
  comment_pk = container.getAttribute('data-pk');
  pk = container.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute('data-pk');
  create_fullscreen("/goods/window/all_community_comment_like/" + pk + "/" + comment_pk + "/", "worker_fullscreen");
});
on('#ajax', 'click', '.c_all_good_comment_dislikes', function() {
  container = this.parentElement.parentElement.parentElement;
  comment_pk = container.getAttribute('data-pk');
  pk = container.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute('data-pk');
  create_fullscreen("/goods/window/all_community_comment_dislike/" + pk + "/" + comment_pk + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.c_all_good_reposts', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  good_pk = container.getAttribute('good-pk');
  create_fullscreen("/goods/window/all_community_reposts/" + good_pk + "/", "worker_fullscreen");
});
