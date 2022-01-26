on('#ajax', 'click', '.copy_user_photo_list', function() {
  on_off_list_in_collections(this, "/gallery/user_progs/add_list_in_collections/", "uncopy_user_photo_list", "copy_user_photo_list", "Удалить")
});
on('#ajax', 'click', '.uncopy_user_photo_list', function() {
  on_off_list_in_collections(this, "/gallery/user_progs/remove_list_from_collections/", "copy_user_photo_list", "uncopy_user_photo_list", "Добавить")
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
  create_fullscreen("/gallery/photo/" + photo_pk + "/", "photo_fullscreen");
  window.history.pushState(null, "vfgffgfgf", window.location.href + "?key=big_page&owner_id=" + pk + "&photo_pk=" + photo_pk);
});

on('#ajax', 'click', '.comment_photo', function() {
  pk = this.getAttribute('photo-pk');
  create_fullscreen("/gallery/user/comment_photo/" + pk + "/", "photo_fullscreen");
});
on('#ajax', 'click', '.post_photo', function() {
  photo_pk = this.getAttribute('photo-pk');
  card = this.parentElement.parentElement.parentElement;
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = card.getAttribute('owner-pk');
  this.getAttribute('data-pk') ? post_pk = this.getAttribute('data-pk') : post_pk = this.parentElement.parentElement.parentElement.getAttribute('data-pk');

  create_fullscreen("/gallery/post_photo/" + post_pk + "/" + photo_pk + "/", "photo_fullscreen");
  window.history.pushState(null, "vfgffgfgf", window.location.href + "?key=wall&owner_id=" + pk + "&photo_pk=" + photo_pk + "&post_pk=" + post_pk);
});
on('body', 'click', '.chat_photo', function() {
  photo_pk = this.getAttribute('photo-pk');
  pk = this.parentElement.getAttribute('chat-pk');
  create_fullscreen("/gallery/chat_photo/" + pk + "/" + photo_pk + "/", "photo_fullscreen");
});

on('#ajax', 'click', '.u_photo_priview', function() {
  pk = this.getAttribute('photo-pk');
  create_fullscreen("/gallery/user/preview_photo/" + pk + "/", "photo_fullscreen");
});

on('#ajax', 'click', '.load_photo_list', function() {
  card = this.parentElement.parentElement;
  photolist_pk = card.getAttribute("photolist-pk");
  owner_pk = card.getAttribute("owner-pk");
  create_fullscreen("/gallery/load_list/" + photolist_pk + "/", "item_fullscreen");
  window.history.pushState(null, "vfgffgfgf", window.location.href + "?key=wall&owner_id=" + owner_pk + "&photolist=" + photolist_pk);
});

on('#ajax', 'click', '.u_photos_add', function() {
  document.querySelector('#photos_add_window').style.display =="none";
});

on('#ajax', 'click', '.u_photo_list_add', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  create_fullscreen("/gallery/user_progs/add_list/" + pk + "/", "worker_fullscreen");
});
on('#ajax', 'click', '.u_photo_list_edit', function() {
  pk = this.parentElement.parentElement.getAttribute('data-pk');
  create_fullscreen("/gallery/user_progs/edit_list/" + pk + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.u_photo_edit', function() {
  document.querySelector('#block_description_form').style.display =="none";
});
