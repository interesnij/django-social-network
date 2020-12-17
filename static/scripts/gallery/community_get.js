on('#ajax', 'click', '.c_photo_detail', function() {
  pk = this.getAttribute('photo-pk');
  this.parentElement.parentElement.parentElement.getAttribute('data-uuid') ? uuid = this.parentElement.parentElement.parentElement.getAttribute('data-uuid') : uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid')
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/community/photo/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.c_post_photo', function() {
  pk = this.getAttribute('photo-pk');
  uuid = this.parentElement.parentElement.parentElement.parentElement.getAttribute('data-uuid');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/community/post_photo/" + uuid + "/" + pk + "/", loader)
});

on('#ajax', 'click', '.c_photo_priview', function() {
  pk = this.getAttribute('photo-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/community/preview_photo/" + pk + "/", loader)
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
  parent = this.parentElement;
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

on('#ajax', 'click', '.c_AV_photo', function() {
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = this.getAttribute('data-pk');
  photo_pk = this.getAttribute('photo-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/community/avatar_photo/" + pk + "/" + photo_pk + "/", loader)
});

on('#ajax', 'click', '.c_AL_photo', function() {
  container = this.parentElement;
  document.body.querySelector(".pk_saver").getAttribute('data-uuid') ? uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid') : uuid = this.getAttribute('data-uuid');
  pk = this.getAttribute('photo-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/community/album_photo/" + pk + "/" + uuid + "/", loader)
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

on('#ajax', 'click', '.c_album_add', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("create_loader");
  open_fullscreen("/gallery/community_progs/add_album/" + pk + "/", loader)
});
on('#ajax', 'click', '.c_album_edit', function() {
  list = document.body.querySelectorAll('.cover_block');
  for (var i = 0; i < list.length; i++) {
    list[i].classList.remove("album_active")
  }
  block = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  block.classList.add("album_active");
  pk = block.getAttribute('data-pk');
  uuid = block.getAttribute('data-uuid');
  loader = document.getElementById("create_loader");
  open_fullscreen("/gallery/community_progs/edit_album/" + pk + "/" + uuid + "/", loader)
});
on('#ajax', 'click', '.c_album_remove', function() {
  block = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = block.getAttribute('data-pk');
  uuid = block.getAttribute('data-uuid');
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/gallery/community_progs/delete_album/" + pk + "/" + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    block.querySelector(".card").style.display = "none";
    $block = document.createElement("div");
    $block.classList.add("card", "delete_card", "rounded-0", "border-0", "mb-3");
    $block.innerHTML = '<div class="card-header"><div class="media"><div class="media-body"><h6 class="mb-0 c_album_abort_remove pointer">Восстановить</h6></div></div></div><div class="card-body"><a><img class="image_fit_200" src="/static/images/no_img/album.jpg" /></a></div>'
    block.append($block);
  }}
  link_.send();
});
on('#ajax', 'click', '.c_album_abort_remove', function() {
  block = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = block.getAttribute('data-pk');
  uuid = block.getAttribute('data-uuid');
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/gallery/community_progs/abort_delete_album/" + pk + "/" + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    block.querySelector(".delete_card").remove();
    block.querySelector(".card").style.display = "block";
  }}
  link_.send();
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
  url = "/gallery/community/comment/" + pk + "/" + uuid + "/";
  list_load(data.querySelector(".c_load_comments"), url);
  this.classList.toggle("comments_open");
});
