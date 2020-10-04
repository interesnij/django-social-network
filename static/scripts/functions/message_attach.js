function clear_message_attach_block(){
  document.body.querySelector(".message_attach_block") ? (a_b = document.body.querySelector(".message_attach_block"), a_b.innerHTML = "", a_b.classList = "", a_b.classList.add("files_0"), a_b.classList.remove("message_attach_block")) : null;
}

function is_full_message_attach(){
  files_block = document.body.querySelector(".message_attach_block");
  if (files_block.classList.contains("files_10")){
    files_block.parentElement.querySelector(".message_dropdown").style.display = "none";
    close_create_window()
  }
  else {
    files_block.parentElement.querySelector(".message_dropdown").style.display = "block"
}
}
function add_file_message_attach(){
  files_block = document.body.querySelector(".message_attach_block");
  if (files_block.classList.contains("files_0")){ files_block.classList.add("files_1"), files_block.classList.remove("files_0")}
  else if (files_block.classList.contains("files_1")){ files_block.classList.add("files_2"), files_block.classList.remove("files_1")}
  else if (files_block.classList.contains("files_2")){ files_block.classList.add("files_3"), files_block.classList.remove("files_2")}
  else if (files_block.classList.contains("files_3")){ files_block.classList.add("files_4"), files_block.classList.remove("files_3")}
  else if (files_block.classList.contains("files_4")){ files_block.classList.add("files_5"), files_block.classList.remove("files_4")}
  else if (files_block.classList.contains("files_5")){ files_block.classList.add("files_6"), files_block.classList.remove("files_5")}
  else if (files_block.classList.contains("files_6")){ files_block.classList.add("files_7"), files_block.classList.remove("files_6")}
  else if (files_block.classList.contains("files_7")){ files_block.classList.add("files_8"), files_block.classList.remove("files_7")}
  else if (files_block.classList.contains("files_8")){ files_block.classList.add("files_9"), files_block.classList.remove("files_8")}
  else if (files_block.classList.contains("files_9")){ files_block.classList.add("files_10"), files_block.classList.remove("files_9")}
}
function remove_file_message_attach(){
  files_block = document.body.querySelector(".message_attach_block");
  if (files_block.classList.contains("files_1")){ files_block.classList.add("files_0"), files_block.classList.remove("files_1")}
  else if (files_block.classList.contains("files_2")){ files_block.classList.add("files_1"), files_block.classList.remove("files_2")}
  else if (files_block.classList.contains("files_3")){ files_block.classList.add("files_2"), files_block.classList.remove("files_3")}
  else if (files_block.classList.contains("files_4")){ files_block.classList.add("files_3"), files_block.classList.remove("files_4")}
  else if (files_block.classList.contains("files_5")){ files_block.classList.add("files_4"), files_block.classList.remove("files_5")}
  else if (files_block.classList.contains("files_6")){ files_block.classList.add("files_5"), files_block.classList.remove("files_6")}
  else if (files_block.classList.contains("files_7")){ files_block.classList.add("files_6"), files_block.classList.remove("files_7")}
  else if (files_block.classList.contains("files_8")){ files_block.classList.add("files_7"), files_block.classList.remove("files_8")}
  else if (files_block.classList.contains("files_9")){ files_block.classList.add("files_8"), files_block.classList.remove("files_9")}
  else if (files_block.classList.contains("files_10")){ files_block.classList.add("files_9"), files_block.classList.remove("files_10")}
}

function photo_message_attach(block, photo_pk, user_pk, src) {
  is_full_message_attach();
    if (!block.querySelector(".select_photo1")){div = create_preview_photo("select_photo1", src, photo_pk, user_pk)}
    else if (!block.querySelector(".select_photo2")){div = create_preview_photo("select_photo2", src, photo_pk, user_pk)}
    else if (!block.querySelector(".select_photo3")){div = create_preview_photo("select_photo3", src, photo_pk, user_pk)}
    else if (!block.querySelector(".select_photo4")){div = create_preview_photo("select_photo4", src, photo_pk, user_pk)}
    else if (!block.querySelector(".select_photo5")){div = create_preview_photo("select_photo5", src, photo_pk, user_pk)}
    else if (!block.querySelector(".select_photo6")){div = create_preview_photo("select_photo6", src, photo_pk, user_pk)}
    else if (!block.querySelector(".select_photo7")){div = create_preview_photo("select_photo7", src, photo_pk, user_pk)}
    else if (!block.querySelector(".select_photo8")){div = create_preview_photo("select_photo8", src, photo_pk, user_pk)}
    else if (!block.querySelector(".select_photo9")){div = create_preview_photo("select_photo9", src, photo_pk, user_pk)}
    else if (!block.querySelector(".select_photo10")){div = create_preview_photo("select_photo10", src, photo_pk, user_pk)}
    block.append(div);
  block.querySelector(".photo_input") ? null : ($photo_input = document.createElement("span"), $photo_input.innerHTML = '<input type="hidden" class="photo_input" name="photo" value="1">', block.append($photo_input));

  add_file_message_attach()
  is_full_message_attach();
}

