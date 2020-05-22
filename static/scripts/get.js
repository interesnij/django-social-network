

//--------------------------------------------------------------------//
// FULLSCREENS //


on('#ajax', 'click', '.item_stat_f', function() {
  var parent, pk, uuid, loader
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = parent.getAttribute("item-uuid");
  loader = document.getElementById("stat_loader");
  open_fullscreen("/stat/item/" + uuid + "/", loader)
});

on('#ajax', 'click', '.article_fullscreen_hide', function() {document.querySelector(".article_fullscreen").style.display = "none";document.getElementById("article_loader").innerHTML=""});
on('#ajax', 'click', '.photo_fullscreen_hide', function() {document.querySelector(".photo_fullscreen").style.display = "none";document.getElementById("photo_loader").innerHTML=""});
on('#ajax', 'click', '.votes_fullscreen_hide', function() {document.querySelector(".votes_fullscreen").style.display = "none";document.getElementById("votes_loader").innerHTML=""});
on('#ajax', 'click', '.item_fullscreen_hide', function() {document.querySelector(".item_fullscreen").style.display = "none";document.getElementById("item_loader").innerHTML=""});
on('#ajax', 'click', '.community_fullscreen_hide', function() {document.querySelector(".community_fullscreen").style.display = "none";document.getElementById("community_loader").innerHTML=""});
on('#ajax', 'click', '.community_manage_fullscreen_hide', function() {document.querySelector(".manage_window_fullscreen").style.display = "none";document.getElementById("load_staff_window").innerHTML=""});
on('#ajax', 'click', '.good_fullscreen_hide', function() {document.querySelector(".good_fullscreen").style.display = "none";document.getElementById("good_loader").innerHTML=""});
on('#ajax', 'click', '.stat_fullscreen_hide', function() {document.querySelector(".stat_fullscreen").style.display = "none";document.getElementById("stat_loader").innerHTML=""});
on('body', 'click', '.video_fullscreen_hide', function() {document.querySelector(".video_fullscreen").style.display = "none";document.getElementById("video_loader").innerHTML=""});
on('body', 'click', '.small_video_fullscreen_hide', function() {
  //document.querySelector(".video_fullscreen").style.display = "none";
  get_normal_screen();
  //document.getElementById("video_loader").innerHTML=""
});

// END FULLSCREENS //
//--------------------------------------------------------------------//

on('#ajax', 'click', '#add_board_hide', function() {
  document.querySelector('#for_settings').style.display = "block";
});
on('#ajax', 'click', '#images_upload', function() {
  document.querySelector('#for_images_upload').style.display = "block";
});
on('#ajax', 'click', '#settings', function() {
  document.querySelector('#for_settings').style.display = "block";
});
on('#ajax', 'click', '#gallery', function() {
  document.querySelector('#for_gallery').style.display = "block";
});
on('#ajax', 'click', '#doc', function() {
  document.querySelector('#for_doc').style.display = "block";
});
on('#ajax', 'click', '#good', function() {
  document.querySelector('#for_good').style.display = "block";
});
on('#ajax', 'click', '#question', function() {
  document.querySelector('#for_question').style.display = "block";
});

on('#ajax', 'click', '.show_replies', function() {
  this.nextElementSibling.classList.toggle('replies_open');
});

on('#ajax', 'click', '.reply_comment', function() {
  var objectUser = this.previousElementSibling.innerHTML;
  var form = this.nextElementSibling.querySelector(".text-comment");
  form.value = objectUser + ', ';
  this.nextElementSibling.style.display = "block";
  form.focus();
})

