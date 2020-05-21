function msToTime(duration) {
  var milliseconds = parseInt((duration % 1000) / 100),
    seconds = Math.floor((duration / 1000) % 60),
    minutes = Math.floor((duration / (1000 * 60)) % 60);

  minutes = (minutes < 10) ? "0" + minutes : minutes;
  seconds = (seconds < 10) ? "0" + seconds : seconds;

  return minutes + ":" + seconds;
}


music_player = new FWDMSP({
		//main settings
		instanceName:"player1",
		playlistsId:"audio_playlists",
		mainFolderPath:"/static/images/",
		skinPath:"audio_white",
		showSoundCloudUserNameInTitle:"no",   // показывать имя пользователя soundcloud
		showMainBackground:"yes",  						// показать общий фон
		verticalPosition:"bottom",                    // расположение плеера
		rightClickContextMenu:"developer",
		useDeepLinking:"no",									// использовать глубокие ссылки - защита от перехвата. Не будет работать с souncloud
		rightClickContextMenu:"no",           // показ контекстног меню по щелчку правой кнопкой мыши
		addKeyboardSupport:"no",             // добавить поддержку клавиатуры
		animate:"yes",												// фнимация
		autoPlay:"no",												// автостарт плеера
		loop:"no",														// повтор песни
		shuffle:"no",													// перемешивание треков
		maxWidth:850,                         // максимальная ширина
		volume:.8,														// громкость по умолчанию 80%

		// controller settings
		showControllerByDefault:"yes",        // показать контроллер по умолчанию
		showThumbnail:"yes",                  // показывать миниатюры
		showNextAndPrevButtons:"yes",					// показывать кнопки переключения треков
		showSoundAnimation:"yes",							// показывать анимацию музыкального воспроизведения
		showLoopButton:"yes",                 // показывать кнопку повтора треков
		showShuffleButton:"yes",              // показывать кнопку перемешивания треков
		expandBackground:"no",
		showBuyButton:"yes",
    showPlaylistItemBuyButton:"no",
		titleColor:"#000000",                 // цвет названия
		timeColor:"#919191",                  // цвет времени

		// настройки выравнивания и размера контроллера (подробно описаны в документации!)
		controllerHeight:76,                 // высота контроллера
		startSpaceBetweenButtons:9,          // начальное пространство между кнопками
		spaceBetweenButtons:8,               // пространство между кнопками
		separatorOffsetOutSpace:5,           // смещение разделителя вне пространства
		separatorOffsetInSpace:9,            // смещение разделителя в пространстве
		lastButtonsOffsetTop:14,             // смещение последних кнопок сверху
		allButtonsOffsetTopAndBottom:14,     // смещение всех кнопок вверх и вниз
		titleBarOffsetTop:13,                // смещение сверху секции названия
		mainScrubberOffsetTop:47,            // смещение сверху скруббера
		spaceBetweenMainScrubberAndTime:10,  // пространство между скруббером и секцией времени
		startTimeSpace:10,                   // пространство относительно начала в секуии времени
		scrubbersOffsetWidth:2,              // ширина смещения скруббера
		scrubbersOffestTotalWidth:0,         // общая ширина смещения скруббера
		volumeButtonAndScrubberOffsetTop:47, // всещение сверху скруббера и кнопки громкости
		spaceBetweenVolumeButtonAndScrubber:6,// пространство между скруббером и кнопкой громмкости
		volumeScrubberOffestWidth:4,         // смещение слева скруббера громкости
		scrubberOffsetBottom:10,             // сммещение скруббера снизу
		equlizerOffsetLeft:1,                // смещение эквалайзера влево

		//playlists window settings
		showPlaylistsSearchInput:"no",      // показывать поле поиска в плейлисте
		usePlaylistsSelectBox:"no",         // показывать поле плейлистов сверху выбранного плейлиста
		showPlaylistsSelectBoxNumbers:"no", // пронумеровать плейлисты в поле выбора плейлиста
		showPlaylistsButtonAndPlaylists:"yes", // показывать кнопку, вызывающую окно плейлистов сверху и сами плейлисты
		showPlaylistsByDefault:"no",         // показывать плейлист по умолчанию
		thumbnailSelectedType:"opacity",     // тип выбора миниатюры (к примеру прозрачность)
		startAtPlaylist:0,                   // воспроизводить с плейлиста номер...
		startAtTrack:0,                      // воспроизводить с трека номер...
		startAtRandomTrack:"no",             // воспроизводить со случайного трека...
		buttonsMargins:0,                    // отступы кнопок
		thumbnailMaxWidth:330,               // макс. ширина миниатюр
		thumbnailMaxHeight:330,              // макс. высота миниатюр
		horizontalSpaceBetweenThumbnails:40, // пространство между миниатюрами по горизонтали
		verticalSpaceBetweenThumbnails:40,   // пространство между миниатюрами по вертикали
		mainSelectorBackgroundSelectedColor:"#FFFFFF", // цвет фона выбранного
		mainSelectorTextNormalColor:"#737373",  // цвет текста селектора
		mainSelectorTextSelectedColor:"#000000", // цвет текста селектора выбранного
		mainButtonTextNormalColor:"#7C7C7C", // цвет текста кнопок
		mainButtonTextSelectedColor:"#FFFFFF", // цвет текста кнопок выбранных

		//playlist settings
		playTrackAfterPlaylistLoad:"no",     // воспроизведение трека после загрузки плейлиста
		//showPlayListButtonAndPlaylist:"yes",
		showPlayListOnAndroid:"yes",         // показывать плейлисты на android
		showPlayListByDefault:"no",          // показывть плейлист по умолчанию
		showPlaylistItemPlayButton:"yes",    // показать кнопку воспроизведения элемента плейлиста
		addScrollBarMouseWheelSupport:"yes",  // прокручивать колесиком мыши
		showTracksNumbers:"yes",							// показывать номер трека
		playlistBackgroundColor:"#000000",    // цвет фона плейлиста
		trackTitleNormalColor:"#737373",      // цвет заголовка трека
		trackTitleSelectedColor:"#000000",    // цвет заголовка выбранного трека
		trackDurationColor:"#7C7C7C",         // цвет времени трека
		maxPlaylistItems:30,                  // Макс. количество плейлистов
		nrOfVisiblePlaylistItems:12,          // число видимых элементов списка воспроизведения
		trackTitleOffsetLeft:0,               // смещение слева заголовка трека
		playPauseButtonOffsetLeftAndRight:11, // смещение слева и справа кнопки play
		durationOffsetRight:9,							  // смещение справа продолжительности трека
		scrollbarOffestWidth:7,               // шмрмна смещения полосы прокрутки

		//playback rate / speed
		showPlaybackRateButton:"yes",         // показать кнопку скорости воспроизведения
		defaultPlaybackRate:1, //min - 0.5 / max - 3 // скорость воспроизведения по умолчанию (от 0,5 до 3)
		playbackRateWindowTextColor:"#888888",// цвет текста на окне выбора скорости

		//search bar settings
		showSearchBar:"no",                  // показывать секцию поиска треков
		showSortButtons:"yes",                // показывать секцию сортировки треков
		searchInputColor:"#999999",						// цвет секции поиска
		searchBarHeight:38,									  // высота секции поиска
		inputSearchTextOffsetTop:1,           // смещение текста ввода поиска сверху
		inputSearchOffsetLeft:0,              // смещение текста ввода поиска слева

		//opener settings
		openerAlignment:"right",              // открывание
		showOpener:"yes",                     // показывать эффект
		showOpenerPlayPauseButton:"yes",      // показывать кнопку плей / пауза
		openerEqulizerOffsetLeft:3,           // сдвигание эквалайзера слева
		openerEqulizerOffsetTop:-1,           // сдвигание эквалайзера сверху

		//a to b loop
		atbTimeBackgroundColor:"transparent", // цвет фона "от / до"
		atbTimeTextColorNormal:"#888888",     // цвет текста "от / до"
		atbTimeTextColorSelected:"#FFFFFF",   // цвет выбранного текста "от / до"
		atbButtonTextNormalColor:"#888888",   // цвет кнопки "от / до"
		atbButtonTextSelectedColor:"#FFFFFF", // цвет выбранной кнопки "от / до"
		atbButtonBackgroundNormalColor:"#FFFFFF", // цвет фона кнопки "от / до"
		atbButtonBackgroundSelectedColor:"#000000", // цвет фона выбранной кнопки "от / до"
	});

