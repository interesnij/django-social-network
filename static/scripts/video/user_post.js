

on('#ajax', 'click', '.u_videoComment', function() {
  form = this.parentElement.parentElement.parentElement;
  send_comment(form, form.parentElement.previousElementSibling, '/video/user_progs/post-comment/');
});

on('#ajax', 'click', '.u_replyVideoComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  block = form.parentElement.parentElement.querySelector(".stream_reply_comments");
  send_comment(form, block, '/video/user_progs/reply-comment/')
  form.parentElement.style.display = "none";
  block.classList.add("replies_open")
});

on('#ajax', 'click', '.u_replyParentVideoComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  block = form.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  send_comment(form, block.parentElement, '/video/user_progs/reply-comment/')
  form.parentElement.style.display = "none";
  block.classList.add("replies_open")
});

on('#ajax', 'click', '.u_video_off_comment', function() {
  send_photo_change(this, "/video/user_progs/off_comment/", "u_video_on_comment", "Вкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".u_video_comments").style.display = "none"
})
on('#ajax', 'click', '.u_video_on_comment', function() {
  send_photo_change(this, "/video/user_progs/on_comment/", "u_video_off_comment", "Выкл. комментарии");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".u_video_comments").style.display = "unset"
})

on('#ajax', 'click', '.u_video_comment_delete', function() {
  comment_delete(this, "/video/user_progs/delete_comment/", "u_video_comment_abort_remove")
})
on('#ajax', 'click', '.u_video_comment_abort_remove', function() {
  comment_abort_delete(this, "/video/user_progs/abort_delete_comment/")
});

on('#ajax', 'click', '.u_video_off_private', function() {
  send_photo_change(this, "/video/user_progs/off_private/", "u_video_on_private", "Вкл. приватность")
})
on('#ajax', 'click', '.u_video_on_private', function() {
  send_photo_change(this, "/video/user_progs/on_private/", "u_video_off_private", "Выкл. приватность")
})

on('#ajax', 'click', '.u_video_edit', function() {
  this.parentElement.nextElementSibling.style.display = "block"
})

on('#ajax', 'click', '.u_video_off_votes', function() {
  send_photo_change(this, "/video/user_progs/off_votes/", "u_video_on_votes", "Вкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "none";
  post.querySelector(".dislike").style.display = "none";
})
on('#ajax', 'click', '.u_video_on_votes', function() {
  send_photo_change(this, "/video/user_progs/on_votes/", "u_video_off_votes", "Выкл. реакции");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".like").style.display = "unset";
  post.querySelector(".dislike").style.display = "unset";
})

on('#ajax', 'click', '.user_video_remove', function() {
  send_photo_change(this, "/video/user_progs/delete/", "user_video_abort_remove", "Отмена");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  this.parentElement.parentElement.nextElementSibling.style.display = "none";
  post.querySelector(".order-2").style.display = "none";
  post.querySelector(".card").style.opacity = "0.5";
  this.style.color = "#FF0000";
})
on('#ajax', 'click', '.user_video_abort_remove', function() {
  send_photo_change(this, "/video/user_progs/abort_delete/", "user_video_remove", "Удалить");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  this.parentElement.parentElement.nextElementSibling.style.display = "unset";
  post.querySelector(".order-2").style.display = "unset";
  post.querySelector(".card").style.opacity = "1";
})

on('#ajax', 'click', '.u_video_like', function() {
  video = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = video.getAttribute("data-uuid");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_like(video, "/video/votes/user_like/" + uuid + "/" + pk + "/");
  vote_reload("/video/video_window/u_like_window/" + uuid + "/", "/video/video_window/u_dislike_window/" + uuid + "/", this.nextElementSibling, this.nextElementSibling.nextElementSibling.nextElementSibling)
});
on('#ajax', 'click', '.u_video_dislike', function() {
  video = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = video.getAttribute("data-uuid");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_dislike(video, "/video/votes/user_dislike/" + uuid + "/" + pk + "/");
  vote_reload("/video/video_window/u_like_window/" + uuid + "/", "/video/video_window/u_dislike_window/" + uuid + "/", this.previousElementSibling, this.nextElementSibling)
});
on('#ajax', 'click', '.u_video_like2', function() {
  _this = this;
  video = _this.parentElement;
  comment_pk = video.getAttribute("data-pk");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_like(video, "/video/votes/user_comment/" + comment_pk + "/" + pk + "/like/");
  vote_reload("/video/video_window/u_comment_like_window/" + comment_pk + "/", "/video/video_window/u_comment_dislike_window/" + comment_pk + "/", _this.nextElementSibling, _this.nextElementSibling.nextElementSibling.nextElementSibling)
});
on('#ajax', 'click', '.u_video_dislike2', function() {
  _this = this;
  video = _this.parentElement;
  comment_pk = video.getAttribute("data-pk");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  send_dislike(video, "/video/votes/user_comment/" + comment_pk + "/" + pk + "/dislike/");
  vote_reload("/video/video_window/u_comment_like_window/" + comment_pk + "/", "/video/video_window/u_comment_dislike_window/" + comment_pk + "/", _this.previousElementSibling, _this.nextElementSibling)
});
