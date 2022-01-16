on('#ajax', 'click', '.load_post_comments', function() {
  clear_comment_dropdown();
  block = this.parentElement.parentElement.parentElement.parentElement;
  block_comments = block.querySelector(".load_comments");
  if (block_comments.classList.contains("show")){
    block_comments.classList.remove("show")
  } else {
    block_comments.firstChild ? null : list_load(block_comments, "/posts/comments/" + block.getAttribute("data-pk") + "/");
    block_comments.classList.add("show")
  }
});

on('#ajax', 'click', '.input_new_post_in_list', function() {
  this.parentElement.nextElementSibling.style.display = "block";
});

on('#ajax', 'click', '.copy_user_post_list', function() {
  on_off_list_in_collections(this, "/posts/user_progs/add_list_in_collections/", "uncopy_user_post_list", "copy_user_post_list", "Удалить")
});
on('#ajax', 'click', '.uncopy_user_post_list', function() {
  on_off_list_in_collections(this, "/posts/user_progs/remove_list_from_collections/", "copy_user_post_list", "uncopy_user_post_list", "Добавить")
});

on('#ajax', 'click', '.u_add_post_list', function() {
  create_fullscreen("/posts/user_progs/add_list/", "worker_fullscreen");
});
on('#ajax', 'click', '.u_edit_post_list', function() {
  list_pk = this.parentElement.parentElement.getAttribute("data-uuid");
  create_fullscreen("/posts/user_progs/edit_list/" + list_pk + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.post_list_change', function() {
  if (!this.classList.contains("tab_active")){
    this.classList.contains("community") ? url = "/communities/list/" : url = "/users/detail/list/";
    parent = this.parentElement.parentElement.parentElement;
    list = parent.querySelectorAll(".list");
    for (var i = 0; i < list.length; i++) {
      list[i].classList.remove("active");
      list[i].classList.add("pointer", "post_list_change");
    };
    block = parent.nextElementSibling;
    list_block_load(block, ".span_list_pk", url + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/" + this.getAttribute("list-pk") + "/");
    this.classList.remove("pointer", "post_list_change");
    this.classList.add("active");
    try{
      reload_list_stat(this)
    }catch {null}
  }
});

on('#ajax', 'click', '.post_list_select', function() {
  parent = this.parentElement;
  lists = parent.parentElement.querySelectorAll(".post_list_select");
  for (var i = 0; i < lists.length; i++){
    lists[i].querySelector("svg") ? (lists[i].querySelector("svg").parentElement.remove(), lists[i].style.paddingLeft = "30px") : null;
  }
  pk = parent.getAttribute("data-pk");
  list = parent.querySelector(".post_list_select");
  list.style.paddingLeft = "14px",
  span = document.createElement("span"),
  span.innerHTML = '<input type="hidden" class="list" name="lists" value="' + pk + '"><svg fill="currentColor" style="width:12px;height:12px;" class="svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg> ',
  list.prepend(span)
});
on('#ajax', 'click', '.cat_list_select', function() {
  parent = this.parentElement;
  lists = parent.parentElement.querySelectorAll(".cat_list_select");
  for (var i = 0; i < lists.length; i++){
    lists[i].querySelector("svg") ? (lists[i].querySelector("svg").parentElement.remove(), lists[i].style.paddingLeft = "30px") : null;
  }
  pk = parent.getAttribute("data-pk");
  list = parent.querySelector(".cat_list_select");
  list.style.paddingLeft = "14px",
  span = document.createElement("span"),
  span.innerHTML = '<input type="hidden" name="cat" value="' + pk + '"><svg fill="currentColor" style="width:12px;height:12px;" class="svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg> ',
  list.prepend(span)
});

on('#ajax', 'click', '#holder_article_image', function() {
  img = this.previousElementSibling.querySelector("#id_g_image")
  get_image_priview(this, img);
});

on('#ajax', 'click', '.wall_fullscreen', function(e) {
  e.preventDefault();
  card = this.parentElement.parentElement.parentElement.parentElement;
  pk = card.getAttribute('data-pk');
  create_fullscreen("/posts/post/" + pk + "/", "worker_fullscreen");
  window.history.pushState(null, "vfgffgfgf", window.location.href + "?key=wall&owner_id=" + pk + "&post_pk=" + pk);
});

on('#ajax', 'click', '.fullscreen', function(e) {
  card = this.parentElement;

  if (this.parentElement.querySelector(".show_post_text")) {
    shower = this.parentElement.querySelector(".show_post_text");
    shower.nextElementSibling.nextElementSibling.style.display = "unset";
    shower.nextElementSibling.remove();
    shower.previousElementSibling.remove();
    shower.remove();
  }

  else if (e.target.classList.contains("action")) {null}
  else {
    pk = card.getAttribute('data-pk');
    create_fullscreen("/posts/post/" + pk + "/", "worker_fullscreen");
    window.history.pushState(null, "vfgffgfgf", window.location.href + "?key=wall&owner_id=" + pk + "&post_pk=" + pk);
  }
});

on('#ajax', 'click', '.fix_fullscreen', function(e) {
  card = this.parentElement;

  if (this.parentElement.querySelector(".show_post_text")) {
    shower = this.parentElement.querySelector(".show_post_text");
    shower.nextElementSibling.nextElementSibling.style.display = "unset";
    shower.nextElementSibling.remove();
    shower.previousElementSibling.remove();
    shower.remove();
  }

  else if (e.target.classList.contains("action")) {null}
  else {
    pk = card.getAttribute('data-pk');
    create_fullscreen("/posts/fix_post/" + pk + "/", "worker_fullscreen");
    window.history.pushState(null, "vfgffgfgf", window.location.href + "?key=wall&owner_id=" + pk + "&post_pk=" + pk);
  }
});

on('#ajax', 'click', '.u_ucm_post_repost', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement
  pk = parent.getAttribute("data-uuid");
  create_fullscreen("/posts/repost/u_ucm_post_window/" + this.parentElement.parentElement.parentElement.parentElement.getAttribute("data-pk") + "/", "worker_fullscreen");
  clear_attach_block();
});

on('#ajax', 'click', '.repost_for_wall', function() {
  this.parentElement.parentElement.parentElement.parentElement.querySelector("#selected_message_target_items").innerHTML = "";
  current_block = this.parentElement.nextElementSibling;
  current_block.querySelector("#chat_items_append").style.display = "none";
  current_block.querySelector("#community_append").style.display = "none";
});
on('#ajax', 'click', '#u_repost_for_community', function() {
  this.parentElement.parentElement.parentElement.parentElement.querySelector("#selected_message_target_items").innerHTML = "";
  current_block = this.parentElement.nextElementSibling;
  current_block.querySelector("#community_append").style.display = "block";
  block = current_block.querySelector("#user_communities_window");
  current_block.querySelector("#chat_items_append").style.display = "none";
  if (!block.querySelector(".load_pag")){
  list_load(block, "/users/load/communities/")
  }
});
on('#ajax', 'click', '#repost_for_message', function() {
  this.parentElement.parentElement.parentElement.parentElement.querySelector("#selected_message_target_items").innerHTML = "";
  current_block = this.parentElement.nextElementSibling;
  current_block.querySelector("#community_append").style.display = "none";
  block = current_block.querySelector("#user_chat_items_window");
  current_block.querySelector("#user_chat_items_window").style.display = "block";
  if (!block.querySelector(".load_pag")){
  list_load(block, "/users/load/chat_items/")
  }
});

on('#ajax', 'click', '.u_post_edit', function() {
  block = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  if (block.querySelector(".post_edit_form")) {
    return
  } else {
    clear_attach_block();
    div = document.createElement("div");
    block.append(div);
    block.querySelector(".text_support") ? block.querySelector(".text_support").style.display = "none" : null;
    block.querySelector(".attach_container") ? block.querySelector(".attach_container").style.display = "none" : null;
    block.querySelector(".card-footer").style.display = "none";

    list_load(div, "/posts/user_progs/edit_post/" + block.getAttribute("data-pk") + "/");
  }
});
on('#ajax', 'click', '.u_article_detail', function() {
  uuid = this.parentElement.getAttribute("data-uuid");
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = this.parentElement.getAttribute('data-pk');
  create_fullscreen("/article/detail/" + pk + "/" + uuid + "/", "item_fullscreen");
});


on('#ajax', 'click', '.u_all_posts_likes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  create_fullscreen("/posts/item_window/all_user_like/" + uuid + "/", "worker_fullscreen");
});
on('#ajax', 'click', '.u_all_posts_dislikes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  create_fullscreen("/posts/item_window/all_user_dislike/" + uuid + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.u_all_posts_comment_likes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  create_fullscreen("/posts/item_window/all_user_comment_like/" + pk + "/", "worker_fullscreen");
});
on('#ajax', 'click', '.u_all_posts_comment_dislikes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  create_fullscreen("/posts/item_window/all_user_comment_dislike/" + pk + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.u_all_item_reposts', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  create_fullscreen("/posts/item_window/all_user_reposts/" + pk + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.u_load_comment_photo', function() {
  this.classList.add("current_file_dropdown");
  document.body.querySelector(".attach_block") ? (attach_block = document.body.querySelector(".attach_block"), attach_block.innerHTML = "", attach_block.classList.remove("attach_block")) : null;
  create_fullscreen('/users/load/u_img_comment_load/', "item_fullscreen");
});
on('#ajax', 'click', '.u_load_comment_video', function() {
  this.classList.add("current_file_dropdown");
  clear_attach_block();
  create_fullscreen('/users/load/u_video_load/', "item_fullscreen");
});
on('#ajax', 'click', '.u_load_comment_music', function() {
  this.classList.add("current_file_dropdown");
  clear_attach_block();
  create_fullscreen('/users/load/u_music_load/', "item_fullscreen");
});
on('#ajax', 'click', '.u_load_comment_doc', function() {
  this.classList.add("current_file_dropdown");
  clear_attach_block();
  create_fullscreen('/users/load/u_doc_load/', "item_fullscreen");
});
on('#ajax', 'click', '.u_load_comment_good', function() {
  this.classList.add("current_file_dropdown");
  clear_attach_block();
  create_fullscreen('/users/load/u_good_load/', "item_fullscreen");
});
on('#ajax', 'click', '.u_load_comment_article', function() {
  this.classList.add("current_file_dropdown");
  clear_attach_block();
  create_fullscreen('/users/load/u_article_load/', "item_fullscreen");
});

