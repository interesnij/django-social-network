function photo_preview_delete(){
  $span = document.createElement("span");
  $span.classList.add("photo_preview_delete");
  $span.innerHTML = '<svg fill="currentColor" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
  $span.setAttribute("tooltip", "Не прикреплять");
  $span.setAttribute("flow", "up");
  return $span
}
function video_preview_delete(){
  $span = document.createElement("span");
  $span.classList.add("video_preview_delete");
  $span.innerHTML = '<svg fill="currentColor" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
  $span.setAttribute("tooltip", "Не прикреплять");
  $span.setAttribute("flow", "up");
  return $span
}
function music_preview_delete(){
  $span = document.createElement("span");
  $span.classList.add("music_preview_delete");
  $span.innerHTML = '<svg fill="currentColor" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
  $span.setAttribute("tooltip", "Не прикреплять");
  $span.setAttribute("flow", "up");
  return $span
}
function good_preview_delete(){
  $span = document.createElement("span");
  $span.classList.add("good_preview_delete");
  $span.innerHTML = '<svg fill="currentColor" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
  $span.setAttribute("tooltip", "Не прикреплять");
  $span.setAttribute("flow", "up");
  return $span
}
function article_preview_delete(){
  $span = document.createElement("span");
  $span.classList.add("article_preview_delete");
  $span.innerHTML = '<svg fill="currentColor" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
  $span.setAttribute("tooltip", "Не прикреплять");
  $span.setAttribute("flow", "up");
  return $span
}

function clear_comment_dropdown(){
  try{
  dropdowns = document.body.querySelectorAll(".current_file_dropdown");
  for (var i = 0; i < dropdowns.length; i++) {
    btn = dropdowns[i].parentElement.parentElement;
    btn.classList.remove("files_two");
    btn.classList.remove("files_one");
    btn.classList.add("files_null");
    btn.style.display = "block";
    dropdowns[i].classList.remove("current_file_dropdown");
  }} catch { null }
  try{
  img_blocks = document.body.querySelectorAll(".img_block");
  for (var i = 0; i < img_blocks.length; i++) {
    img_blocks[i].innerHTML = "";
  }} catch { null }
}
function clear_attach_block(){
  document.body.querySelector(".attach_block") ? (a_b = document.body.querySelector(".attach_block"), a_b.innerHTML = "", a_b.classList = "", a_b.classList.add("files_0"), a_b.classList.remove("attach_block")) : null;
}
function is_full_dropdown(){
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  if (dropdown.classList.contains("files_two")){
    dropdown.style.display = "none";
    document.querySelector(".create_fullscreen").style.display = "none";
    document.getElementById("create_loader").innerHTML="";
  }
  if (dropdown.classList.contains("files_one") || dropdown.classList.contains("files_null")){
    dropdown.style.display = "block"}
}
function add_file_dropdown(){
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  if (dropdown.classList.contains("files_null")){
    dropdown.classList.add("files_one"),
    dropdown.classList.remove("files_null")}
  else if(dropdown.classList.contains("files_one")){
    dropdown.classList.add("files_two"), dropdown.classList.remove("files_one")};
}
function remove_file_dropdown(){
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  if (dropdown.classList.contains("files_one")){
    dropdown.classList.add("files_null"), dropdown.classList.remove("files_one")}
  else if(dropdown.classList.contains("files_two")){
    dropdown.classList.add("files_one"), dropdown.classList.remove("files_two")};
}

