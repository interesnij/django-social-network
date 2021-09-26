on('#ajax', 'click', '.c_copy_good_list', function() {
  on_off_list_in_collections(this, "/goods/community_progs/add_list_in_collections/", "c_uncopy_good_list", "c_copy_good_list", "Удалить")
});
on('#ajax', 'click', '.c_uncopy_good_list', function() {
  on_off_list_in_collections(this, "/goods/community_progs/remove_list_from_collections/", "c_copy_good_list", "c_uncopy_good_list", "Добавить")
});

on('#ajax', 'click', '.c_all_good_likes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  good_pk = container.getAttribute('good-pk');
  create_fullscreen("/goods/window/all_community_like/" + pk + "/" + good_pk + "/", "item_fullscreen");
});
on('#ajax', 'click', '.c_all_good_dislikes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  good_pk = container.getAttribute('good-pk');
  create_fullscreen("/goods/window/all_community_dislike/" + pk + "/" + good_pk + "/", "item_fullscreen");
});
on('#ajax', 'click', '.c_goods_list_create', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  create_fullscreen("/goods/community_progs/add_list/" + pk + "/", "item_fullscreen");
});

on('#ajax', 'click', '.c_good_list_add', function() {
  create_fullscreen("/goods/community_progs/add_list/" + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/", "item_fullscreen");
});
on('#ajax', 'click', '.c_good_list_edit', function() {
  uuid = this.parentElement.parentElement.getAttribute('data-uuid');
  create_fullscreen("/goods/community_progs/edit_list/" + uuid + "/", "item_fullscreen");
});

on('#ajax', 'click', '.c_ucm_good_repost', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement
  good_pk = container.getAttribute('good-pk');
  parent.getAttribute('data-pk') ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  create_fullscreen("/goods/repost/c_ucm_good_window/" + pk + "/" + good_pk + "/", "item_fullscreen");
  clear_attach_block();
})
on('#ajax', 'click', '.c_ucm_good_list_repost', function() {
  parent = this.parentElement.parentElement.parentElement;
  parent.getAttribute("data-pk") ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  parent.getAttribute("data-uuid") ? uuid = parent.getAttribute('data-uuid') : uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid');
  create_fullscreen("/goods/repost/c_ucm_list_window/" + pk + "/" + uuid + "/", "item_fullscreen");
  clear_attach_block();
})

on('#ajax', 'click', '.c_good_detail', function() {
  this.getAttribute('data-uuid') ? uuid = this.getAttribute('data-uuid') : uuid = this.parentElement.parentElement.getAttribute('data-uuid')
  pk = this.getAttribute('good-pk');
  create_fullscreen('/goods/community/good/' + pk + '/' + uuid + '/', "item_fullscreen");
  setTimeout(function() {good_gallery(loader)}, 1000)
});
on('#ajax', 'click', '.c_all_good_comment_likes', function() {12
  container = this.parentElement.parentElement.parentElement;
  comment_pk = container.getAttribute('data-pk');
  pk = container.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute('data-pk');
  create_fullscreen("/goods/window/all_community_comment_like/" + pk + "/" + comment_pk + "/", "item_fullscreen");
});
on('#ajax', 'click', '.c_all_good_comment_dislikes', function() {
  container = this.parentElement.parentElement.parentElement;
  comment_pk = container.getAttribute('data-pk');
  pk = container.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute('data-pk');
  create_fullscreen("/goods/window/all_community_comment_dislike/" + pk + "/" + comment_pk + "/", "item_fullscreen");
});

on('#ajax', 'click', '.c_all_good_reposts', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  good_pk = container.getAttribute('good-pk');
  create_fullscreen("/goods/window/all_community_reposts/" + good_pk + "/", "item_fullscreen");
});

on('#ajax', 'click', '.c_good_comments', function() {
  clear_comment_dropdown();
  block = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = block.getAttribute("data-pk");
  good_pk = block.getAttribute("good-pk");
  block_comments = block.querySelector(".c_load_comments");
  if (block_comments.classList.contains("show")){
    block_comments.classList.remove("show")
  } else {
    block_comments.firstChild ? null : list_load(block_comments, "/goods/community/comment/" + uuid + "/" + pk + "/");
    block_comments.classList.add("show")
  }
});
