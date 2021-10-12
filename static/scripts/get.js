on('#ajax', 'click', '.load_next_list_comments', function() {
  _this = this;
    var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    ajax_link.open('GET', _this.getAttribute("data-link"), true);
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            elem_ = document.createElement('span');
            elem_.innerHTML = ajax_link.responseText;

            elem_2 = document.createElement('span');
            elem_2.innerHTML = elem_.querySelector(".stream_comments").innerHTML
            _this.parentElement.append(elem_2);
            _this.remove();
            fullscreen_resize();
        }
    }
    ajax_link.send()
});

on('#ajax', 'keydown', '.new_element_text', function(e) {
  if (e.shiftKey && e.keyCode === 8) {
    e.preventDefault();
    console.log(e.previousElementSibling)
    e.remove();
  }
  else if (e.keyCode == 13) {
    e.preventDefault();
    this.append("\n\n");
  }
});

on('#ajax', 'click', '.u_add_survey', function() {
  create_fullscreen('/survey/user_progs/add/', "worker_fullscreen");
});

on('#ajax', 'click', '.hide_comment_form', function() {
  block = this.parentElement.parentElement.parentElement.parentElement.parentElement
  block.querySelector(".col").style.display = "block";
  block.querySelector(".comment_text").style.display = "block";
  block.querySelector(".attach_container") ? block.querySelector(".attach_container").style.display = "block" : null;
  this.parentElement.parentElement.parentElement.remove();
});

on('#ajax', 'resize', '#fullscreen_loader', function() {
  console.log("resize!");
});

on('#ajax', 'click', '.smile_dropdown', function() {
  block = this.nextElementSibling;
  if (!block.querySelector(".card")) {
    list_load(block, "/users/load/smiles/")
  };
  block.classList.toggle("show");
});

on('#ajax', 'click', '.comment_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  if (form.classList.contains("u_post_comment")) {
  send_comment(form, form.parentElement.previousElementSibling, '/posts/user_progs/add_comment/')
} else if (form.classList.contains("c_post_comment")) {
  send_comment(form, form.parentElement.previousElementSibling, '/posts/community_progs/add_comment/')
} else if (form.classList.contains("u_video_comment")) {
  send_comment(form, form.parentElement.previousElementSibling, '/video/user_progs/add_comment/')
} else if (form.classList.contains("c_video_comment")) {
  send_comment(form, form.parentElement.previousElementSibling, '/video/community_progs/add_comment/')
} else if (form.classList.contains("u_photo_comment")) {
  send_comment(form, form.parentElement.previousElementSibling, '/gallery/user_progs/add_comment/')
} else if (form.classList.contains("c_photo_comment")) {
  send_comment(form, form.parentElement.previousElementSibling, '/gallery/community_progs/add_comment/')
} else if (form.classList.contains("u_good_comment")) {
  send_comment(form, form.parentElement.previousElementSibling, '/goods/user_progs/add_comment/')
} else if (form.classList.contains("c_good_comment")) {
  send_comment(form, form.parentElement.previousElementSibling, '/goods/community_progs/add_comment/')
}
});

on('#ajax', 'click', '.reply_comment_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  block = form.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement
  if (form.classList.contains("u_post_comment")) {
  send_comment(form, block, '/posts/user_progs/reply_comment/')
} else if (form.classList.contains("c_post_comment")) {
  send_comment(form, block, '/posts/community_progs/reply_comment/')
} else if (form.classList.contains("u_video_comment")) {
  send_comment(form, block, '/video/user_progs/reply_comment/')
} else if (form.classList.contains("c_video_comment")) {
  send_comment(form, block, '/video/community_progs/reply_comment/')
} else if (form.classList.contains("u_photo_comment")) {
  send_comment(form, block, '/gallery/user_progs/reply_comment/')
} else if (form.classList.contains("c_photo_comment")) {
  send_comment(form, block, '/gallery/community_progs/reply_comment/')
} else if (form.classList.contains("u_good_comment")) {
  send_comment(form, block, '/goods/user_progs/reply_comment/')
} else if (form.classList.contains("c_good_comment")) {
  send_comment(form, block, '/goods/community_progs/reply_comment/')
};
form.parentElement.style.display = "none";
block.classList.add("replies_open")
});

