
on('#ajax', 'click', '.c_videoComment', function() {
  form = this.parentElement.parentElement.parentElement;
  send_comment(form, form.parentElement.previousElementSibling, '/video/community_progs/post-comment/');
});

on('#ajax', 'click', '.c_replyVideoComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  block = form.parentElement.parentElement.querySelector(".stream_reply_comments");
  send_comment(form, block, '/video/community_progs/reply-comment/')
  form.parentElement.style.display = "none";
  block.classList.add("replies_open")
});

on('#ajax', 'click', '.c_replyParentVideoComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  block = form.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  send_comment(form, block.parentElement, '/video/community_progs/reply-comment/')
  form.parentElement.style.display = "none";
  block.classList.add("replies_open")
});

on('#ajax', 'click', '.c_video_off_comment', function() {
  send_photo_change(this, "/video/community_progs/off_comment/", "c_video_on_comment", "Вкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".c_video_comments").style.display = "none"
})
on('#ajax', 'click', '.c_video_on_comment', function() {
  send_photo_change(this, "/video/community_progs/on_comment/", "c_video_off_comment", "Выкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".c_video_comments").style.display = "unset"
})

on('#ajax', 'click', '.c_video_comment_delete', function() {
  comment_delete(this, "/video/community_progs/delete_comment/", "c_video_comment_abort_remove")
})
on('#ajax', 'click', '.c_video_comment_abort_remove', function() {
  comment_abort_delete(this, "/video/community_progs/abort_delete_comment/")
});


on('#ajax', 'click', '.u_video_off_private', function() {
  send_photo_change(this, "/video/community_progs/off_private/", "c_video_on_private", "Вкл. приватность")
})
on('#ajax', 'click', '.c_video_on_private', function() {
  send_photo_change(this, "/video/community_progs/on_private/", "c_video_off_private", "Выкл. приватность")
})

on('#ajax', 'click', '.c_video_off_votes', function() {
  send_photo_change(this, "/video/community_progs/off_votes/", "c_video_on_votes", "Вкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "none";
  post.querySelector(".dislike").style.display = "none";
})
on('#ajax', 'click', '.c_video_on_votes', function() {
  send_photo_change(this, "/video/community_progs/on_votes/", "c_video_off_votes", "Выкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "unset";
  post.querySelector(".dislike").style.display = "unset";
})

on('#ajax', 'click', '.community_video_remove', function() {
  send_photo_change(this, "/video/community_progs/delete/", "community_video_abort_remove", "Отмена");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  this.parentElement.parentElement.nextElementSibling.style.display = "none";
  post.querySelector(".order-2").style.display = "none";
  post.querySelector(".card").style.opacity = "0.5";
  this.style.color = "#FF0000";
})
on('#ajax', 'click', '.community_video_abort_remove', function() {
  send_photo_change(this, "/video/community_progs/abort_delete/", "community_video_remove", "Удалить");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  this.parentElement.parentElement.nextElementSibling.style.display = "unset";
  post.querySelector(".order-2").style.display = "unset";
  post.querySelector(".card").style.opacity = "1";
})

on('#ajax', 'click', '.c_video_like', function() {
  video = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = document.body.querySelector(".data_display").getAttribute("data-uuid");
  pk = document.body.querySelector(".data_display").getAttribute("data-pk");
  send_like(video, "/video/votes/community_like/" + uuid + "/" + pk + "/");
  vote_reload("/video/video_window/c_like_window/" + uuid + "/", "/video/video_window/c_dislike_window/" + uuid + "/", this.nextElementSibling, this.nextElementSibling.nextElementSibling.nextElementSibling)
});
on('#ajax', 'click', '.c_video_dislike', function() {
  video = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = document.body.querySelector(".data_display").getAttribute("data-uuid");
  pk = document.body.querySelector(".data_display").getAttribute("data-pk");
  send_dislike(video, "/video/votes/community_dislike/" + uuid + "/" + pk + "/");
  vote_reload("/video/video_window/c_like_window/" + uuid + "/", "/video/video_window/c_dislike_window/" + uuid + "/", this.previousElementSibling, this.nextElementSibling)
});
on('#ajax', 'click', '.c_video_like2', function() {
  _this = this;
  video = _this.parentElement;
  comment_pk = video.getAttribute("data-pk");
  send_like(video, "/video/votes/community_comment/" + comment_pk + "/like/");
  vote_reload("/video/video_window/c_comment_like_window/" + comment_pk + "/", "/video/video_window/c_comment_dislike_window/" + comment_pk + "/", _this.nextElementSibling, _this.nextElementSibling.nextElementSibling.nextElementSibling)
});
on('#ajax', 'click', '.c_video_dislike2', function() {
  _this = this;
  video = _this.parentElement;
  comment_pk = video.getAttribute("data-pk");
  send_dislike(video, "/video/votes/community_comment/" + comment_pk + "/" + "/dislike/");
  vote_reload("/video/video_window/c_comment_like_window/" + comment_pk + "/", "/video/video_window/c_comment_dislike_window/" + comment_pk + "/", _this.previousElementSibling, _this.nextElementSibling)
});
