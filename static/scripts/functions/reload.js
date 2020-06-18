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

function scrolled(block, link, block_2){
	// скрипты для работы с прокруткой: пагинация, просмотры и т.д.
	onscroll = function(){
		var box = block.querySelector('.last');
		if(box && box.classList.contains("last")){
				inViewport = elementInViewport(box);
				if(inViewport){
					box.classList.remove("last");
					console.log(i + " удалил класс last");
					paginate(block, link, block_2)
		}};
	}
}
page = 2;
loaded = false;
function paginate(block, link, block_2){
	if(block.getElementsByClassName('pag').length === (page-1)*15){
		if (loaded){return};
		var link_3 = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
		link_3.open( 'GET', link + '/?page=' + page++, true );

		link_3.onreadystatechange = function () {
		if ( this.readyState == 4 && this.status == 200 ) {
			var elem = document.createElement('span');
			elem.innerHTML = link_3.responseText;
			if(elem.getElementsByClassName('pag').length < 15){loaded = true; return};
			if (elem.querySelector(block_2)){
				xxx = document.createElement("span");
				xxx.innerHTML = elem.querySelector(block_2).innerHTML;
				block.append(xxx);
				console.log(xxx);
			} else {block.append(elem)}
			}
		}
		link_3.send();
	}
}

