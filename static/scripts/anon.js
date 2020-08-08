function on(elSelector,eventName,selector,fn) {var element = document.querySelector(elSelector);element.addEventListener(eventName, function(event) {var possibleTargets = element.querySelectorAll(selector);var target = event.target;for (var i = 0, l = possibleTargets.length; i < l; i++) {var el = target;var p = possibleTargets[i];while(el && el !== element) {if (el === p) {return fn.call(p, event);}el = el.parentNode;}}});};

function loadScripts( src ) {
    var script = document.createElement("SCRIPT"),
        head = document.getElementsByTagName( "head" )[ 0 ],
        error = false;

    script.type = "text/javascript";

    script.onload = script.onreadystatechange = function( e ){

        if ( ( !this.readyState || this.readyState == "loaded" || this.readyState == "complete" ) ) {
            if ( !error ) {
                removeListeners();
            } else {
                null
            }
        }
    };

    script.onerror = function() {
        error = true;
        removeListeners();
    }

    function errorHandle( msg, url, line ) {

        if ( url == src ) {
            error = true;
            removeListeners();
        }
        return false;
    }

    function removeListeners() {
        script.onreadystatechange = script.onload = script.onerror = null;

        if ( window.removeEventListener ) {
            window.removeEventListener('error', errorHandle, false );
        } else {
            window.detachEvent("onerror", errorHandle );
        }
    }

    if ( window.addEventListener ) {
        window.addEventListener('error', errorHandle, false );
    } else {
        window.attachEvent("onerror", errorHandle );
    }

    script.src = src;
    head.appendChild( script );
}

function elementInViewport(el){var bounds = el.getBoundingClientRect();return ((bounds.top + bounds.height > 0) && (window.innerHeight - bounds.top > 0));}

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

on('body', 'click', '#register_ajax', function() {
  form_data = new FormData(document.querySelector("#signup"));
  reg_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  reg_link.open( 'POST', "/rest-auth/registration/", true );
  reg_link.onreadystatechange = function () {
  if ( reg_link.readyState == 4 && reg_link.status == 200 ) {
    window.location.href = "/phone_send/"
    }};
  reg_link.send(form_data);
})
on('body', 'click', '#logg', function() {
  form_data = new FormData(document.querySelector("#login_form"));
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'POST', "/rest-auth/login/", true );
  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    window.location.href = "/main/";
    }};
  link.send(form_data);
});


function dragElement(elmnt) {
  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  document.querySelector("#draggable-header").onmousedown = dragMouseDown;
	document.querySelector("#draggable-resize").onmousedown = resizeMouseDown;

  function dragMouseDown(e) {
    e = e || window.event;
    e.preventDefault();
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    document.onmousemove = elementDrag;
  }

	function resizeMouseDown(e) {
    e = e || window.event;
    e.preventDefault();
    pos3 = 0;
    pos4 = 0;
    document.onmouseup = closeDragElement;
    document.onmousemove = elementResize;
  }

	function elementResize(e) {
		e = e || window.event;
    e.preventDefault();
		var content = document.querySelector(".draggable");
		var width = content.offsetWidth;
		var height = content.offsetHeight;

		pos1 = (e.clientX - width) - content.offsetLeft;
    pos2 = (e.clientY - height) - content.offsetTop;

		content.style.width = width + pos1 + 'px';
		content.style.height = height + pos2 + 'px';
	}

  function elementDrag(e) {
    e = e || window.event;
    e.preventDefault();
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
    elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
  }

  function closeDragElement() {
    document.onmouseup = null;
    document.onmousemove = null;
  }
}

