
function get_post_view(){
	if(document.querySelector(".post_stream")){
		container = document.querySelector(".post_stream");
		link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    list = container.querySelectorAll('.pag');
    for (var i = 0; i < list.length; i++) {
      if(!list[i].classList.contains("showed")){
        inViewport = elementInViewport(list[i]);
        if(inViewport){
					try{
          uuid = list[i].getAttribute('data-uuid');
					if (list[i].querySelector(".reklama")){
						link.open( 'GET', '/posts/user_progs/post_market_view/' + uuid + "/", true );
					} else if(!list[i].querySelector(".reklama")){
						link.open( 'GET', '/posts/user_progs/post_view/' + uuid + "/", true );
				}}catch{ null }
				link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

				link.send();
				list[i].classList.add("showed");
				console.log(i + " получил класс showed");
    }}}}}

function scrolled(link, block_id, target){
	// работа с прокруткой:
	// 1. Ссылка на страницу с пагинацией
	// 2. id блока, куда нужно грузить следующие страницы
	// 3. Указатель на нужность работы просмотров элементов в ленте. Например, target=1 - просмотры постов в ленте
	onscroll = function(){
		_block = document.body.querySelector(block_id);
		box = _block.querySelector('.last');
		if(box && box.classList.contains("last")){
				inViewport = elementInViewport(box);
				if(inViewport){
					box.classList.remove("last");
					paginate(link, block_id);
		}};
		if (target == 1){get_post_view()}
	}
}
page = 2;
loaded = false;
function paginate(link, block_id){
	block = document.body.querySelector(block_id);
	if(block.getElementsByClassName('pag').length === (page-1)*15){
		if (loaded){return};
		var link_3 = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
		link_3.open( 'GET', link + '?page=' + page++, true );
		link_3.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

		link_3.onreadystatechange = function () {
		if ( this.readyState == 4 && this.status == 200 ) {
			var elem = document.createElement('span');
			elem.innerHTML = link_3.responseText;
			if(elem.getElementsByClassName('pag').length < 15){loaded = true};
			if (elem.querySelector(block_id)){
				xxx = document.createElement("span");
				xxx.innerHTML = elem.querySelector(block_id).innerHTML;
				block.insertAdjacentHTML('beforeend', xxx.innerHTML)
				//block.append(xxx);
			} else {
				//block.append(elem)
				block.insertAdjacentHTML('beforeend', elem.innerHTML)
			}
			}
		}
		link_3.send();
	}
}

function create_pagination(block){
list = "#user_tracks_container, #user_tracks_list_container, #user_video_container";
split_list = list.split(',');
for (i in split_list){
	if(block.querySelector(i)){scrolled(window.location.href,i,target="0")}
}
}

function if_list(block){
  // проверяем, если ли на странице блок с подгрузкой списка. Если есть, грузим список/С пагинацией сразу
  if(block.querySelector('#lenta_load')){
    lenta_load = block.querySelector('#lenta_load');
		link = lenta_load.getAttribute("data-link");
    list_load(lenta_load, link);
		scrolled(link, '#lenta_load', target=1)
  }else if(block.querySelector('#lenta_community')){
    lenta_community = block.querySelector('#lenta_community');link = lenta_community.getAttribute("data-link");
    list_load(block.querySelector("#lenta_community"), link);
		scrolled(link, '#lenta_community', target=1)
  }else if(block.querySelector('#photo_load')){
    photo_load = block.querySelector('#photo_load');link = photo_load.getAttribute("data-link");
    list_load(block.querySelector("#photo_load"), link);
		scrolled(link, '#photo_load', target=0)
  }else if(block.querySelector('#c_photo_load')){
    photo_load = block.querySelector('#c_photo_load');link = photo_load.getAttribute("data-link");
    list_load(block.querySelector("#c_photo_load"), link);
		scrolled(link, '#c_photo_load', target=0)
  }else if(block.querySelector('#album_photo_load')){
    album_photo_load = block.querySelector('#album_photo_load');link = album_photo_load.getAttribute("data-link");
    list_load(block.querySelector("#album_photo_load"), link);
		scrolled(link, '#album_photo_load', target=0)
  }else if(block.querySelector('#c_album_photo_load')){
    album_photo_load = block.querySelector('#c_album_photo_load');link = album_photo_load.getAttribute("data-link");
    list_load(block.querySelector("#c_album_photo_load"), link);
		scrolled(link, '#c_album_photo_load', target=0)
  };
}
if_list(document.getElementById('ajax'));
create_pagination(document.getElementById('ajax'));

function list_load(block,link) {
  var request = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
	request.open( 'GET', link, true ); request.setRequestHeader('X-Requested-With', 'XMLHttpRequest'); request.onreadystatechange = function () {if ( request.readyState == 4 && request.status == 200 ) {block.innerHTML = request.responseText;}};request.send( null );
}

function ajax_get_reload(url) {
	// перезагрузка основного блока на страницу с указанным url
  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', url, true );
		ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
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
        load_chart();
				page = 2;
				loaded = false;
				create_pagination(rtr);
      }
    }
    ajax_link.send();
}

function this_page_reload(url) {
  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', url, true );
		ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        elem_ = document.createElement('span');
        elem_.innerHTML = ajax_link.responseText;
        ajax = elem_.querySelector("#reload_block");
        rtr = document.getElementById('ajax');
        rtr.innerHTML = ajax.innerHTML;
        window.scrollTo(0,0);
        if_list(rtr);
				page = 2;
				loaded = false;
				create_pagination(rtr);
      }
    }
    ajax_link.send();
}
