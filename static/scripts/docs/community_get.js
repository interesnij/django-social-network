on('#ajax', 'click', '.c_copy_doc_list', function() {
  on_off_list_in_collections(this, "/docs/community_progs/add_list_in_collections/", "c_uncopy_doc_list", "c_copy_doc_list", "Удалить")
});
on('#ajax', 'click', '.c_uncopy_doc_list', function() {
  on_off_list_in_collections(this, "/docs/community_progs/remove_list_from_collections/", "c_copy_doc_list", "c_uncopy_doc_list", "Добавить")
});


on('#ajax', 'click', '.c_doc_list_add', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  create_fullscreen("/docs/community_progs/add_list/" + pk + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.c_doc_create', function(e) {
  e.preventDefault();
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  create_fullscreen("/docs/community_progs/create_doc/" + pk + "/", "worker_fullscreen");
});
on('body', 'click', '.c_doc_edit', function() {
  parent = this.parentElement.parentElement.parentElement;
  blocks = document.body.querySelectorAll('.col-sm-12');
  for (var i = 0; i < blocks.length; i++) {blocks[i].classList.remove("edited_doc")}

  parent.parentElement.parentElement.parentElement.classList.add("edited_doc")
  create_fullscreen("/docs/community_progs/edit_doc/" + parent.getAttribute("data-pk") + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.c_doc_list_edit', function() {
  uuid = this.parentElement.parentElement.getAttribute('data-uuid');
  create_fullscreen("/docs/community_progs/edit_list/" + uuid + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.c_ucm_doc_repost', function() {
  parent = this.parentElement;
  doc_pk = parent.getAttribute("doc-pk");
  parent.getAttribute('data-pk') ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  create_fullscreen("/docs/repost/c_ucm_doc_window/" + pk + "/" + doc_pk + "/", "worker_fullscreen");
  clear_attach_block();
})
on('#ajax', 'click', '.c_ucm_doc_list_repost', function() {
  parent = this.parentElement.parentElement.parentElement;
  parent.getAttribute("data-pk") ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  parent.getAttribute("data-uuid") ? uuid = parent.getAttribute('data-uuid') : uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid');
  create_fullscreen("/docs/repost/c_ucm_list_window/" + pk + "/" + uuid + "/", "worker_fullscreen");
  clear_attach_block();
})
