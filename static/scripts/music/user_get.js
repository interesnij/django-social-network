on('#ajax', 'click', '.u_soundcloud_set_create', function() {
  uuid = this.parentElement.getAttribute('data-uuid');
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("create_loader");
  open_fullscreen("/music/user_progs/souncloud_create_list_window/" + pk + "/", loader)
});
on('#ajax', 'click', '.u_soundcloud_set_list_main', function() {
  uuid = this.parentElement.getAttribute('data-uuid');
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("create_loader");
  open_fullscreen("/music/user_progs/souncloud_list_window_main/" + pk + "/", loader)
});
on('#ajax', 'click', '.u_soundcloud_set_list', function() {
  uuid = this.parentElement.getAttribute('data-uuid');
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("create_loader");
  open_fullscreen("/music/user_progs/souncloud_list_window/" + pk + "/", loader)
});

on('#ajax', 'click', '.u_ucm_music_repost', function() {
  parent = this.parentElement;
  track_pk = parent.getAttribute("data-pk");
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = parent.getAttribute('user-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/music/repost/u_ucm_music_window/" + pk + "/" + track_pk + "/", loader);
  clear_attach_block();
})