function is_full_attach(){
  files_block = document.body.querySelector(".attach_block");
  if (files_block.classList.contains("files_10")){
    files_block.querySelector(".attach_panel").style.display = "none";
    document.querySelector(".create_fullscreen").style.display = "none";
    document.getElementById("create_loader").innerHTML="";
  }
  if (!files_block.classList.contains("files_10")){
    files_block.querySelector(".attach_panel") ? files_block.querySelector(".attach_panel").style.display = "block" : null}
}
function add_file_attach(){
  files_block = document.body.querySelector(".attach_block");
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
function remove_file_attach(){
  files_block = document.body.querySelector(".attach_block");
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

function create_preview_photo(div_class, img_src, pk){
  $div = document.createElement("div");
  $div.classList.add("col-md-4", "photo", div_class);
  $input = document.createElement("span");
  $input.innerHTML = '<input type="hidden" name="' + div_class + '" value="' + pk + '">';
  $img = document.createElement("img");
  $img.classList.add("u_photo_detail", "image_fit");
  $img.src = img_src;
  $img.setAttribute('photo-uuid', pk);
  $div.append(photo_preview_delete());
  $div.append($input);
  $div.append($img);
  return $div
}
function photo_comment_attach(_this, dropdown) {
  is_full_dropdown();
  img_block = dropdown.parentElement.previousElementSibling;

  if (img_block.querySelector( '[photo-uuid=' + '"' + _this.getAttribute('photo-uuid') + '"' + ']' )){
    _this.parentElement.setAttribute("tooltip", "Изображение уже выбрано");
    _this.parentElement.setAttribute("flow", "up");
    return
  };
  _this.classList.add("attach_toggle");
  pk = _this.getAttribute('photo-uuid');
    if (img_block.querySelector(".select_photo1")){
        div = create_preview_photo("select_photo2", _this.getAttribute('data-src'), pk)
      }
    else if (img_block.querySelector(".select_photo2") || !img_block.querySelector(".select_photo1")){
        div = create_preview_photo("select_photo1", _this.getAttribute('data-src'), pk)
      }
  img_block.append(div);
  img_block.querySelector(".photo_input") ? null : ($photo_input = document.createElement("span"), $photo_input.innerHTML = '<input type="hidden" class="photo_input" name="photo" value="1">', img_block.append($photo_input));

  add_file_dropdown()
  is_full_dropdown();
}
function photo_post_attach(_this, block) {
  is_full_attach();
  if (block.querySelector( '[photo-uuid=' + '"' + _this.getAttribute('photo-uuid') + '"' + ']' )){
    _this.parentElement.setAttribute("tooltip", "Изображение уже выбрано");
    _this.parentElement.setAttribute("flow", "up");
    return
  };
  _this.classList.add("attach_toggle");
  pk = _this.getAttribute('photo-uuid');
    if (!block.querySelector(".photo_input")){div = create_preview_photo("select_photo1", _this.getAttribute('data-src'), pk)}
    else if (block.querySelector(".select_photo1")){div = create_preview_photo("select_photo2", _this.getAttribute('data-src'), pk)}
    else if (block.querySelector(".select_photo2")){div = create_preview_photo("select_photo3", _this.getAttribute('data-src'), pk)}
    else if (block.querySelector(".select_photo3")){div = create_preview_photo("select_photo4", _this.getAttribute('data-src'), pk)}
    else if (block.querySelector(".select_photo4")){div = create_preview_photo("select_photo5", _this.getAttribute('data-src'), pk)}
    else if (block.querySelector(".select_photo5")){div = create_preview_photo("select_photo6", _this.getAttribute('data-src'), pk)}
    else if (block.querySelector(".select_photo6")){div = create_preview_photo("select_photo7", _this.getAttribute('data-src'), pk)}
    else if (block.querySelector(".select_photo7")){div = create_preview_photo("select_photo8", _this.getAttribute('data-src'), pk)}
    else if (block.querySelector(".select_photo8")){div = create_preview_photo("select_photo9", _this.getAttribute('data-src'), pk)}
    else if (block.querySelector(".select_photo9")){div = create_preview_photo("select_photo10", _this.getAttribute('data-src'), pk)}
  block.append(div);
  block.querySelector(".photo_input") ? null : ($photo_input = document.createElement("span"), $photo_input.innerHTML = '<input type="hidden" class="photo_input" name="photo" value="1">', block.append($photo_input));

  add_file_attach()
  is_full_attach();
}

function photo_comment_upload_attach(response, dropdown){
  is_full_dropdown();
  photo_list = response.querySelectorAll(".u_photo_detail");
  img_block = dropdown.parentElement.previousElementSibling;
  if (img_block.querySelector(".select_photo1")){
    div = create_preview_photo("select_photo2", photo_list[0].querySelector("img").getAttribute('data-src'), photo_list[0].getAttribute("photo-uuid"))
    img_block.append(div);
    add_file_dropdown();
    document.querySelector(".create_fullscreen").style.display = "none";
    document.getElementById("create_loader").innerHTML="";
    }
  else if (img_block.querySelector(".select_photo2") && !img_block.querySelector(".select_photo1")){
    div = create_preview_photo("select_photo1", photo_list[0].querySelector("img").getAttribute('data-src'), photo_list[0].getAttribute("photo-uuid"))
    img_block.append(div);
    add_file_dropdown();
    document.querySelector(".create_fullscreen").style.display = "none";
    document.getElementById("create_loader").innerHTML="";
  }
  else if (!img_block.querySelector(".select_photo2") || !img_block.querySelector(".select_photo1")){
    div = create_preview_photo("select_photo1", photo_list[0].querySelector("img").getAttribute('data-src'), photo_list[0].getAttribute("photo-uuid"))
    img_block.append(div);
    add_file_dropdown();
    div2 = create_preview_photo("select_photo2", photo_list[1].querySelector("img").getAttribute('data-src'), photo_list[1].getAttribute("photo-uuid"))
    img_block.append(div2);
    img_block.querySelector(".photo_input") ? null : ($photo_input = document.createElement("span"), $photo_input.innerHTML = '<input type="hidden" class="photo_input" name="photo" value="1">', img_block.append($photo_input));
    add_file_dropdown();
    is_full_dropdown();
}
}

function create_preview_video(div_class, img_src, pk, counter){
  $div = document.createElement("div");
  $div.classList.add("col", "video", div_class);
  $input = document.createElement("span");
  $input.innerHTML = '<input type="hidden" name="' + div_class + '" value="' + pk + '">';
  $img = document.createElement("img");
  $icon_div = document.createElement("div");
  $img.classList.add("image_fit");
  $img.src = img_src;
  $icon_div.classList.add("video_icon_play_v2", "u_video_list_detail");
  $icon_div.setAttribute("video-counter", counter);

  $div.append(video_preview_delete());
  $div.append($input);
  $div.append($img);
  $div.append($icon_div);
  return $div
}
function video_comment_attach(_this, dropdown){
  is_full_dropdown(dropdown);
  img_block = dropdown.parentElement.previousElementSibling;
  counter = _this.getAttribute('video-counter');
  if (img_block.querySelector( '[video-counter=' + '"' + counter + '"' + ']' )){
    _this.parentElement.setAttribute("tooltip", "Видеоролик уже выбран");
    _this.parentElement.setAttribute("flow", "up");
    return
  };

  pk = _this.getAttribute('data-pk');

    if (img_block.querySelector(".select_video1")){
        create_preview_video("select_video2", _this.getAttribute('data-src'), pk, counter)
      }
    else if (img_block.querySelector(".select_video2") || !img_block.querySelector(".select_video1")){
        create_preview_video("select_video1", _this.getAttribute('data-src'), pk, counter)
      }
  img_block.append($div);
  img_block.querySelector(".video_input") ? null : ($video_input = document.createElement("span"), $video_input.innerHTML = '<input type="hidden" class="video_input" name="video" value="1">', img_block.append($video_input));

  add_file_dropdown()
  is_full_dropdown();
}

function video_post_attach(_this, block) {
  is_full_attach();
  counter = _this.getAttribute('video-counter');
  if (block.querySelector( '[video-counter=' + '"' + counter + '"' + ']' )){
    _this.parentElement.setAttribute("tooltip", "Видеоролик уже выбран");
    _this.parentElement.setAttribute("flow", "up");
    return
  };
  _this.classList.add("attach_toggle");
  pk = _this.getAttribute('data-pk');
    if (!block.querySelector("video_input")){div = create_preview_video("select_video1", _this.getAttribute('data-src'), pk, counter)}
    else if (block.querySelector(".select_video1")){div = create_preview_video("select_video2", _this.getAttribute('data-src'), pk, counter)}
    else if (block.querySelector(".select_video2")){div = create_preview_video("select_video3", _this.getAttribute('data-src'), pk, counter)}
    else if (block.querySelector(".select_video3")){div = create_preview_video("select_video4", _this.getAttribute('data-src'), pk, counter)}
    else if (block.querySelector(".select_video4")){div = create_preview_video("select_video5", _this.getAttribute('data-src'), pk, counter)}
    else if (block.querySelector(".select_video5")){div = create_preview_video("select_video6", _this.getAttribute('data-src'), pk, counter)}
    else if (block.querySelector(".select_video6")){div = create_preview_video("select_video7", _this.getAttribute('data-src'), pk, counter)}
    else if (block.querySelector(".select_video7")){div = create_preview_video("select_video8", _this.getAttribute('data-src'), pk, counter)}
    else if (block.querySelector(".select_video8")){div = create_preview_video("select_video9", _this.getAttribute('data-src'), pk, counter)}
    else if (block.querySelector(".select_video9")){div = create_preview_video("select_video10", _this.getAttribute('data-src'), pk, counter)}
  block.append(div);
  block.querySelector(".video_input") ? null : ($video_input = document.createElement("span"), $video_input.innerHTML = '<input type="hidden" class="video_input" name="video" value="1">', block.append($video_input));

  add_file_attach()
  is_full_attach();
}

function create_preview_music(div_class, img_src, pk, counter){
  $div = document.createElement("div");
  $input = document.createElement("span");
  $img = document.createElement("img");
  $figure = document.createElement("figure");
  $media = document.createElement("div");

  media_body = _this.querySelector(".media-body");

  $div.classList.add("col-md-12", "music", div_class);
  $div.style.display = "flex";
  $div.style.margin = "5px";
  $div.setAttribute('music-counter', counter);

  $input.innerHTML = '<input type="hidden" name="' + div_class + '" value="' + pk + '">';

  $img.src = img_src;
  $img.style.width = "50px";
  $figure.append($img);

  $media.innerHTML = media_body.innerHTML;
  $media.style.marginLeft = "10px";
  h6 = $media.querySelector("h6");
  h6.classList.add("music_list_item");

  $div.append(music_preview_delete());
  $div.append($input);
  $div.append($figure);
  $div.append($media);
  return $div
}
function music_comment_attach(_this, dropdown){
  is_full_dropdown(dropdown);

  counter = _this.getAttribute('music-counter');
  img_block = dropdown.parentElement.previousElementSibling;

  if (img_block.querySelector( '[music-counter=' + '"' + counter + '"' + ']' )){
    _this.setAttribute("tooltip", "Аудиозапись уже выбрана");
    _this.setAttribute("flow", "up");
    return
  };
  _this.classList.add("attach_toggle");
    if (img_block.querySelector(".select_music1")){
        div = create_preview_music("select_music2", _this.querySelector("img").getAttribute('data-src'), _this.getAttribute('data-pk'), _this.getAttribute('music-counter') )
      }
    else if (img_block.querySelector(".select_music2") || !img_block.querySelector(".select_music1")){
        div = create_preview_music("select_music1", _this.querySelector("img").getAttribute('data-src'), _this.getAttribute('data-pk'), _this.getAttribute('music-counter') )
      }
    add_file_dropdown();
    img_block.append(div)
    img_block.querySelector(".music_input") ? null : ($music_input = document.createElement("span"), $music_input.innerHTML = '<input type="hidden" class="music_input" name="music" value="1">', img_block.append($music_input));

  is_full_dropdown();
}

function music_post_attach(_this, block) {
  is_full_attach();
  counter = _this.getAttribute('music-counter');
  if (block.querySelector( '[music-uuid=' + '"' + counter + '"' + ']' )){
    _this.parentElement.setAttribute("tooltip", "Аудиозапись уже выбрана");
    _this.parentElement.setAttribute("flow", "up");
    return
  };
  _this.classList.add("attach_toggle");
  pk = _this.getAttribute('data-pk');
    if (!block.querySelector("video_input")){div = create_preview_music("select_music1", _this.querySelector("img").getAttribute('data-src'), pk, counter)}
    else if (block.querySelector(".select_music1")){div = create_preview_music("select_music2", _this.querySelector("img").getAttribute('data-src'), pk, counter)}
    else if (block.querySelector(".select_music2")){div = create_preview_music("select_music3", _this.querySelector("img").getAttribute('data-src'), pk, counter)}
    else if (block.querySelector(".select_music3")){div = create_preview_music("select_music4", _this.querySelector("img").getAttribute('data-src'), pk, counter)}
    else if (block.querySelector(".select_music4")){div = create_preview_music("select_music5", _this.querySelector("img").getAttribute('data-src'), pk, counter)}
    else if (block.querySelector(".select_music5")){div = create_preview_music("select_music6", _this.querySelector("img").getAttribute('data-src'), pk, counter)}
    else if (block.querySelector(".select_music6")){div = create_preview_music("select_music7", _this.querySelector("img").getAttribute('data-src'), pk, counter)}
    else if (block.querySelector(".select_music7")){div = create_preview_music("select_music8", _this.querySelector("img").getAttribute('data-src'), pk, counter)}
    else if (block.querySelector(".select_music8")){div = create_preview_music("select_music9", _this.querySelector("img").getAttribute('data-src'), pk, counter)}
    else if (block.querySelector(".select_music9")){div = create_preview_music("select_music10", _this.querySelector("img").getAttribute('data-src'), pk, counter)}
  block.append(div);
  block.querySelector(".music_input") ? null : ($music_input = document.createElement("span"), $music_input.innerHTML = '<input type="hidden" class="music_input" name="music" value="1">', block.append($music_input));

  add_file_attach()
  is_full_attach();
}

function create_preview_good(div_class, img_src, pk, title){
  $div = document.createElement("div");
  $div.classList.add("col", "u_good_detail", "good", div_class);
  $div.setAttribute('good-pk', pk);
  $div.style.cursor = "pointer";

  $input = document.createElement("span");
  $title = document.createElement("span");
  $title.innerHTML = '<span class="badge badge-info mb-2" style="position: absolute;bottom:-8px;"><svg style="padding-bottom: 1px" height="13" fill="#FFFFFF" viewBox="0 0 24 24" width="13"><path d="M0 0h24v24H0z" fill="none"/><path d="M17.21 9l-4.38-6.56c-.19-.28-.51-.42-.83-.42-.32 0-.64.14-.83.43L6.79 9H2c-.55 0-1 .45-1 1 0 .09.01.18.04.27l2.54 9.27c.23.84 1 1.46 1.92 1.46h13c.92 0 1.69-.62 1.93-1.46l2.54-9.27L23 10c0-.55-.45-1-1-1h-4.79zM9 9l3-4.4L15 9H9zm3 8c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2z"/></svg>' + title + '</span>';
  $input.innerHTML = '<input type="hidden" name="' + div_class + '" value="' + pk + '">';
  $img = document.createElement("img");
  $img.classList.add("image_fit");
  $img.src = img_src;

  $div.append(good_preview_delete());
  $div.append($input);
  $div.append($title);
  $div.append($img);
  return $div
}
function good_comment_attach(_this, dropdown){
  is_full_dropdown();
  img_block = dropdown.parentElement.previousElementSibling;

  if (img_block.querySelector( '[good-pk=' + '"' + _this.getAttribute('good-pk') + '"' + ']' )){
    _this.setAttribute("tooltip", "Товар уже выбран");
    _this.setAttribute("flow", "up");
    return
  };

  _this.classList.add("attach_toggle");
  pk = _this.getAttribute('good-pk');
  title = _this.querySelector(".good_title").innerHTML;

    if (img_block.querySelector(".select_good1")){
      div = create_preview_good("select_good2", _this.querySelector("img").getAttribute('data-src'), pk, _this.querySelector(".good_title").innerHTML)
    }
    else if (img_block.querySelector(".select_good2") && !img_block.querySelector(".select_good1")){
      div = create_preview_good("select_good1", _this.querySelector("img").getAttribute('data-src'), pk, _this.querySelector(".good_title").innerHTML)
    }
    else {
      div = create_preview_good("select_good1", _this.querySelector("img").getAttribute('data-src'), pk, _this.querySelector(".good_title").innerHTML)
    }

  img_block.append(div);
  img_block.querySelector(".good_input") ? null : ($good_input = document.createElement("span"), $good_input.innerHTML = '<input type="hidden" class="good_input" name="good" value="1">', img_block.append($good_input));

  add_file_dropdown()
  is_full_dropdown();
}

function create_preview_article(div_class, img_src, uuid, title){
  $div = document.createElement("div");
  $div.classList.add("col", "article", div_class);
  $title = document.createElement("span");
  $div.setAttribute('item-uuid', uuid);
  $div.style.cursor = "pointer";

  $input = document.createElement("span");
  $input.innerHTML = '<input type="hidden" name="' + div_class + '" value="' + uuid + '">';

  $img = document.createElement("img");
  $img.style.width = "100%";
  $img.classList.add("image_fit");
  $p = document.createElement("p");
  $figure = document.createElement("figure");
  $figure.classList.add("u_article_detail");

  $img.src = img_src;
  $figure.append($img);
  $title.innerHTML = '<span class="badge badge-info mb-2" style="position: absolute;bottom:-8px;"><svg style="padding-bottom: 1px" height="13" fill="#FFFFFF" viewBox="0 0 24 24" width="13"><path d="M0 0h24v24H0z" fill="none"/><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>' + title + '</span>'

  $div.append(article_preview_delete());
  $div.append($input);
  $div.append($figure);
  $div.append($title);
  return $div
}
function article_comment_attach(_this, dropdown){
  is_full_dropdown(dropdown);
  uuid = _this.getAttribute('item-uuid');
  img_block = dropdown.parentElement.previousElementSibling;

  if (img_block.querySelector( '[item-uuid=' + '"' + uuid + '"' + ']' )){
    _this.setAttribute("tooltip", "Статья уже выбрана");
    _this.setAttribute("flow", "up");
    return
  };

  _this.classList.add("attach_toggle");

    if (img_block.querySelector(".select_article1")){
        div = create_preview_article("select_article2", _this.querySelector("img").getAttribute('data-src'), uuid, _this.querySelector(".article_title").innerHTML)
      }
    else if (img_block.querySelector(".select_article2") || !img_block.querySelector(".select_article1")){
        div = create_preview_article("select_article1", _this.querySelector("img").getAttribute('data-src'), uuid, _this.querySelector(".article_title").innerHTML)
      }
  img_block.append(div);
  img_block.querySelector(".article_input") ? null : ($article_input = document.createElement("span"), $article_input.innerHTML = '<input type="hidden" class="article_input" name="article" value="1">', img_block.append($article_input));

  add_file_dropdown()
  is_full_dropdown();
}

function create_reload_page(form, post_link, history_link) {
	form_data = new FormData(form);
  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'POST', post_link, true );
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
          elem_ = document.createElement('span');
          elem_.innerHTML = ajax_link.responseText;
          ajax = elem_.querySelector("#reload_block");
          rtr = document.getElementById('ajax');
          rtr.innerHTML = ajax.innerHTML;
          pk = rtr.querySelector(".pk_saver").getAttribute("data-pk");
          window.scrollTo(0,0);
          document.title = elem_.querySelector('title').innerHTML;
          if_list(rtr);
          window.history.pushState(null, "vfgffgfgf", history_link + pk + '/');
      }
    }
    ajax_link.send(form_data);
}

