
on('#ajax', 'click', '.u_doc_list_create_window', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  loader = document.getElementById("create_loader");
  open_fullscreen("/docs/user_progs/create_list_window/" + pk + "/", loader)
});

on('#ajax', 'click', '.u_doc_create_window', function(e) {
  e.preventDefault();
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  loader = document.getElementById("create_loader");
  open_fullscreen("/docs/user_progs/create_doc_window/" + pk + "/", loader);
});

on('#ajax', 'click', '.u_ucm_doc_repost', function() {
  parent = this.parentElement.parentElement.parentElement;
  doc_pk = parent.getAttribute("data-pk");
  parent.getAttribute('user-pk') ? pk = parent.getAttribute('user-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/docs/repost/u_ucm_doc_window/" + pk + "/" + doc_pk + "/", loader);
  clear_attach_block();
})
on('#ajax', 'click', '.u_ucm_doc_list_repost', function() {
  parent = this.parentElement;
  parent.getAttribute("data-pk") ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  parent.getAttribute("data-uuid") ? uuid = parent.getAttribute('data-uuid') : uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/docs/repost/u_ucm_list_window/" + pk + "/" + uuid + "/", loader);
  clear_attach_block();
})
