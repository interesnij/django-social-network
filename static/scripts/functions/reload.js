
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
		try{
		_block = document.body.querySelector(block_id)

		box = _block.querySelector('.last');
		if(box && box.classList.contains("last")){
				inViewport = elementInViewport(box);
				if(inViewport){
					box.classList.remove("last");
					paginate(link, block_id);
		}};
		if (target == 1){get_post_view()}
	} catch { return }
}}
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
function create_load_pagination(block){
	// подключаем пагинцию списков в подгружаемых окнах.
	if(block.querySelector('.img_load_container')){
		_block = block.querySelector('.img_load_container');
		scrolled(_block.getAttribute("data-link"), '.img_load_container', target=0)
	}
	else if(block.querySelector('.articles_load_container')){_block = block.querySelector('.articles_load_container');scrolled(_block.getAttribute("data-link"), '.articles_load_container', target=0)}
	else if(block.querySelector('.goods_load_container')){_block = block.querySelector('.goods_load_container');scrolled(_block.getAttribute("data-link"), '.goods_load_container', target=0)}
	else if(block.querySelector('.music_load_container')){_block = block.querySelector('.music_load_container');scrolled(_block.getAttribute("data-link"), '.music_load_container', target=0)}
	else if(block.querySelector('.music_list_load_container')){_block = block.querySelector('.music_list_load_container');scrolled(_block.getAttribute("data-link"), '.music_list_load_container', target=0)}

	else if(block.querySelector('.video_load_container')){_block = block.querySelector('.video_load_container');scrolled(_block.getAttribute("data-link"), '.video_load_container', target=0)}
}


