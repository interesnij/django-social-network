on('#ajax', 'click', '.c_load_profile_photo_list', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  profile_list_block_load(this, ".load_block", "/communities/" + pk + "/photo_list/" + this.parentElement.parentElement.parentElement.getAttribute("data-uuid") + "/", "c_load_profile_photo_list");
});

on('#ajax', 'click', '.c_AVA_photo', function() {
  photo_pk = this.getAttribute('photo-pk');
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/community/avatar_photo/" + pk + "/" + photo_pk + "/", loader)
});

on('#ajax', 'click', '.c_load_attach_photo_list', function() {
  profile_list_block_load(this, ".load_block", "/users/load/u_photo_list_load/" + this.parentElement.parentElement.parentElement.getAttribute("data-uuid") + "/", "c_load_attach_photo_list");
});

on('#ajax', 'click', '.c_MAI_photo', function() {
  pk = this.getAttribute('photo-pk');
  this.parentElement.parentElement.parentElement.getAttribute('data-uuid') ? uuid = this.parentElement.parentElement.parentElement.getAttribute('data-uuid') : uuid = document.body.querySelector(".uuid_saver").getAttribute('data-uuid');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/community/photo/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.c_post_photo', function() {
  pk = this.getAttribute('photo-pk');
  uuid = this.parentElement.parentElement.parentElement.getAttribute('data-uuid');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/community/post_photo/" + uuid + "/" + pk + "/", loader)
});

on('#ajax', 'click', '.c_photo_priview', function() {
  pk = this.getAttribute('photo-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/community/preview_photo/" + pk + "/", loader)
});

on('#ajax', 'click', '.c_load_photo_list', function() {
  parent = this.parentElement.parentElement;
  uuid = parent.getAttribute("data-uuid"); pk = parent.getAttribute("data-pk");
  loader = document.getElementById("item_loader");
  open_fullscreen("/gallery/community/load/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.c_ucm_photo_repost', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement
  uuid = parent.getAttribute("data-uuid");
  pk = parent.getAttribute("data-pk");
  loader = document.getElementById("votes_loader");
  open_fullscreen("/gallery/repost/c_ucm_photo_window/" + pk + "/" + uuid + "/", loader);
  clear_attach_block();
})
on('#ajax', 'click', '.c_ucm_photo_list_repost', function() {
  parent = this.parentElement.parentElement.parentElement;
  parent.getAttribute('data-pk') ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk')
  parent.getAttribute('data-uuid') ? uuid = parent.getAttribute('data-uuid') : uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid')
  loader = document.getElementById("votes_loader");
  open_fullscreen("/gallery/repost/c_ucm_list_window/" + pk + "/" + uuid + "/", loader);
  clear_attach_block();
})

on('#ajax', 'click', '.c_avatar_detail', function() {
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = this.getAttribute('data-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/community/avatar/" + pk + "/", loader)
});

on('#ajax', 'click', '.c_LIS_photo', function() {
  this.parentElement.getAttribute('data-uuid') ? uuid = this.parentElement.getAttribute('data-uuid') : uuid = this.getAttribute('data-uuid');
  pk = this.getAttribute('photo-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/community/list_photo/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.c_WA_photo', function() {
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = this.getAttribute('data-pk');
  photo_pk = this.getAttribute('photo-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/community/wall_photo/" + pk + "/" + photo_pk + "/", loader)
});

on('#ajax', 'click', '.c_photos_add', function() {
  document.querySelector('#photos_add_window').style.display =="none";
})

on('#ajax', 'click', '.c_photo_list_add', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("create_loader");
  open_fullscreen("/gallery/community_progs/add_list/" + pk + "/", loader)
});
on('#ajax', 'click', '.c_photo_list_edit', function() {
  uuid = this.parentElement.parentElement.getAttribute('data-uuid');
  loader = document.getElementById("create_loader");
  open_fullscreen("/gallery/community_progs/edit_list/" + uuid + "/", loader)
});

on('#ajax', 'click', '.c_photo_edit', function() {
  document.querySelector('#block_description_form').style.display =="none";
})

on('#ajax', 'click', '.c_all_photo_likes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/gallery/window/all_community_like/" + uuid + "/", loader)
});
on('#ajax', 'click', '.c_all_photo_dislikes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/gallery/window/all_community_dislike/" + uuid + "/", loader)
});

on('#ajax', 'click', '.c_all_photo_comment_likes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/gallery/window/all_community_comment_like/" + pk + "/", loader)
});
on('#ajax', 'click', '.c_all_photo_comment_dislikes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/gallery/window/all_community_comment_dislike/" + pk + "/", loader)
});

on('#ajax', 'click', '.c_all_photo_reposts', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/gallery/window/all_community_reposts/" + uuid + "/", loader)
});

on('#ajax', 'click', '.c_photo_comments', function() {
  clear_comment_dropdown();
  data = document.body.querySelector(".data_display");
  pk = data.getAttribute("data-pk");
  uuid = data.getAttribute("data-uuid");
  block = data.querySelector(".c_load_comments");
  if (block.classList.contains("show")){
    block.classList.remove("show")
  } else {
    block.firstChild ? null : list_load(block, "/gallery/community/comment/" + pk + "/" + uuid + "/");
    block.classList.add("show")
  }
});
