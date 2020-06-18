
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

    if (document.querySelector(".current_file_dropdown")){
      dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
      is_full_dropdown();
      img_block = dropdown.parentElement.previousElementSibling;
      data_pk = new_good.getAttribute("good-pk")

      if (img_block.querySelector( '[good-pk=' + '"' + data_pk + '"]' )){
        new_good.setAttribute("tooltip", "Товар уже выбран");
        new_good.setAttribute("flow", "up");
        return
      };
      new_good.classList.add("attach_toggle");
      title = new_good.querySelector(".good_title").innerHTML;
      if (!img_block.querySelector(".select_good1")){
        div = create_preview_good("select_good1", new_good.querySelector("img").getAttribute('data-src'), data_pk, title)
      } else if (!img_block.querySelector(".select_good2")){
        div = create_preview_good("select_good2", new_good.querySelector("img").getAttribute('data-src'), data_pk, title)
      }
      img_block.append(div);
      img_block.querySelector(".good_input") ? null : ($good_input = document.createElement("span"), $good_input.innerHTML = '<input type="hidden" class="good_input" name="good" value="1">', img_block.append($good_input));

      add_file_dropdown()
      is_full_dropdown();

    } else if (document.querySelector(".attach_block")){
      block = document.body.querySelector(".attach_block");
      is_full_attach();
      data_pk = new_good.getAttribute('good-pk');
      title = new_good.querySelector(".good_title").innerHTML;

      if (block.querySelector( '[good-pk=' + '"' + data_pk + '"]' )){
        new_good.setAttribute("tooltip", "Товар уже выбран");
        new_good.setAttribute("flow", "up");
        return
      };
      new_good.classList.add("attach_toggle");
      if (!block.querySelector(".good_input")){div = create_preview_good("select_good1", new_good.querySelector("img").getAttribute('data-src'), data_pk, title)}
      else if (!block.querySelector(".select_good2")){div = create_preview_good("select_good2", new_good.querySelector("img").getAttribute('data-src'), data_pk, title)}
      else if (!block.querySelector(".select_good3")){div = create_preview_good("select_good3", new_good.querySelector("img").getAttribute('data-src'), data_pk, title)}
      else if (!block.querySelector(".select_good4")){div = create_preview_good("select_good4", new_good.querySelector("img").getAttribute('data-src'), data_pk, title)}
      else if (!block.querySelector(".select_good5")){div = create_preview_good("select_good5", new_good.querySelector("img").getAttribute('data-src'), data_pk, title)}
      else if (!block.querySelector(".select_good6")){div = create_preview_good("select_good6", new_good.querySelector("img").getAttribute('data-src'), data_pk, title)}
      else if (!block.querySelector(".select_good7")){div = create_preview_good("select_good7", new_good.querySelector("img").getAttribute('data-src'), data_pk, title)}
      else if (!block.querySelector(".select_good8")){div = create_preview_good("select_good8", new_good.querySelector("img").getAttribute('data-src'), data_pk, title)}
      else if (!block.querySelector(".select_good9")){div = create_preview_good("select_good9", new_good.querySelector("img").getAttribute('data-src'), data_pk, title)}
      else if (!block.querySelector(".select_good10")){div = create_preview_good("select_good10", new_good.querySelector("img").getAttribute('data-src'), data_pk, title)}
    block.append(div);
    block.querySelector(".good_input") ? null : ($good_input = document.createElement("span"), $good_input.innerHTML = '<input type="hidden" class="good_input" name="good" value="1">', block.append($good_input));

    add_file_attach()
    is_full_attach();
    }
    else {
      goods = document.body.querySelector("#goods_container");
      new_good.querySelector(".new_image") ? (goods.prepend(new_good), toast_info("Товар создан!"),
                                              goods.querySelector(".goods_empty") ? goods.querySelector(".goods_empty").style.display = "none" : null)
               : null;
  }
  console.log(new_good);
  document.querySelector(".create_fullscreen").style.display = "none";
  document.getElementById("create_loader").innerHTML="";
  toast_info("Товар создан!")
  }};
  link_.send(form_data);
});