on('#ajax', 'click', '.reply_parent_btn', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  block = form.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  if (form.classList.contains("u_post_comment")) {
  send_comment(form, block, '/posts/user_progs/reply_comment/')
} else if (form.classList.contains("c_post_comment")) {
  send_comment(form, block, '/posts/community_progs/reply_comment/')
} else if (form.classList.contains("u_video_comment")) {
  send_comment(form, block, '/video/user_progs/reply_comment/')
} else if (form.classList.contains("c_video_comment")) {
  send_comment(form, block, '/video/community_progs/reply_comment/')
} else if (form.classList.contains("u_photo_comment")) {
  send_comment(form, block, '/gallery/user_progs/reply_comment/')
} else if (form.classList.contains("c_photo_comment")) {
  send_comment(form, block, '/gallery/community_progs/reply_comment/')
} else if (form.classList.contains("u_good_comment")) {
  send_comment(form, block, '/goods/user_progs/reply_comment/')
} else if (form.classList.contains("c_good_comment")) {
  send_comment(form, block, '/goods/community_progs/reply_comment/')
};
form.parentElement.style.display = "none";
block.classList.add("replies_open");
});

on('#ajax', 'click', '.tab_smiles', function() {
  if (!this.classList.contains("active")) {
    parent = this.parentElement.parentElement.parentElement;
    parent.querySelector(".stickers_panel").classList.remove("active", "show");
    parent.querySelector(".smiles_panel").classList.add("active", "show");
    this.classList.add("active");
    this.parentElement.querySelector(".tab_stickers").classList.remove("active");
  }
});
on('#ajax', 'click', '.tab_stickers', function() {
  if (!this.classList.contains("active")) {
    parent = this.parentElement.parentElement.parentElement;
    parent.querySelector(".smiles_panel").classList.remove("active", "show");
    parent.querySelector(".stickers_panel").classList.add("active", "show");
    this.classList.add("active");
    this.parentElement.querySelector(".tab_smiles").classList.remove("active");
  }
});

on('#ajax', 'click', '.previous_click', function() {
  this.previousElementSibling.click();
})
on('body', 'click', '.menu_drop', function() {
  block = this.nextElementSibling;
  if (block.classList.contains("show")) { block.classList.remove("show") }
  else {
  all_drop = document.body.querySelectorAll(".dropdown-menu");
  for(i=0; i<all_drop.length; i++) {
    all_drop[i].classList.remove("show")
  } block.classList.add("show")}
});

on('body', 'click', '.user_nav_button', function() {
  document.body.querySelector(".settings_block_hide") ? (settings_block = document.body.querySelector(".settings_block_hide"),settings_block.classList.add("settings_block_show"),settings_block.classList.remove("settings_block_hide"))
  : (settings_block = document.body.querySelector(".settings_block_show"),settings_block.classList.add("settings_block_hide"),settings_block.classList.remove("settings_block_show"))
});

