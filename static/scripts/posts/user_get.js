on('#ajax', 'click', '.fullscreen', function() {
  container = this.parentElement;
  uuid = container.getAttribute('data-uuid');
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  loader = document.getElementById("item_loader");
  open_fullscreen("/users/detail/post/" + pk + "/" + uuid + "/", loader)
})

on('#ajax', 'click', '.u_article_detail', function() {
  uuid = this.parentElement.getAttribute("data-uuid");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  loader = document.getElementById("article_loader");
  open_fullscreen("/article/detail/" + pk + "/" + uuid + "/", loader)
});

on('body', 'click', '#u_multi_comments_photos', function(event) {
  this.previousElementSibling.click();
})

on('#ajax', 'click', '.u_all_posts_likes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/posts/item_window/all_user_like/" + uuid + "/", loader)
});
on('#ajax', 'click', '.u_all_posts_dislikes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/posts/item_window/all_user_dislike/" + uuid + "/", loader)
});

on('#ajax', 'click', '.u_all_posts_comment_likes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/posts/item_window/all_user_comment_like/" + pk + "/", loader)
});
on('#ajax', 'click', '.u_all_posts_comment_dislikes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/posts/item_window/all_user_comment_dislike/" + pk + "/", loader)
});

on('#ajax', 'click', '.u_all_item_reposts', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/posts/item_window/all_user_reposts/" + uuid + "/", loader)
});

on('#ajax', 'click', '.u_item_comments', function() {
  clear_comment_dropdown();
  parent = this.parentElement.parentElement.parentElement.parentElement;
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  uuid = parent.getAttribute("data-uuid");
  //this.parentElement.parentElement.nextElementSibling.classList.toggle("comments_open");
  url = "/posts/user/comment/" + uuid + "/" + pk + "/";
  list_load(parent.querySelector(".u_load_comments"), url);
  this.classList.toggle("comments_open");
});

on('#ajax', 'click', '.u_comment_photo', function() {
  this.classList.add("current_file_dropdown");
  document.body.querySelector(".attach_block") ? (attach_block = document.body.querySelector(".attach_block"), attach_block.innerHTML = "", attach_block.classList.remove("attach_block")) : null;
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/u_img_comment_load/', loader)
});
on('#ajax', 'click', '.u_comment_video', function() {
  this.classList.add("current_file_dropdown");
  clear_attach_block();
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/u_video_load/', loader)
});
on('#ajax', 'click', '.u_comment_music', function() {
  this.classList.add("current_file_dropdown");
  clear_attach_block();
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/u_music_load/', loader)
});
on('#ajax', 'click', '.u_comment_good', function() {
  this.classList.add("current_file_dropdown");
  clear_attach_block();
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/u_good_load/', loader)
});
on('#ajax', 'click', '.u_comment_article', function() {
  this.classList.add("current_file_dropdown");
  clear_attach_block();
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/u_article_load/', loader)
});

on('#ajax', 'click', '.u_select_photo', function() {
  this.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/u_img_load/', loader)
});
on('#ajax', 'click', '.u_select_video', function() {
  this.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/u_video_load/', loader)
});
on('#ajax', 'click', '.u_select_music', function() {
  this.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/u_music_load/', loader)
});
on('#ajax', 'click', '.u_select_good', function() {
  this.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/u_good_load/', loader)
});
on('#ajax', 'click', '.u_select_article', function() {
  this.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/u_article_load/', loader)
});

on('#ajax', 'click', '.delete_thumb', function(e) {
  e.preventDefault();
  this.nextElementSibling.remove();
  block = document.createElement("div");
  this.parentElement.innerHTML = "<h4>Изображение</h4><i>(обязательно)</i>";
  this.remove();
})
