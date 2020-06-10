on('#ajax', 'click', '.avatar_detail', function() {
  var uuid, pk, loader;
  pk = this.getAttribute('photo-pk');
  uuid = document.body.querySelector(".pk_saver").getAttribute("data-uuid");
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/load/avatar_detail/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.fullscreen', function() {
  var container, uuid, pk, loader;
  container = this.parentElement;
  uuid = container.getAttribute('item-uuid'); 
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  loader = document.getElementById("item_loader");
  open_fullscreen("/users/detail/item/" + pk + "/" + uuid + "/", loader)
})

on('#ajax', 'click', '.u_article_detail', function() {
  uuid = this.parentElement.getAttribute("item-uuid");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  loader = document.getElementById("article_loader");
  open_fullscreen("/article/detail/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '#article_add', function() {
  var pk = this.getAttribute('data-pk');
  open_fullscreen("/article/u_article_window/" + pk + "/", document.getElementById("create_loader"));
  //setTimeout(function() { CKEDITOR.replace('id_content'); CKEDITOR.instances.id_content.updateElement(); }, 1000);
});

on('#ajax', 'click', '.u_all_likes', function() {
  var container, uuid, pk, loader;
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  uuid = container.getAttribute('item-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/item_window/all_user_like/" + uuid + "/" + pk + "/", loader)
});
on('#ajax', 'click', '.u_all_dislikes', function() {
  var container, uuid, pk, loader;
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  uuid = container.getAttribute('item-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/item_window/all_user_dislike/" + uuid + "/" + pk + "/", loader)
});
on('#ajax', 'click', '.u_all_reposts', function() {
  var container, uuid, pk, loader;
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  uuid = container.getAttribute('item-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/item_window/all_user_reposts/" + uuid + "/" + pk + "/", loader)
});

on('#ajax', 'click', '.u_item_comments', function() {
  try{
  dropdowns = document.body.querySelectorAll(".current_file_dropdown");
  for (var i = 0; i < dropdowns.length; i++) {
    dropdowns[i].classList.remove("current_file_dropdown")
  }} catch { null }

  parent = this.parentElement.parentElement.parentElement.parentElement;
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  uuid = parent.getAttribute("item-uuid");
  //this.parentElement.parentElement.nextElementSibling.classList.toggle("comments_open");
  url = "/user/comment/" + uuid + "/" + pk + "/";
  list_load(parent.querySelector(".u_load_comments"), url);
  this.classList.toggle("comments_open");
});
on('#ajax', 'click', '.comments_open', function() {
  parent = this.parentElement.parentElement.nextElementSibling;
  parent.innerHTML="";
  this.classList.toggle("comments_open");  this.parentElement.parentElement.nextElementSibling.classList.toggle("comments_open");
});