on('body', 'click', '.ajax', function(event) {
  event.preventDefault();
  this.querySelector(".unread_count") ? (minus_one_chat(), console.log("minus_one_chat")) : null
  var url = this.getAttribute('href');
  if (url != window.location.pathname){
    ajax_get_reload(url);
  } else {toast_info("Вы уже на этой странице")}
})
on('body', 'click', '.notify_ajax', function(event) {
  event.preventDefault();
  _this = this;
  url = _this.getAttribute('href');

  ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
  ajax_link.open('GET', url, true);
  ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  ajax_link.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
          // если есть блок с классом "user_notify_block", то пользователь на странице видит блоки уведомлений.
          // и, если есть у блока (в который переходит пользователь) непрочитанные уведомления, нужно убавить общий счетчик уведомлений на число этого блока
          if (document.body.querySelector(".user_notify_block")){
            _this.parentElement.classList.contains("card-body") && _this.querySelector(".tab_badge") ? (_count = _this.querySelector(".tab_badge").innerHTML.replace(/\s+/g, ''),
                                                             _count = _count*1,
                                                             notify = document.body.querySelector(".new_unread_notify"),
                                                             all_count = notify.querySelector(".tab_badge").innerHTML.replace(/\s+/g, ''),
                                                             all_count = all_count*1,
                                                             result = all_count - _count,
                                                             result > 0 ? notify.querySelector(".tab_badge").innerHTML = result : notify.innerHTML = '',
                                                             console.log("Вычитаем основной счетчик")
                                                           ) : null;
          }
          elem_ = document.createElement('span');
          elem_.innerHTML = ajax_link.responseText;
          ajax = elem_.querySelector("#reload_block");
          rtr = document.getElementById('ajax');
          rtr.innerHTML = ajax.innerHTML;
          window.scrollTo(0, 0);
          title = elem_.querySelector('title').innerHTML;
          window.history.pushState(null, "vfgffgfgf", url);
          document.title = title;
          loaded = false;
          create_pagination(rtr);
          if (rtr.querySelector(".user_all_notify_container")) {
            document.body.querySelector(".new_unread_notify").innerHTML = "";
            console.log("Обнуляем основной счетчик")
          }
      }
  }
  ajax_link.send()
})

window.addEventListener('popstate', function (e) {
  e.preventDefault();
  ajax_get_reload(document.referrer);
});

on('body', 'click', '.next_item', function(event) {
  event.preventDefault();
  this.style.display = "none";
  change_this_fullscreen(this, document.getElementById('item_loader'));
})
on('body', 'click', '.prev_item', function(event) {
  event.preventDefault();
  this.style.display = "none";
  change_this_fullscreen(this, document.getElementById('item_loader'));
});

on('#ajax', 'click', '.item_stat_f', function() {
  var parent, pk, uuid, loader
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = parent.getAttribute("data-uuid");
  create_fullscreen("/stat/item/" + uuid + "/", "item_fullscreen");
});

on('#ajax', 'click', '.item_fullscreen_hide', function() {
  get_document_opacity_1(document.getElementById("ajax"));
  this.parentElement.parentElement.parentElement.parentElement.parentElement.remove()
});
on('body', 'click', '.video_fullscreen_hide', function() {get_document_opacity_1(document.getElementById("video_loader"));document.querySelector(".video_fullscreen").style.display = "none";document.getElementById("video_loader").innerHTML=""});
on('body', 'click', '.small_video_fullscreen_hide', function() {
  document.querySelector(".video_fullscreen").style.display = "none";
  video_window = document.querySelector(".video_fullscreen");
  get_document_opacity_1(document.getElementById("video_loader"));
  video_window.classList.remove("video_fullscreen_resized", "draggable");
  document.body.querySelector(".video_btn_small").style.display = "none";
  document.body.querySelector(".video_btn_big").style.display = "block";
  document.getElementById("video_loader").innerHTML=""
});

on('#ajax', 'click', '.show_replies', function() {
  this.nextElementSibling.classList.toggle('replies_open');
});

on('body', 'click', '.reply_comment', function() {
  div = this.nextElementSibling;
  input = div.querySelector(".comment_text");
  input.innerHTML = this.previousElementSibling.innerHTML + ',&nbsp;';
  div.style.display = "block";
  focus_block(input)
})
function focus_block(value) {
  range = document.createRange();
  range.selectNodeContents(value);
  range.collapse(false);
  sel = window.getSelection();
  sel.removeAllRanges();
  sel.addRange(range);
}


