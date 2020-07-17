on('#ajax', 'click', '.c_all_video_likes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/video/window/all_community_like/" + uuid + "/", loader)
});
on('#ajax', 'click', '.c_all_video_dislikes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/video/window/all_community_dislike/" + uuid + "/", loader)
});

on('#ajax', 'click', '.c_all_video_comment_likes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/video/window/all_community_comment_like/" + pk + "/", loader)
});
on('#ajax', 'click', '.c_all_video_comment_dislikes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/video/window/all_community_comment_dislike/" + pk + "/", loader)
});

on('#ajax', 'click', '.c_all_video_reposts', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/video/window/all_community_reposts/" + uuid + "/", loader)
});

on('#ajax', 'click', '.c_video_comments', function() {
  clear_comment_dropdown();
  data = document.body.querySelector(".data_display");
  pk = data.getAttribute("data-pk");
  uuid = data.getAttribute("data-uuid");
  url = "/video/community_progs/comment/" + uuid + "/" + pk + "/";
  list_load(data.querySelector(".c_load_comments"), url);
  this.classList.toggle("comments_open");
});