function photo_message_upload_attach(photo_list, block, block_divs_length){
  is_full_message_attach();
  for (var i = 0; i < block_divs_length; i++){
    parent = photo_list[i].parentElement
    if (!block.querySelector(".select_photo1")){
      div = create_preview_photo("select_photo1", parent.getAttribute('data-href'), parent.getAttribute("photo-pk"), parent.getAttribute("data-pk")); add_file_message_attach(); block.append(div);
    } else if (!block.querySelector(".select_photo2")){
      div = create_preview_photo("select_photo1", parent.getAttribute('data-href'), parent.getAttribute("photo-pk"), parent.getAttribute("data-pk")); add_file_message_attach(); block.append(div);
    }
    else if (!block.querySelector(".select_photo2")){
      div = create_preview_photo("select_photo2", parent.getAttribute('data-href'), parent.getAttribute("photo-pk"), parent.getAttribute("data-pk")); add_file_message_attach(); block.append(div);
    }
    else if (!block.querySelector(".select_photo3")){
      div = create_preview_photo("select_photo3", parent.getAttribute('data-href'), parent.getAttribute("photo-pk"), parent.getAttribute("data-pk")); add_file_message_attach(); block.append(div);
    }
    else if (!block.querySelector(".select_photo4")){
      div = create_preview_photo("select_photo4", parent.getAttribute('data-href'), parent.getAttribute("photo-pk"), parent.getAttribute("data-pk")); add_file_message_attach(); block.append(div);
    }
    else if (!block.querySelector(".select_photo5")){
      div = create_preview_photo("select_photo5", parent.getAttribute('data-href'), parent.getAttribute("photo-pk"), parent.getAttribute("data-pk")); add_file_message_attach(); block.append(div);
    }
    else if (!block.querySelector(".select_photo6")){
      div = create_preview_photo("select_photo6", parent.getAttribute('data-href'), parent.getAttribute("photo-pk"), parent.getAttribute("data-pk")); add_file_message_attach(); block.append(div);
    }
    else if (!block.querySelector(".select_photo7")){
      div = create_preview_photo("select_photo7", parent.getAttribute('data-href'), parent.getAttribute("photo-pk"), parent.getAttribute("data-pk")); add_file_message_attach(); block.append(div);
    }
    else if (!block.querySelector(".select_photo8")){
      div = create_preview_photo("select_photo8", parent.getAttribute('data-href'), parent.getAttribute("photo-pk"), parent.getAttribute("data-pk")); add_file_message_attach(); block.append(div);
    }
    else if (!block.querySelector(".select_photo9")){
      div = create_preview_photo("select_photo9", parent.getAttribute('data-href'), parent.getAttribute("photo-pk"), parent.getAttribute("data-pk")); add_file_message_attach(); block.append(div);
    }
    else if (!block.querySelector(".select_photo10")){
      div = create_preview_photo("select_photo10", parent.getAttribute('data-href'), parent.getAttribute("photo-pk"), parent.getAttribute("data-pk")); add_file_message_attach(); block.append(div);
    }
  }
  block.querySelector(".photo_input") ? null : ($photo_input = document.createElement("span"), $photo_input.innerHTML = '<input type="hidden" class="photo_input" name="photo" value="1">', block.append($photo_input));
  close_create_window()
  }


