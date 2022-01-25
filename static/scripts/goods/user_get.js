on('#ajax', 'click', '.copy_user_good_list', function() {
  on_off_list_in_collections(this, "/goods/user_progs/add_list_in_collections/", "uncopy_user_good_list", "copy_user_good_list", "Удалить")
});
on('#ajax', 'click', '.uncopy_user_good_list', function() {
  on_off_list_in_collections(this, "/goods/user_progs/remove_list_from_collections/", "copy_user_good_list", "uncopy_user_good_list", "Добавить")
});

on('#ajax', 'click', '.load_profile_good_list', function() {
  profile_list_block_load(this, ".load_block", "/goods_list/", "load_profile_good_list");
});

on('#ajax', 'click', '.load_attach_good_list', function() {
  profile_list_block_attach(this, ".load_block", "/u_good_list_load/", "load_attach_good_list");
});

on('#ajax', 'click', '.good_detail', function() {
  pk = this.getAttribute('good-pk');
  create_fullscreen('/goods/good/' + pk + '/', "item_fullscreen");
  container = document.body.querySelector("#fullscreens_container");
  loader = container.querySelector(".card_fullscreen");
  setTimeout(function() {good_gallery(loader)}, 1000)
});

on('#ajax', 'click', '.u_ucm_good_repost', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement
  pk = parent.getAttribute("data-pk");
  create_fullscreen("/goods/repost/u_ucm_good_window/" + pk + "/", "worker_fullscreen");
  clear_attach_block();
});
on('#ajax', 'click', '.u_ucm_good_list_repost', function() {
  parent = this.parentElement.parentElement;
  pk = parent.getAttribute('data-pk');
  create_fullscreen("/goods/repost/u_ucm_list_window/" + pk + "/", "worker_fullscreen");
  clear_attach_block();
});

on('#ajax', 'click', '.u_good_list_add', function() {
  create_fullscreen("/goods/user_progs/add_list/" + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/", "worker_fullscreen");
});
on('#ajax', 'click', '.u_good_list_edit', function() {
  pk = this.parentElement.parentElement.getAttribute('data-pk');
  create_fullscreen("/goods/user_progs/edit_list/" + pk + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.u_goods_list_create', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  create_fullscreen("/goods/user_progs/add_list/" + pk + "/", "worker_fullscreen");
});
on('#ajax', 'click', '.u_all_good_likes', function() {
  pk = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute('good-pk');
  create_fullscreen("/goods/window/all_user_like/" + pk + "/", "worker_fullscreen");
});
on('#ajax', 'click', '.u_all_good_dislikes', function() {
  pk = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute('good-pk');
  create_fullscreen("/goods/window/all_user_dislike/" + pk + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.u_all_good_comment_likes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  create_fullscreen("/goods/window/all_user_comment_like/" + pk + "/", "worker_fullscreen");
});
on('#ajax', 'click', '.u_all_good_comment_dislikes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  create_fullscreen("/goods/window/all_user_comment_dislike/" + pk + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.u_all_good_reposts', function() {
  pk = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute('good-pk');
  create_fullscreen("/goods/window/all_user_reposts/" + pk + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.load_good_list', function() {
  parent = this.parentElement.parentElement.parentElement;
  create_fullscreen("/goods/load_list/" + parent.getAttribute("goodlist-pk") + "/", "item_fullscreen");
});
