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


on('#ajax', 'click', '.load_good_list', function() {
  parent = this.parentElement.parentElement.parentElement;
  create_fullscreen("/goods/load_list/" + parent.getAttribute("goodlist-pk") + "/", "item_fullscreen");
});
