
on('#ajax', 'click', '.c_doc_list_create_window', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  loader = document.getElementById("create_loader");
  open_fullscreen("/docs/community_progs/create_list_window/" + pk + "/", loader)
});

on('#ajax', 'click', '.c_ucm_doc_repost', function() {
  parent = this.parentElement;
  doc_pk = parent.getAttribute("data-pk");
  parent.getAttribute('data-pk') ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/docs/repost/c_ucm_doc_window/" + pk + "/" + track_pk + "/", loader);
  clear_attach_block();
})
on('#ajax', 'click', '.c_ucm_doc_list_repost', function() {
  parent = this.parentElement;
  parent.getAttribute("data-pk") ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  parent.getAttribute("data-uuid") ? uuid = parent.getAttribute('data-uuid') : uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/docs/repost/c_ucm_list_window/" + pk + "/" + uuid + "/", loader);
  clear_attach_block();
})
