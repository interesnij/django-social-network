on('#ajax', 'click', '.u_all_good_likes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/goods/window/all_user_like/" + uuid + "/", loader)
});
on('#ajax', 'click', '.u_all_good_dislikes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/goods/window/all_user_dislike/" + uuid + "/", loader)
});

on('#ajax', 'click', '.u_all_good_comment_likes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/goods/window/all_user_comment_like/" + pk + "/", loader)
});
on('#ajax', 'click', '.u_all_good_comment_dislikes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/goods/window/all_user_comment_dislike/" + pk + "/", loader)
});

on('#ajax', 'click', '.u_all_good_reposts', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/goods/window/all_user_reposts/" + uuid + "/", loader)
});

on('#ajax', 'click', '.u_good_comments', function() {
  clear_comment_dropdown();
  data = document.body.querySelector(".data_display");
  pk = data.getAttribute("user-pk");
  uuid = data.getAttribute("data-uuid");
  url = "/goods/user_progs/comment/" + uuid + "/" + pk + "/";
  list_load(data.querySelector(".u_load_comments"), url);
  this.classList.toggle("comments_open");
});
