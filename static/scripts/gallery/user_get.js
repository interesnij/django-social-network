on('#ajax', 'click', '.u_photo_detail', function() {
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = this.getAttribute('data-pk');
  uuid = this.getAttribute('photo-uuid');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/user/photo/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.u_ucm_photo_repost', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement
  uuid = parent.getAttribute("data-uuid");
  pk = parent.getAttribute("user-pk");
  loader = document.getElementById("votes_loader");
  open_fullscreen("/gallery/repost/u_ucm_photo_window/" + pk + "/" + uuid + "/", loader);
  clear_attach_block();
})
on('#ajax', 'click', '.u_ucm_photo_list_repost', function() {
  parent = this.parentElement;
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

on('#ajax', 'click', '.u_AV_photo', function() {
  document.body.querySelector(".pk_saver") ? uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid') : uuid = this.getAttribute('data-uuid');
  pk = this.getAttribute('photo-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/user/avatar_photo/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.u_AL_photo', function() {
  document.body.querySelector(".pk_saver").getAttribute('data-uuid') ? uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid') : uuid = this.getAttribute('data-uuid');
  pk = this.getAttribute('photo-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/user/album_photo/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.u_WA_photo', function() {
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = this.getAttribute('data-pk');
  photo_pk = this.getAttribute('photo-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/user/wall_photo/" + pk + "/" + photo_pk + "/", loader)
});

on('#ajax', 'click', '.u_photos_add', function() {
  document.querySelector('#photos_add_window').style.display =="none";
})

on('#ajax', 'click', '.u_albums_add', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("create_loader");
  open_fullscreen("/gallery/user_progs/add_album/" + pk + "/", loader)
});
on('#ajax', 'click', '.u_albums_edit', function() {
  list = document.body.querySelectorAll('.cover_block');
  for (var i = 0; i < list.length; i++) {
    h6 = list[i].querySelector('h6');
    h6.classList.remove("album_title_active")
  }
  parent = this.parentElement;
  title = parent.parentElement.previousElementSibling.querySelector("h6");
  title.classList.add("album_title_active");
  pk = parent.getAttribute('data-pk');
  uuid = parent.getAttribute('data-uuid');
  loader = document.getElementById("create_loader");
  open_fullscreen("/gallery/user_progs/edit_album/" + pk + "/" + uuid + "/", loader)
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
  pk = data.getAttribute("user-pk");
  uuid = data.getAttribute("data-uuid");
  url = "/gallery/user_progs/comment/" + uuid + "/" + pk + "/";
  list_load(data.querySelector(".u_load_comments"), url);
  this.classList.toggle("comments_open");
});