class ToastManager {
	constructor(){
		this.id = 0;
		this.toasts = [];
		this.icons = {
			'SUCCESS': "",
			'ERROR': '',
			'INFO': '',
			'WARNING': '',
		};

		var body = document.querySelector('#ajax');
		this.toastsContainer = document.createElement('div');
		this.toastsContainer.classList.add('toasts', 'border-0');
		body.appendChild(this.toastsContainer);
	}

	showSuccess(message) {
		return this._showToast(message, 'SUCCESS');
	}
	showError(message) {
		return this._showToast(message, 'ERROR');
	}
	showInfo(message) {
		return this._showToast(message, 'INFO');
	}
	showWarning(message) {
		return this._showToast(message, 'WARNING');
	}
	_showToast(message, toastType) {
		var newId = this.id + 1;

		var newToast = document.createElement('div');
		newToast.style.display = 'inline-block';
		newToast.classList.add(toastType.toLowerCase());
		newToast.classList.add('toast');
		newToast.innerHTML = `
			<progress max="100" value="0"></progress>
			<h3> ${message} </h3>`;
		var newToastObject = {
			id: newId,
			message,
			type: toastType,
			timeout: 4000,
			progressElement: newToast.querySelector('progress'),
			counter: 0,
			timer: setInterval(() => {
				newToastObject.counter += 1000 / newToastObject.timeout;
				newToastObject.progressElement.value = newToastObject.counter.toString();
        if(newToastObject.counter >= 100) {
					newToast.style.display = 'none';
					clearInterval(newToastObject.timer);
					this.toasts = this.toasts.filter((toast) => {
						return toast.id === newToastObject.id;
					});
				}
			}, 10)
		}

		newToast.addEventListener('click', () => {
			newToast.style.display = 'none';
			clearInterval(newToastObject.timer);
			this.toasts = this.toasts.filter((toast) => {
				return toast.id === newToastObject.id;
			});
		});

		this.toasts.push(newToastObject);
		this.toastsContainer.appendChild(newToast);
		return this.id++;
	}
}
function toast_success(text){
	var toasts = new ToastManager();
	toasts.showSuccess(text);
}
function toast_error(text){
	var toasts = new ToastManager();
	toasts.showError(text);
}
function toast_info(text){
	var toasts = new ToastManager();
	toasts.showInfo(text);
}
function toast_warning(text){
	var toasts = new ToastManager();
	toasts.showWarning(text);
}

