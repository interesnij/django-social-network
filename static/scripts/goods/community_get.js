on('#ajax', 'click', '.c_all_good_likes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  good_pk = container.getAttribute('good-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/goods/window/all_community_like/" + pk + "/" + good_pk + "/", loader)
});
on('#ajax', 'click', '.c_all_good_dislikes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  good_pk = container.getAttribute('good-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/goods/window/all_community_dislike/" + pk + "/" + good_pk + "/", loader)
});
on('#ajax', 'click', '.c_goods_list_create_window', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  loader = document.getElementById("create_loader");
  open_fullscreen("/goods/community_progs/add_album/" + pk + "/", loader)
});

on('#ajax', 'click', '.c_good_list_edit_window', function() {
  body = document.body.querySelector(".pk_saver");
  pk = body.getAttribute("data-pk");
  uuid = body.getAttribute("data-uuid");
  loader = document.getElementById("create_loader");
  open_fullscreen("/goods/community_progs/edit_album/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.c_ucm_good_repost', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement
  good_pk = container.getAttribute('good-pk');
  parent.getAttribute('data-pk') ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/goods/repost/c_ucm_good_window/" + pk + "/" + good_pk + "/", loader);
  clear_attach_block();
})
on('#ajax', 'click', '.c_ucm_good_list_repost', function() {
  parent = this.parentElement;
  parent.getAttribute("data-pk") ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  parent.getAttribute("data-uuid") ? uuid = parent.getAttribute('data-uuid') : uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/goods/repost/c_ucm_list_window/" + pk + "/" + uuid + "/", loader);
  clear_attach_block();
})

on('#ajax', 'click', '.c_good_detail', function() {
  this.getAttribute('data-uuid') ? uuid = this.getAttribute('data-uuid') : uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid')
  pk = this.getAttribute('good-pk');
  loader = document.getElementById("good_loader");
  open_fullscreen('/goods/community/good/' + pk + '/' + uuid + '/', loader);
  setTimeout(function() {good_gallery(loader)}, 1000)
});
on('#ajax', 'click', '.c_all_good_comment_likes', function() {12
  container = this.parentElement.parentElement.parentElement;
  comment_pk = container.getAttribute('comment-pk');
  pk = container.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/goods/window/all_community_comment_like/" + pk + "/" + comment_pk + "/", loader)
});
on('#ajax', 'click', '.c_all_good_comment_dislikes', function() {
  container = this.parentElement.parentElement.parentElement;
  comment_pk = container.getAttribute('comment-pk');
  pk = container.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/goods/window/all_community_comment_dislike/" + pk + "/" + comment_pk + "/", loader)
});

on('#ajax', 'click', '.c_all_good_reposts', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  good_pk = container.getAttribute('good-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/goods/window/all_community_reposts/" + good_pk + "/", loader)
});

on('#ajax', 'click', '.c_good_comments', function() {
  clear_comment_dropdown();
  block = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = block.getAttribute("data-pk");
  good_pk = block.getAttribute("good-pk");
  url = "/goods/community/comment/" + good_pk + "/" + pk + "/";
  list_load(block.querySelector(".c_load_comments"), url);
  this.classList.toggle("comments_open");
});
