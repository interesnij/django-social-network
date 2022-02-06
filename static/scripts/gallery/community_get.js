on('#ajax', 'click', '.c_photo_priview', function() {
  pk = this.getAttribute('photo-pk');
  create_fullscreen("/gallery/community/preview_photo/" + pk + "/", "photo_fullscreen");
});

on('#ajax', 'click', '.c_photo_edit', function() {
  document.querySelector('#block_description_form').style.display =="none";
});