function elementInViewport(el){var bounds = el.getBoundingClientRect();return ((bounds.top + bounds.height > 0) && (window.innerHeight - bounds.top > 0));}
function on(elSelector,eventName,selector,fn) {var element = document.querySelector(elSelector);element.addEventListener(eventName, function(event) {var possibleTargets = element.querySelectorAll(selector);var target = event.target;for (var i = 0, l = possibleTargets.length; i < l; i++) {var el = target;var p = possibleTargets[i];while(el && el !== element) {if (el === p) {return fn.call(p, event);}el = el.parentNode;}}});};

function send_comment(form, block, link){
  form_comment = new FormData(form);
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', link, true );
	(form.querySelector(".text-comment").value || form.querySelector(".img_block").firstChild) ? null : toast_error("Напишите или прикрепите что-нибудь");
  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    form.querySelector(".form-control-rounded").value="";
    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
		block.append(new_post);
		toast_success(" Комментарий опубликован");
    form.querySelector(".img_block").innerHTML = "";
    try{form_dropdown = form.querySelector(".current_file_dropdown");form_dropdown.classList.remove("current_file_dropdown");form_dropdown.parentElement.parentElement.classList.remove("files_one", "files_two");form_dropdown.parentElement.parentElement.classList.add("files_null")}catch { null }
  }};

  link_.send(form_comment);
}

function is_full_dropdown(){
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  if (dropdown.classList.contains("files_two")){
    dropdown.style.display = "none";
    document.querySelector(".create_fullscreen").style.display = "none";
    document.getElementById("create_loader").innerHTML="";
  }
  if (dropdown.classList.contains("files_one") || dropdown.classList.contains("files_null")){
    dropdown.style.display = "block"}
}
function add_file_dropdown(){
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  if (dropdown.classList.contains("files_null")){
    dropdown.classList.add("files_one"),
    dropdown.classList.remove("files_null")}
  else if(dropdown.classList.contains("files_one")){
    dropdown.classList.add("files_two"), dropdown.classList.remove("files_one")};
}
function remove_file_dropdown(){
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  if (dropdown.classList.contains("files_one")){
    dropdown.classList.add("files_null"), dropdown.classList.remove("files_one")}
  else if(dropdown.classList.contains("files_two")){
    dropdown.classList.add("files_one"), dropdown.classList.remove("files_two")};
}

function load_chart() {
  try{
var ctx = document.getElementById('canvas');
var dates = ctx.getAttribute('data-dates').split(",");
var data_1 = ctx.getAttribute('data-data_1').split(",");
var data_2 = ctx.getAttribute('data-data_2').split(",");
var label_1 = ctx.getAttribute('data-label_1');
var label_2 = ctx.getAttribute('data-label_2');

var config = {
type: 'line',
data: {
  labels: dates,
  datasets: [{
    label: label_1,
    backgroundColor: 'rgb(255, 99, 132)',
    borderColor: 'rgb(255, 99, 132)',
    data: data_1,
    fill: false,
  }, {
    label: label_2,
    fill: false,
    backgroundColor: 'rgb(54, 162, 235)',
    borderColor: 'rgb(54, 162, 235)',
    data: data_2,
  }]
},
options: {
  responsive: true,
  title: {display: true,text: ''},
  tooltips: {mode: 'index',intersect: false,},
  hover: {mode: 'nearest',intersect: true},
  scales: {
  xAxes: [{display: true,scaleLabel: {display: true,labelString: ''}}],
  yAxes: [{display: true,scaleLabel: {display: true,labelString: ''}}]
  }
}
};

ctx.getContext('2d');window.myLine = new Chart(ctx, config);
}catch{return}
}

function addStyleSheets (href) {
  $head = document.head,
  $link = document.createElement('link');
  $link.rel = 'stylesheet';
  $link.classList.add("my_color_settings");
  $link.href = href;
  $head.appendChild($link);
  console.log("added!")
}

function dragElement(elmnt) {
  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  document.querySelector("#draggable-header").onmousedown = dragMouseDown;
	document.querySelector("#draggable-resize").onmousedown = resizeMouseDown;

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
		var content = document.querySelector(".draggable");
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

function open_fullscreen(link, block) {
  var link_, elem;
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', link, true );
  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    block.parentElement.style.display = "block";
    block.innerHTML = elem
  }};
  link_.send();
}
function if_list(block){
  // проверяем, если ли на странице блок с подгрузкой списка. Если есть, грузим список
  if(block.querySelector('#news_load')){
    var news_load, link;
    news_load = block.querySelector('#news_load');link = news_load.getAttribute("data-link");
    list_load(block.querySelector("#news_load"), link);
  }else if(block.querySelector('#lenta_load')){
    var lenta_load, link;
    lenta_load = block.querySelector('#lenta_load');link = lenta_load.getAttribute("data-link");
    list_load(block.querySelector("#lenta_load"), link);
  }else if(block.querySelector('#lenta_community')){
    var lenta_community, link;
    lenta_community = block.querySelector('#lenta_community');link = lenta_community.getAttribute("data-link");
    list_load(block.querySelector("#lenta_community"), link);
  }else if(block.querySelector('#photo_load')){
    var photo_load, link;
    photo_load = block.querySelector('#photo_load');link = photo_load.getAttribute("data-link");
    list_load(block.querySelector("#photo_load"), link);
  }else if(block.querySelector('#album_photo_load')){
    var album_photo_load, link;
    album_photo_load = block.querySelector('#album_photo_load');link = album_photo_load.getAttribute("data-link");
    list_load(block.querySelector("#album_photo_load"), link);
  };
}

