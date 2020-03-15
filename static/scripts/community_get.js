
$('#ajax').on('click', '#community_add', function() {$('#community_loader').html('').load("/communities/progs/add/");$('.community_fullscreen').show();console.log("add community open")})
$('#ajax').on('click', '#community_article_add', function() {btn = $(this);pk = btn.data('pk');$('#article_loader').html('').load("/article/add_community/" + pk + "/");$('.article_fullscreen').show();console.log("add community article open")})


on('#ajax', 'click', '.c_comment.comments_close', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement;
  container = parent.querySelector(".load_comments");
  pk = parent.parentElement.getAttribute("community-id");
  uuid = parent.getAttribute("item-id");
  container = parent.querySelector(".load_comments");
  url = "/community/comment/" + uuid + "/" + pk + "/";
  list_load(container, url);
  this.classList.add("comments_open");
  this.classList.remove("comments_close");
});
on('#ajax', 'click', '.c_comment.comments_open', function() {
  parent = this.parentElement.parentElement;
  container = parent.querySelector(".load_comments");
  container.innerHTML="";
  this.classList.add("comments_close");
  this.classList.remove("comments_open");
});
on('#ajax', 'click', '.c_all_likes', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = parent.parentElement.getAttribute("community-id");
  uuid = parent.getAttribute("item-id");
  loader = document.getElementById("votes_loader");
  url = "/window/all_community_like/" + uuid + "/" + pk + "/";
  list_load(loader, url);
  loader.parentElement.style.display = "block";
});
on('#ajax', 'click', '.c_all_dislikes', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = parent.parentElement.getAttribute("community-id");
  uuid = parent.getAttribute("item-id");
  loader = document.getElementById("votes_loader");
  url = "/window/all_community_dislike/" + uuid + "/" + pk + "/";
  list_load(loader, url);
  loader.parentElement.style.display = "block";
});
on('#ajax', 'click', '.c_all_reposts', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = parent.parentElement.getAttribute("community-id");
  uuid = parent.getAttribute("item-id");
  loader = document.getElementById("votes_loader");
  url = "/window/all_community_reposts/" + uuid + "/" + pk + "/";
  list_load(loader, url);
  loader.parentElement.style.display = "block";
});
on('#ajax', 'click', '.show_staff_window', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = parent.getAttribute("data-pk");
  uuid = parent.getAttribute("data-uuid");
  loader = document.getElementById("load_staff_window");
  url = "/communities/manage/staff_window/" + pk + "/" + uuid + "/";
  list_load(loader, url);
  loader.parentElement.style.display = "block";
});
on('#ajax', 'click', '.c_fullscreen', function() {
  parent = this.parentElement; parent2 = parent.parentElement;
  pk = parent2.getAttribute("community-id");
  uuid = parent.getAttribute("item-id");
  loader = document.getElementById("item_loader");
  url = "/communities/item/" + pk + "/" + uuid + "/";
  list_load(loader, url);
  loader.parentElement.style.display = "block";
});
on('#ajax', 'click', '.c_article_detail', function() {
  parent = this.parentElement; parent2 = parent.parentElement;
  pk = parent2.getAttribute("community-id");
  uuid = parent.getAttribute("item-id");
  loader = document.getElementById("article_loader");
  url = "/article/read/" + pk + "/" + uuid + "/"
  list_load(loader, url);
  loader.parentElement.style.display = "block";
});
on('#ajax', 'click', '.community_fullscreen_hide', function() {document.querySelector(".community_fullscreen").style.display = "none";document.getElementById("community_loader").innerHTML=""});
on('#ajax', 'click', '.community_manage_fullscreen_hide', function() {document.querySelector(".manage_window_fullscreen").style.display = "none";document.getElementById("load_staff_window").innerHTML=""});