function create_pagination(block){
	// подключаем подгрузкку списков всех страниц с содержимым. Прозванивать придется все страницы со списками.
if(block.querySelector('#tag_container')){
	music_tag = block.querySelector('#tag_container');
	scrolled(music_tag, music_tag.getAttribute("data-link"), '#tag_container')
	console.log(music_tag);
	console.log(music_tag.getAttribute("data-link"));
 }
else if(block.querySelector('#lenta_load')){lenta_load = block.querySelector('#lenta_load'); scrolled(lenta_load, lenta_load.getAttribute("data-link"), '#lenta_load')}
else if(block.querySelector('#genre_container')){music_genre = block.querySelector('#genre_container'); scrolled(music_genre, music_genre.getAttribute("data-link"), '#genre_container')}
else if(block.querySelector('#all_communities_container')){all_communities = block.querySelector('#all_communities_container'); scrolled(all_communities, all_communities.getAttribute("data-link"), '#all_communities_container')}
else if(block.querySelector('#cat_communities_container')){all_communities = block.querySelector('#cat_communities_container'); scrolled(cat_communities, cat_communities.getAttribute("data-link"), '#cat_communities_container')}
else if(block.querySelector('#cat_friends_container')){frends_communities = block.querySelector('#cat_friends_container'); scrolled(frends_communities, frends_communities.getAttribute("data-link"), '#cat_friends_container')}
else if(block.querySelector('#communities_members_container')){communities_members = block.querySelector('#communities_members_container'); scrolled(communities_members, communities_members.getAttribute("data-link"), '#communities_members_container')}
else if(block.querySelector('#com_admins_container')){admins_container = block.querySelector('#com_admins_container'); scrolled(admins_container, admins_container.getAttribute("data-link"), '#com_admins_container')}
else if(block.querySelector('#com_advertisers_container')){com_advertisers = block.querySelector('#com_advertisers_container'); scrolled(com_advertisers, com_advertisers.getAttribute("data-link"), '#com_advertisers_container')}
else if(block.querySelector('#com_blacklist_container')){com_blacklist = block.querySelector('#com_blacklist_container'); scrolled(com_blacklist, com_blacklist.getAttribute("data-link"), '#com_blacklist_container')}
else if(block.querySelector('#com_editors_container')){com_editors = block.querySelector('#com_editors_container'); scrolled(com_editors, com_editors.getAttribute("data-link"), '#com_editors_container')}
else if(block.querySelector('#com_follows_container')){com_follows = block.querySelector('#com_follows_container'); scrolled(com_follows, com_follows.getAttribute("data-link"), '#com_follows_container')}
else if(block.querySelector('#com_members_container')){com_members = block.querySelector('#com_members_container'); scrolled(com_members, com_members.getAttribute("data-link"), '#com_members_container')}
else if(block.querySelector('#com_moders_container')){com_moders = block.querySelector('#com_moders_container'); scrolled(com_moders, com_moders.getAttribute("data-link"), '#com_moders_container')}
else if(block.querySelector('#follows_container')){follows = block.querySelector('#follows_container'); scrolled(follows, follows.getAttribute("data-link"), '#follows_container')}
else if(block.querySelector('#followings_container')){followings = block.querySelector('#followings_container'); scrolled(followings, followings.getAttribute("data-link"), '#followings_container')}
else if(block.querySelector('#friends_container')){friends = block.querySelector('#friends_container'); scrolled(friends, friends.getAttribute("data-link"), '#friends_container')}
else if(block.querySelector('#common_friends_container')){common_friends = block.querySelector('#common_friends_container'); scrolled(common_friends, common_friends.getAttribute("data-link"), '#common_friends_container')}
else if(block.querySelector('#online_friends_container')){online_friends = block.querySelector('#online_friends_container'); scrolled(online_friends, online_friends.getAttribute("data-link"), '#online_friends_container')}
else if(block.querySelector('#user_goods_container')){user_goods = block.querySelector('#user_goods_container'); scrolled(user_goods, user_goods.getAttribute("data-link"), '#user_goods_container')}
else if(block.querySelector('#music_tags_container')){music_tags = block.querySelector('#music_tags_container'); scrolled(music_tags, music_tags.getAttribute("data-link"), '#music_tags_container')}
else if(block.querySelector('#articles_load_container')){articles_load = block.querySelector('#articles_load_container'); scrolled(articles_load, articles_load.getAttribute("data-link"), '#articles_load_container')}
else if(block.querySelector('#goods_load_container')){goods_load = block.querySelector('#goods_load_container'); scrolled(goods_load, goods_load.getAttribute("data-link"), '#goods_load_container')}
else if(block.querySelector('#music_load_container')){music_load = block.querySelector('#music_load_container'); scrolled(music_load, music_load.getAttribute("data-link"), '#music_load_container')}
else if(block.querySelector('#img_load_container')){img_load = block.querySelector('#img_load_container'); scrolled(img_load, img_load.getAttribute("data-link"), '#img_load_container')}
else if(block.querySelector('#video_load_container')){video_load = block.querySelector('#video_load_container'); scrolled(video_load, video_load.getAttribute("data-link"), '#video_load_container')}
else if(block.querySelector('#communities_container')){communities = block.querySelector('#communities_container'); scrolled(communities, communities.getAttribute("data-link"), '#communities_container')}
else if(block.querySelector('#staff_communities_container')){staff_communities = block.querySelector('#staff_communities_container'); scrolled(staff_communities, staff_communities.getAttribute("data-link"), '#staff_communities_container')}
else if(block.querySelector('#user_tracks_container')){user_tracks = block.querySelector('#user_tracks_container'); scrolled(user_tracks, user_tracks.getAttribute("data-link"), '#user_tracks_container')}
else if(block.querySelector('#user_video_container')){user_video = block.querySelector('#user_video_container'); scrolled(user_video, user_video.getAttribute("data-link"), '#user_video_container')}
else if(block.querySelector('#all_users_container')){all_users = block.querySelector('#all_users_container'); scrolled(all_users, all_users.getAttribute("data-link"), '#all_users_container')}
else if(block.querySelector('#possible_friends_container')){possible_friends = block.querySelector('#possible_friends_container'); scrolled(possible_friends, possible_friends.getAttribute("data-link"), '#possible_friends_container')}
else if(block.querySelector('#quan_container')){quan = block.querySelector('#quan_container'); scrolled(quan, quan.getAttribute("data-link"), '#quan_container')}

}

function if_list(block){
  // проверяем, если ли на странице блок с подгрузкой списка. Если есть, грузим список/С пагинацией сразу
  if(block.querySelector('#news_load')){
    news_load = block.querySelector('#news_load');link = news_load.getAttribute("data-link");
    list_load(block.querySelector("#news_load"), link);
  }else if(block.querySelector('#lenta_load')){
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
  }else if(block.querySelector('#album_photo_load')){
    album_photo_load = block.querySelector('#album_photo_load');link = album_photo_load.getAttribute("data-link");
    list_load(block.querySelector("#album_photo_load"), link);
		scrolled(album_photo_load, link, '#album_photo_load')
  };
}
if_list(document.getElementById('ajax'));
create_pagination(document.getElementById('ajax'));

function list_load(block,link) {
  // подгрузка списка
  var request = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );request.open( 'GET', link, true );request.onreadystatechange = function () {if ( request.readyState == 4 && request.status == 200 ) {block.innerHTML = request.responseText;}};request.send( null );
}

function ajax_get_reload(url) {
	// перезагрузка основного блока на страницу с указанным url
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
        load_chart();
				page = 2;
				loaded = false;
				create_pagination(rtr);
      }
    }
    ajax_link.send();
}
