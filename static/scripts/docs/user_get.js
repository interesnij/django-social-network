on('#ajax', 'click', '.u_copy_doc_list', function() {
  on_off_list_in_collections(this, "/docs/user_progs/add_list_in_collections/", "u_uncopy_doc_list", "u_copy_doc_list", "Удалить")
});
on('#ajax', 'click', '.u_uncopy_doc_list', function() {
  on_off_list_in_collections(this, "/docs/user_progs/remove_list_from_collections/", "u_copy_doc_list", "u_uncopy_doc_list", "Добавить")
});

on('#ajax', 'click', '.load_profile_doc_list', function() {
  profile_list_block_load(this, ".load_block", "/doc_list/", "load_profile_doc_list");
});

on('#ajax', 'click', '.load_attach_doc_list', function() {
  profile_list_block_attach(this, ".load_block", "/u_doc_list_load/", "load_attach_doc_list");
});

on('#ajax', 'click', '.u_doc_list_add', function() {
  create_fullscreen("/docs/user_progs/add_list/" + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.u_doc_add', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  create_fullscreen("/docs/user_progs/create_doc/" + pk + "/", "worker_fullscreen");
});
on('body', 'click', '.u_doc_edit', function() {
  parent = this.parentElement.parentElement.parentElement;
  blocks = document.body.querySelectorAll('.col-sm-12');
  for (var i = 0; i < blocks.length; i++) {blocks[i].classList.remove("edited_doc")}

  parent.parentElement.parentElement.parentElement.classList.add("edited_doc")
  create_fullscreen("/docs/user_progs/edit_doc/" + parent.getAttribute("data-pk") +"/", "worker_fullscreen");
});

on('#ajax', 'click', '.u_doc_list_edit', function() {
  pk = this.parentElement.parentElement.getAttribute('data-pk');
  create_fullscreen("/docs/user_progs/edit_list/" + pk + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.load_doc_list', function() {
  card = this.parentElement.parentElement.parentElement;
  doclist_pk = card.getAttribute("doclist-pk");
  owner_pk = card.getAttribute("owner-pk");

  create_fullscreen("/docs/load_list/" + doclist_pk + "/", "item_fullscreen");
  window.history.pushState(null, "vfgffgfgf", window.location.href + "?key=wall&owner_id=" + owner_pk + "&doclist=" + doclist_pk);
});

on('#ajax', 'click', '.u_ucm_doc_repost', function() {
  parent = this.parentElement;
  doc_pk = parent.getAttribute("doc-pk");
  parent.getAttribute('data-pk') ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  create_fullscreen("/docs/repost/u_ucm_doc_window/" + pk + "/" + doc_pk + "/", "worker_fullscreen");
  clear_attach_block();
});
on('#ajax', 'click', '.u_ucm_doc_list_repost', function() {
  parent = this.parentElement.parentElement.parentElement;
  parent.getAttribute("data-pk") ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  list_pk = parent.getAttribute('list-pk');
  create_fullscreen("/docs/repost/u_ucm_list_window/" + pk + "/" + list_pk + "/", "worker_fullscreen");
  clear_attach_block();
});