function create_pagination(block){
	// подключаем подгрузкку списков всех страниц с содержимым. Прозванивать придется все страницы со списками.
	if(block.querySelector('.profile_block_paginate')){
		if(block.querySelector('#user_tracks_container')){scrolled(window.location.href,'#user_tracks_container',target=0)}
		else if(block.querySelector('#user_tracks_list_container')){scrolled(window.location.href, '#user_tracks_list_container', target=0)}
		else if(block.querySelector('#user_video_container')){scrolled(window.location.href, '#user_video_container', target=0)}
		else if(block.querySelector('#friends_container')){scrolled(window.location.href, '#friends_container', target=0)}
		else if(block.querySelector('#follows_container')){scrolled(window.location.href, '#follows_container', target=0)}
		else if(block.querySelector('#followings_container')){scrolled(window.location.href, '#followings_container', target=0)}
		else if(block.querySelector('#online_friends_container')){scrolled(window.location.href, '#online_friends_container', target=0)}
		else if(block.querySelector('#possible_friends_container')){scrolled(window.location.href, '#possible_friends_container', target=0)}
		else if(block.querySelector('#common_friends_container')){scrolled(window.location.href, '#common_friends_container', target=0)}
		else if(block.querySelector('#user_goods_container')){scrolled(window.location.href, '#user_goods_container', target=0)}
		else if(block.querySelector('#user_list_goods_container')){scrolled(window.location.href, '#user_list_goods_container', target=0)}

		else if(block.querySelector('#communities_container')){scrolled(window.location.href, '#communities_container', target=0)}
		else if(block.querySelector('#staff_communities_container')){scrolled(window.location.href, '#staff_communities_container', target=0)}
		else if(block.querySelector('#user_blacklist_container')){scrolled(window.location.href, '#user_blacklist_container', target=0)}
	}
	else if(block.querySelector('.news_block_paginate')){
		if(block.querySelector('#news_post_list')){scrolled(window.location.href, '#news_post_list', target=1)}
		else if(block.querySelector('#news_photo_list')){scrolled(window.location.href, '#news_photo_list', target=0)}
		else if(block.querySelector('#news_video_list')){scrolled(window.location.href, '#news_video_list', target=0)}
		else if(block.querySelector('#news_good_list')){scrolled(window.location.href, '#news_good_list', target=0)}
		else if(block.querySelector('#news_audio_list')){scrolled(window.location.href, '#news_audio_list', target=0)}
		else if(block.querySelector('#news_featured_post_list')){scrolled(window.location.href, '#news_featured_post_list', target=1)}
		else if(block.querySelector('#news_featured_photo_list')){scrolled(window.location.href, '#news_featured_photo_list', target=0)}
		else if(block.querySelector('#news_featured_video_list')){scrolled(window.location.href, '#news_featured_video_list', target=0)}
		else if(block.querySelector('#news_featured_good_list')){scrolled(window.location.href, '#news_featured_good_list', target=0)}
		else if(block.querySelector('#news_featured_audio_list')){scrolled(window.location.href, '#news_featured_audio_list', target=0)}
	}
	else if(block.querySelector('.community_block_paginate')){
		if(block.querySelector('#community_members_container')){scrolled(window.location.href, '#community_members_container', target=0)}
		else if(block.querySelector('#community_friends_container')){scrolled(window.location.href, '#community_friends_container', target=0)}
		else if(block.querySelector('#community_goods_container')){scrolled(window.location.href, '#community_goods_container', target=0)}
		else if(block.querySelector('#community_list_goods_container')){scrolled(window.location.href, '#community_list_goods_container', target=0)}		else if(block.querySelector('#community_draft_post_container')){scrolled(window.location.href, '#community_draft_post_container', target=0)}
		else if(block.querySelector('#community_draft_post_container')){scrolled(window.location.href, '#community_draft_post_container', target=0)}
		else if(block.querySelector('#community_user_draft_post_container')){scrolled(window.location.href, '#community_user_draft_post_container', target=0)}
		else if(block.querySelector('#community_tracks_list_container')){scrolled(window.location.href, '#community_tracks_list_container', target=0)}
		else if(block.querySelector('#community_tracks_container')){scrolled(window.location.href, '#community_tracks_container', target=0)}

	}
	else if(block.querySelector('.staff_community_block_paginate')){
		if(block.querySelector('#community_admins_container')){scrolled(window.location.href, '#community_admins_container', target=0)}
		else if(block.querySelector('#community_advertisers_container')){scrolled(window.location.href, '#community_advertisers_container', target=0)}
		else if(block.querySelector('#community_blacklist_container')){scrolled(window.location.href, '#community_blacklist_container', target=0)}
		else if(block.querySelector('#community_editors_container')){scrolled(window.location.href, '#community_editors_container', target=0)}
		else if(block.querySelector('#community_follows_container')){scrolled(window.location.href, '#community_follows_container', target=0)}
		else if(block.querySelector('#community_staff_members_container')){scrolled(window.location.href, '#community_staff_members_container', target=0)}
		else if(block.querySelector('#community_moders_container')){scrolled(window.location.href, '#community_moders_container', target=0)}
	}
	else if(block.querySelector('.music_block_paginate')){
		if(block.querySelector('#genre_container')){scrolled(window.location.href, '#genre_container', target=0)}
		else if(block.querySelector('#music_tags_container')){scrolled(window.location.href, '#music_tags_container', target=0)}
		else if(block.querySelector('#tag_container')){scrolled(window.location.href, '#tag_container', target=0)}
	}
	else if(block.querySelector('.list_block_paginate')){
		if(block.querySelector('#all_communities_container')){scrolled(window.location.href, '#all_communities_container', target=0)}
		else if(block.querySelector('#all_users_container')){scrolled(window.location.href, '#all_users_container'), target=0}
		else if(block.querySelector('#quan_container')){scrolled(window.location.href, '#quan_container'), target=0}
		else if(block.querySelector('#cat_communities_container')){scrolled(window.location.href, '#cat_communities_container', target=0)}
	}
	else if(block.querySelector('.moderation_block_paginate')){
		if(block.querySelector('#moderation_community_container')){scrolled(window.location.href, '#moderation_community_container', target=0)}
		else if(block.querySelector('#moderation_post_comment_container')){scrolled(window.location.href, '#moderation_post_comment_container'), target=0}
		else if(block.querySelector('#moderation_post_container')){scrolled(window.location.href, '#moderation_post_container'), target=0}
		else if(block.querySelector('#moderation_users_container')){scrolled(window.location.href, '#moderation_users_container', target=0)}
		else if(block.querySelector('#penalty_community_container')){scrolled(window.location.href, '#penalty_community_container', target=0)}
		else if(block.querySelector('#penalty_post_comment_container')){scrolled(window.location.href, '#penalty_post_comment_container', target=0)}
		else if(block.querySelector('#penalty_post_container')){scrolled(window.location.href, '#penalty_post_container', target=0)}
		else if(block.querySelector('#penalty_users_container')){scrolled(window.location.href, '#penalty_users_container', target=0)}
	}
}
function gotoBottom(block){
   var element = block;
   element.scrollTop = element.scrollHeight - element.clientHeight;
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
  }else if(block.querySelector('.chatlist')){
    block.scrollTo({ top: 1000, behavior: 'smooth' });
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