function list_load(block,link) {
  // подгрузка списка
  var request = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );request.open( 'GET', link, true );request.onreadystatechange = function () {if ( request.readyState == 4 && request.status == 200 ) {block.innerHTML = request.responseText;}};request.send( null );
}

function msToTime(duration) {
  var milliseconds = parseInt((duration % 1000) / 100),
    seconds = Math.floor((duration / 1000) % 60),
    minutes = Math.floor((duration / (1000 * 60)) % 60);

  minutes = (minutes < 10) ? "0" + minutes : minutes;
  seconds = (seconds < 10) ? "0" + seconds : seconds;

  return minutes + ":" + seconds;
}

function vote_reload(link_1, link_2, _like_block, _dislike_block){
  like_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  like_link.open( 'GET', link_1, true );
  like_link.onreadystatechange = function () {
  if ( like_link.readyState == 4 && like_link.status == 200 ) {
    span_1 = document.createElement("span");
    span_1.innerHTML = like_link.responseText;
    _like_block.innerHTML = "";
    _like_block.innerHTML = span_1.innerHTML;
  }}
  like_link.send( null );

  dislike_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  dislike_link.open( 'GET', link_2, true );
  dislike_link.onreadystatechange = function () {
  if ( dislike_link.readyState == 4 && like_link.status == 200 ) {
    span_2 = document.createElement("span");
    span_2.innerHTML = dislike_link.responseText;
    _dislike_block.innerHTML = "";
    _dislike_block.innerHTML = span_2.innerHTML;
  }}
  dislike_link.send( null );
}

function send_like(item, link){
  like = item.querySelector(".like");
  dislike = item.querySelector(".dislike");
  link__ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link__.overrideMimeType("application/json");
  link__.open( 'GET', link, true );

  link__.onreadystatechange = function () {
  if ( link__.readyState == 4 && link__.status == 200 ) {
    jsonResponse = JSON.parse(link__.responseText);
    likes_count = item.querySelector(".likes_count");
    dislikes_count = item.querySelector(".dislikes_count");
    likes_count.innerHTML = jsonResponse.like_count;
    dislikes_count.innerHTML = jsonResponse.dislike_count;
    like.classList.toggle("btn_success");
    like.classList.toggle("btn_default");
    dislike.classList.add("btn_default");
    dislike.classList.remove("btn_danger");
  }};
  link__.send( null );
}

function send_dislike(item, link){
  like = item.querySelector(".like");
  dislike = item.querySelector(".dislike");
  link__ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link__.overrideMimeType("application/json");
  link__.open( 'GET', link, true );

  link__.onreadystatechange = function () {
  if ( link__.readyState == 4 && link__.status == 200 ) {
    jsonResponse = JSON.parse(link__.responseText);
    likes_count = item.querySelector(".likes_count");
    dislikes_count = item.querySelector(".dislikes_count");
    likes_count.innerHTML = jsonResponse.like_count;
    dislikes_count.innerHTML = jsonResponse.dislike_count;
    dislike.classList.toggle("btn_danger");
    dislike.classList.toggle("btn_default");
    like.classList.add("btn_default");
    like.classList.remove("btn_success");
  }};
  link__.send( null );
}

function get_video_dop(){
  styles = document.querySelectorAll(".my_color_settings");
  style= styles[styles.length- 1];
  settings = [];
  if (style.href.indexOf("white") != -1
      || style.href.indexOf("orange") != -1
      || style.href.indexOf("grey") != -1
      || style.href.indexOf("brown") != -1
      || style.href.indexOf("teal") != -1
      || style.href.indexOf("skyblue") != -1
      || style.href.indexOf("blue") != -1
      || style.href.indexOf("purple") != -1
      || style.href.indexOf("red") != -1){
    settings += ["images/video_white",'#eeeeee','#FFFFFF']
  }else if (style.href.indexOf("dark-grey") != -1){
    settings += ["images/video_dark",'#000000','#000000']
  }
  return settings.split(',')
}

