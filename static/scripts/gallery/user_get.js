on('#ajax', 'click', '.u_copy_photo_list', function() {
  on_off_list_in_collections(this, "/gallery/user_progs/add_list_in_collections/", "u_uncopy_photo_list", "u_copy_photo_list", "Удалить")
});
on('#ajax', 'click', '.u_uncopy_photo_list', function() {
  on_off_list_in_collections(this, "/gallery/user_progs/remove_list_from_collections/", "u_copy_photo_list", "u_uncopy_photo_list", "Добавить")
});

on('#ajax', 'click', '.u_load_profile_photo_list', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk')
  profile_list_block_load(this, ".load_block", "/users/" + pk + "/photo_list/" + this.parentElement.parentElement.parentElement.getAttribute("data-uuid") + "/", "u_load_profile_photo_list");
});

on('#ajax', 'click', '.u_load_attach_photo_list', function() {
  profile_list_block_load(this, ".load_block", "/users/load/u_photo_list_load/" + this.parentElement.parentElement.parentElement.getAttribute("data-uuid") + "/", "u_load_attach_photo_list");
});

on('#ajax', 'click', '.u_MAI_photo', function() {
  pk = this.getAttribute('photo-pk');
  this.parentElement.parentElement.parentElement.getAttribute('data-uuid') ? uuid = this.parentElement.parentElement.parentElement.getAttribute('data-uuid') : uuid = document.body.querySelector(".uuid_saver").getAttribute('data-uuid')
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/user/photo/" + pk + "/" + uuid + "/", loader)
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

on('#ajax', 'click', '.u_load_photo_photo_list', function() {
  parent = this.parentElement.parentElement;
  uuid = parent.getAttribute("data-uuid");
  loader = document.getElementById("item_loader");
  open_fullscreen("/gallery/user/load/" + uuid + "/", loader)
});

on('#ajax', 'click', '.u_ucm_photo_photo_list_repost', function() {
  parent = this.parentElement.parentElement.parentElement;
  parent.getAttribute('data-pk') ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk')
  parent.getAttribute('data-uuid') ? uuid = parent.getAttribute('data-uuid') : uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid')
  loader = document.getElementById("votes_loader");
  open_fullscreen("/gallery/repost/u_ucm_list_window/" + pk + "/" + uuid + "/", loader);
  clear_attach_block();
})

on('#ajax', 'click', '.u_avatar_detail', function() {
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = this.getAttribute('data-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/user/avatar/" + pk + "/", loader)
});

on('#ajax', 'click', '.u_LIS_photo', function() {
  this.parentElement.getAttribute('data-uuid') ? uuid = this.parentElement.parentElement.getAttribute('data-uuid') : uuid = this.getAttribute('data-uuid');
  pk = this.getAttribute('photo-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/user/list_photo/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.u_WAL_photo', function() {
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = this.getAttribute('data-pk');
  photo_pk = this.getAttribute('photo-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/user/wall_photo/" + pk + "/" + photo_pk + "/", loader)
});
on('#ajax', 'click', '.u_AVA_photo', function() {
  photo_pk = this.getAttribute('photo-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/user/avatar_photo/" + photo_pk + "/", loader)
});

on('#ajax', 'click', '.u_photos_add', function() {
  document.querySelector('#photos_add_window').style.display =="none";
})

on('#ajax', 'click', '.u_photo_list_add', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("create_loader");
  open_fullscreen("/gallery/user_progs/add_list/" + pk + "/", loader)
});
on('#ajax', 'click', '.u_photo_list_edit', function() {
  list = document.body.querySelectorAll('.cover_block');
  for (var i = 0; i < list.length; i++) {
    list[i].classList.remove("list_active")
  }
  block = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  block.classList.add("list_active");
  pk = block.getAttribute('data-pk');
  uuid = block.getAttribute('data-uuid');
  loader = document.getElementById("create_loader");
  open_fullscreen("/gallery/user_progs/edit_list/" + pk + "/" + uuid + "/", loader)
});
on('#ajax', 'click', '.u_photo_list_remove', function() {
  block = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = block.getAttribute('data-pk');
  uuid = block.getAttribute('data-uuid');
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/gallery/user_progs/delete_list/" + pk + "/" + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    block.querySelector(".card").style.display = "none";
    $block = document.createElement("div");
    $block.classList.add("card", "delete_card", "rounded-0", "border-0", "mb-3");
    $block.innerHTML = '<div class="card-header"><div class="media"><div class="media-body"><h6 class="mb-0 u_photo_list_restore pointer">Восстановить</h6></div></div></div><div class="card-body"><a><img class="image_fit_200" src="/static/images/no_img/list.jpg" /></a></div>'
    block.append($block);
  }}
  link_.send();
});
on('#ajax', 'click', '.u_photo_list_restore', function() {
  uuid = this.getAttribute('data-uuid');
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/gallery/user_progs/restore_list/" + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    block.querySelector(".delete_card").remove();
    block.querySelector(".card").style.display = "block";
  }}
  link_.send();
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
