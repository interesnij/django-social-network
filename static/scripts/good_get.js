
on('#ajax', 'click', '#good_image', function() {
  img = this.previousElementSibling.querySelector("#id_image")
  get_image_priview(this, img);
});
on('#ajax', 'click', '#good_image2', function() {
  img = this.previousElementSibling.querySelector("#id_image2")
  get_image_priview(this, img);
});
on('#ajax', 'click', '#good_image3', function() {
  img = this.previousElementSibling.querySelector("#id_image3")
  get_image_priview(this, img);
});
on('#ajax', 'click', '#good_image4', function() {
  img = this.previousElementSibling.querySelector("#id_image4")
  get_image_priview(this, img);
});
on('#ajax', 'click', '#good_image5', function() {
  img = this.previousElementSibling.querySelector("#id_image5")
  get_image_priview(this, img);
});


on('#ajax', 'click', '.u_good_detail', function() {
  uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid');
  pk = this.getAttribute('good-pk');
  loader = document.getElementById("good_loader");
  open_fullscreen('/goods/user/good/' + pk + '/' + uuid + '/', loader);
  setTimeout(function() {good_gallery(loader)}, 1000)
});

on('#ajax', 'click', '#c_good_add', function() {
  pk = this.getAttribute('data-pk');
  loader = document.getElementById("good_add_loader");
  open_fullscreen('/goods/community/add/' + pk + '/', loader)
});
on('#ajax', 'click', '#u_good_add', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("create_loader");
  open_fullscreen('/goods/user/add/' + pk + '/', loader)
});
on('#ajax', 'click', '#good_add_attach', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("create_loader");
  open_fullscreen('/goods/user/add_attach/' + pk + '/', loader);
});

on('#ajax', 'change', '.goods_category', function() {
  var val = this.value;
  if (val == '') {
    document.getElementById('subcat').innerHTML = "";
  } else {
    var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    link.open( 'GET', "/goods/progs/cat/" + val + "/", true );
    link.onreadystatechange = function () {
      if ( link.readyState == 4 ) {
          if ( link.status == 200 ) {
              var sub = document.getElementById("subcat");
              sub.innerHTML = link.responseText;
          }
      }
  };
  link.send( null );
  };
});

function good_gallery(loader){
  thumb_list = loader.querySelectorAll(".thumb_list li");
  thumb = loader.querySelector(".big_img");
  thumb_list.forEach((item) => {
    item.addEventListener("mouseover", function () {
    image = item.children[0].src;
      thumb.src = image;
    });
  });
}

on('#ajax', 'click', '#add_good_user_btn', function() {
  if (!document.body.querySelector("#id_title").value){
    document.body.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else if (!document.body.querySelector("#category").value){
    document.body.querySelector("#category").style.border = "1px #FF0000 solid";
    toast_error("Категория - обязательное поле!")
  } else if (!document.body.querySelector("#id_description").value){
    document.body.querySelector("#id_description").style.border = "1px #FF0000 solid";
    toast_error("Описание товара - обязательное поле!");
  } else if (!document.body.querySelector("#id_image").value){
    document.body.querySelector("#good_image").style.border = "1px #FF0000 solid";
    toast_error("Фотография на обложку обязательна!")
  }
  pk_block = document.body.querySelector(".pk_saver");
  pk = pk_block.getAttribute("data-pk");
  form_data = new FormData(document.body.querySelector("#add_good_user_form"));
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/goods/user/add/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    new_good = document.createElement("span");
    new_good.innerHTML = elem;

    if (document.querySelector(".is_comment_attach")){
      dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
      is_full_dropdown();
      img_block = dropdown.parentElement.previousElementSibling;
      xxx = new_good.querySelector(".new_image")
      pk = xxx.getAttribute('good-pk');

        $input = document.createElement("span");
        $img = document.createElement("img");
        $title = document.createElement("span");

        if (img_block.querySelector(".select_good2")){
            is_full_dropdown()}
        else if (img_block.querySelector(".select_good1")){
            $div = document.createElement("div");
            $div.classList.add("col-md-6", "select_good2");
            $input.innerHTML = '<input type="hidden" name="select_good2" value="' + pk + '">';;
          }
        else {
            $div = document.createElement("div", "select_good1");
            $div.classList.add("col-md-6", "select_good1");
            $input.innerHTML = '<input type="hidden" name="select_good" value="' + pk + '">';
          }

      $div.setAttribute('good-pk', pk);
      $div.style.cursor = "pointer";
      $div.classList.add("u_good_detail");

      $img.classList.add("image_fit");
      $img.src = xxx.querySelector("img").getAttribute('data-src');

      title = new_good.querySelector(".good_title").innerHTML;
      $title.innerHTML = '<span class="badge badge-info mb-2" style="position: absolute;bottom:-8px;"><svg style="padding-bottom: 1px" height="13" fill="#FFFFFF" viewBox="0 0 24 24" width="13"><path d="M0 0h24v24H0z" fill="none"/><path d="M17.21 9l-4.38-6.56c-.19-.28-.51-.42-.83-.42-.32 0-.64.14-.83.43L6.79 9H2c-.55 0-1 .45-1 1 0 .09.01.18.04.27l2.54 9.27c.23.84 1 1.46 1.92 1.46h13c.92 0 1.69-.62 1.93-1.46l2.54-9.27L23 10c0-.55-.45-1-1-1h-4.79zM9 9l3-4.4L15 9H9zm3 8c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2z"/></svg>' + title + '</span>'

      $div.append(get_delete_span());
      $div.append($input);
      $div.append($title);
      $div.append($img);
      img_block.append($div);
      add_file_dropdown();
      toast_info("Товар создан!")
    } else {
      goods = document.body.querySelector("#goods_container");
      new_good.querySelector(".new_image") ? (goods.prepend(new_good), toast_info("Товар создан!"),
                                              goods.querySelector(".goods_empty") ? goods.querySelector(".goods_empty").style.display = "none" : null)
               : null;
  }
  document.querySelector(".create_fullscreen").style.display = "none";
  document.getElementById("create_loader").innerHTML="";
  }};
  link_.send(form_data);
});
