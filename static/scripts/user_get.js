on('#ajax', 'click', '.avatar_detail', function() {
  var uuid, pk, loader;
  uuid = this.getAttribute('data-uuid');
  pk = this.getAttribute('data-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/load/avatar_detail/" + pk + "/" + uuid + "/", loader)
});


function dragElement(elmnt) {
  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  document.getElementById("draggable-header").onmousedown = dragMouseDown;
	document.getElementById("draggable-resize").onmousedown = resizeMouseDown;

  function dragMouseDown(e) {
    e = e || window.event;
    e.preventDefault();
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    document.onmousemove = elementDrag;
  }

	function resizeMouseDown(e) {
    e = e || window.event;
    e.preventDefault();
    pos3 = 0;
    pos4 = 0;
    document.onmouseup = closeDragElement;
    document.onmousemove = elementResize;
  }

	function elementResize(e) {
		e = e || window.event;
    e.preventDefault();
		var content = document.getElementById("draggable");
		var width = content.offsetWidth;
		var height = content.offsetHeight;

		pos1 = (e.clientX - width) - content.offsetLeft;
    pos2 = (e.clientY - height) - content.offsetTop;

		content.style.width = width + pos1 + 'px';
		content.style.height = height + pos2 + 'px';
	}

  function elementDrag(e) {
    e = e || window.event;
    e.preventDefault();
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
    elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
  }

  function closeDragElement() {
    document.onmouseup = null;
    document.onmousemove = null;
  }
}

on('#ajax', 'click', '.u_video_detail', function() {
  var uuid, pk, loader;
  counter = this.getAttribute('data-counter');
  parent = this.parentElement.parentElement;
  pk = parent.getAttribute('data-pk');
  uuid = parent.getAttribute('data-uuid');
  loader = document.getElementById("video_loader");
  open_fullscreen("/video/get_video_playlist/" + pk + "/" + uuid + "/", loader);
  video_saver = document.body.querySelector("#video_id_saver");
  video_player_id = video_saver.getAttribute('data-video');
  video_saver.setAttribute('data-video', video_player_id + "a");
  setTimeout(function() {
    load_video_playlist(video_player_id + "a", counter);
    video_player.addListener(FWDUVPlayer.READY, onReady);
    function onReady(){
    console.log("video player ready");
    setTimeout(function() {video_player.playVideo(counter);video_player.play()}, 1000);
    }
  }, 500);
});

on('body', 'click', '.video_fullscreen_resize', function() {
  video_window = document.querySelector(".video_fullscreen");
  video_window.classList.add("video_fullscreen_resized", "video_draggable");
  document.body.querySelector(".video_btn_big").style.display = "none";
  document.body.querySelector(".video_btn_small").style.display = "block";
  get_resize_screen();

});
on('body', 'click', '.video_fullscreen_normal', function() {
  video_window = document.querySelector(".video_fullscreen");
  video_window.classList.remove("video_fullscreen_resized");
  document.body.querySelector(".video_btn_small").style.display = "none";
  document.body.querySelector(".video_btn_big").style.display = "block";
  get_normal_screen()
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
  open_fullscreen("/article/add_user/" + pk + "/", document.getElementById("community_loader"))
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
