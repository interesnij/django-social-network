on('#ajax', 'click', '.c_copy_doc_list', function() {
  on_off_list_in_collections(this, "/docs/community_progs/add_list_in_collections/", "uncopy_community_doc_list", "copy_community_doc_list", "Удалить")
});
on('#ajax', 'click', '.c_uncopy_doc_list', function() {
  on_off_list_in_collections(this, "/docs/community_progs/remove_list_from_collections/", "copy_community_doc_list", "uncopy_community_doc_list", "Добавить")
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
  pk = this.parentElement.parentElement.getAttribute('data-pk');
  create_fullscreen("/docs/community_progs/edit_list/" + pk + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.c_ucm_doc_repost', function() {
  parent = this.parentElement.parentElement.parentElement;
  pk = parent.getAttribute("data-pk");
  create_fullscreen("/docs/repost/c_ucm_doc_window/" + pk + "/", "worker_fullscreen");
  clear_attach_block();
});
on('#ajax', 'click', '.c_ucm_doc_list_repost', function() {
  parent = this.parentElement.parentElement;
  pk = parent.getAttribute('data-pk');
  create_fullscreen("/docs/repost/c_ucm_list_window/" + pk + "/", "worker_fullscreen");
  clear_attach_block();
});
