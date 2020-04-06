
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

class Index {
  // класс, работающий с подгрузкой блоков на сайте. Смена основного блока, листание отдельных элементов, и т.д.
  static initLink() {document.body.querySelectorAll('.ajax').forEach( lin => lin.addEventListener('click', Index.push_url) );}
  static push_url(event){
    event.preventDefault();
    var ajax_link, url;
    ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    url = this.getAttribute('href');
    if (url != window.location.pathname){
      ajax_link.open( 'GET', url, true );
      ajax_link.onreadystatechange = function () {
        if ( this.readyState == 4 && this.status == 200 ) {
          var rtr, elem_, ajax;
          rtr = document.getElementById('ajax');
          elem_ = document.createElement('span');
          elem_.innerHTML = ajax_link.responseText;
          ajax = elem_.querySelector("#reload_block");
          rtr.innerHTML = ajax.innerHTML;
          document.title = elem_.querySelector('title').innerHTML;
          window.history.pushState({route: url}, "network", url);

          Index.initLink();
          if_list(rtr);
          load_chart();
        }
      }
      ajax_link.send();
    }
  };
}

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
  console.log(img_block);
  if (img_block != null){img_block.innerHTML = ""};
  img_block.innerHTML = '<span class="close_upload_block" title="Закрыть панель загрузки фото"><svg fill="currentColor" style="width:15px;margin-top: 20px" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span><div class="col-lg-6 col-md-6"><a href="#" style="display:none" class="delete_thumb1">Удалить</a><input class="file1 hide_image" type="file" name="photo" accept="image/*" id="id_item_comment_photo"><div class="comment_photo1"><h4 class="svg_default"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/>+<path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg></h4></div></div><div class="col-lg-6 col-md-6"><a href="#" style="display:none" class="delete_thumb1">Удалить</a><input class="file2 hide_image" type="file" name="photo2" accept="image/*" id="id_item_comment_photo2"><div class="comment_photo2"><h4 class="svg_default"><svg fill="currentColor" viewBox="0 0 24 24">+<path d="M0 0h24v24H0z" fill="none"/><path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg></h4></div></div>'
});

on('#ajax', 'click', '.close_upload_block', function() {
  this.this.parentElement.innerHTML = ""
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

//$('body').on('click', '.select_photo', function() {uuid = $(this).data("uuid");$('#photo_loader').html("").load("/users/load/img_load/" + uuid + "/"); $('.photo_fullscreen').show();console.log("select image for comment form")});



Index.initLink();
if_list(document.getElementById('ajax'));

on('body', 'click', '.menu_drop', function() {var block = this.nextElementSibling;block.classList.toggle("show");});
