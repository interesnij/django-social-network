on('#ajax', 'click', '.user_create_chat', function() {
  loader = document.getElementById("create_loader");
  pk = this.getAttribute("data-pk");
  open_fullscreen("/chat/chat_progs/create_chat/" + pk + "/", loader)
});

on('#ajax', 'click', '.user_add_members', function() {
  block = this.parentElement.parentElement.parentElement.querySelector("#chat_members");
  list_load(block, "/users/load/friends/")
})