FWDMSPUtils.onReady(function(){
        music_player.addListener(FWDMSP.READY, music_onReady);
        music_player.addListener(FWDMSP.PLAY, music_onPlay);
        music_player.addListener(FWDMSP.PAUSE, music_onPause);
    });

function music_onReady(){console.log("Аудио плеер готов");}

function music_onPause(){
  try{
  div = document.createElement("div");
  div.innerHTML = music_player.getTrackTitle();
  title = div.querySelector('span').innerHTML;
  document.title = "Музыка приостановлена";
  if(document.querySelector(".user_status")){
    document.querySelector(".user_status").innerHTML = "Музыка приостановлена";
  }}catch{var a=0}
}
function music_onPlay(){
    console.log("Воспроизводится трек № : " + music_player.getTrackId());
    try{
    div = document.createElement("div");
    div.innerHTML = music_player.getTrackTitle();
    title = div.querySelector('span').innerHTML;
    document.title = title;
    if(document.querySelector(".user_status")){
      document.querySelector(".user_status").innerHTML = title;
    }}catch{var a=0};
    try{video_player.pause();}catch{var a=0}
};

function save_playlist(suffix, post_link, get_link, track_id){
    var playlist_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    playlist_link.open( 'GET', post_link, true );
    playlist_link.onreadystatechange = function () {
    if ( playlist_link.readyState == 4 && playlist_link.status == 200 ) {
      document.querySelector("body").className = "";
      document.querySelector("body").classList.add(suffix);

      var _link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
      _link.open( 'GET', get_link, true );
      _link.onreadystatechange = function () {
        if ( _link.readyState == 4 && _link.status == 200 ) {
          var response = document.createElement('span');
          response.innerHTML = _link.responseText;
          var list = response.querySelectorAll("li");
          var count = list.length;
          for(i=0; i<count; i++) {
            _source=list[i].getAttribute("data-path") + '/stream?client_id=' + 'dce5652caa1b66331903493735ddd64d';
            _title=list[i].getAttribute("data-title");
            _thumbPath=list[i].getAttribute("data-thumbpath");
            _duration=list[i].getAttribute("data-duration");
            time = msToTime(_duration);
            music_player.addTrack(_source, _title, _thumbPath, time, true, false, null);
          }
          music_player.loadPlaylist(0);
          if (FWDMSP.LOAD_PLAYLIST_COMPLETE){
            console.log("Плейдист загружен!");
          setTimeout(function() {music_player.playSpecificTrack(suffix, track_id)}, 50);
        }
      }};
      _link.send( null );
    }};
    playlist_link.send( null );
    };


