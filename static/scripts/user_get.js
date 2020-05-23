on('#ajax', 'click', '.avatar_detail', function() {
  var uuid, pk, loader;
  uuid = this.getAttribute('data-uuid');
  pk = this.getAttribute('data-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/load/avatar_detail/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.fullscreen', function() {
  var container, uuid, pk, loader;
  container = this.parentElement;
  uuid = container.getAttribute('item-uuid');
  pk = container.parentElement.getAttribute('user-pk');
  loader = document.getElementById("item_loader");
  open_fullscreen("/users/detail/item/" + pk + "/" + uuid + "/", loader)
})

on('#ajax', 'click', '.u_article_detail', function() {
  var container, uuid, pk, loader;
  container = this.parentElement;
  uuid = container.getAttribute('item-uuid');
  pk = container.parentElement.getAttribute('user-pk');
  loader = document.getElementById("article_loader");
  open_fullscreen("/users/detail/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '#article_add', function() {
  var pk = this.getAttribute('data-pk');
  open_fullscreen("/article/u_article_window/" + pk + "/", document.getElementById("create_loader"));
  CKEDITOR.replace('id_content', { height: 100 });
});

on('#ajax', 'click', '.u_all_likes', function() {
  var container, uuid, pk, loader;
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = container.parentElement.getAttribute('user-pk');
  uuid = container.getAttribute('item-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/item_window/all_user_like/" + uuid + "/" + pk + "/", loader)
});
on('#ajax', 'click', '.u_all_dislikes', function() {
  var container, uuid, pk, loader;
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = container.parentElement.getAttribute('user-pk');
  uuid = container.getAttribute('item-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/item_window/all_user_dislike/" + uuid + "/" + pk + "/", loader)
});
on('#ajax', 'click', '.u_all_reposts', function() {
  var container, uuid, pk, loader;
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = container.parentElement.getAttribute('user-pk');
  uuid = container.getAttribute('item-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/item_window/all_user_reposts/" + uuid + "/" + pk + "/", loader)
});

on('#ajax', 'click', '.u_item_comments.comments_close', function() {
  var parent, pk, uuid, url
  parent = this.parentElement.parentElement.parentElement.parentElement;
  pk = parent.parentElement.getAttribute("user-pk");
  uuid = parent.getAttribute("item-uuid");
  _this = parent.querySelector(".u_item_comments");
  _this.classList.add("comments_open");
  _this.classList.remove("comments_close");
  url = "/user/comment/" + uuid + "/" + pk + "/";
  list_load(parent.querySelector(".u_load_comments"), url);
});
on('#ajax', 'click', '.u_item_comments.comments_open', function() {
  parent = this.parentElement.parentElement.parentElement;
  container = parent.querySelector(".u_load_comments");
  container.innerHTML="";
  _this = parent.querySelector(".u_item_comments");
  _this.classList.add("comments_close");
  _this.classList.remove("comments_open");
});