on('#ajax', 'click', '.comment_image', function() {
  var uuid, pk, loader;
  pk = this.getAttribute('data-id');
  uuid = this.getAttribute('data-uuid');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/load/comment/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.upload_photo', function() {
  var img_block;
  img_block = this.parentElement.parentElement.parentElement.previousElementSibling;
  if (img_block != null){img_block.innerHTML = ""};
  img_block.innerHTML = '<span class="close_upload_block" title="Закрыть панель загрузки фото"><svg fill="currentColor" style="width:15px;margin-top: 20px" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span><div class="col-lg-6 col-md-6"><a href="#" style="display:none" class="delete_thumb1">Удалить</a><input class="file1 hide_image" type="file" name="photo" accept="image/*" id="id_item_comment_photo"><div class="comment_photo1"><h4 class="svg_default"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/>+<path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg></h4></div></div><div class="col-lg-6 col-md-6"><a href="#" style="display:none" class="delete_thumb1">Удалить</a><input class="file2 hide_image" type="file" name="photo2" accept="image/*" id="id_item_comment_photo2"><div class="comment_photo2"><h4 class="svg_default"><svg fill="currentColor" viewBox="0 0 24 24">+<path d="M0 0h24v24H0z" fill="none"/><path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg></h4></div></div>'
});

on('#ajax', 'click', '.close_upload_block', function() {
  this.parentElement.innerHTML = ""
});

on('#ajax', 'click', '.select_photo', function() {
  var uuid, loader;
  uuid = this.getAttribute('data-uuid');
  pk = this.getAttribute('data-id');
  loader = document.getElementById("good_loader");
  open_fullscreen('/users/load/img_load/' + uuid + '/', loader)
});


//'#ajax', 'click', '.comment_photo1', function() {
//mg = this;
//ntrou = false;
//mageLoader = this.previousElementSibling;
//mageLoader.click();
//n('#ajax', 'change', imageLoader, function() {
//  if (!entrou) {
//    imgPath = this.value;
//    extn = imgPath.substring(imgPath.lastIndexOf(".") + 1).toLowerCase();
//    if (extn == "gif" || extn == "png" || extn == "jpg" || extn == "jpeg")
//    {if (typeof FileReader != "undefined") {
//      image_holder = this;
//      image_holder.innerHTML = "";
//      reader = new FileReader();
//      reader.onload = function(e) {
//        $img = document.createElement("img"),
//        $img.id = "targetImageCrop";
//        $img.src = e.target.result;
//        $img.class = "thumb-image";
//        image_holder.append($img)
//        image_holder.style.display == "none";
//      }
//        reader.readAsDataURL(this.files);
//    }
//     else {this.value = null;}
//  } entrou = true;
//  setTimeout(function() { entrou = false; }, 1000);
//  this.previousElementSibling.previousElementSibling.style.display == "block";
//  );});

//$('body').on('click', '.comment_photo2', function() {
//  img = $(this);
//  entrou = false;
//  imageLoader = img.prev();
//  imageLoader.click();
//  $(imageLoader).on("change", function() {
//    if (!entrou) {imgPath = $(this)[0].value;extn = imgPath.substring(imgPath.lastIndexOf(".") + 1).toLowerCase();
//    if (extn == "gif" || extn == "png" || extn == "jpg" || extn == "jpeg")
//    {if (typeof FileReader != "undefined") {image_holder = $(img); image_holder.empty();reader = new FileReader();reader.onload = function(e) { $img = $("<img />", { id: "targetImageCrop", src: e.target.result, class: "thumb-image" }).appendTo(image_holder); }; image_holder.show(); reader.readAsDataURL($(this)[0].files[0]);} } else { this.value = null; } } entrou = true; setTimeout(function() { entrou = false; }, 1000); img.prev().prev().show();console.log("upload comment image 2")});});

//$('body').on('click', '.delete_thumb1', function(e) {e.preventDefault(); var a = $(this); a.parent().empty().append('<a href="#" style="display:none" class="delete_thumb1">Удалить</a><input class="file1 hide_image" type="file" name="photo" accept="image/*" id="id_item_comment_photo"><div class="comment_photo1"><h4 class="svg_default"><svg width="35" height="35" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none" /><path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z" /></svg></h4></div>');console.log("comment image deleted")});


Index.initLink();
if_list(document.getElementById('ajax'));

on('body', 'click', '.menu_drop', function() {var block = this.nextElementSibling;block.classList.toggle("show");});