function video_message_attach(block, pk, counter, src) {
  is_full_message_attach();
    if (!block.querySelector(".video_input")){div = create_preview_video("select_video1", src, pk, counter)}
    else if (!block.querySelector(".select_video2")){div = create_preview_video("select_video2", src, pk, counter)}
    else if (!block.querySelector(".select_video3")){div = create_preview_video("select_video3", src, pk, counter)}
    else if (!block.querySelector(".select_video4")){div = create_preview_video("select_video4", src, pk, counter)}
    else if (!block.querySelector(".select_video5")){div = create_preview_video("select_video5", src, pk, counter)}
    else if (!block.querySelector(".select_video6")){div = create_preview_video("select_video6", src, pk, counter)}
    else if (!block.querySelector(".select_video7")){div = create_preview_video("select_video7", src, pk, counter)}
    else if (!block.querySelector(".select_video8")){div = create_preview_video("select_video8", src, pk, counter)}
    else if (!block.querySelector(".select_video9")){div = create_preview_video("select_video9", src, pk, counter)}
    else if (!block.querySelector(".select_video10")){div = create_preview_video("select_video10", src, pk, counter)}
  block.append(div);
  block.querySelector(".video_input") ? null : ($video_input = document.createElement("span"), $video_input.innerHTML = '<input type="hidden" class="video_input" name="video" value="1">', block.append($video_input));

  add_file_message_attach()
  is_full_message_attach();
}

function music_message_attach(block, pk, counter, src) {
  is_full_message_attach();
    if (!block.querySelector(".select_music1")){div = create_preview_music("select_music1", src, pk, counter)}
    else if (!block.querySelector(".select_music2")){div = create_preview_music("select_music2", src, pk, counter)}
    else if (!block.querySelector(".select_music3")){div = create_preview_music("select_music3", src, pk, counter)}
    else if (!block.querySelector(".select_music4")){div = create_preview_music("select_music4", src, pk, counter)}
    else if (!block.querySelector(".select_music5")){div = create_preview_music("select_music5", src, pk, counter)}
    else if (!block.querySelector(".select_music6")){div = create_preview_music("select_music6", src, pk, counter)}
    else if (!block.querySelector(".select_music7")){div = create_preview_music("select_music7", src, pk, counter)}
    else if (!block.querySelector(".select_music8")){div = create_preview_music("select_music8", src, pk, counter)}
    else if (!block.querySelector(".select_music9")){div = create_preview_music("select_music9", src, pk, counter)}
    else if (!block.querySelector(".select_music10")){div = create_preview_music("select_music10", src, pk, counter)}
  block.append(div);

  add_file_message_attach()
  is_full_message_attach();
}

function doc_message_attach(_this, block) {
  is_full_message_attach();
  pk = _this.getAttribute('data-pk');
  if (block.querySelector( '[data-pk=' + '"' + pk + '"' + ']' )){
    _this.parentElement.setAttribute("tooltip", "Документ уже выбран");
    _this.parentElement.setAttribute("flow", "up");
    return
  };
  _this.parentElement.classList.add("attach_toggle");
  pk = _this.getAttribute('data-pk');
    if (!block.querySelector(".doc_input")){
      div = create_preview_doc("select_doc1", pk);
      $doc_input = document.createElement("span");
      $doc_input.innerHTML = '<input type="hidden" class="doc_input" name="doc" value="1">';
      block.append($doc_input)
    }
    else if (!block.querySelector(".select_doc2")){div = create_preview_doc("select_doc2", pk)}
    else if (!block.querySelector(".select_doc3")){div = create_preview_doc("select_doc3", pk)}
    else if (!block.querySelector(".select_doc4")){div = create_preview_doc("select_doc4", pk)}
    else if (!block.querySelector(".select_doc5")){div = create_preview_doc("select_doc5", pk)}
    else if (!block.querySelector(".select_doc6")){div = create_preview_doc("select_doc6", pk)}
    else if (!block.querySelector(".select_doc7")){div = create_preview_doc("select_doc7", pk)}
    else if (!block.querySelector(".select_doc8")){div = create_preview_doc("select_doc8", pk)}
    else if (!block.querySelector(".select_doc9")){div = create_preview_doc("select_doc9", pk)}
    else if (!block.querySelector(".select_doc10")){div = create_preview_doc("select_doc10", pk)}
  block.append(div);

  add_file_message_attach()
  is_full_message_attach();
}

