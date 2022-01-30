
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