on('#ajax', 'click', '.tag_item', function() {
  var track_id = this.parentElement.parentElement.getAttribute('music-counter');
  var tag_pk = document.querySelector(".tag_playlist").getAttribute('data-pk');
  if (!document.body.classList.contains("tag_" + tag_pk)){
    save_playlist("tag_" + tag_pk, '/music/manage/temp_tag/' + tag_pk, '/music/get/tag/' + tag_pk + "/", track_id)
  }else{
    music_player.loadPlaylist(0);
    if (FWDMSP.LOAD_PLAYLIST_COMPLETE){
    setTimeout(function() {music_player.playSpecificTrack("tag_" + tag_pk + "/", track_id)}, 50);
  }
  }
  });

on('#ajax', 'click', '.genre_item', function() {
  var track_id = this.parentElement.parentElement.getAttribute('music-counter') - 1;
  var genre_pk = document.querySelector(".genre_playlist").getAttribute('data-pk');
  if (!document.body.classList.contains("genre_" + genre_pk)){
    save_playlist("genre_" + genre_pk, '/music/manage/temp_genre/' + genre_pk, '/music/get/genre/' + genre_pk + "/", track_id)
  }else{
    music_player.loadPlaylist(0);
    if (FWDMSP.LOAD_PLAYLIST_COMPLETE){
    setTimeout(function() {music_player.playSpecificTrack("genre_" + list_pk + "/", track_id)}, 50);
  }
  }
});

on('#ajax', 'click', '.music_list_post', function() {
  var track_id = this.parentElement.parentElement.getAttribute('music-counter');
  item = this.parentElement.parentElement.parentElement.parentElement;
  var item_pk = item.getAttribute('data-pk');
  if (!document.body.classList.contains("item_" + item_pk)){
    document.querySelector("body").classList = "";
    document.querySelector("body").classList.add("item_" + item_pk);
    list = [].slice.call(item.querySelectorAll(".music"), 0).reverse();
    for(i=0; i<list.length; i++) {
      _source=list[i].getAttribute("data-path") + '/stream?client_id=' + 'dce5652caa1b66331903493735ddd64d';
      _title=list[i].querySelector(".music_title").innerHTML;
      try{_thumbPath= list[i].querySelector("img").getAttribute("data-src")} catch {_thumbPath = "/static/images/no_track_img.jpg"};
      _duration=list[i].getAttribute("data-duration");
      time = msToTime(_duration);
      music_player.addTrack(_source, _title, _thumbPath, time, true, false, null);
    }
    music_player.playSpecificTrack("item_" + item_pk, track_id)
  }else{
    music_player.loadPlaylist(0);
    if (FWDMSP.LOAD_PLAYLIST_COMPLETE){
    setTimeout(function() {music_player.playSpecificTrack("item_" + item_pk, track_id)}, 50);
  }
  }
});

on('#ajax', 'click', '.music_list_comment', function() {
  var track_id = this.parentElement.parentElement.getAttribute('music-counter');
  comment = this.parentElement.parentElement.parentElement.parentElement;
  var comment_pk = comment.getAttribute('data-pk');
  if (!document.body.classList.contains("comment_" + comment_pk)){
    document.querySelector("body").classList = "";
    document.querySelector("body").classList.add("comment_" + comment_pk);
    list = [].slice.call(comment.querySelectorAll(".media"), 0).reverse();
    for(i=0; i<list.length; i++) {
      _source=list[i].getAttribute("data-path") + '/stream?client_id=' + 'dce5652caa1b66331903493735ddd64d';
      _title=list[i].querySelector(".music_title").innerHTML;
      try{_thumbPath= list[i].querySelector("img").getAttribute("data-src")} catch {_thumbPath = "/static/images/no_track_img.jpg"};
      _duration=list[i].getAttribute("data-duration");
      time = msToTime(_duration);
      music_player.addTrack(_source, _title, _thumbPath, time, true, false, null);
    }
    music_player.playSpecificTrack("comment_" + comment_pk, track_id)
  }else{
    music_player.loadPlaylist(0);
    if (FWDMSP.LOAD_PLAYLIST_COMPLETE){
    setTimeout(function() {music_player.playSpecificTrack("comment_" + comment_pk, track_id)}, 50);
  }
  }
});
