on('#ajax', 'click', '.c_photo_detail', function() {
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = this.getAttribute('data-pk');
  uuid = this.getAttribute('photo-uuid');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/community/photo/" + pk + "/" + uuid + "/", loader)
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
  pk = this.getAttribute('photo-pk');
  document.body.querySelector(".pk_saver") ? uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid') : uuid = this.getAttribute('data-uuid');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/community/avatar_photo/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.c_AL_photo', function() {
  container = this.parentElement;
  document.body.querySelector(".pk_saver").getAttribute('data-uuid') ? uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid') : uuid = this.getAttribute('data-uuid');
  pk = this.getAttribute('photo-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/community/album_photo/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.c_WA_photo', function() {
  this.getAttribute('data-pk') ? uuid = this.getAttribute('data-uuid') : uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid')
  pk = this.getAttribute('photo-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/community/wall_photo/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.c_photos_add', function() {
  document.querySelector('#photos_add_window').style.display =="none";
})

on('#ajax', 'click', '.c_albums_add', function() {
  container = this.parentElement;
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("create_loader");
  open_fullscreen("/gallery/community_progs/add_album/" + pk + "/", loader)
});

on('#ajax', 'click', '.c_photo_edit', function() {
  document.querySelector('#block_description_form').style.display =="none";
})


on('#ajax', 'click', '#c_create_album_btn', function() {
  form = document.body.querySelector("#c_create_album_form");
  form_data = new FormData(form);
  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { null }
  post_and_load_object_page(form, "/gallery/community_progs/add_album/", "/communities/", "/album/");
});

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
  url = "/gallery/community_progs/comment/" + uuid + "/" + pk + "/";
  list_load(data.querySelector(".c_load_comments"), url);
  this.classList.toggle("comments_open");
});