function open_fullscreen(link, block) {
  var link_, elem;
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', link, true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    block.parentElement.style.display = "block";
    block.innerHTML = elem
  }};
  link_.send();
}
function if_list(block){
  // проверяем, если ли на странице блок с подгрузкой списка. Если есть, грузим список/С пагинацией сразу
  if(block.querySelector('#lenta_load')){
    lenta_load = block.querySelector('#lenta_load');
		link = lenta_load.getAttribute("data-link");
    list_load(lenta_load, link);
		scrolled(link, '#lenta_load', target=0)
  }else if(block.querySelector('#lenta_community')){
    lenta_community = block.querySelector('#lenta_community');link = lenta_community.getAttribute("data-link");
    list_load(block.querySelector("#lenta_community"), link);
		scrolled(link, '#lenta_community', target=0)
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

function list_load(block,link) {
  var request = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  request.open( 'GET', link, true );
  request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  request.onreadystatechange = function () {if ( request.readyState == 4 && request.status == 200 ) {block.innerHTML = request.responseText;}};request.send( null );
}
function ajax_get_reload(url) {
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
        document.title = elem_.querySelector('title').innerHTML;
        window.history.pushState({route: url}, "network", url);
        if_list(rtr);
      }
    }
    ajax_link.send();
}


on('body', 'click', '.ajax', function(event) {
  event.preventDefault();
  var url = this.getAttribute('href');
  if (url != window.location.pathname){
    ajax_get_reload(url);
  }
})

if_list(document.getElementById('ajax'));

page = 2;
loaded = false;
function paginate(link, block_id){
	block = document.body.querySelector(block_id);
	if(block.getElementsByClassName('pag').length === (page-1)*15){
		if (loaded){return};
		var link_3 = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
		link_3.open( 'GET', link + '/?page=' + page++, true );
		link_3.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

		link_3.onreadystatechange = function () {
		if ( this.readyState == 4 && this.status == 200 ) {
			var elem = document.createElement('span');
			elem.innerHTML = link_3.responseText;
			if(elem.getElementsByClassName('pag').length < 15){loaded = true};
			if (elem.querySelector(block_id)){
				xxx = document.createElement("span");
				xxx.innerHTML = elem.querySelector(block_id).innerHTML;
				block.append(xxx);
			} else {block.append(elem)}
			}
		}
		link_3.send();
	}
}
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
	}
}

