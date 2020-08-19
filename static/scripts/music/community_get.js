on('#ajax', 'click', '.c_ucm_music_repost', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement
  track_pk = parent.getAttribute("data-pk");
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = parent.getAttribute('community-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/music/repost/c_ucm_music_window/" + pk + "/" + track_pk + "/", loader);
  clear_attach_block();
})