function load_video_playlist(video_saver_id, counter) {
  video_saver = document.body.querySelector("#video_id_saver");
  styles = document.querySelectorAll(".my_color_settings");
  style = styles[styles.length- 1];

video_player = new FWDUVPlayer({
    instanceName:video_saver_id,
    parentId: "video_player",
    playlistsId:"video_playlists",
    skinPath: get_video_dop()[0],
    mainFolderPath:"/static",
    displayType:"responsive",                 // тип дисплея (выбран отзывчивый к размерам экрана)
    useVectorIcons:"no",                      // использование векторной графики
    fillEntireVideoScreen:"no",               // заполнение всего экрана видео-роликом
    fillEntireposterScreen:"yes",             // заполнение всего экрана постером
    goFullScreenOnButtonPlay:"no",            // показывать кнопку включения полноэкранного режима
    playsinline:"yes",                        // играет в ряд
    initializeOnlyWhenVisible:"no",           // инициализировать плеер только тогда, когда он виден
    youtubeAPIKey:'AIzaSyCgbixU3aIWCkiZ76h_E-XpEGig5mFhnVY', // ключ разработчика для ютуба
    useHEXColorsForSkin:"no",                 // использование hex кодировки для скина
    normalHEXButtonsColor:"#FF0000",          // цвет кнопки
    selectedHEXButtonsColor:"#000000",        // цвет нажатой кнопки
    useResumeOnPlay:"no",                     // использование резюме при проигрывании
    useDeepLinking:"no",                      // использование глубоких ссылок для ограничения перехвата ссылки на видео
    showPreloader:"yes",                      // gjrfpsdfnm ghtkjflth ghb pfuheprt gktthf
    preloaderBackgroundColor:"#000000",       // цвет фона прелоадера
    preloaderFillColor:"#FFFFFF",             // цвет прелоадера
    addKeyboardSupport:"no",                 // использовать поддержку клавиатуры
    autoScale:"yes",                          // автоматическое масштабирование
    stopVideoWhenPlayComplete:"no",           // остановить плеер после проигрывания последнего ролика
    playAfterVideoStop:"yes",                 // воспроизведение после остановки видео
    autoPlay:"no",                            // автоматический старт проигрывания
    loop:"no",                                // повтор видео сразу
    shuffle:"no",                             // перемешивание видео сразу
    showErrorInfo:"no",                       // показывать информацию об ошибках
    maxWidth:1170,                            // максимальная ширина
    maxHeight:659,                            // максимальная высота
    volume:.8,                                // начальная громкость плеера (1 - 100%)
    backgroundColor:get_video_dop()[1],                // цвет фона
    videoBackgroundColor:"#000000",           // цвет фона видео-секции
    posterBackgroundColor:"#000000",          // цвет фона постера

    //logo settings
    showLogo:"no",                            // показывать логотип над секцией видео справа

    //playlists/categories settings
    showPlaylistsSearchInput:"no",            // показывать поле поиска плейлиста
    usePlaylistsSelectBox:"no",              // использовать выбор плейлистов в окне сверху
    showPlaylistsByDefault:"no",              // показать плейлист по умолчанию
    thumbnailSelectedType:"opacity",          // анимация выбранного плейлиста в окне сверху
    startAtPlaylist:0,                        // проигрывать плейлист номер ...
    buttonsMargins:15,                        // расстояние между кнопками
    thumbnailMaxWidth:350,                    // максимальная ширина миниатюры
    thumbnailMaxHeight:350,                   // максимальная высота миниатюры
    horizontalSpaceBetweenThumbnails:40,      // расстояние между миниатюрами по горизонтали
    verticalSpaceBetweenThumbnails:40,        // расстояние между миниатюрами по вертикали
    inputBackgroundColor:"#333333",           // цвет фона поля ввода
    inputColor:"#000000",                     // цвет текста поля ввода

    //playlist settings
    showPlaylistButtonAndPlaylist:"yes",      // показывать кнопку выбора плейлистов и сами плейлисты сверху
    playlistPosition:"right",                 // расположение плейлиста
    showPlaylistByDefault:"yes",              // показать плейлист по умолчанию
    showPlaylistName:"no",                   // показывать название плейлиста
    showSearchInput:"no",                    // показывать поле поиска
    showLoopButton:"yes",                     // показывать кнопку повтора
    showShuffleButton:"yes",                  // показывать кнопку перемешивания
    showPlaylistOnFullScreen:"no",            // показывать плейлист в режиме полного экрана
    showNextAndPrevButtons:"yes",             // показывать кнопки пред/след видео
    showThumbnail:"yes",                      // показывать миниатюры
    addMouseWheelSupport:"yes",               // поддержка управления мыши
    startAtRandomVideo:"no",                  // начинать воспроиведение со случайного видео ролика
    stopAfterLastVideoHasPlayed:"no",         // останавливать воспроизведение после последнего ролика
    addScrollOnMouseMove:"no",                // перемотка движениями мыши
    randomizePlaylist:'no',                   // случайные плейлисты
    folderVideoLabel:"VIDEO ",                // название папки видео
    playlistRightWidth:320,                   // ширина плейлиста справа
    playlistBottomHeight:380,                 // высота плейлиста снизу
    startAtVideo:0,                           // начинать с ролика номер ...
    maxPlaylistItems:50,                      // максимальное количество роликов в плейлисте
    thumbnailWidth:71,                        // ширина миниатюры
    thumbnailHeight:71,                       // высота миниатюры
    spaceBetweenControllerAndPlaylist:1,      // расстояние между контроллером и плейлистом
    spaceBetweenThumbnails:1,                 // расстояние между миниатюрами
    scrollbarOffestWidth:8,                   // отступ ширины скроллбара
    scollbarSpeedSensitivity:.5,              // скорость отклика скроллбара
    playlistBackgroundColor:get_video_dop()[1],         // цвет фона плейлиста
    playlistNameColor:get_video_dop()[1],              // цвет названия плейлиста
    thumbnailNormalBackgroundColor:get_video_dop()[2], // цвет фона миниатюры
    thumbnailHoverBackgroundColor:get_video_dop()[1],  // цвет фона активной миниатюры
    thumbnailDisabledBackgroundColor:get_video_dop()[1], // цвет фона disabled миниатюры
    youtubeAndFolderVideoTitleColor:get_video_dop()[1],// цвет плейлиста роликов с папок и ютуба
    youtubeOwnerColor:"#919191",              // цвет названия ролика я ютуба
    youtubeDescriptionColor:"#919191",        // цвет описания ролика я ютуба
    mainSelectorBackgroundSelectedColor:get_video_dop()[2], // цвет фона плейлиста при наведении
    mainSelectorTextNormalColor:get_video_dop()[1],    // цвет текста плейлиста
    mainSelectorTextSelectedColor:get_video_dop()[2],
    mainButtonBackgroundNormalColor:get_video_dop()[2],// цвет фона кнопок
    mainButtonBackgroundSelectedColor:get_video_dop()[2],// цвет фона нажатой кнопки
    mainButtonTextNormalColor:get_video_dop()[2],      // цвет текста кнопок
    mainButtonTextSelectedColor:get_video_dop()[2],    // цвет текста нажатой кнопки

    //controller settings
    showController:"yes",                     // показывать контроллер
    showControllerWhenVideoIsStopped:"yes",   // показывать контроллер при остановке проигрывания
    showNextAndPrevButtonsInController:"no",  // показывать кнопки пред / след на контроллере
    showRewindButton:"yes",                   // показать кнопку перемотки назад
    showPlaybackRateButton:"yes",             // показать кнопку выбора скорости воспроизведения
    showVolumeButton:"yes",                   // показать кнопку громкости
    showTime:"yes",                           // показать время воспроизведения
    showQualityButton:"yes",                  // показать время выбора качества видео
    showInfoButton:"no",                     // показывать кнопку информации ролика
    showShareButton:"no",                     // показывать кнопку расшаривания ролика
    showEmbedButton:"no",                    // показывать кнопку получения ссылки ролика и фрейма для вставки на другие сайты
    showChromecastButton:"no",                // показывать кнопку подкастов
    showFullScreenButton:"yes",               // показывать кнопку полноэкранного режима
    disableVideoScrubber:"no",                // выключить ползунок переключения времени видео
    showScrubberWhenControllerIsHidden:"yes", // показывать ползунок времени воспроизведенного ролика при скрытом контроллере
    showDefaultControllerForVimeo:"no",       // показывать контроллер vimeo
    repeatBackground:"yes",                   // повтор бекгроунда
    controllerHeight:42,                      // высота контроллера
    controllerHideDelay:3,                    // время, через которое скроется контроллер
    startSpaceBetweenButtons:7,               // начальное расстояние между кнопками
    spaceBetweenButtons:8,                    // расстояние между кнопками
    scrubbersOffsetWidth:2,                   // ширина отступа скруббера
    mainScrubberOffestTop:14,                 // отступ скруббера всерху
    timeOffsetLeftWidth:5,                    // ширина отступа времени воспроизведения слева
    timeOffsetRightWidth:3,                   // ширина отступа времени воспроизведения справа
    timeOffsetTop:0,                          // отступ времени воспроизведения сверху
    volumeScrubberHeight:80,                  // высота скруббера громкости
    volumeScrubberOfsetHeight:12,             // отступскруббера громкости по высоте
    timeColor:"#919191",                      // цвет времени воспроизведения
    youtubeQualityButtonNormalColor:"#919191",// кнопка выбора качества плейлитса ютуба
    youtubeQualityButtonSelectedColor:"#000000",// нажатая кнопка выбора качества плейлитса ютуба

    //advertisement on pause window
    aopwTitle:"Advertisement",                // название рекламной вставки
    aopwWidth:400,                            // ширина вставки
    aopwHeight:240,                           // высота вставки
    aopwBorderSize:6,                         // размер рамки вставки
    aopwTitleColor:"#000000",                 // цветназвания вставки

    //subtitle
    subtitlesOffLabel:"Субтитры откл.",       // надпись, когда субтитры отключены

    //popup add windows
    showPopupAdsCloseButton:"no",            // показать кнопку закрытия окна подставки

    //окно размещения и информации
    embedAndInfoWindowCloseButtonMargins:15,  // отступ кнопки закрытия
    borderColor:"#CDCDCD",                    // цвет рамки
    mainLabelsColor:"#000000",                // цвет названия
    secondaryLabelsColor:"#444444",           // вторичный цвет названия
    shareAndEmbedTextColor:"#777777",         // цвет тектса овна расшаривания и вставки
    inputBackgroundColor:"#c0c0c0",           // цвет фона поля ввода
    inputColor:"#333333",                     // цвет фона текста ввода

    //audio visualizer
    audioVisualizerLinesColor:"#ff9f00",      // цвет линий аудио визуализатора
    audioVisualizerCircleColor:"#FFFFFF",     // цвет кругов аудио визуализатора

    //lightbox settings
    lightBoxBackgroundOpacity:.6,             // прозрачность
    lightBoxBackgroundColor:"#000000",        // цвет фона

    //sticky on scroll
    stickyOnScroll:"no",                      // липкое листание
    stickyOnScrollShowOpener:"yes",           // показывать эффект
    stickyOnScrollWidth:"700",                // ширина
    stickyOnScrollHeight:"394",               // высота

    //настройки липкого дисплея
    showOpener:"yes",                         // показывать вставки
    showOpenerPlayPauseButton:"yes",          // показывать кнопку плей при паузе
    verticalPosition:"bottom",                // позиция по вертикали
    horizontalPosition:"center",              // позиция по горизонтали
    showPlayerByDefault:"yes",                // показывать плеер по умолчанию
    animatePlayer:"yes",                      // анимировать плеер
    openerAlignment:"right",                  // выравнивание вставки
    mainBackgroundImagePath:"main-background.png", // путь до изображения фона
    openerEqulizerOffsetTop:-1,               // отступ эквалайзера сверху
    openerEqulizerOffsetLeft:3,               // отступ эквалайзера слева
    offsetX:0,                                // отступ по оси X
    offsetY:0,																// отступ по оси Y

    //скорость воспроизведения
    defaultPlaybackRate:1,                   //0.25, 0.5, 1, 1.25, 1.2, 2
    //cuepoints
    executeCuepointsOnlyOnce:"no",           // выполнение ключевых точек только один раз
    //annotations
    showAnnotationsPositionTool:"no",        // показывать координаты аннотаций на экране

    //ads
    openNewPageAtTheEndOfTheAds:"no",        // открыть новую страницу в конце объявления
    adsButtonsPosition:"left",               // позиция окна рекламы
    skipToVideoText:"Закрыть через: ",       // текст окна рекламы
    skipToVideoButtonText:"Закрыть",         // текст кнопки закрытия рекламного окна
    adsTextNormalColor:"#888888",            // цвет рекламного текста
    adsTextSelectedColor:"#000000",          // цвет выбранного текста
    adsBorderNormalColor:"#AAAAAA",          // цвет рамки рекламного окна
    adsBorderSelectedColor:"#000000",        // цвет выбраной рамки рекламного окна

    //a to b loop
    useAToB:"no",                            // использование повтора от...до
    atbTimeBackgroundColor:"transparent",    // время фона от...до
    atbTimeTextColorNormal:"#888888",        // время текста от...до
    atbTimeTextColorSelected:"#FFFFFF",
    atbButtonTextNormalColor:"#888888",
    atbButtonTextSelectedColor:"#FFFFFF",
    atbButtonBackgroundNormalColor:"#FFFFFF",
    atbButtonBackgroundSelectedColor:"#000000",

    //thumbnails preview
    thumbnailsPreviewWidth:196,              // ширина предпросмотра миниатюры
    thumbnailsPreviewHeight:110,             // высота предпросмотра миниатюры
    thumbnailsPreviewBackgroundColor:get_video_dop()[1],// цвет фона  миниатюры
    thumbnailsPreviewBorderColor:"#666",     // цвет названия миниатюры
    thumbnailsPreviewLabelBackgroundColor:"#666", // цвет фона названия минатюры
    thumbnailsPreviewLabelFontColor:"#FFF",
    // context menu
    showContextmenu:'no',
    showScriptDeveloper:"no",
    contextMenuBackgroundColor:"#ebebeb",
    contextMenuBorderColor:"#ebebeb",
    contextMenuSpacerColor:"#CCC",
    contextMenuItemNormalColor:"#888888",
    contextMenuItemSelectedColor:"#000",
    contextMenuItemDisabledColor:"#BBB"
});
}

