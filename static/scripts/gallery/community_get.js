on('#ajax', 'click', '.c_photo_priview', function() {
  pk = this.getAttribute('photo-pk');
  create_fullscreen("/gallery/community/preview_photo/" + pk + "/", "photo_fullscreen");
});

on('#ajax', 'click', '.c_photos_add', function() {
  document.querySelector('#photos_add_window').style.display =="none";
});

on('#ajax', 'click', '.c_photo_list_add', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  create_fullscreen("/gallery/community_progs/add_list/" + pk + "/", "worker_fullscreen");
});
on('#ajax', 'click', '.c_photo_list_edit', function() {
  pk = this.parentElement.parentElement.getAttribute('data-pk');
  create_fullscreen("/gallery/community_progs/edit_list/" + pk + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.c_photo_edit', function() {
  document.querySelector('#block_description_form').style.display =="none";
});
