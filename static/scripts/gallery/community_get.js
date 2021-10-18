

on('#ajax', 'click', '.c_photo_priview', function() {
  pk = this.getAttribute('photo-pk');
  create_fullscreen("/gallery/community/preview_photo/" + pk + "/", "photo_fullscreen");
});

on('#ajax', 'click', '.c_ucm_photo_repost', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement
  uuid = parent.getAttribute("data-uuid");
  pk = parent.getAttribute("data-pk");
  create_fullscreen("/gallery/repost/c_ucm_photo_window/" + pk + "/" + uuid + "/", "worker_fullscreen");
  clear_attach_block();
})
on('#ajax', 'click', '.c_ucm_photo_list_repost', function() {
  parent = this.parentElement.parentElement.parentElement;
  parent.getAttribute('data-pk') ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk')
  parent.getAttribute('data-uuid') ? uuid = parent.getAttribute('data-uuid') : uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid')
  create_fullscreen("/gallery/repost/c_ucm_list_window/" + pk + "/" + uuid + "/", "worker_fullscreen");
  clear_attach_block();
})

on('#ajax', 'click', '.c_avatar_detail', function() {
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = this.getAttribute('data-pk');
  create_fullscreen("/gallery/community/avatar/" + pk + "/", "photo_fullscreen");
});

on('#ajax', 'click', '.c_photos_add', function() {
  document.querySelector('#photos_add_window').style.display =="none";
})

on('#ajax', 'click', '.c_photo_list_add', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  create_fullscreen("/gallery/community_progs/add_list/" + pk + "/", "worker_fullscreen");
});
on('#ajax', 'click', '.c_photo_list_edit', function() {
  uuid = this.parentElement.parentElement.getAttribute('data-uuid');
  create_fullscreen("/gallery/community_progs/edit_list/" + uuid + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.c_photo_edit', function() {
  document.querySelector('#block_description_form').style.display =="none";
})

on('#ajax', 'click', '.c_all_photo_likes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  create_fullscreen("/gallery/window/all_community_like/" + uuid + "/", "worker_fullscreen");
});
on('#ajax', 'click', '.c_all_photo_dislikes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  create_fullscreen("/gallery/window/all_community_dislike/" + uuid + "/", "worker_fullscreen");
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
  uuid = container.getAttribute('data-uuid');
  create_fullscreen("/gallery/window/all_community_reposts/" + uuid + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.c_photo_comments', function() {
  clear_comment_dropdown();
  data = document.body.querySelector(".data_display");
  uuid = data.getAttribute("data-uuid");
  block = data.querySelector(".c_load_comments");
  if (block.classList.contains("show")){
    block.classList.remove("show")
  } else {
    block.firstChild ? null : list_load(block, "/gallery/community/comment/" + uuid + "/");
    block.classList.add("show")
  }
});