function get_resize_screen(){
  video_player.maxWidth = 360;
  video_player.maxHeight = 270;
  video_player.showPlaylist();
}
function get_normal_screen(){
  video_player.maxWidth = 1170;
  video_player.maxHeight = 659;
  video_player.hidePlaylist();
}

function save_playlist(suffix, post_link, get_link, track_id){
    var playlist_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    playlist_link.open( 'GET', post_link, true );
    playlist_link.onreadystatechange = function () {
    if ( playlist_link.readyState == 4 && playlist_link.status == 200 ) {
      document.querySelector("body").className = "";
      document.querySelector("body").classList.add(suffix);

      var _link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
      _link.open( 'GET', get_link, true );
      _link.onreadystatechange = function () {
        if ( _link.readyState == 4 && _link.status == 200 ) {
          var response = document.createElement('span');
          response.innerHTML = _link.responseText;
          var list = response.querySelectorAll("li");
          var count = list.length;
          for(i=0; i<count; i++) {
            _source=list[i].getAttribute("data-path") + '/stream?client_id=' + 'dce5652caa1b66331903493735ddd64d';
            _title=list[i].getAttribute("data-title");
            _thumbPath=list[i].getAttribute("data-thumbpath");
            _duration=list[i].getAttribute("data-duration");
            time = msToTime(_duration);
            music_player.addTrack(_source, _title, _thumbPath, time, true, false, null);
          }
          music_player.loadPlaylist(0);
          if (FWDMSP.LOAD_PLAYLIST_COMPLETE){
            console.log("Плейлист загружен!");
          setTimeout(function() {music_player.playSpecificTrack(suffix, track_id)}, 50);
        }
      }};
      _link.send( null );
    }};
    playlist_link.send( null );
    };

    music_player = new FWDMSP({
    		//main settings
    		instanceName:"player1",
    		playlistsId:"audio_playlists",
    		mainFolderPath:"/static/images/",
    		skinPath:"audio_white",
    		showSoundCloudUserNameInTitle:"no",   // показывать имя пользователя soundcloud
    		showMainBackground:"yes",  						// показать общий фон
    		verticalPosition:"bottom",                    // расположение плеера
    		rightClickContextMenu:"developer",
    		useDeepLinking:"no",									// использовать глубокие ссылки - защита от перехвата. Не будет работать с souncloud
    		rightClickContextMenu:"no",           // показ контекстног меню по щелчку правой кнопкой мыши
    		addKeyboardSupport:"no",             // добавить поддержку клавиатуры
    		animate:"yes",												// фнимация
    		autoPlay:"no",												// автостарт плеера
    		loop:"no",														// повтор песни
    		shuffle:"no",													// перемешивание треков
    		maxWidth:850,                         // максимальная ширина
    		volume:.8,														// громкость по умолчанию 80%

    		// controller settings
    		showControllerByDefault:"yes",        // показать контроллер по умолчанию
    		showThumbnail:"yes",                  // показывать миниатюры
    		showNextAndPrevButtons:"yes",					// показывать кнопки переключения треков
    		showSoundAnimation:"yes",							// показывать анимацию музыкального воспроизведения
    		showLoopButton:"yes",                 // показывать кнопку повтора треков
    		showShuffleButton:"yes",              // показывать кнопку перемешивания треков
    		expandBackground:"no",
    		showBuyButton:"yes",
        showPlaylistItemBuyButton:"no",
    		titleColor:"#000000",                 // цвет названия
    		timeColor:"#919191",                  // цвет времени

    		// настройки выравнивания и размера контроллера (подробно описаны в документации!)
    		controllerHeight:76,                 // высота контроллера
    		startSpaceBetweenButtons:9,          // начальное пространство между кнопками
    		spaceBetweenButtons:8,               // пространство между кнопками
    		separatorOffsetOutSpace:5,           // смещение разделителя вне пространства
    		separatorOffsetInSpace:9,            // смещение разделителя в пространстве
    		lastButtonsOffsetTop:14,             // смещение последних кнопок сверху
    		allButtonsOffsetTopAndBottom:14,     // смещение всех кнопок вверх и вниз
    		titleBarOffsetTop:13,                // смещение сверху секции названия
    		mainScrubberOffsetTop:47,            // смещение сверху скруббера
    		spaceBetweenMainScrubberAndTime:10,  // пространство между скруббером и секцией времени
    		startTimeSpace:10,                   // пространство относительно начала в секуии времени
    		scrubbersOffsetWidth:2,              // ширина смещения скруббера
    		scrubbersOffestTotalWidth:0,         // общая ширина смещения скруббера
    		volumeButtonAndScrubberOffsetTop:47, // всещение сверху скруббера и кнопки громкости
    		spaceBetweenVolumeButtonAndScrubber:6,// пространство между скруббером и кнопкой громмкости
    		volumeScrubberOffestWidth:4,         // смещение слева скруббера громкости
    		scrubberOffsetBottom:10,             // сммещение скруббера снизу
    		equlizerOffsetLeft:1,                // смещение эквалайзера влево

    		//playlists window settings
    		showPlaylistsSearchInput:"no",      // показывать поле поиска в плейлисте
    		usePlaylistsSelectBox:"no",         // показывать поле плейлистов сверху выбранного плейлиста
    		showPlaylistsSelectBoxNumbers:"no", // пронумеровать плейлисты в поле выбора плейлиста
    		showPlaylistsButtonAndPlaylists:"yes", // показывать кнопку, вызывающую окно плейлистов сверху и сами плейлисты
    		showPlaylistsByDefault:"no",         // показывать плейлист по умолчанию
    		thumbnailSelectedType:"opacity",     // тип выбора миниатюры (к примеру прозрачность)
    		startAtPlaylist:0,                   // воспроизводить с плейлиста номер...
    		startAtTrack:0,                      // воспроизводить с трека номер...
    		startAtRandomTrack:"no",             // воспроизводить со случайного трека...
    		buttonsMargins:0,                    // отступы кнопок
    		thumbnailMaxWidth:330,               // макс. ширина миниатюр
    		thumbnailMaxHeight:330,              // макс. высота миниатюр
    		horizontalSpaceBetweenThumbnails:40, // пространство между миниатюрами по горизонтали
    		verticalSpaceBetweenThumbnails:40,   // пространство между миниатюрами по вертикали
    		mainSelectorBackgroundSelectedColor:"#FFFFFF", // цвет фона выбранного
    		mainSelectorTextNormalColor:"#737373",  // цвет текста селектора
    		mainSelectorTextSelectedColor:"#000000", // цвет текста селектора выбранного
    		mainButtonTextNormalColor:"#7C7C7C", // цвет текста кнопок
    		mainButtonTextSelectedColor:"#FFFFFF", // цвет текста кнопок выбранных

    		//playlist settings
    		playTrackAfterPlaylistLoad:"no",     // воспроизведение трека после загрузки плейлиста
    		//showPlayListButtonAndPlaylist:"yes",
    		showPlayListOnAndroid:"yes",         // показывать плейлисты на android
    		showPlayListByDefault:"no",          // показывть плейлист по умолчанию
    		showPlaylistItemPlayButton:"yes",    // показать кнопку воспроизведения элемента плейлиста
    		addScrollBarMouseWheelSupport:"yes",  // прокручивать колесиком мыши
    		showTracksNumbers:"yes",							// показывать номер трека
    		playlistBackgroundColor:"#000000",    // цвет фона плейлиста
    		trackTitleNormalColor:"#737373",      // цвет заголовка трека
    		trackTitleSelectedColor:"#000000",    // цвет заголовка выбранного трека
    		trackDurationColor:"#7C7C7C",         // цвет времени трека
    		maxPlaylistItems:30,                  // Макс. количество плейлистов
    		nrOfVisiblePlaylistItems:12,          // число видимых элементов списка воспроизведения
    		trackTitleOffsetLeft:0,               // смещение слева заголовка трека
    		playPauseButtonOffsetLeftAndRight:11, // смещение слева и справа кнопки play
    		durationOffsetRight:9,							  // смещение справа продолжительности трека
    		scrollbarOffestWidth:7,               // шмрмна смещения полосы прокрутки

    		//playback rate / speed
    		showPlaybackRateButton:"yes",         // показать кнопку скорости воспроизведения
    		defaultPlaybackRate:1, //min - 0.5 / max - 3 // скорость воспроизведения по умолчанию (от 0,5 до 3)
    		playbackRateWindowTextColor:"#888888",// цвет текста на окне выбора скорости

    		//search bar settings
    		showSearchBar:"no",                  // показывать секцию поиска треков
    		showSortButtons:"yes",                // показывать секцию сортировки треков
    		searchInputColor:"#999999",						// цвет секции поиска
    		searchBarHeight:38,									  // высота секции поиска
    		inputSearchTextOffsetTop:1,           // смещение текста ввода поиска сверху
    		inputSearchOffsetLeft:0,              // смещение текста ввода поиска слева

    		//opener settings
    		openerAlignment:"right",              // открывание
    		showOpener:"yes",                     // показывать эффект
    		showOpenerPlayPauseButton:"yes",      // показывать кнопку плей / пауза
    		openerEqulizerOffsetLeft:3,           // сдвигание эквалайзера слева
    		openerEqulizerOffsetTop:-1,           // сдвигание эквалайзера сверху

    		//a to b loop
    		atbTimeBackgroundColor:"transparent", // цвет фона "от / до"
    		atbTimeTextColorNormal:"#888888",     // цвет текста "от / до"
    		atbTimeTextColorSelected:"#FFFFFF",   // цвет выбранного текста "от / до"
    		atbButtonTextNormalColor:"#888888",   // цвет кнопки "от / до"
    		atbButtonTextSelectedColor:"#FFFFFF", // цвет выбранной кнопки "от / до"
    		atbButtonBackgroundNormalColor:"#FFFFFF", // цвет фона кнопки "от / до"
    		atbButtonBackgroundSelectedColor:"#000000", // цвет фона выбранной кнопки "от / до"
    	});

    FWDMSPUtils.onReady(function(){
            music_player.addListener(FWDMSP.READY, music_onReady);
            music_player.addListener(FWDMSP.PLAY, music_onPlay);
            music_player.addListener(FWDMSP.PAUSE, music_onPause);
        });

