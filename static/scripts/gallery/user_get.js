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
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement
  this.getAttribute('data-pk') ? pk = this.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk')
  this.getAttribute('data-uuid') ? uuid = this.getAttribute('data-uuid') : uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid')
  loader = document.getElementById("votes_loader");
  open_fullscreen("/gallery/repost/u_ucm_photo_album_window/" + pk + "/" + uuid + "/", loader);
  clear_attach_block();
})

on('#ajax', 'click', '.u_avatar_detail', function() {
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = this.getAttribute('data-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/user/avatar/" + pk + "/", loader)
});

on('#ajax', 'click', '.u_AV_photo', function() {
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = this.getAttribute('data-pk');
  uuid = this.getAttribute("photo-uuid");
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/user/avatar_photo/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.u_AL_photo', function() {
  document.body.querySelector(".pk_saver") ? uuid = document.body.querySelector(".pk_saver").getAttribute('data-pk') : uuid = this.getAttribute('data-pk');
  photo_uuid = this.getAttribute('photo-uuid');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/user/album_photo/" + uuid + "/" + photo_uuid + "/", loader)
});

on('#ajax', 'click', '.u_WA_photo', function() {
  uuid = this.getAttribute('photo-uuid');
  this.getAttribute('data-pk') ? pk = this.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk')
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/user/wall_photo/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.u_photos_add', function() {
  document.querySelector('#photos_add_window').style.display =="none";
})

on('#ajax', 'click', '.u_albums_add', function() {
  var container, uuid, loader;
  container = this.parentElement;
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("create_loader");
  open_fullscreen("/gallery/user_progs/add_album/" + pk + "/", loader)
});

on('#ajax', 'click', '.u_photo_edit', function() {
  document.querySelector('#block_description_form').style.display =="none";
})


on('#ajax', 'click', '#u_create_album_btn', function() {
  form = document.body.querySelector("#u_create_album_form");
  form_data = new FormData(form);
  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { null }
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  post_and_load_object_page(form, "/gallery/user_progs/add_album/", "/users/", "/album/");
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
