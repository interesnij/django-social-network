
on('#ajax', 'click', '.c_fullscreen', function() {
  uuid = this.parentElement.getAttribute('data-uuid');
  pk = document.body.querySelector(".pk_saver").getAttribute('community-pk');
  loader = document.getElementById("item_loader");
  open_fullscreen("/communities/item/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.c_avatar_detail', function() {
  uuid = this.getAttribute('photo-uuid');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/load/community_avatar_detail/" + uuid + "/", loader)
});

on('#ajax', 'click', '.c_article_detail', function() {
  var uuid, pk, loader;
  uuid = this.parentElement.getAttribute('data-uuid');
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

on('#ajax', 'click', '.c_all_posts_likes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('item-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/posts/item_window/all_community_like/" + uuid + "/", loader)
});
on('#ajax', 'click', '.c_all_posts_dislikes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('item-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/posts/item_window/all_community_dislike/" + uuid + "/", loader)
});
on('#ajax', 'click', '.c_all_item_reposts', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('item-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/posts/item_window/all_community_reposts/" + uuid + "/", loader)
});

on('#ajax', 'click', '.c_all_posts_comment_likes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/posts/item_window/all_community_comment_like/" + pk + "/", loader)
});
on('#ajax', 'click', '.c_all_posts_comment_dislikes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/posts/item_window/all_community_comment_dislike/" + pk + "/", loader)
});

on('#ajax', 'click', '#community_article_add', function() {
  var pk = this.getAttribute('data-pk');
  open_fullscreen("/article/c_article_window/" + pk + "/", document.getElementById("create_loader"))
});


on('#ajax', 'click', '.c_item_comments', function() {
  clear_comment_dropdown();
  parent = this.parentElement.parentElement.parentElement.parentElement;
  pk = document.body.querySelector(".pk_saver").getAttribute("community-pk");
  uuid = parent.getAttribute("item-uuid");
  //this.parentElement.parentElement.nextElementSibling.classList.toggle("comments_open");
  url = "/posts/community/comment/" + uuid + "/" + pk + "/";
  list_load(parent.querySelector(".c_load_comments"), url);
  this.classList.toggle("comments_open");
});