on('#ajax', 'click', '.u_select_photo', function() {
  this.parentElement.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  this.parentElement.classList.remove("show");
  clear_comment_dropdown();
  create_fullscreen('/users/load/u_img_load/', "item_fullscreen");
});
on('#ajax', 'click', '.u_select_survey', function() {
  this.parentElement.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  this.parentElement.classList.remove("show");
  clear_comment_dropdown();
  create_fullscreen('/users/load/u_survey_load/', "item_fullscreen");
});

on('#ajax', 'click', '.u_select_video', function() {
  this.parentElement.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  this.parentElement.classList.remove("show");
  clear_comment_dropdown();
  create_fullscreen('/users/load/u_video_load/', "item_fullscreen");
});
on('#ajax', 'click', '.u_select_music', function() {
  this.parentElement.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  this.parentElement.classList.remove("show");
  clear_comment_dropdown();
  create_fullscreen('/users/load/u_music_load/', "item_fullscreen");
});
on('#ajax', 'click', '.u_select_doc', function() {
  this.parentElement.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  this.parentElement.classList.remove("show");
  clear_comment_dropdown();
  create_fullscreen('/users/load/u_doc_load/', "item_fullscreen");
});
on('#ajax', 'click', '.u_select_good', function() {
  this.parentElement.classList.remove("show");
  this.parentElement.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  clear_comment_dropdown();
  create_fullscreen('/users/load/u_good_load/', "item_fullscreen");
});
on('#ajax', 'click', '.u_select_article', function() {
  this.parentElement.parentElement.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  this.parentElement.classList.remove("show");
  clear_comment_dropdown();
  create_fullscreen('/users/load/u_article_load/', "item_fullscreen");
});

