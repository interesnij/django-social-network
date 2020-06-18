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

window.addEventListener('scroll', function() {
  console.log("scroooool");
	get_pagination(items, link, items_list) {
	page = 2;
	loaded = false;
	try{
		if(items.getElementsByClassName('item').length === (page-1)*30){
	  var height = document.documentElement.clientHeight-1;
	  if(window.scrollY+1 >= document.documentElement.scrollHeight-height){
	    if (loaded){return};
	    var link_3 = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
	    link_3.open( 'GET', link + '/?page=' + page++, true );
	    link_3.send();
	    link_3.onreadystatechange = function () {
	    if ( this.readyState == 4 && this.status == 200 ) {
	      var elem = document.createElement('span');
	      elem.innerHTML = link_3.responseText;
	      if(items_list.getElementsByClassName('infinite-item').length < 30){loaded = false;};
	      items.append(items_list);
	      }
	    }
	  }}
	}catch{return}
	}
}

function if_list(block){
  // проверяем, если ли на странице блок с подгрузкой списка. Если есть, грузим список
  if(block.querySelector('#news_load')){
    news_load = block.querySelector('#news_load');link = news_load.getAttribute("data-link");
    list_load(block.querySelector("#news_load"), link);
  }else if(block.querySelector('#lenta_load')){
    lenta_load = block.querySelector('#lenta_load');
		link = lenta_load.getAttribute("data-link");
    list_load(lenta_load, link);
		get_pagination(lenta_load, link, lenta_load.querySelector(".stream"))

  }else if(block.querySelector('#lenta_community')){
    lenta_community = block.querySelector('#lenta_community');link = lenta_community.getAttribute("data-link");
    list_load(block.querySelector("#lenta_community"), link);
  }else if(block.querySelector('#photo_load')){
    photo_load = block.querySelector('#photo_load');link = photo_load.getAttribute("data-link");
    list_load(block.querySelector("#photo_load"), link);
  }else if(block.querySelector('#album_photo_load')){
    album_photo_load = block.querySelector('#album_photo_load');link = album_photo_load.getAttribute("data-link");
    list_load(block.querySelector("#album_photo_load"), link);
  };
}
if_list(document.getElementById('ajax'));

function list_load(block,link) {
  // подгрузка списка
  var request = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );request.open( 'GET', link, true );request.onreadystatechange = function () {if ( request.readyState == 4 && request.status == 200 ) {block.innerHTML = request.responseText;}};request.send( null );
}

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