function music_onReady(){console.log("Аудио плеер готов");}

    function music_onPause(){
      try{
      div = document.createElement("div");
      div.innerHTML = music_player.getTrackTitle();
      title = div.querySelector('span').innerHTML;
      document.title = "Музыка приостановлена";
      if(document.querySelector(".user_status")){
        document.querySelector(".user_status").innerHTML = "Музыка приостановлена";
      }}catch{null}
    }
    function music_onPlay(){
        console.log("Воспроизводится трек № : " + music_player.getTrackId());
        try{
        div = document.createElement("div");
        div.innerHTML = music_player.getTrackTitle();
        title = div.querySelector('span').innerHTML;
        document.title = title;
        if(document.querySelector(".user_status")){
          document.querySelector(".user_status").innerHTML = title;
        }}catch{null};
        try{video_player.pause();}catch{null}
    };


    function get_image_priview(ggg, img) {
    entrou = false;
    img.click();

    img.onchange = function() {
      if (!entrou) {imgPath = img.value;
        extn = imgPath.substring(imgPath.lastIndexOf(".") + 1).toLowerCase();
      if (extn == "gif" || extn == "png" || extn == "jpg" || extn == "jpeg")
      {if (typeof FileReader != "undefined") {
        if (ggg){

        }
        ggg.innerHTML = "";
        reader = new FileReader();
        reader.onload = function(e) {
          $img = document.createElement("img");
          $img.id = "targetImageCrop";
          $img.src = e.target.result;
          $img.class = "thumb-image";
          ggg.innerHTML = '<a href="#" style="position: absolute;right:15px;top: 0;" class="delete_thumb">Удалить</a>'
          ggg.append($img);
          };
          reader.readAsDataURL(img.files[0]);
        }
      } else { this.value = null; }
    } entrou = true;
    setTimeout(function() { entrou = false; }, 1000);
    }};

    function ajax_get_reload(url) {
      var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
        ajax_link.open( 'GET', url, true );
        ajax_link.onreadystatechange = function () {
          if ( this.readyState == 4 && this.status == 200 ) {
            elem_ = document.createElement('span');
            elem_.innerHTML = ajax_link.responseText;
            ajax = elem_.querySelector("#reload_block");
            rtr = document.getElementById('ajax');
            rtr.innerHTML = ajax.innerHTML;
            window.scrollTo(0,0);
            title = elem_.querySelector('title').innerHTML;
            window.history.pushState(null, "vfgffgfgf", url);
            document.title = title;
            if_list(rtr);
            load_chart()
          }
        }
        ajax_link.send();
    }

if_list(document.getElementById('ajax'));
load_chart()
