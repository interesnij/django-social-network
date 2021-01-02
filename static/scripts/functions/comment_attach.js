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
    close_create_window()
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

function photo_comment_attach(dropdown, photo_pk, user_pk, src) {
  is_full_dropdown();
  img_block = dropdown.parentElement.previousElementSibling;
  div = create_preview_photo(src, photo_pk, user_pk);
  img_block.append(div);
  add_file_dropdown()
  is_full_dropdown();
}

function photo_comment_upload_attach(photo_list, dropdown, block_divs_length){
  is_full_dropdown();

  img_block = dropdown.parentElement.previousElementSibling;
  for (var i = 0; i < block_divs_length; i++){
    div = create_preview_photo(parent.getAttribute('data-href'), parent.getAttribute("photo-pk"), parent.getAttribute("data-pk"));
    block.append(div);
    img_block.append(div);
    add_file_dropdown()
    is_full_dropdown();
  }
close_create_window()
}

function video_comment_attach(dropdown, pk, counter, src){
  is_full_dropdown(dropdown);
  img_block = dropdown.parentElement.previousElementSibling;
  div = create_preview_video(src, pk, counter)
  img_block.append($div);
  add_file_dropdown()
  is_full_dropdown();
}

function music_comment_attach(dropdown, pk, counter, src){
  is_full_dropdown(dropdown);
  img_block = dropdown.parentElement.previousElementSibling;
  div = create_preview_music(src, pk, counter )
  add_file_dropdown();
  img_block.append(div)
  is_full_dropdown();
}
function doc_comment_attach(dropdown, media_block, pk){
  is_full_dropdown(dropdown);
  img_block = dropdown.parentElement.previousElementSibling;
  div = create_preview_doc(media_block, pk)
  add_file_dropdown();
  img_block.append(div)
  is_full_dropdown();
}
function good_comment_attach(dropdown, src, pk, uuid, title){
  is_full_dropdown();
  img_block = dropdown.parentElement.previousElementSibling;
  div = create_preview_good(src, pk, uuid, title)
  img_block.append(div);
  add_file_dropdown()
  is_full_dropdown();
}

function article_comment_attach(_this, dropdown){
  is_full_dropdown(dropdown);
  uuid = _this.getAttribute('data-uuid');
  img_block = dropdown.parentElement.previousElementSibling;
  div = create_preview_article(_this.querySelector("img").getAttribute('data-src'), uuid, _this.parentElement.querySelector(".article_title").innerHTML)
  img_block.append(div);
  add_file_dropdown()
  is_full_dropdown();
}