function create_pagination(block){
	// подключаем подгрузкку списков всех страниц с содержимым. Прозванивать придется все страницы со списками.

	if(block.querySelector('.profile_block_paginate')){
		if(block.querySelector('#user_tracks_container')){scrolled(block.querySelector('#user_tracks_container').getAttribute("data-link"), '#user_tracks_container', target=0)}
		else if(block.querySelector('#user_tracks_list_container')){scrolled(block.querySelector('#user_tracks_list_container').getAttribute("data-link"), '#user_tracks_list_container', target=0)}
		else if(block.querySelector('#user_video_container')){scrolled(block.querySelector('#user_video_container').getAttribute("data-link"), '#user_video_container', target=0)}
		else if(block.querySelector('#friends_container')){scrolled(block.querySelector('#friends_container').getAttribute("data-link"), '#friends_container', target=0)}
		else if(block.querySelector('#follows_container')){scrolled(block.querySelector('#follows_container').getAttribute("data-link"), '#follows_container', target=0)}
		else if(block.querySelector('#followings_container')){scrolled(block.querySelector('#followings_container').getAttribute("data-link"), '#followings_container', target=0)}
		else if(block.querySelector('#online_friends_container')){scrolled(block.querySelector('#online_friends_container').getAttribute("data-link"), '#online_friends_container', target=0)}
		else if(block.querySelector('#possible_friends_container')){scrolled(block.querySelector('#possible_friends_container').getAttribute("data-link"), '#possible_friends_container', target=0)}
		else if(block.querySelector('#common_friends_container')){scrolled(block.querySelector('#common_friends_container').getAttribute("data-link"), '#common_friends_container', target=0)}
		else if(block.querySelector('#user_goods_container')){scrolled(block.querySelector('#user_goods_container').getAttribute("data-link"), '#user_goods_container', target=0)}
		else if(block.querySelector('#communities_container')){scrolled(block.querySelector('#communities_container').getAttribute("data-link"), '#communities_container', target=0)}
		else if(block.querySelector('#staff_communities_container')){scrolled(block.querySelector('#staff_communities_container').getAttribute("data-link"), '#staff_communities_container', target=0)}
		else if(block.querySelector('#user_blacklist_container')){scrolled(block.querySelector('#user_blacklist_container').getAttribute("data-link"), '#user_blacklist_container', target=0)}
	}
	else if(block.querySelector('.community_block_paginate')){
		if(block.querySelector('#community_members_container')){scrolled(block.querySelector('#community_members_container').getAttribute("data-link"), '#community_members_container', target=0)}
		else if(block.querySelector('#community_friends_container')){scrolled(block.querySelector('#community_friends_container').getAttribute("data-link"), '#community_friends_container', target=0)}
		else if(block.querySelector('#community_goods_container')){scrolled(block.querySelector('#community_goods_container').getAttribute("data-link"), '#community_goods_container', target=0)}
		else if(block.querySelector('#community_draft_post_container')){scrolled(block.querySelector('#community_draft_post_container').getAttribute("data-link"), '#community_draft_post_container', target=0)}
		else if(block.querySelector('#community_user_draft_post_container')){scrolled(block.querySelector('#community_user_draft_post_container').getAttribute("data-link"), '#community_user_draft_post_container', target=0)}
	}
	else if(block.querySelector('.music_block_paginate')){
		if(block.querySelector('#genre_container')){scrolled(block.querySelector('#genre_container').getAttribute("data-link"), '#genre_container', target=0)}
		else if(block.querySelector('#music_tags_container')){scrolled(block.querySelector('#music_tags_container').getAttribute("data-link"), '#music_tags_container', target=0)}
		else if(block.querySelector('#tag_container')){scrolled(block.querySelector('#tag_container').getAttribute("data-link"), '#tag_container', target=0)}
	}
	else if(block.querySelector('.list_block_paginate')){
		if(block.querySelector('#all_communities_container')){scrolled(block.querySelector('#all_communities_container').getAttribute("data-link"), '#all_communities_container', target=0)}
		else if(block.querySelector('#all_users_container')){scrolled(block.querySelector('#all_users_container').getAttribute("data-link"), '#all_users_container'), target=0}
		else if(block.querySelector('#quan_container')){scrolled(block.querySelector('#quan_container').getAttribute("data-link"), '#quan_container'), target=0}
		else if(block.querySelector('#cat_communities_container')){scrolled(block.querySelector('#cat_communities_container').getAttribute("data-link"), '#cat_communities_container', target=0)}
		else if(block.querySelector('#articles_load_container')){scrolled(block.querySelector('#articles_load_container').getAttribute("data-link"), '#articles_load_container', target=0)}
		else if(block.querySelector('#music_load_container')){scrolled(block.querySelector('#music_load_container').getAttribute("data-link"), '#music_load_container', target=0)}
		else if(block.querySelector('#img_load_container')){scrolled(block.querySelector('#img_load_container').getAttribute("data-link"), '#img_load_container', target=0)}
		else if(block.querySelector('#video_load_container')){scrolled(block.querySelector('#video_load_container').getAttribute("data-link"), '#video_load_container', target=0)}
		else if(block.querySelector('#goods_load_container')){scrolled(block.querySelector('#goods_load_container').getAttribute("data-link"), '#goods_load_container', target=0)}
	}
}

