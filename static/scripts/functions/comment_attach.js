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

function photo_comment_upload_attach(photo_list, dropdown, block_divs_length){
  is_full_dropdown();

  img_block = dropdown.parentElement.previousElementSibling;
  for (var i = 0; i < block_divs_length; i++){
    if (!img_block.querySelector(".select_photo1")){
      div = create_preview_photo("select_photo1", photo_list[i].querySelector("img").getAttribute('data-src'), photo_list[i].getAttribute("photo-uuid"))
    }
    else if(!img_block.querySelector(".select_photo2")){
      div = create_preview_photo("select_photo2", photo_list[i].querySelector("img").getAttribute('data-src'), photo_list[i].getAttribute("photo-uuid"))
    }
    img_block.append(div);
    add_file_dropdown()
    is_full_dropdown();
  }
img_block.querySelector(".photo_input") ? null : ($photo_input = document.createElement("span"), $photo_input.innerHTML = '<input type="hidden" class="photo_input" name="photo" value="1">', img_block.append($photo_input));
document.querySelector(".create_fullscreen").style.display = "none";
document.getElementById("create_loader").innerHTML="";
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
function good_comment_attach(_this, dropdown){
  is_full_dropdown();
  img_block = dropdown.parentElement.previousElementSibling;
  pk = _this.getAttribute('good-pk');

  if (img_block.querySelector( '[good-pk=' + '"' + pk + '"]' )){
    _this.setAttribute("tooltip", "Товар уже выбран");
    _this.setAttribute("flow", "up");
    return
  };

  _this.classList.add("attach_toggle");
  title = _this.querySelector(".good_title").innerHTML;

    if (img_block.querySelector(".select_good1")){
      div = create_preview_good("select_good2", _this.querySelector("img").getAttribute('data-src'), pk, title)
    }
    else if (img_block.querySelector(".select_good2") && !img_block.querySelector(".select_good1")){
      div = create_preview_good("select_good1", _this.querySelector("img").getAttribute('data-src'), pk, title)
    }
    else {
      div = create_preview_good("select_good1", _this.querySelector("img").getAttribute('data-src'), pk, title)
    }

  img_block.append(div);
  img_block.querySelector(".good_input") ? null : ($good_input = document.createElement("span"), $good_input.innerHTML = '<input type="hidden" class="good_input" name="good" value="1">', img_block.append($good_input));

  add_file_dropdown()
  is_full_dropdown();
}

function article_comment_attach(_this, dropdown){
  is_full_dropdown(dropdown);
  uuid = _this.getAttribute('data-uuid');
  img_block = dropdown.parentElement.previousElementSibling;

  if (img_block.querySelector( '[data-uuid=' + '"' + uuid + '"' + ']' )){
    _this.setAttribute("tooltip", "Статья уже выбрана");
    _this.setAttribute("flow", "up");
    return
  };

  _this.classList.add("attach_toggle");

    if (img_block.querySelector(".select_article1")){
        div = create_preview_article("select_article2", _this.querySelector("img").getAttribute('data-src'), uuid, _this.parentElement.querySelector(".article_title").innerHTML)
      }
    else if (img_block.querySelector(".select_article2") || !img_block.querySelector(".select_article1")){
        div = create_preview_article("select_article1", _this.querySelector("img").getAttribute('data-src'), uuid, _this.parentElement.querySelector(".article_title").innerHTML)
      }
  img_block.append(div);
  img_block.querySelector(".article_input") ? null : ($article_input = document.createElement("span"), $article_input.innerHTML = '<input type="hidden" class="article_input" name="article" value="1">', img_block.append($article_input));

  add_file_dropdown()
  is_full_dropdown();
}