on('#ajax', 'click', '.tag_item', function() {
  var track_id = this.parentElement.parentElement.getAttribute('data-counter');
  var tag_pk = document.querySelector(".tag_playlist").getAttribute('data-pk');
  if (!document.body.classList.contains("tag_" + tag_pk)){
    save_playlist("tag_" + tag_pk, '/music/manage/temp_tag/' + tag_pk, '/music/get/tag/' + tag_pk, track_id)
  }else{
    music_player.loadPlaylist(0);
    if (FWDMSP.LOAD_PLAYLIST_COMPLETE){
      console.log("Плейдист загружен!");
    setTimeout(function() {music_player.playSpecificTrack("tag_" + tag_pk, track_id)}, 50);
  }
  }
  });

on('#ajax', 'click', '.genre_item', function() {
  var track_id = this.parentElement.parentElement.getAttribute('data-counter');
  var genre_pk = document.querySelector(".genre_playlist").getAttribute('data-pk');
  if (!document.body.classList.contains("genre_" + genre_pk)){
    save_playlist("genre_" + genre_pk, '/music/manage/temp_genre/' + genre_pk, '/music/get/genre/' + genre_pk, track_id)
  }else{
    music_player.loadPlaylist(0);
    if (FWDMSP.LOAD_PLAYLIST_COMPLETE){
      console.log("Плейдист загружен!");
    setTimeout(function() {music_player.playSpecificTrack("genre_" + list_pk, track_id)}, 50);
  }
  }
});