on('body', 'click', '.next_item', function(event) {
  event.preventDefault();
  var url = this.getAttribute('href');
  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', url, true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        elem_ = document.createElement('span');
        elem_.innerHTML = ajax_link.responseText;
        rtr = document.getElementById('item_loader');
        rtr.innerHTML = elem_.innerHTML;
      }
    }
    ajax_link.send();
})
on('body', 'click', '.prev_item', function(event) {
  event.preventDefault();
  var url = this.getAttribute('href');
  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', url, true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        elem_ = document.createElement('span');
        elem_.innerHTML = ajax_link.responseText;
        rtr = document.getElementById('item_loader');
        rtr.innerHTML = elem_.innerHTML;
      }
    }
    ajax_link.send();
})

on('body', 'click', '.next_photo', function(event) {
  event.preventDefault();
  var url = this.getAttribute('href');
  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', url, true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        elem_ = document.createElement('span');
        elem_.innerHTML = ajax_link.responseText;
        rtr = document.getElementById('photo_loader');
        rtr.innerHTML = elem_.innerHTML;
      }
    }
    ajax_link.send();
})
on('body', 'click', '.prev_photo', function(event) {
  event.preventDefault();
  var url = this.getAttribute('href');
  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', url, true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        elem_ = document.createElement('span');
        elem_.innerHTML = ajax_link.responseText;
        rtr = document.getElementById('photo_loader');
        rtr.innerHTML = elem_.innerHTML;
      }
    }
    ajax_link.send();
})

on('#ajax', 'click', '.article_fullscreen_hide', function() {document.querySelector(".article_fullscreen").style.display = "none";document.getElementById("article_loader").innerHTML=""});
on('#ajax', 'click', '.photo_fullscreen_hide', function() {document.querySelector(".photo_fullscreen").style.display = "none";document.getElementById("photo_loader").innerHTML=""});
on('#ajax', 'click', '.votes_fullscreen_hide', function() {document.querySelector(".votes_fullscreen").style.display = "none";document.getElementById("votes_loader").innerHTML=""});
on('#ajax', 'click', '.item_fullscreen_hide', function() {document.querySelector(".item_fullscreen").style.display = "none";document.getElementById("item_loader").innerHTML=""});
on('#ajax', 'click', '.community_fullscreen_hide', function() {document.querySelector(".community_fullscreen").style.display = "none";document.getElementById("community_loader").innerHTML=""});
on('#ajax', 'click', '.good_fullscreen_hide', function() {document.querySelector(".good_fullscreen").style.display = "none";document.getElementById("good_loader").innerHTML=""});
on('#ajax', 'click', '.stat_fullscreen_hide', function() {document.querySelector(".stat_fullscreen").style.display = "none";document.getElementById("stat_loader").innerHTML=""});
on('body', 'click', '.video_fullscreen_hide', function() {document.querySelector(".video_fullscreen").style.display = "none";document.getElementById("video_loader").innerHTML=""});
on('body', 'click', '.small_video_fullscreen_hide', function() {
  document.querySelector(".video_fullscreen").style.display = "none";
  video_window = document.querySelector(".video_fullscreen");
  video_window.classList.remove("video_fullscreen_resized", "draggable");
  document.body.querySelector(".video_btn_small").style.display = "none";
  document.body.querySelector(".video_btn_big").style.display = "block";
  document.getElementById("video_loader").innerHTML=""
});
on('body', 'click', '.create_fullscreen_hide', function() {document.querySelector(".create_fullscreen").style.display = "none";document.getElementById("create_loader").innerHTML=""});

on('#ajax', 'click', '.show_replies', function() {
  this.nextElementSibling.classList.toggle('replies_open');
});

loadScripts('/static/scripts/lib/lazysizes.min.js')
loadScripts('/static/scripts/posts/community_get.js')
loadScripts('/static/scripts/posts/user_get.js')
loadScripts('/static/scripts/gallery/community_get.js')
loadScripts('/static/scripts/gallery/user_get.js')
loadScripts('/static/scripts/goods/community_get.js')
loadScripts('/static/scripts/goods/user_get.js')
loadScripts('/static/scripts/video/community_get.js')
loadScripts('/static/scripts/video/user_get.js')
