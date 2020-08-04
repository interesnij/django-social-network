on('#ajax', 'click', '.u_news_fullscreen', function() {
  container = this.parentElement;
  uuid = container.getAttribute('data-uuid');
  pk = container.getAttribute("data-pk");
  loader = document.getElementById("item_loader");
  open_fullscreen("/users/detail/post/" + pk + "/" + uuid + "/", loader)
})

on('#ajax', 'click', '.u_news_item_comments', function() {
  clear_comment_dropdown();
  parent = this.parentElement.parentElement.parentElement.parentElement;
  pk = parent.getAttribute("data-pk");
  uuid = parent.getAttribute("data-uuid");
  url = "/posts/user/comment/" + uuid + "/" + pk + "/";
  list_load(parent.querySelector(".u_load_comments"), url);
  this.classList.toggle("comments_open");
});

on('#ajax', 'click', '.u_news_wall_image', function() {
  uuid = this.getAttribute('data-uuid');
  pk = this.getAttribute("data-pk");
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/load/user_wall/" + pk + "/" + uuid + "/", loader)
});