function good_message_attach(_this, block) {
  is_full_message_attach();
  pk = _this.getAttribute('good-pk');
  uuid = _this.getAttribute('data-uuid');
  if (block.querySelector( '[good-pk=' + '"' + pk + '"]' )){
    _this.parentElement.setAttribute("tooltip", "Товар уже выбран");
    _this.parentElement.setAttribute("flow", "up");
    return
  };
  _this.parentElement.classList.add("attach_toggle");
  title = _this.querySelector(".good_title").innerHTML;
    if (!block.querySelector(".good_input")){div = create_preview_good("select_good1", _this.querySelector("img").getAttribute('data-src'), pk, uuid, title)}
    else if (!block.querySelector(".select_good2")){div = create_preview_good("select_good2", _this.querySelector("img").getAttribute('data-src'), pk, uuid, title)}
    else if (!block.querySelector(".select_good3")){div = create_preview_good("select_good3", _this.querySelector("img").getAttribute('data-src'), pk, uuid, title)}
    else if (!block.querySelector(".select_good4")){div = create_preview_good("select_good4", _this.querySelector("img").getAttribute('data-src'), pk, uuid, title)}
    else if (!block.querySelector(".select_good5")){div = create_preview_good("select_good5", _this.querySelector("img").getAttribute('data-src'), pk, uuid, title)}
    else if (!block.querySelector(".select_good6")){div = create_preview_good("select_good6", _this.querySelector("img").getAttribute('data-src'), pk, uuid, title)}
    else if (!block.querySelector(".select_good7")){div = create_preview_good("select_good7", _this.querySelector("img").getAttribute('data-src'), pk, uuid, title)}
    else if (!block.querySelector(".select_good8")){div = create_preview_good("select_good8", _this.querySelector("img").getAttribute('data-src'), pk, uuid, title)}
    else if (!block.querySelector(".select_good9")){div = create_preview_good("select_good9", _this.querySelector("img").getAttribute('data-src'), pk, uuid, title)}
    else if (!block.querySelector(".select_good10")){div = create_preview_good("select_good10", _this.querySelector("img").getAttribute('data-src'), pk, uuid, title)}
  block.append(div);
  block.querySelector(".good_input") ? null : ($good_input = document.createElement("span"), $good_input.innerHTML = '<input type="hidden" class="good_input" name="good" value="1">', block.append($good_input));

  add_file_message_attach()
  is_full_message_attach();
}

function article_message_attach(_this, block) {
  is_full_message_attach();
  uuid = _this.getAttribute('data-uuid');
  if (block.querySelector( '[data-uuid=' + '"' + uuid + '"' + ']' )){
    _this.parentElement.setAttribute("tooltip", "Статья уже выбрана");
    _this.parentElement.setAttribute("flow", "up");
    return
  };
  _this.parentElement.classList.add("attach_toggle");
  title = _this.parentElement.querySelector(".article_title").innerHTML;

    if (!block.querySelector(".article_input")){div = create_preview_article("select_article1", _this.querySelector("img").getAttribute('data-src'), uuid, title)}
    else if (!block.querySelector(".select_article2")){div = create_preview_article("select_article2", _this.querySelector("img").getAttribute('data-src'), uuid, title)}
    else if (!block.querySelector(".select_article3")){div = create_preview_article("select_article3", _this.querySelector("img").getAttribute('data-src'), uuid, title)}
    else if (!block.querySelector(".select_article4")){div = create_preview_article("select_article4", _this.querySelector("img").getAttribute('data-src'), uuid, title)}
    else if (!block.querySelector(".select_article5")){div = create_preview_article("select_article5", _this.querySelector("img").getAttribute('data-src'), uuid, title)}
    else if (!block.querySelector(".select_article6")){div = create_preview_article("select_article6", _this.querySelector("img").getAttribute('data-src'), uuid, title)}
    else if (!block.querySelector(".select_article7")){div = create_preview_article("select_article7", _this.querySelector("img").getAttribute('data-src'), uuid, title)}
    else if (!block.querySelector(".select_article8")){div = create_preview_article("select_article8", _this.querySelector("img").getAttribute('data-src'), uuid, title)}
    else if (!block.querySelector(".select_article9")){div = create_preview_article("select_article9", _this.querySelector("img").getAttribute('data-src'), uuid, title)}
    else if (!block.querySelector(".select_article10")){div = create_preview_article("select_article10", _this.querySelector("img").getAttribute('data-src'), uuid, title)}
  block.append(div);
  block.querySelector(".article_input") ? null : ($article_input = document.createElement("span"), $article_input.innerHTML = '<input type="hidden" class="article_input" name="article" value="1">', block.append($article_input));

  add_file_message_attach()
  is_full_message_attach();
}
