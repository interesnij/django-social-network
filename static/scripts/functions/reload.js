
function get_post_view(){
	if(document.querySelector(".post_stream")){
		container = document.querySelector(".post_stream");
		link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    list = container.querySelectorAll('.pag');
    for (var i = 0; i < list.length; i++) {
      if(!list[i].classList.contains("showed")){
        inViewport = elementInViewport(list[i]);
        if(inViewport){
          uuid = list[i].getAttribute('data-uuid');
					if (list[i].querySelector(".reklama")){
						link.open( 'GET', '/posts/user_progs/post_market_view/' + uuid + "/", true );
					} else if(!list[i].querySelector(".reklama")){
						link.open( 'GET', '/posts/user_progs/post_view/' + uuid + "/", true );
				}
				link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

				link.send();
				list[i].classList.add("showed");
				console.log(i + " получил класс showed");
    }}}}}

function scrolled(block, link, block_2, target){
	// скрипты для работы с прокруткой:
	// 1. блок, к которому применяется скролл
	// 2.
	onscroll = function(){
		box = block.querySelector('.last');
		if(box && box.classList.contains("last")){
				inViewport = elementInViewport(box);
				if(inViewport){
					box.classList.remove("last");
					paginate(block, link, block_2);
		}};
		if (target == 1){get_post_view()}
	}
}
page = 2;
loaded = false;
function paginate(block, link, block_2){
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
			if (elem.querySelector(block)){ //
				xxx = document.createElement("span");
				xxx.innerHTML = elem.querySelector(block).innerHTML; //
				block.append(xxx);
			} else {block.append(elem)}
			}
		}
		link_3.send();
	}
}

