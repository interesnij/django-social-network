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
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/photo/" + photo_pk + "/", loader)
});

on('#ajax', 'click', '.u_avatar_detail', function() {
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = this.getAttribute('data-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/user/photo/" + pk + "/", loader)
});

on('#ajax', 'click', '.comment_photo', function() {
  pk = this.getAttribute('photo-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/user/comment_photo/" + pk + "/", loader)
});
on('#ajax', 'click', '.u_post_photo', function() {
  pk = this.getAttribute('photo-pk');
  uuid = this.parentElement.parentElement.parentElement.getAttribute('data-uuid');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/user/post_photo/" + uuid + "/" + pk + "/", loader)
});
on('#ajax', 'click', '.u_photo_priview', function() {
  pk = this.getAttribute('photo-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/user/preview_photo/" + pk + "/", loader)
});

on('#ajax', 'click', '.photo_fullscreen_hide_2', function() {
  this.parentElement.parentElement.parentElement.parentElement.parentElement.style.display = "none";
  this.parentElement.parentElement.parentElement.parentElement.innerHTML = "";
});
on('#ajax', 'click', '.good_fullscreen_hide_2', function() {
  this.parentElement.parentElement.parentElement.parentElement.parentElement.style.display = "none";
  this.parentElement.parentElement.parentElement.parentElement.innerHTML = "";
});
on('#ajax', 'click', '.create_fullscreen_hide_2', function() {
  this.parentElement.parentElement.parentElement.parentElement.parentElement.style.display = "none";
  this.parentElement.parentElement.parentElement.parentElement.innerHTML = "";
});
on('#ajax', 'click', '.item_fullscreen_hide_2', function() {
  this.parentElement.parentElement.parentElement.parentElement.parentElement.style.display = "none";
  this.parentElement.parentElement.parentElement.parentElement.innerHTML = "";
});

on('#ajax', 'click', '.u_all_photo_likes', function() {
  uuid = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/gallery/window/all_user_like/" + uuid + "/", loader)
});
on('#ajax', 'click', '.u_all_photo_dislikes', function() {
  uuid = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/gallery/window/all_user_dislike/" + uuid + "/", loader)
});

on('#ajax', 'click', '.u_ucm_photo_repost', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement
  uuid = parent.getAttribute("data-uuid");
  pk = parent.getAttribute("data-pk");
  loader = document.getElementById("votes_loader");
  open_fullscreen("/gallery/repost/u_ucm_photo_window/" + pk + "/" + uuid + "/", loader);
  clear_attach_block();
})

on('#ajax', 'click', '.u_load_photo_list', function() {
  parent = this.parentElement.parentElement;
  uuid = parent.getAttribute("data-uuid");
  loader = document.getElementById("item_loader");
  open_fullscreen("/gallery/user/load/" + uuid + "/", loader)
});

on('#ajax', 'click', '.u_ucm_photo_list_repost', function() {
  parent = this.parentElement.parentElement.parentElement;
  parent.getAttribute('data-pk') ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk')
  parent.getAttribute('data-uuid') ? uuid = parent.getAttribute('data-uuid') : uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid')
  loader = document.getElementById("votes_loader");
  open_fullscreen("/gallery/repost/u_ucm_list_window/" + pk + "/" + uuid + "/", loader);
  clear_attach_block();
})

on('#ajax', 'click', '.u_photos_add', function() {
  document.querySelector('#photos_add_window').style.display =="none";
})

on('#ajax', 'click', '.u_photo_list_add', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("create_loader");
  open_fullscreen("/gallery/user_progs/add_list/" + pk + "/", loader)
});
on('#ajax', 'click', '.u_photo_list_edit', function() {
  uuid = this.parentElement.parentElement.getAttribute('data-uuid');
  loader = document.getElementById("create_loader");
  open_fullscreen("/gallery/user_progs/edit_list/" + uuid + "/", loader)
});

on('#ajax', 'click', '.u_photo_edit', function() {
  document.querySelector('#block_description_form').style.display =="none";
})

on('#ajax', 'click', '.u_all_photo_comment_likes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/gallery/window/all_user_comment_like/" + pk + "/", loader)
});
on('#ajax', 'click', '.u_all_photo_comment_dislikes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/gallery/window/all_user_comment_dislike/" + pk + "/", loader)
});

on('#ajax', 'click', '.u_all_photo_reposts', function() {
  uuid = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/gallery/window/all_user_reposts/" + uuid + "/", loader)
});

on('#ajax', 'click', '.u_photo_comments', function() {
  clear_comment_dropdown();
  data = document.body.querySelector(".data_display");
  pk = data.getAttribute("data-pk");
  uuid = data.getAttribute("data-uuid");
  block = data.querySelector(".u_load_comments");
  if (block.classList.contains("show")){
    block.classList.remove("show")
  } else {
    block.firstChild ? null : list_load(block, "/gallery/user/comment/" + pk + "/" + uuid + "/");
    block.classList.add("show")
  }
});
