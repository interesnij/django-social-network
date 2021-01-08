on('#ajax', 'click', '.u_soundcloud_set_create', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen("/music/user_progs/souncloud_create_list_window/", loader)
});
on('#ajax', 'click', '.u_soundcloud_set_list_main', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen("/music/user_progs/souncloud_list_window_main/", loader)
});
on('#ajax', 'click', '.u_soundcloud_set_list', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen("/music/user_progs/souncloud_list_window/", loader)
});
on('#ajax', 'click', '.u_music_list_create_window', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen("/music/user_progs/create_list_window/", loader)
});
on('#ajax', 'click', '.u_music_list_edit_window', function() {
  body = document.body.querySelector(".pk_saver");
  uuid = body.getAttribute("data-uuid");
  loader = document.getElementById("create_loader");
  open_fullscreen("/music/user_progs/edit_list_window/" + uuid + "/", loader)
});

on('#ajax', 'click', '.u_load_music_list', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement;
  uuid = parent.getAttribute("data-uuid"); pk = parent.getAttribute("data-pk");
  loader = document.getElementById("create_loader");
  open_fullscreen("/music/user/load/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.u_ucm_music_repost', function() {
  parent = this.parentElement;
  track_pk = parent.getAttribute("data-pk");
  parent.getAttribute('user-pk') ? pk = parent.getAttribute('user-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/music/repost/u_ucm_music_window/" + pk + "/" + track_pk + "/", loader);
  clear_attach_block();
})
on('#ajax', 'click', '.u_ucm_music_list_repost', function() {
  parent = this.parentElement.parentElement.parentElement; 
  parent.getAttribute("data-pk") ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  parent.getAttribute("data-uuid") ? uuid = parent.getAttribute('data-uuid') : uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/music/repost/u_ucm_list_window/" + pk + "/" + uuid + "/", loader);
  clear_attach_block();
})
