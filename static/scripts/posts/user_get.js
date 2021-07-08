on('#ajax', 'click', '.u_copy_post_list', function() {
  on_off_list_in_collections(this, "/posts/user_progs/add_list_in_collections/", "u_uncopy_post_list", "u_copy_post_list", "Удалить")
});
on('#ajax', 'click', '.u_uncopy_post_list', function() {
  on_off_list_in_collections(this, "/posts/user_progs/remove_list_from_collections/", "u_copy_post_list", "u_uncopy_post_list", "Добавить")
});

on('#ajax', 'click', '.u_add_post_list', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen("/posts/user_progs/add_list/", loader)
});
on('#ajax', 'click', '.u_edit_post_list', function() {
  list_pk = this.parentElement.parentElement.parentElement.getAttribute("list-pk");
  loader = document.getElementById("create_loader");
  open_fullscreen("/posts/user_progs/edit_list/" + list_pk + "/", loader)
});

on('#ajax', 'click', '.post_list_change', function() {
  if (!this.classList.contains("tab_active")){
    this.classList.contains("community") ? url = "/communities/list/" : url = "/users/detail/list/";
    parent = this.parentElement.parentElement.parentElement;
    list = parent.querySelectorAll(".list");
    for (var i = 0; i < list.length; i++) {
      list[i].classList.remove("tab_active");
      list[i].classList.add("pointer", "post_list_change");
    };
    block = parent.nextElementSibling;
    list_block_load(block, ".span_list_pk", url + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/" + this.getAttribute("list-pk") + "/");
    this.classList.remove("pointer", "post_list_change");
    this.classList.add("tab_active");
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

on('#ajax', 'click', '.fullscreen', function() {
  uuid = this.parentElement.getAttribute('data-uuid');
  open_fullscreen("/users/detail/post/" + uuid + "/", document.getElementById("item_loader"))
})
on('#ajax', 'click', '.fix_fullscreen', function() {
  container = this.parentElement;
  uuid = container.getAttribute('data-uuid');
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("item_loader");
  open_fullscreen("/users/detail/fix_post/" + pk + "/" + uuid + "/", loader)
})
on('#ajax', 'click', '.u_ucm_post_repost', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement
  uuid = parent.getAttribute("data-uuid");
  parent.getAttribute('data-pk') ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  //document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = parent.getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/posts/repost/u_ucm_post_window/" + pk + "/" + uuid + "/", loader);
  clear_attach_block();
})
on('#ajax', 'click', '.repost_for_wall', function() {
  this.parentElement.parentElement.parentElement.parentElement.querySelector("#selected_message_target_items").innerHTML = "";
  current_block = this.parentElement.nextElementSibling;
  current_block.querySelector("#chat_items_append").style.display = "none";
  current_block.querySelector("#community_append").style.display = "none";
})
on('#ajax', 'click', '#u_repost_for_community', function() {
  this.parentElement.parentElement.parentElement.parentElement.querySelector("#selected_message_target_items").innerHTML = "";
  current_block = this.parentElement.nextElementSibling;
  current_block.querySelector("#community_append").style.display = "block";
  block = current_block.querySelector("#user_communities_window");
  current_block.querySelector("#chat_items_append").style.display = "none";
  if (!block.querySelector(".load_pag")){
  list_load(block, "/users/load/communities/")
  }
})
on('#ajax', 'click', '#repost_for_message', function() {
  this.parentElement.parentElement.parentElement.parentElement.querySelector("#selected_message_target_items").innerHTML = "";
  current_block = this.parentElement.nextElementSibling;
  current_block.querySelector("#community_append").style.display = "none";
  block = current_block.querySelector("#user_chat_items_window");
  current_block.querySelector("#user_chat_items_window").style.display = "block";
  if (!block.querySelector(".load_pag")){
  list_load(block, "/users/load/chat_items/")
  }
})

on('#ajax', 'click', '.u_post_edit', function() {
  block = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  if (block.querySelector(".post_edit_form")) {
    return
  } else {
    clear_attach_block();
    div = document.createElement("div");
    block.append(div);
    block.querySelector(".fullscreen") ? block.querySelector(".fullscreen").style.display = "none" : null;
    block.querySelector(".attach_container") ? block.querySelector(".attach_container").style.display = "none" : null;
    block.querySelector(".card-footer").style.display = "none";

    list_load(div, "/posts/user_progs/edit_post/" + block.getAttribute("data-uuid") + "/");
    focus_block(div.querySelector(".smile_supported"));
  }
})
on('#ajax', 'click', '.u_article_detail', function() {
  uuid = this.parentElement.getAttribute("data-uuid");
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = this.parentElement.getAttribute('data-pk');
  loader = document.getElementById("article_loader");
  open_fullscreen("/article/detail/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.create_ajax', function() {
  link = this.getAttribute("data-href");
    loader = document.getElementById("create_loader");
    open_load_fullscreen(link, loader)
});


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
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = parent.getAttribute('data-pk');
  uuid = parent.getAttribute("data-uuid");
  block = parent.querySelector(".u_load_comments");
  if (block.classList.contains("show")){
    block.classList.remove("show")
  } else {
    block.firstChild ? null : list_load(block, "/posts/user/comment/" + uuid + "/" + pk + "/");
    block.classList.add("show")
  }
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
  open_load_fullscreen('/users/load/u_video_load/', loader);
});
on('#ajax', 'click', '.u_comment_music', function() {
  this.classList.add("current_file_dropdown");
  clear_attach_block();
  loader = document.getElementById("create_loader");
  open_load_fullscreen('/users/load/u_music_load/', loader)
});
on('#ajax', 'click', '.u_comment_doc', function() {
  this.classList.add("current_file_dropdown");
  clear_attach_block();
  loader = document.getElementById("create_loader");
  open_load_fullscreen('/users/load/u_doc_load/', loader)
});
on('#ajax', 'click', '.u_comment_good', function() {
  this.classList.add("current_file_dropdown");
  clear_attach_block();
  loader = document.getElementById("create_loader");
  open_load_fullscreen('/users/load/u_good_load/', loader)
});
on('#ajax', 'click', '.u_comment_article', function() {
  this.classList.add("current_file_dropdown");
  clear_attach_block();
  loader = document.getElementById("create_loader");
  open_load_fullscreen('/users/load/u_article_load/', loader)
});

on('#ajax', 'click', '.u_select_photo', function() {
  this.parentElement.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  this.parentElement.classList.remove("show");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_load_fullscreen('/users/load/u_img_load/', loader)
});
on('#ajax', 'click', '.u_select_survey', function() {
  this.parentElement.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  this.parentElement.classList.remove("show");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_load_fullscreen('/users/load/u_survey_load/', loader)
});

on('#ajax', 'click', '.u_select_video', function() {
  this.parentElement.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  this.parentElement.classList.remove("show");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_load_fullscreen('/users/load/u_video_load/', loader)
});
on('#ajax', 'click', '.u_select_music', function() {
  this.parentElement.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  this.parentElement.classList.remove("show");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_load_fullscreen('/users/load/u_music_load/', loader)
});
on('#ajax', 'click', '.u_select_doc', function() {
  this.parentElement.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  this.parentElement.classList.remove("show");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_load_fullscreen('/users/load/u_doc_load/', loader)
});
on('#ajax', 'click', '.u_select_good', function() {
  this.parentElement.classList.remove("show");
  this.parentElement.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_load_fullscreen('/users/load/u_good_load/', loader)
});
on('#ajax', 'click', '.u_select_article', function() {
  this.parentElement.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  this.parentElement.classList.remove("show");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_load_fullscreen('/users/load/u_article_load/', loader)
});

on('#ajax', 'click', '.m_select_photo', function() {
  this.parentElement.classList.remove("show");
  this.parentElement.parentElement.parentElement.previousElementSibling.classList.add("message_attach_block");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_load_fullscreen('/users/load/u_img_load/', loader)
});
on('#ajax', 'click', '.m_select_video', function() {
  this.parentElement.classList.remove("show");
  this.parentElement.parentElement.parentElement.previousElementSibling.classList.add("message_attach_block");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_load_fullscreen('/users/load/u_video_load/', loader)
});
on('#ajax', 'click', '.m_select_music', function() {
  this.parentElement.classList.remove("show");
  this.parentElement.parentElement.parentElement.previousElementSibling.classList.add("message_attach_block");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_load_fullscreen('/users/load/u_music_load/', loader)
});
on('#ajax', 'click', '.m_select_doc', function() {
  this.parentElement.classList.remove("show");
  this.parentElement.parentElement.parentElement.previousElementSibling.classList.add("message_attach_block");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_load_fullscreen('/users/load/u_doc_load/', loader)
});
on('#ajax', 'click', '.m_select_good', function() {
  this.parentElement.classList.remove("show");
  this.parentElement.parentElement.parentElement.previousElementSibling.classList.add("message_attach_block");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_load_fullscreen('/users/load/u_good_load/', loader)
});
on('#ajax', 'click', '.m_select_article', function() {
  this.parentElement.classList.remove("show");
  this.parentElement.parentElement.parentElement.previousElementSibling.classList.add("message_attach_block");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_load_fullscreen('/users/load/u_article_load/', loader)
});

on('#ajax', 'click', '.delete_thumb', function(e) {
  e.preventDefault();
  this.nextElementSibling.remove();
  block = document.createElement("div");
  this.parentElement.innerHTML = "<h4>Изображение</h4><i>(обязательно)</i>";
  this.remove();
})
