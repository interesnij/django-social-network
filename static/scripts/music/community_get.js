on('#ajax', 'click', '.c_ucm_music_repost', function() {
  parent = this.parentElement;
  track_pk = parent.getAttribute("data-pk");
  parent.getAttribute('community-pk') ? pk = parent.getAttribute('user-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/music/repost/c_ucm_music_window/" + pk + "/" + track_pk + "/", loader);
  clear_attach_block();
})