on('#ajax', 'click', '.music_list_item', function() {
  var track_id = this.parentElement.parentElement.getAttribute('data-counter');
  var list_pk = document.querySelector(".music_playlist").getAttribute('data-pk');
  if (!document.body.classList.contains("list_" + list_pk)){
    save_playlist("list_" + list_pk, '/music/manage/temp_list/' + list_pk, '/music/get/list/' + list_pk, track_id)
  }else{
    music_player.loadPlaylist(0);
    if (FWDMSP.LOAD_PLAYLIST_COMPLETE){
      console.log("Плейлист загружен!");
    setTimeout(function() {music_player.playSpecificTrack("list_" + list_pk, track_id)}, 50);
  }
  }
});


on('#ajax', 'click', '#load_1', function(e) {
  music_player.loadPlaylist(0);
})
on('#ajax', 'click', '#load_2', function(e) {
  music_player.loadPlaylist(1);
})
on('#ajax', 'click', '#load_3', function(e) {
  music_player.loadPlaylist(2);
})

on('#ajax', 'click', '.track_add', function(e) {
  block = this.parentElement;
  pk = block.parentElement.getAttribute("data-pk");
  var _link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  _link.open( 'GET', "/music/manage/add_track/" + pk, true );
  _link.onreadystatechange = function () {
    if ( _link.readyState == 4 && _link.status == 200 ) {
      block.innerHTML = "";
      block.innerHTML = "<span class='track_remove' title='Удалить'><svg xmlns='http://www.w3.org/2000/svg' fill='currentColor' style='width:22px;height:22px;' class='svg_default' viewBox='0 0 2424'><path fill='none' d='M0 0h24v24H0z'/><path d='M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z'/></svg></span>"
  }};
  _link.send( null );
});

on('#ajax', 'click', '.track_remove', function(e) {
  block = this.parentElement;
  pk = block.parentElement.getAttribute("data-pk");
  var _link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  _link.open( 'GET', "/music/manage/remove_track/" + pk, true );
  _link.onreadystatechange = function () {
    if ( _link.readyState == 4 && _link.status == 200 ) {
      block.innerHTML = "";
      block.innerHTML = "<span class='track_add' title='Добавить'><svg fill='currentColor' style='width:22px;height:22px;' class='svg_default' xmlns='http://www.w3.org/2000/svg' viewBox='0 024 24'><path d='M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z'/><path d='M0 0h24v24H0z' fill='none'/></svg></span>"
  }};
  _link.send( null );
});



