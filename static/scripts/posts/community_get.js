on('#ajax', 'click', '.c_post_edit', function() {
  block = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  if (block.querySelector(".post_edit_form")) {
    return
  } else {
    clear_attach_block();
    div = document.createElement("div");
    block.append(div);
    block.querySelector(".c_fullscreen") ? block.querySelector(".c_fullscreen").style.display = "none" : null;
    block.querySelector(".attach_container") ? block.querySelector(".attach_container").style.display = "none" : null;
    block.querySelector(".card-footer").style.display = "none";

    list_load(div, "/posts/community_progs/edit_post/" + block.getAttribute("data-uuid") + "/")
  }
})

on('#ajax', 'click', '.c_copy_post_list', function() {
  on_off_list_in_collections(this, "/posts/community_progs/add_list_in_collections/", "c_uncopy_post_list", "c_copy_post_list", "Удалить")
});
on('#ajax', 'click', '.c_uncopy_post_list', function() {
  on_off_list_in_collections(this, "/posts/community_progs/remove_list_from_collections/", "c_copy_post_list", "c_uncopy_post_list", "Добавить")
});

on('#ajax', 'click', '.c_add_post_list', function() {
  loader = document.getElementById("create_loader");
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk')
  open_fullscreen("/posts/community_progs/add_list/" + pk + "/", loader)
});
on('#ajax', 'click', '.c_edit_post_list', function() {
  list_pk = this.parentElement.parentElement.parentElement.getAttribute("list-pk");
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk')
  loader = document.getElementById("create_loader");
  open_fullscreen("/posts/community_progs/edit_list/" + pk + "/" + list_pk + "/", loader)
});

on('#ajax', 'click', '#c_repost_for_community', function() {
  this.parentElement.parentElement.parentElement.parentElement.querySelector("#selected_message_target_items").innerHTML = "";
  current_block = this.parentElement.nextElementSibling;
  current_block.querySelector("#community_append").style.display = "block";
  block = current_block.querySelector("#user_communities_window");
  current_block.querySelector("#chat_items_append").style.display = "none";
  if (!block.querySelector(".load_pag")){
  list_load(block, "/users/load/communities/")
  }
})

on('#ajax', 'click', '.c_fullscreen', function() {
  uuid = this.parentElement.getAttribute('data-uuid');
  open_fullscreen("/communities/post/" + uuid + "/", document.getElementById("item_loader"))
});
on('#ajax', 'click', '.c_fix_fullscreen', function() {
  container = this.parentElement;
  uuid = container.getAttribute('data-uuid');
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("item_loader");
  open_fullscreen("/communities/fix_post/" + pk + "/" + uuid + "/", loader)
})

on('#ajax', 'click', '.c_ucm_post_repost', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement
  uuid = parent.getAttribute("data-uuid");
  parent.getAttribute('data-pk') ? pk = parent.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  //document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = parent.getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/posts/repost/c_ucm_post_window/" + pk + "/" + uuid + "/", loader);
  clear_attach_block();
})
on('#ajax', 'click', '.c_article_detail', function() {
  var uuid, pk, loader;
  uuid = this.parentElement.getAttribute('data-uuid');
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = this.parentElement.getAttribute('data-pk');
  loader = document.getElementById("article_loader");
  open_fullscreen("/article/read/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.c_all_posts_likes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/posts/item_window/all_community_like/" + uuid + "/", loader)
});
on('#ajax', 'click', '.c_all_posts_dislikes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/posts/item_window/all_community_dislike/" + uuid + "/", loader)
});
on('#ajax', 'click', '.c_all_item_reposts', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/posts/item_window/all_community_reposts/" + uuid + "/", loader)
});

on('#ajax', 'click', '.c_all_posts_comment_likes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/posts/item_window/all_community_comment_like/" + pk + "/", loader)
});
on('#ajax', 'click', '.c_all_posts_comment_dislikes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/posts/item_window/all_community_comment_dislike/" + pk + "/", loader)
});

on('#ajax', 'click', '.c_item_comments', function() {
  clear_comment_dropdown();
  parent = this.parentElement.parentElement.parentElement.parentElement;
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = parent.getAttribute('data-pk');
  uuid = parent.getAttribute("data-uuid");
  block = parent.querySelector(".c_load_comments");
  if (block.classList.contains("show")){
    block.classList.remove("show")
  } else {
    block.firstChild ? null : list_load(block, "/posts/community/comment/" + uuid + "/" + pk + "/");
    block.classList.add("show")
  }
});


on('#ajax', 'click', '.c_comment_photo', function() {
  this.classList.add("current_file_dropdown");
  document.body.querySelector(".attach_block") ? (attach_block = document.body.querySelector(".attach_block"), attach_block.innerHTML = "", attach_block.classList.remove("attach_block")) : null;
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/c_img_comment_load/', loader)
});
on('#ajax', 'click', '.c_comment_video', function() {
  this.classList.add("current_file_dropdown");
  clear_attach_block();
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/c_video_load/', loader)
});
on('#ajax', 'click', '.c_comment_music', function() {
  this.classList.add("current_file_dropdown");
  clear_attach_block();
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/c_music_load/', loader)
});
on('#ajax', 'click', '.c_comment_good', function() {
  this.classList.add("current_file_dropdown");
  clear_attach_block();
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/c_good_load/', loader)
});
on('#ajax', 'click', '.c_comment_article', function() {
  this.classList.add("current_file_dropdown");
  clear_attach_block();
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/c_article_load/', loader)
});

on('#ajax', 'click', '.c_select_photo', function() {
  this.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/c_img_load/', loader)
});
on('#ajax', 'click', '.c_select_video', function() {
  this.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/c_video_load/', loader)
});
on('#ajax', 'click', '.c_select_music', function() {
  this.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/c_music_load/', loader)
});
on('#ajax', 'click', '.c_select_good', function() {
  this.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/c_good_load/', loader)
});
on('#ajax', 'click', '.c_select_article', function() {
  this.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/c_article_load/', loader)
});