function create_pagination(block){
	// подключаем подгрузкку списков всех страниц с содержимым. Прозванивать придется все страницы со списками.

	if(block.querySelector('.profile_block_paginate')){
		if(block.querySelector('#user_tracks_container')){user_tracks = block.querySelector('#user_tracks_container'); scrolled(user_tracks, user_tracks.getAttribute("data-link"), '#user_tracks_container', target=0)}
		else if(block.querySelector('#user_tracks_list_container')){user_tracks = block.querySelector('#user_tracks_list_container'); scrolled(user_tracks, user_tracks.getAttribute("data-link"), '#user_tracks_list_container', target=0)}
		else if(block.querySelector('#user_video_container')){user_video = block.querySelector('#user_video_container'); scrolled(user_video, user_video.getAttribute("data-link"), '#user_video_container', target=0)}
		else if(block.querySelector('#friends_container')){friends = block.querySelector('#friends_container'); scrolled(friends, friends.getAttribute("data-link"), '#friends_container', target=0)}
		else if(block.querySelector('#follows_container')){follows = block.querySelector('#follows_container'); scrolled(follows, follows.getAttribute("data-link"), '#follows_container', target=0)}
		else if(block.querySelector('#followings_container')){followings = block.querySelector('#followings_container'); scrolled(followings, followings.getAttribute("data-link"), '#followings_container', target=0)}
		else if(block.querySelector('#online_friends_container')){online_friends = block.querySelector('#online_friends_container'); scrolled(online_friends, online_friends.getAttribute("data-link"), '#online_friends_container', target=0)}
		else if(block.querySelector('#possible_friends_container')){possible_friends = block.querySelector('#possible_friends_container'); scrolled(possible_friends, possible_friends.getAttribute("data-link"), '#possible_friends_container', target=0)}
		else if(block.querySelector('#common_friends_container')){common_friends = block.querySelector('#common_friends_container'); scrolled(common_friends, common_friends.getAttribute("data-link"), '#common_friends_container', target=0)}
		else if(block.querySelector('#user_goods_container')){user_goods = block.querySelector('#user_goods_container'); scrolled(user_goods, user_goods.getAttribute("data-link"), '#user_goods_container', target=0)}
		else if(block.querySelector('#communities_container')){communities = block.querySelector('#communities_container'); scrolled(communities, communities.getAttribute("data-link"), '#communities_container', target=0)}
		else if(block.querySelector('#staff_communities_container')){staff_communities = block.querySelector('#staff_communities_container'); scrolled(staff_communities, staff_communities.getAttribute("data-link"), '#staff_communities_container', target=0)}
		else if(block.querySelector('#user_blacklist_container')){user_blacklist = block.querySelector('#user_blacklist_container'); scrolled(user_blacklist, user_blacklist.getAttribute("data-link"), '#user_blacklist_container', target=0)}
	}
	else if(block.querySelector('.news_block_paginate')){
		if(block.querySelector('#news_post_list')){post_list = block.querySelector('#news_post_list'); scrolled(post_list, post_list.getAttribute("data-link"), '#news_post_list', target=1)}
		else if(block.querySelector('#news_photo_list')){photo_list = block.querySelector('#news_photo_list'); scrolled(photo_list, photo_list.getAttribute("data-link"), '#news_photo_list', target=0)}
		else if(block.querySelector('#news_video_list')){video_list = block.querySelector('#news_video_list'); scrolled(video_list, video_list.getAttribute("data-link"), '#news_video_list', target=0)}
		else if(block.querySelector('#news_good_list')){good_list = block.querySelector('#news_good_list'); scrolled(good_list, good_list.getAttribute("data-link"), '#news_good_list', target=0)}
		else if(block.querySelector('#news_audio_list')){audio_list = block.querySelector('#news_audio_list'); scrolled(audio_list, audio_list.getAttribute("data-link"), '#news_audio_list', target=0)}
		else if(block.querySelector('#news_featured_post_list')){post_list = block.querySelector('#news_featured_post_list'); scrolled(post_list, post_list.getAttribute("data-link"), '#news_featured_post_list', target=1)}
		else if(block.querySelector('#news_featured_photo_list')){photo_list = block.querySelector('#news_featured_photo_list'); scrolled(photo_list, photo_list.getAttribute("data-link"), '#news_featured_photo_list', target=0)}
		else if(block.querySelector('#news_featured_video_list')){video_list = block.querySelector('#news_featured_video_list'); scrolled(video_list, video_list.getAttribute("data-link"), '#news_featured_video_list', target=0)}
		else if(block.querySelector('#news_featured_good_list')){good_list = block.querySelector('#news_featured_good_list'); scrolled(good_list, good_list.getAttribute("data-link"), '#news_featured_good_list', target=0)}
		else if(block.querySelector('#news_featured_audio_list')){audio_list = block.querySelector('#news_featured_audio_list'); scrolled(audio_list, audio_list.getAttribute("data-link"), '#news_featured_audio_list', target=0)}
	}
	else if(block.querySelector('.community_block_paginate')){
		if(block.querySelector('#community_members_container')){community_members = block.querySelector('#community_members_container'); scrolled(community_members, community_members.getAttribute("data-link"), '#community_members_container', target=0)}
		else if(block.querySelector('#community_friends_container')){frends_community = block.querySelector('#community_friends_container'); scrolled(community_communities, community_communities.getAttribute("data-link"), '#community_friends_container', target=0)}
		else if(block.querySelector('#community_goods_container')){community_goods = block.querySelector('#community_goods_container'); scrolled(community_goods, community_goods.getAttribute("data-link"), '#community_goods_container', target=0)}
		else if(block.querySelector('#community_draft_post_container')){draft_post = block.querySelector('#community_draft_post_container'); scrolled(draft_post, draft_post.getAttribute("data-link"), '#community_draft_post_container', target=0)}
		else if(block.querySelector('#community_user_draft_post_container')){draft_post = block.querySelector('#community_user_draft_post_container'); scrolled(draft_post, draft_post.getAttribute("data-link"), '#community_user_draft_post_container', target=0)}
	}
	else if(block.querySelector('.staff_community_block_paginate')){
		if(block.querySelector('#community_admins_container')){admins_container = block.querySelector('#com_admins_container'); scrolled(admins_container, admins_container.getAttribute("data-link"), '#community_admins_container', target=0)}
		else if(block.querySelector('#community_advertisers_container')){com_advertisers = block.querySelector('#community_advertisers_container'); scrolled(com_advertisers, com_advertisers.getAttribute("data-link"), '#community_advertisers_container', target=0)}
		else if(block.querySelector('#community_blacklist_container')){com_blacklist = block.querySelector('#community_blacklist_container'); scrolled(com_blacklist, com_blacklist.getAttribute("data-link"), '#community_blacklist_container', target=0)}
		else if(block.querySelector('#community_editors_container')){com_editors = block.querySelector('#community_editors_container'); scrolled(com_editors, com_editors.getAttribute("data-link"), '#community_editors_container', target=0)}
		else if(block.querySelector('#community_follows_container')){com_follows = block.querySelector('#community_follows_container'); scrolled(com_follows, com_follows.getAttribute("data-link"), '#community_follows_container', target=0)}
		else if(block.querySelector('#community_staff_members_container')){com_members = block.querySelector('#community_staff_members_container'); scrolled(com_members, com_members.getAttribute("data-link"), '#community_staff_members_container', target=0)}
		else if(block.querySelector('#community_moders_container')){com_moders = block.querySelector('#community_moders_container'); scrolled(com_moders, com_moders.getAttribute("data-link"), '#community_moders_container', target=0)}
	}
	else if(block.querySelector('.music_block_paginate')){
		if(block.querySelector('#genre_container')){music_genre = block.querySelector('#genre_container'); scrolled(music_genre, music_genre.getAttribute("data-link"), '#genre_container', target=0)}
		else if(block.querySelector('#music_tags_container')){music_tags = block.querySelector('#music_tags_container'); scrolled(music_tags, music_tags.getAttribute("data-link"), '#music_tags_container', target=0)}
		else if(block.querySelector('#tag_container')){music_tag = block.querySelector('#tag_container');scrolled(music_tag, music_tag.getAttribute("data-link"), '#tag_container', target=0)}
	}
	else if(block.querySelector('.list_block_paginate')){
		if(block.querySelector('#all_communities_container')){all_communities = block.querySelector('#all_communities_container'); scrolled(all_communities, all_communities.getAttribute("data-link"), '#all_communities_container', target=0)}
		else if(block.querySelector('#all_users_container')){all_users = block.querySelector('#all_users_container'); scrolled(all_users, all_users.getAttribute("data-link"), '#all_users_container'), target=0}
		else if(block.querySelector('#quan_container')){quan = block.querySelector('#quan_container'); scrolled(quan, quan.getAttribute("data-link"), '#quan_container'), target=0}
		else if(block.querySelector('#cat_communities_container')){cat_communities = block.querySelector('#cat_communities_container'); scrolled(cat_communities, cat_communities.getAttribute("data-link"), '#cat_communities_container', target=0)}
		else if(block.querySelector('#articles_load_container')){articles_load = block.querySelector('#articles_load_container'); scrolled(articles_load, articles_load.getAttribute("data-link"), '#articles_load_container', target=0)}
		else if(block.querySelector('#music_load_container')){music_load = block.querySelector('#music_load_container'); scrolled(music_load, music_load.getAttribute("data-link"), '#music_load_container', target=0)}
		else if(block.querySelector('#img_load_container')){img_load = block.querySelector('#img_load_container'); scrolled(img_load, img_load.getAttribute("data-link"), '#img_load_container', target=0)}
		else if(block.querySelector('#video_load_container')){video_load = block.querySelector('#video_load_container'); scrolled(video_load, video_load.getAttribute("data-link"), '#video_load_container', target=0)}
		else if(block.querySelector('#goods_load_container')){goods_load = block.querySelector('#goods_load_container'); scrolled(goods_load, goods_load.getAttribute("data-link"), '#goods_load_container', target=0)}
	}
}