function load_video_playlist(counter) {
video_player = new FWDUVPlayer({
		//main settings
		instanceName:"player_white",
		parentId:"video_player",
		playlistsId:"video_playlists",
		mainFolderPath:"/static",
		skinPath:"images/video_white/",
		displayType:"responsive",                 // тип дисплея (выбран отзывчивый к размерам экрана)
		useVectorIcons:"no",                      // использование векторной графики
		fillEntireVideoScreen:"no",               // заполнение всего экрана видео-роликом
		fillEntireposterScreen:"yes",             // заполнение всего экрана постером
		goFullScreenOnButtonPlay:"yes",            // показывать кнопку включения полноэкранного режима
		playsinline:"yes",                        // играет в ряд
		initializeOnlyWhenVisible:"no",           // инициализировать плеер только тогда, когда он виден
		youtubeAPIKey:'AIzaSyCgbixU3aIWCkiZ76h_E-XpEGig5mFhnVY', // ключ разработчика для ютуба
		useHEXColorsForSkin:"no",                 // использование hex кодировки для скина
		normalHEXButtonsColor:"#FF0000",          // цвет кнопки
		selectedHEXButtonsColor:"#000000",        // цвет нажатой кнопки
		useResumeOnPlay:"no",                     // использование резюме при проигрывании
		useDeepLinking:"no",                      // использование глубоких ссылок для ограничения перехвата ссылки на видео
		showPreloader:"yes",                      // gjrfpsdfnm ghtkjflth ghb pfuheprt gktthf
		preloaderBackgroundColor:"#000000",       // цвет фона прелоадера
		preloaderFillColor:"#FFFFFF",             // цвет прелоадера
		addKeyboardSupport:"no",                 // использовать поддержку клавиатуры
		autoScale:"yes",                          // автоматическое масштабирование
		stopVideoWhenPlayComplete:"no",           // остановить плеер после проигрывания последнего ролика
		playAfterVideoStop:"yes",                 // воспроизведение после остановки видео
		autoPlay:"yes",                            // автоматический старт проигрывания
		loop:"no",                                // повтор видео сразу
		shuffle:"no",                             // перемешивание видео сразу
		showErrorInfo:"no",                       // показывать информацию об ошибках
		maxWidth:1170,                            // максимальная ширина
		maxHeight:659,                            // максимальная высота
		volume:.8,                                // начальная громкость плеера (1 - 100%)
		backgroundColor:"#eeeeee",                // цвет фона
		videoBackgroundColor:"#000000",           // цвет фона видео-секции
		posterBackgroundColor:"#000000",          // цвет фона постера

		//logo settings
		showLogo:"no",                            // показывать логотип над секцией видео справа

		//playlists/categories settings
		showPlaylistsSearchInput:"no",            // показывать поле поиска плейлиста
		usePlaylistsSelectBox:"no",              // использовать выбор плейлистов в окне сверху
		showPlaylistsByDefault:"no",              // показать плейлист по умолчанию
		thumbnailSelectedType:"opacity",          // анимация выбранного плейлиста в окне сверху
		startAtPlaylist:0,                        // проигрывать плейлист номер ...
		buttonsMargins:15,                        // расстояние между кнопками
		thumbnailMaxWidth:350,                    // максимальная ширина миниатюры
		thumbnailMaxHeight:350,                   // максимальная высота миниатюры
		horizontalSpaceBetweenThumbnails:40,      // расстояние между миниатюрами по горизонтали
		verticalSpaceBetweenThumbnails:40,        // расстояние между миниатюрами по вертикали
		inputBackgroundColor:"#333333",           // цвет фона поля ввода
		inputColor:"#000000",                     // цвет текста поля ввода

		//playlist settings
		showPlaylistButtonAndPlaylist:"yes",      // показывать кнопку выбора плейлистов и сами плейлисты сверху
		playlistPosition:"right",                 // расположение плейлиста
		showPlaylistByDefault:"yes",              // показать плейлист по умолчанию
		showPlaylistName:"no",                   // показывать название плейлиста
		showSearchInput:"no",                    // показывать поле поиска
		showLoopButton:"yes",                     // показывать кнопку повтора
		showShuffleButton:"yes",                  // показывать кнопку перемешивания
		showPlaylistOnFullScreen:"no",            // показывать плейлист в режиме полного экрана
		showNextAndPrevButtons:"yes",             // показывать кнопки пред/след видео
		showThumbnail:"yes",                      // показывать миниатюры
		addMouseWheelSupport:"yes",               // поддержка управления мыши
		startAtRandomVideo:"no",                  // начинать воспроиведение со случайного видео ролика
		stopAfterLastVideoHasPlayed:"no",         // останавливать воспроизведение после последнего ролика
		addScrollOnMouseMove:"no",                // перемотка движениями мыши
		randomizePlaylist:'no',                   // случайные плейлисты
		folderVideoLabel:"VIDEO ",                // название папки видео
		playlistRightWidth:320,                   // ширина плейлиста справа
		playlistBottomHeight:380,                 // высота плейлиста снизу
		startAtVideo:0,                           // начинать с ролика номер ...
		maxPlaylistItems:50,                      // максимальное количество роликов в плейлисте
		thumbnailWidth:71,                        // ширина миниатюры
		thumbnailHeight:71,                       // высота миниатюры
		spaceBetweenControllerAndPlaylist:1,      // расстояние между контроллером и плейлистом
		spaceBetweenThumbnails:1,                 // расстояние между миниатюрами
		scrollbarOffestWidth:8,                   // отступ ширины скроллбара
		scollbarSpeedSensitivity:.5,              // скорость отклика скроллбара
		playlistBackgroundColor:"#eeeeee",        // цвет фона плейлиста
		playlistNameColor:"#000000",              // цвет названия плейлиста
		thumbnailNormalBackgroundColor:"#ffffff", // цвет фона миниатюры
		thumbnailHoverBackgroundColor:"#eeeeee",  // цвет фона активной миниатюры
		thumbnailDisabledBackgroundColor:"#eeeeee", // цвет фона disabled миниатюры
		searchInputBackgroundColor:"#F3F3F3",     // цвет фона поля поиска
		searchInputColor:"#888888",               // цвет фона текста поиска
		youtubeAndFolderVideoTitleColor:"#000000",// цвет плейлиста роликов с папок и ютуба
		youtubeOwnerColor:"#919191",              // цвет названия ролика я ютуба
		youtubeDescriptionColor:"#919191",        // цвет описания ролика я ютуба
		mainSelectorBackgroundSelectedColor:"#000000", // цвет фона плейлиста при наведении
		mainSelectorTextNormalColor:"#000000",    // цвет текста плейлиста
		mainSelectorTextSelectedColor:"#FFFFFFF", // цвет текста плейлиста при наведении
		mainButtonBackgroundNormalColor:"#FFFFFF",// цвет фона кнопок
		mainButtonBackgroundSelectedColor:"#000000",// цвет фона нажатой кнопки
		mainButtonTextNormalColor:"#000000",      // цвет текста кнопок
		mainButtonTextSelectedColor:"#FFFFFF",    // цвет текста нажатой кнопки

		//controller settings
		showController:"yes",                     // показывать контроллер
		showControllerWhenVideoIsStopped:"yes",   // показывать контроллер при остановке проигрывания
		showNextAndPrevButtonsInController:"no",  // показывать кнопки пред / след на контроллере
		showRewindButton:"yes",                   // показать кнопку перемотки назад
		showPlaybackRateButton:"yes",             // показать кнопку выбора скорости воспроизведения
		showVolumeButton:"yes",                   // показать кнопку громкости
		showTime:"yes",                           // показать время воспроизведения
		showQualityButton:"yes",                  // показать время выбора качества видео
		showInfoButton:"no",                     // показывать кнопку информации ролика
		showShareButton:"no",                     // показывать кнопку расшаривания ролика
		showEmbedButton:"no",                    // показывать кнопку получения ссылки ролика и фрейма для вставки на другие сайты
		showChromecastButton:"no",                // показывать кнопку подкастов
		showFullScreenButton:"yes",               // показывать кнопку полноэкранного режима
		disableVideoScrubber:"no",                // выключить ползунок переключения времени видео
		showScrubberWhenControllerIsHidden:"yes", // показывать ползунок времени воспроизведенного ролика при скрытом контроллере
		showDefaultControllerForVimeo:"no",       // показывать контроллер vimeo
		repeatBackground:"yes",                   // повтор бекгроунда
		controllerHeight:42,                      // высота контроллера
		controllerHideDelay:3,                    // время, через которое скроется контроллер
		startSpaceBetweenButtons:7,               // начальное расстояние между кнопками
		spaceBetweenButtons:8,                    // расстояние между кнопками
		scrubbersOffsetWidth:2,                   // ширина отступа скруббера
		mainScrubberOffestTop:14,                 // отступ скруббера всерху
		timeOffsetLeftWidth:5,                    // ширина отступа времени воспроизведения слева
		timeOffsetRightWidth:3,                   // ширина отступа времени воспроизведения справа
		timeOffsetTop:0,                          // отступ времени воспроизведения сверху
		volumeScrubberHeight:80,                  // высота скруббера громкости
		volumeScrubberOfsetHeight:12,             // отступскруббера громкости по высоте
		timeColor:"#919191",                      // цвет времени воспроизведения
		youtubeQualityButtonNormalColor:"#919191",// кнопка выбора качества плейлитса ютуба
		youtubeQualityButtonSelectedColor:"#000000",// нажатая кнопка выбора качества плейлитса ютуба

		//advertisement on pause window
		aopwTitle:"Advertisement",                // название рекламной вставки
		aopwWidth:400,                            // ширина вставки
		aopwHeight:240,                           // высота вставки
		aopwBorderSize:6,                         // размер рамки вставки
		aopwTitleColor:"#000000",                 // цветназвания вставки

		//subtitle
		subtitlesOffLabel:"Субтитры откл.",       // надпись, когда субтитры отключены

		//popup add windows
		showPopupAdsCloseButton:"no",            // показать кнопку закрытия окна подставки

		//окно размещения и информации
		embedAndInfoWindowCloseButtonMargins:15,  // отступ кнопки закрытия
		borderColor:"#CDCDCD",                    // цвет рамки
		mainLabelsColor:"#000000",                // цвет названия
		secondaryLabelsColor:"#444444",           // вторичный цвет названия
		shareAndEmbedTextColor:"#777777",         // цвет тектса овна расшаривания и вставки
		inputBackgroundColor:"#c0c0c0",           // цвет фона поля ввода
		inputColor:"#333333",                     // цвет фона текста ввода

		//audio visualizer
		audioVisualizerLinesColor:"#ff9f00",      // цвет линий аудио визуализатора
		audioVisualizerCircleColor:"#FFFFFF",     // цвет кругов аудио визуализатора

		//lightbox settings
		lightBoxBackgroundOpacity:.6,             // прозрачность
		lightBoxBackgroundColor:"#000000",        // цвет фона

		//sticky on scroll
		stickyOnScroll:"no",                      // липкое листание
		stickyOnScrollShowOpener:"yes",           // показывать эффект
		stickyOnScrollWidth:"700",                // ширина
		stickyOnScrollHeight:"394",               // высота

		//настройки липкого дисплея
		showOpener:"yes",                         // показывать вставки
		showOpenerPlayPauseButton:"yes",          // показывать кнопку плей при паузе
		verticalPosition:"bottom",                // позиция по вертикали
		horizontalPosition:"center",              // позиция по горизонтали
		showPlayerByDefault:"yes",                // показывать плеер по умолчанию
		animatePlayer:"yes",                      // анимировать плеер
		openerAlignment:"right",                  // выравнивание вставки
		mainBackgroundImagePath:"main-background.png", // путь до изображения фона
		openerEqulizerOffsetTop:-1,               // отступ эквалайзера сверху
		openerEqulizerOffsetLeft:3,               // отступ эквалайзера слева
		offsetX:0,                                // отступ по оси X
		offsetY:0,																// отступ по оси Y

		//скорость воспроизведения
		defaultPlaybackRate:1,                   //0.25, 0.5, 1, 1.25, 1.2, 2
		//cuepoints
		executeCuepointsOnlyOnce:"no",           // выполнение ключевых точек только один раз
		//annotations
		showAnnotationsPositionTool:"no",        // показывать координаты аннотаций на экране

		//ads
		openNewPageAtTheEndOfTheAds:"no",        // открыть новую страницу в конце объявления
		adsButtonsPosition:"left",               // позиция окна рекламы
		skipToVideoText:"Закрыть через: ",       // текст окна рекламы
		skipToVideoButtonText:"Закрыть",         // текст кнопки закрытия рекламного окна
		adsTextNormalColor:"#888888",            // цвет рекламного текста
		adsTextSelectedColor:"#000000",          // цвет выбранного текста
		adsBorderNormalColor:"#AAAAAA",          // цвет рамки рекламного окна
		adsBorderSelectedColor:"#000000",        // цвет выбраной рамки рекламного окна

		//a to b loop
		useAToB:"no",                            // использование повтора от...до
		atbTimeBackgroundColor:"transparent",    // время фона от...до
		atbTimeTextColorNormal:"#888888",        // время текста от...до
		atbTimeTextColorSelected:"#FFFFFF",
		atbButtonTextNormalColor:"#888888",
		atbButtonTextSelectedColor:"#FFFFFF",
		atbButtonBackgroundNormalColor:"#FFFFFF",
		atbButtonBackgroundSelectedColor:"#000000",

		//thumbnails preview
		thumbnailsPreviewWidth:196,              // ширина предпросмотра миниатюры
		thumbnailsPreviewHeight:110,             // высота предпросмотра миниатюры
		thumbnailsPreviewBackgroundColor:"#000000",// цвет фона  миниатюры
		thumbnailsPreviewBorderColor:"#666",     // цвет названия миниатюры
		thumbnailsPreviewLabelBackgroundColor:"#666", // цвет фона названия минатюры
		thumbnailsPreviewLabelFontColor:"#FFF",
		// context menu
		showContextmenu:'no',
		showScriptDeveloper:"no",
		contextMenuBackgroundColor:"#ebebeb",
		contextMenuBorderColor:"#ebebeb",
		contextMenuSpacerColor:"#CCC",
		contextMenuItemNormalColor:"#888888",
		contextMenuItemSelectedColor:"#000",
		contextMenuItemDisabledColor:"#BBB"
});
}
