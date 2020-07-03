function photo_preview_delete(){
  $span = document.createElement("span");
  $span.classList.add("photo_preview_delete");
  $span.innerHTML = '<svg fill="#FF0000" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
  $span.setAttribute("tooltip", "Не прикреплять");
  $span.setAttribute("flow", "up");
  return $span
}
function video_preview_delete(){
  $span = document.createElement("span");
  $span.classList.add("video_preview_delete");
  $span.innerHTML = '<svg fill="#FF0000" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
  $span.setAttribute("tooltip", "Не прикреплять");
  $span.setAttribute("flow", "up");
  return $span
}
function music_preview_delete(){
  $span = document.createElement("span");
  $span.classList.add("music_preview_delete");
  $span.innerHTML = '<svg fill="#FF0000" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
  $span.setAttribute("tooltip", "Не прикреплять");
  $span.setAttribute("flow", "up");
  return $span
}
function good_preview_delete(){
  $span = document.createElement("span");
  $span.classList.add("good_preview_delete");
  $span.innerHTML = '<svg fill="#FF0000" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
  $span.setAttribute("tooltip", "Не прикреплять");
  $span.setAttribute("flow", "up");
  return $span
}
function article_preview_delete(){
  $span = document.createElement("span");
  $span.classList.add("article_preview_delete");
  $span.innerHTML = '<svg fill="#FF0000" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
  $span.setAttribute("tooltip", "Не прикреплять");
  $span.setAttribute("flow", "up");
  return $span
}

function create_preview_photo(div_class, img_src, pk){
  $div = document.createElement("div");
  $div.classList.add("col-md-4", "photo", div_class);
  $input = document.createElement("span");
  $input.innerHTML = '<input type="hidden" name="' + div_class + '" value="' + pk + '">';
  $img = document.createElement("img");
  $img.classList.add("u_photo_detail", "image_fit", "lazyload");
  $img.setAttribute("data-src", img_src);
  $img.setAttribute('photo-uuid', pk);
  $div.append(photo_preview_delete());
  $div.append($input);
  $div.append($img);
  return $div
}

function create_preview_video(div_class, img_src, pk, counter){
  $div = document.createElement("div");
  $div.classList.add("col-md-4", "video", div_class);
  $input = document.createElement("span");
  $input.innerHTML = '<input type="hidden" name="' + div_class + '" value="' + pk + '">';
  $img = document.createElement("img");
  $icon_div = document.createElement("span");
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
function create_preview_music(div_class, img_src, pk, counter){
  $div = document.createElement("div");
  $input = document.createElement("span");
  $img = document.createElement("img");
  $figure = document.createElement("figure");
  $media = document.createElement("span");

  media_body = _this.querySelector(".media-body");

  $div.classList.add("col-md-12", "music", div_class);
  $div.style.display = "flex";
  $div.style.margin = "5px";
  $div.style.flexBasis = "100%";
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

function create_preview_good(div_class, img_src, pk, title){
  $div = document.createElement("div");
  $div.classList.add("col-md-4", "u_good_detail", "good", div_class);
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
function create_preview_article(div_class, img_src, uuid, title){
  $div = document.createElement("div");
  $div.classList.add("col-md-4", "article", div_class);
  $title = document.createElement("span");
  $div.setAttribute('data-uuid', uuid);
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

on('#ajax', 'click', '.photo_preview_delete', function() {
  parent = this.parentElement;
  block = parent.parentElement;
  parent.remove();
  block.querySelector(".photo") ? null : block.querySelector(".photo_input").parentElement.remove();

  try{ remove_file_dropdown(); is_full_dropdown()} catch { remove_file_attach(), is_full_attach()}
});
on('#ajax', 'click', '.video_preview_delete', function() {
  parent = this.parentElement;
  block = parent.parentElement;
  parent.remove();
  block.querySelector(".video") ? null : block.querySelector(".video_input").parentElement.remove();
  try{ remove_file_dropdown(); is_full_dropdown()} catch { remove_file_attach(), is_full_attach()}
});
on('#ajax', 'click', '.music_preview_delete', function() {
  parent = this.parentElement;
  block = parent.parentElement;
  parent.remove();
  block.querySelector(".music") ? null : block.querySelector(".music_input").parentElement.remove();
  try{ remove_file_dropdown(); is_full_dropdown()} catch { remove_file_attach(), is_full_attach()}
});
on('#ajax', 'click', '.good_preview_delete', function() {
  parent = this.parentElement;
  block = parent.parentElement;
  parent.remove();
  block.querySelector(".good") ? null : block.querySelector(".good_input").parentElement.remove();
  try{ remove_file_dropdown(); is_full_dropdown()} catch { remove_file_attach(), is_full_attach()}
});
on('#ajax', 'click', '.article_preview_delete', function() {
  parent = this.parentElement;
  block = parent.parentElement;
  parent.remove();
  block.querySelector(".article") ? null : block.querySelector(".article_input").parentElement.remove();
  try{ remove_file_dropdown(); is_full_dropdown()} catch { remove_file_attach(), is_full_attach()}
});