function if_list(block){
  // проверяем, если ли на странице блок с подгрузкой списка. Если есть, грузим список/С пагинацией сразу
  if(block.querySelector('#lenta_load')){
    lenta_load = block.querySelector('#lenta_load');
		link = lenta_load.getAttribute("data-link");
    list_load(lenta_load, link);
		scrolled(lenta_load, link, '#lenta_load')
  }else if(block.querySelector('#lenta_community')){
    lenta_community = block.querySelector('#lenta_community');link = lenta_community.getAttribute("data-link");
    list_load(block.querySelector("#lenta_community"), link);
		scrolled(lenta_community, link, '#lenta_community')
  }else if(block.querySelector('#photo_load')){
    photo_load = block.querySelector('#photo_load');link = photo_load.getAttribute("data-link");
    list_load(block.querySelector("#photo_load"), link);
		scrolled(photo_load, link, '#photo_load')
  }else if(block.querySelector('#c_photo_load')){
    photo_load = block.querySelector('#c_photo_load');link = photo_load.getAttribute("data-link");
    list_load(block.querySelector("#c_photo_load"), link);
		scrolled(photo_load, link, '#c_photo_load')
  }else if(block.querySelector('#album_photo_load')){
    album_photo_load = block.querySelector('#album_photo_load');link = album_photo_load.getAttribute("data-link");
    list_load(block.querySelector("#album_photo_load"), link);
		scrolled(album_photo_load, link, '#album_photo_load')
  }else if(block.querySelector('#c_album_photo_load')){
    album_photo_load = block.querySelector('#c_album_photo_load');link = album_photo_load.getAttribute("data-link");
    list_load(block.querySelector("#c_album_photo_load"), link);
		scrolled(album_photo_load, link, '#c_album_photo_load')
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
