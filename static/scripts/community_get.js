
on('#ajax', 'click', '.c_fullscreen', function() {
  var uuid, pk, loader;
  uuid = this.parentElement.getAttribute('item-uuid');
  pk = document.body.querySelector(".pk_saver").getAttribute('community-pk');
  loader = document.getElementById("item_loader");
  open_fullscreen("/communities/item/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.c_avatar_detail', function() {
  uuid = this.getAttribute('photo-uuid');
  pk = document.body.querySelector(".pk_saver").getAttribute("community-pk");
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/load/c_avatar_detail/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.c_article_detail', function() {
  var uuid, pk, loader;
  uuid = this.parentElement.getAttribute('item-uuid');
  pk = document.body.querySelector(".pk_saver").getAttribute('community-pk');
  loader = document.getElementById("article_loader");
  open_fullscreen("/article/read/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.show_staff_window', function() {
  var parent, pk, uuid, loader
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = parent.getAttribute("data-pk");
  uuid = parent.getAttribute("data-uuid");
  loader = document.getElementById("load_staff_window");
  open_fullscreen("/communities/manage/staff_window/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.c_all_likes', function() {
  var container, uuid, pk, loader;
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = container.getAttribute('community-pk');
  uuid = container.getAttribute('item-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/posts/item_window/all_community_like/" + uuid + "/" + pk + "/", loader)
});
on('#ajax', 'click', '.c_all_dislikes', function() {
  var container, uuid, pk, loader;
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = container.getAttribute('community-pk');
  uuid = container.getAttribute('item-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/posts/item_window/all_community_dislike/" + uuid + "/" + pk + "/", loader)
});
on('#ajax', 'click', '.c_all_reposts', function() {
  var container, uuid, pk, loader;
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = container.getAttribute('community-pk');
  uuid = container.getAttribute('item-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/posts/item_window/all_community_reposts/" + uuid + "/" + pk + "/", loader)
});

on('#ajax', 'click', '#community_article_add', function() {
  var pk = this.getAttribute('data-pk');
  open_fullscreen("/article/c_article_window/" + pk + "/", document.getElementById("create_loader"))
});


on('#ajax', 'click', '.c_item_comments.comments_close', function() {
  try{
  dropdowns = document.body.querySelectorAll(".current_file_dropdown");
  for (var i = 0; i < dropdowns.length; i++) {
    dropdowns[i].classList.remove("current_file_dropdown");
  }} catch { null }
  parent = this.parentElement.parentElement.parentElement.parentElement;
  pk = document.body.querySelector(".pk_saver").getAttribute("community-pk");
  uuid = parent.getAttribute("item-uuid");
  _this = parent.querySelector(".c_item_comments");
  this.className = '';
  this.classList.add("c_item_comments","comments_open");
  list_load(this.parentElement.parentElement.parentElement.querySelector(".c_load_comments"), "/posts/community/comment/" + uuid + "/" + pk + "/");
});
on('#ajax', 'click', '.c_item_comments.comments_open', function() {
  parent = this.parentElement.parentElement.parentElement;
  _this = parent.querySelector(".c_load_comments");
  _this.innerHTML="";
  this.className = '';
  this.classList.add("c_item_comments","comments_close");
});
