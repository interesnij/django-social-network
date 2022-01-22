on('#ajax', 'click', '.c_photo_priview', function() {
  pk = this.getAttribute('photo-pk');
  create_fullscreen("/gallery/community/preview_photo/" + pk + "/", "photo_fullscreen");
});

on('#ajax', 'click', '.c_ucm_photo_repost', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement
  pk = parent.getAttribute("data-pk");
  create_fullscreen("/gallery/repost/c_ucm_photo_window/" + pk + "/", "worker_fullscreen");
  clear_attach_block();
});
on('#ajax', 'click', '.c_ucm_photo_list_repost', function() {
  parent = this.parentElement.parentElement.parentElement;
  parent.getAttribute('data-pk') ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk')
  item_id = parent.getAttribute('owner-pk');
  create_fullscreen("/gallery/repost/c_ucm_list_window/" + pk + "/" + item_id + "/", "worker_fullscreen");
  clear_attach_block();
});

on('#ajax', 'click', '.c_photos_add', function() {
  document.querySelector('#photos_add_window').style.display =="none";
});

on('#ajax', 'click', '.c_photo_list_add', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  create_fullscreen("/gallery/community_progs/add_list/" + pk + "/", "worker_fullscreen");
});
on('#ajax', 'click', '.c_photo_list_edit', function() {
  pk = this.parentElement.parentElement.getAttribute('data-pk');
  create_fullscreen("/gallery/community_progs/edit_list/" + pk + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.c_photo_edit', function() {
  document.querySelector('#block_description_form').style.display =="none";
});

on('#ajax', 'click', '.c_all_photo_likes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  create_fullscreen("/gallery/window/all_community_like/" + pk + "/", "worker_fullscreen");
});
on('#ajax', 'click', '.c_all_photo_dislikes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  create_fullscreen("/gallery/window/all_community_dislike/" + pk + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.c_all_photo_comment_likes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  create_fullscreen("/gallery/window/all_community_comment_like/" + pk + "/", "worker_fullscreen");
});
on('#ajax', 'click', '.c_all_photo_comment_dislikes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  create_fullscreen("/gallery/window/all_community_comment_dislike/" + pk + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.c_all_photo_reposts', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-pk');
  create_fullscreen("/gallery/window/all_community_reposts/" + pk + "/", "worker_fullscreen");
});
