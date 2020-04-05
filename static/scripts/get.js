
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

//$('.add_board_hide').on('click', function() {$('#for_settings').hide();});
//$('#images_upload').on('click', function() {$('#for_images_upload').show();});
//$('#settings').on('click', function() {$('#for_settings').show();});
//$('#gallery').on('click', function() {$('#for_gallery').show();});
//$('#doc').on('click', function() {$('#for_doc').show();});
//('#good').on('click', function() {$('#for_good').show();});
//$('#question').on('click', function() {$('#for_question').show();});
/*!
   fullscreen open scripts for community
  */

  //$('#ajax').on('click', '#good_add', function() {$('#good_add_loader').html('').load("{% url 'good_add_community' pk=user.pk %}");$('.good_add_fullscreen').show();})
  //$('#ajax').on('click', '#article_add', function() {$('#article_loader').html('').load("{% url 'article_add_user' pk=user.pk %}"); $('.article_fullscreen').show();})
  //$('#ajax').on('click', '.u_photos_add', function() { $('#photos_add_window').show();console.log("user photos add open")})
  //$('#ajax').on('click', '.u_albums_add', function() {user = $(this);user_id = user.data("uuid"); $('#photo_add_loader').html('').load("/gallery/user/add_album/" + user_id + "/"); $('.photofullscreen').show();console.log("user album photos add open")})
  //$('body').on('click', '.u_photo_edit', function() {$('#block_description_form').show();console.log("user description photo open");});
  //$("#u_albums_add").click(function() {$('#photos_add_window').show();console.log("user photo form open")})
  //$("#u_albums_add").click(function() {user = $(this);user_id = user.data("uuid");$('#photo_add_loader').html('').load("/gallery/user/add_album/" + user_id + "/");$('.photo_fullscreen').show();console.log("user album add open")})

  /*!
     comments scripts
    */
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

//$('body').on('click', '.comment_image', function() {photo = $(this);pk = photo.data("id");uuid = photo.data("uuid");$('#photo_loader').html('').load("/gallery/load/comment/" + pk + "/" + uuid + "/"); $('.photo_fullscreen').show();console.log("show user photos for select image")});

//$('body').on('click', '.upload_photo', function() {
//  btn = $(this); img_block = btn.parent().parent().prev();
//  if (!img_block.empty()){img_block.empty()};
//  img_block.append('<span class="close_upload_block" title="Закрыть панель загрузки фото"><svg fill="currentColor" style="width:15px" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span><div class="col-lg-6 col-md-6"><a href="#" style="display:none" class="delete_thumb1">Удалить</a><input class="file1 hide_image" type="file" //name="photo" accept="image/*" id="id_item_comment_photo"><div class="comment_photo1"><h4 class="svg_default"><svg width="35" height="35" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/>+<path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg></h4></div></div><div class="col-lg-6 col-md-6"><a href="#" style="display:none" //class="delete_thumb1">Удалить</a><input class="file2 hide_image" type="file" name="photo2" accept="image/*" id="id_item_comment_photo2"><div class="comment_photo2"><h4 class="svg_default"><svg width="35" height="35" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">+<path d="M0 0h24v24H0z" fill="none"/><path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg></h4></div><///div>');img_block.show();console.log("load comment upload block")});

//$('body').on('click', '.comment_photo1', function() {img = $(this);entrou = false;imageLoader = img.prev();imageLoader.click();$(imageLoader).on("change", function() {if (!entrou) {imgPath = $(this)[0].value;extn = imgPath.substring(imgPath.lastIndexOf(".") + 1).toLowerCase();if (extn == "gif" || extn == "png" || extn == "jpg" || extn == "jpeg") {if (typeof FileReader != "undefined") {image_holder = $(img); image_holder.empty();reader = new FileReader();reader.onload = function(e) { $img = $("<img />", { id: "targetImageCrop", src: e.target.result, class: "thumb-image" }).appendTo(image_holder); }; image_holder.show(); reader.readAsDataURL($(this)[0].files[0]);} } else { this.value = null; } } entrou = true; setTimeout(function() { entrou = false; }, 1000); img.prev().prev().show();console.log("upload comment image 1")});});

//$('body').on('click', '.comment_photo2', function() {img = $(this);entrou = false;imageLoader = img.prev();imageLoader.click();$(imageLoader).on("change", function() {if (!entrou) {imgPath = $(this)[0].value;extn = imgPath.substring(imgPath.lastIndexOf(".") + 1).toLowerCase();if (extn == "gif" || extn == "png" || extn == "jpg" || extn == "jpeg") {if (typeof FileReader != "undefined") {image_holder = $(img); image_holder.empty();reader = new FileReader();reader.onload = function(e) { $img = $("<img />", { id: "targetImageCrop", src: e.target.result, class: "thumb-image" }).appendTo(image_holder); }; image_holder.show(); reader.readAsDataURL($(this)[0].files[0]);} } else { this.value = null; } } entrou = true; setTimeout(function() { entrou = false; }, 1000); img.prev().prev().show();console.log("upload comment image 2")});});

//$('body').on('click', '.close_upload_block', function() {$(this).parent().empty();console.log("comment upload block closed")});
//$('body').on('click', '.delete_thumb1', function(e) {e.preventDefault(); var a = $(this); a.parent().empty().append('<a href="#" style="display:none" class="delete_thumb1">Удалить</a><input class="file1 hide_image" type="file" name="photo" accept="image/*" id="id_item_comment_photo"><div class="comment_photo1"><h4 class="svg_default"><svg width="35" height="35" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none" /><path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z" /></svg></h4></div>');console.log("comment image deleted")});

//$('body').on('click', '.select_photo', function() {uuid = $(this).data("uuid");$('#photo_loader').html("").load("/users/load/img_load/" + uuid + "/"); $('.photo_fullscreen').show();console.log("select image for comment form")});



Index.initLink();
if_list(document.getElementById('ajax'));

on('body', 'click', '.menu_drop', function() {var block = this.nextElementSibling;block.classList.toggle("show");});