on('#ajax', 'click', '.m_select_photo', function() {
  this.parentElement.classList.remove("show");
  this.parentElement.parentElement.parentElement.parentElement.previousElementSibling.classList.add("message_attach_block");
  clear_comment_dropdown();
  create_fullscreen('/users/load/u_img_message_load/', "item_fullscreen");
});
on('#ajax', 'click', '.m_select_video', function() {
  this.parentElement.classList.remove("show");
  this.parentElement.parentElement.parentElement.parentElement.previousElementSibling.classList.add("message_attach_block");
  clear_comment_dropdown();
  create_fullscreen('/users/load/u_video_load/', "item_fullscreen");
});
on('#ajax', 'click', '.m_select_music', function() {
  this.parentElement.classList.remove("show");
  this.parentElement.parentElement.parentElement.parentElement.previousElementSibling.classList.add("message_attach_block");
  clear_comment_dropdown();
  create_fullscreen('/users/load/u_music_load/', "item_fullscreen");
});
on('#ajax', 'click', '.m_select_doc', function() {
  this.parentElement.classList.remove("show");
  this.parentElement.parentElement.parentElement.parentElement.previousElementSibling.classList.add("message_attach_block");
  clear_comment_dropdown();
  create_fullscreen('/users/load/u_doc_load/', "item_fullscreen");
});
on('#ajax', 'click', '.m_select_good', function() {
  this.parentElement.classList.remove("show");
  this.parentElement.parentElement.parentElement.parentElement.previousElementSibling.classList.add("message_attach_block");
  clear_comment_dropdown();
  create_fullscreen('/users/load/u_good_load/', "item_fullscreen");
});
on('#ajax', 'click', '.m_select_article', function() {
  this.parentElement.classList.remove("show");
  this.parentElement.parentElement.parentElement.parentElement.previousElementSibling.classList.add("message_attach_block");
  clear_comment_dropdown();
  create_fullscreen('/users/load/u_article_load/', "item_fullscreen");
});

on('#ajax', 'click', '.delete_thumb', function(e) {
  e.preventDefault();
  this.nextElementSibling.remove();
  block = document.createElement("div");
  this.parentElement.innerHTML = "<h4>Изображение</h4><i>(обязательно)</i>";
  this.remove();
});
