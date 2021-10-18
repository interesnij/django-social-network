on('#ajax', 'click', '.u_copy_photo_list', function() {
  on_off_list_in_collections(this, "/gallery/user_progs/add_list_in_collections/", "u_uncopy_photo_list", "u_copy_photo_list", "Удалить")
});
on('#ajax', 'click', '.u_uncopy_photo_list', function() {
  on_off_list_in_collections(this, "/gallery/user_progs/remove_list_from_collections/", "u_copy_photo_list", "u_uncopy_photo_list", "Добавить")
});

on('#ajax', 'click', '.load_profile_photo_list', function() {
  profile_list_block_load(this, ".load_block", "/photo_list/", "load_profile_photo_list");
});

on('#ajax', 'click', '.load_attach_photo_list', function() {
  profile_list_block_attach(this, ".load_block", "/u_photo_list_load/", "load_attach_photo_list");
});

on('#ajax', 'click', '.detail_photo', function() {
  photo_pk = this.getAttribute('photo-pk');
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = card.getAttribute('data-pk');
  block = document.body.querySelector(".main-container");
  if (block.classList.contains("user_container")) {
    where_from = "user_wall=1&id=" + pk
  } else if (block.classList.contains("community_container")) {
    where_from = "community_wall=1&id=" + pk
  } else if (block.classList.contains("user_container")) {
    where_from = "user_gallery=1&id=" + pk
  } else if (block.classList.contains("community_container")) {
    where_from = "community_gallery=1&id=" + pk
  } else if (block.classList.contains("feed_container")) {
    where_from = "feed_wall=1&"
  } else if (block.classList.contains("chat_container")) {
    where_from = "chat_wall=1&id=" + pk
  } else if (block.classList.contains("search_container")) {
    where_from = "search_wall=1&id=" + pk
  } else if (block.classList.contains("featured_container")) {
    where_from = "featured_wall=1&id=" + pk
  } else { where_from = "null" };
  create_fullscreen("/gallery/photo/" + photo_pk + "/?" + where_from, "photo_fullscreen")
});

on('#ajax', 'click', '.u_avatar_detail', function() {
  document.body.querySelector(".avatar_figure") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = this.getAttribute('data-pk');
  create_fullscreen("/gallery/user/avatar/" + pk + "/", "photo_fullscreen")
});

on('#ajax', 'click', '.comment_photo', function() {
  pk = this.getAttribute('photo-pk');
  create_fullscreen("/gallery/user/comment_photo/" + pk + "/", "photo_fullscreen");
});
on('#ajax', 'click', '.u_post_photo', function() {
  pk = this.getAttribute('photo-pk');
  this.getAttribute('data-uuid') ? uuid = this.getAttribute('data-uuid') : uuid = this.parentElement.parentElement.parentElement.getAttribute('data-uuid');
  create_fullscreen("/gallery/user/post_photo/" + uuid + "/" + pk + "/", "photo_fullscreen");
});
on('#ajax', 'click', '.message_photo', function() {
  pk = this.getAttribute('photo-pk');
  uuid = this.parentElement.parentElement.parentElement.parentElement.getAttribute('data-uuid');
  create_fullscreen("/gallery/message_photo/" + uuid + "/" + pk + "/", "photo_fullscreen");
});

on('#ajax', 'click', '.u_photo_priview', function() {
  pk = this.getAttribute('photo-pk');
  create_fullscreen("/gallery/user/preview_photo/" + pk + "/", "photo_fullscreen");
});

on('#ajax', 'click', '.u_all_photo_likes', function() {
  uuid = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute('data-uuid');
  create_fullscreen("/gallery/window/all_user_like/" + uuid + "/", "worker_fullscreen");
});
on('#ajax', 'click', '.u_all_photo_dislikes', function() {
  uuid = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute('data-uuid');
  create_fullscreen("/gallery/window/all_user_dislike/" + uuid + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.u_ucm_photo_repost', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement
  uuid = parent.getAttribute("data-uuid");
  pk = parent.getAttribute("data-pk");
  create_fullscreen("/gallery/window/u_ucm_photo_window/" + pk + "/" + uuid + "/", "worker_fullscreen");
  clear_attach_block();
})

on('#ajax', 'click', '.load_photo_list', function() {
  create_fullscreen("/gallery/load_list/" + this.parentElement.parentElement.getAttribute("photolist-pk") + "/", "item_fullscreen")
});

on('#ajax', 'click', '.u_ucm_photo_list_repost', function() {
  parent = this.parentElement.parentElement.parentElement;
  parent.getAttribute('data-pk') ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk')
  parent.getAttribute('data-uuid') ? uuid = parent.getAttribute('data-uuid') : uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid')
  create_fullscreen("/gallery/repost/u_ucm_list_window/" + pk + "/" + uuid + "/", "worker_fullscreen");
  clear_attach_block();
})

on('#ajax', 'click', '.u_photos_add', function() {
  document.querySelector('#photos_add_window').style.display =="none";
})

on('#ajax', 'click', '.u_photo_list_add', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  create_fullscreen("/gallery/user_progs/add_list/" + pk + "/", "worker_fullscreen");
});
on('#ajax', 'click', '.u_photo_list_edit', function() {
  uuid = this.parentElement.parentElement.getAttribute('data-uuid');
  create_fullscreen("/gallery/user_progs/edit_list/" + uuid + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.u_photo_edit', function() {
  document.querySelector('#block_description_form').style.display =="none";
})

on('#ajax', 'click', '.u_all_photo_comment_likes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  create_fullscreen("/gallery/window/all_user_comment_like/" + pk + "/", "worker_fullscreen");
});
on('#ajax', 'click', '.u_all_photo_comment_dislikes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  create_fullscreen("/gallery/window/all_user_comment_dislike/" + pk + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.u_all_photo_reposts', function() {
  uuid = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute('data-uuid');
  create_fullscreen("/gallery/window/all_user_reposts/" + uuid + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.u_photo_comments', function() {
  clear_comment_dropdown();
  data = document.body.querySelector(".data_display");
  uuid = data.getAttribute("data-uuid");
  block = data.querySelector(".u_load_comments");
  if (block.classList.contains("show")){
    block.classList.remove("show")
  } else {
    block.firstChild ? null : list_load(block, "/gallery/user/comment/" + uuid + "/");
    block.classList.add("show")
  }
});
