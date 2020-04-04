

audio_player = new MUSIC({
		//main settings
		instanceName:"player1",
		playlistsId:"audio_playlists",
		mainFolderPath:"/static/images/",
		skinPath:"audio_white",
		showSoundCloudUserNameInTitle:"no",   // показывать имя пользователя soundcloud
		showMainBackground:"yes",  						// показать общий фон
		position:"bottom",                    // расположение плеера
		rightClickContextMenu:"developer",
		useDeepLinking:"no",									// использовать глубокие ссылки - защита от перехвата. Не будет работать с souncloud
		rightClickContextMenu:"no",           // показ контекстног меню по щелчку правой кнопкой мыши
		addKeyboardSupport:"yes",             // добавить поддержку клавиатуры
		animate:"yes",												// фнимация
		autoPlay:"no",												// автостарт плеера
		loop:"no",														// повтор песни
		shuffle:"no",													// перемешивание треков
		maxWidth:850,                         // максимальная ширина
		volume:.8,														// громкость по умолчанию 80%

		// controller settings
		showControllerByDefault:"yes",        // показать контроллер по умолчанию
		showThumbnail:"yes",                  // показывать миниатюры
		// showFullScreenButton:"yes",        // показывать кнопку включения полноэкранного режима
		showNextAndPrevButtons:"yes",					// показывать кнопки переключения треков
		showSoundAnimation:"yes",							// показывать анимацию музыкального воспроизведения
		showLoopButton:"yes",                 // показывать кнопку повтора треков
		showShuffleButton:"yes",              // показывать кнопку перемешивания треков
		showDownloadMp3Button:"yes",          // показывать кнопку скачивания mp3
		expandBackground:"no",              	// развернуть фон
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
		showPlaylistsSearchInput:"yes",      // показывать поле поиска в плейлисте
		usePlaylistsSelectBox:"yes",         // показывать поле плейлистов сверху выбранного плейлиста
		showPlaylistsSelectBoxNumbers:"yes", // пронумеровать плейлисты в поле выбора плейлиста
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
		showPlaylistItemDownloadButton:"yes",// показать кнопку загрузки элемента плейлиста
		forceDisableDownloadButtonForPodcast:"yes", // принудительно отключить кнопку загрузки для подкаста
		forceDisableDownloadButtonForOfficialFM:"yes", // принудительно отключить кнопку загрузки для радио передачи
		forceDisableDownloadButtonForFolder:"yes", // принудительно отключить кнопку загрузки для попки
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
		downloadButtonOffsetRight:11,         // отступ справа кнопки загрузки трека (в плейлисте)
		scrollbarOffestWidth:7,               // шмрмна смещения полосы прокрутки

		//playback rate / speed
		showPlaybackRateButton:"yes",         // показать кнопку скорости воспроизведения
		defaultPlaybackRate:1, //min - 0.5 / max - 3 // скорость воспроизведения по умолчанию (от 0,5 до 3)
		playbackRateWindowTextColor:"#888888",// цвет текста на окне выбора скорости

		//search bar settings
		showSearchBar:"yes",                  // показывать секцию поиска треков
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
		goFullScreenOnButtonPlay:"no",            // показывать кнопку включения полноэкранного режима
		playsinline:"no",                        // играет в ряд
		initializeOnlyWhenVisible:"yes",           // инициализировать плеер только тогда, когда он виден
		youtubeAPIKey:'AIzaSyCgbixU3aIWCkiZ76h_E-XpEGig5mFhnVY', // ключ разработчика для ютуба
		useHEXColorsForSkin:"no",                 // использование hex кодировки для скина
		normalHEXButtonsColor:"#FF0000",          // цвет кнопки
		selectedHEXButtonsColor:"#000000",        // цвет нажатой кнопки
		useResumeOnPlay:"no",                     // использование резюме при проигрывании
		useDeepLinking:"no",                      // использование глубоких ссылок для ограничения перехвата ссылки на видео
		showPreloader:"yes",                      // gjrfpsdfnm ghtkjflth ghb pfuheprt gktthf
		preloaderBackgroundColor:"#000000",       // цвет фона прелоадера
		preloaderFillColor:"#FFFFFF",             // цвет прелоадера
		addKeyboardSupport:"yes",                 // использовать поддержку клавиатуры
		autoScale:"yes",                          // автоматическое масштабирование
		stopVideoWhenPlayComplete:"no",           // остановить плеер после проигрывания последнего ролика
		playAfterVideoStop:"yes",                 // воспроизведение после остановки видео
		autoPlay:"no",                            // автоматический старт проигрывания
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
		usePlaylistsSelectBox:"yes",              // использовать выбор плейлистов в окне сверху
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
		showPlaylistName:"yes",                   // показывать название плейлиста
		showSearchInput:"yes",                    // показывать поле поиска
		showLoopButton:"yes",                     // показывать кнопку повтора
		showShuffleButton:"yes",                  // показывать кнопку перемешивания
		showPlaylistOnFullScreen:"no",            // показывать плейлист в режиме полного экрана
		showNextAndPrevButtons:"yes",             // показывать кнопки пред/след видео
		showThumbnail:"yes",                      // показывать миниатюры
		forceDisableDownloadButtonForFolder:"yes",// принудительно скрывать кнопку загрузки видео из локальных папок
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
		showInfoButton:"yes",                     // показывать кнопку информации ролика
		showDownloadButton:"no",                  // показывать кнопку загрузки ролика
		showShareButton:"no",                     // показывать кнопку расшаривания ролика
		showEmbedButton:"yes",                    // показывать кнопку получения ссылки ролика и фрейма для вставки на другие сайты
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
		showPopupAdsCloseButton:"yes",            // показать кнопку закрытия окна подставки

		//окно размещения и информации
		embedAndInfoWindowCloseButtonMargins:15,  // отступ кнопки закрытия
		borderColor:"#CDCDCD",                    // цвет рамки
		mainLabelsColor:"#000000",                // цвет названия
		secondaryLabelsColor:"#444444",           // вторичный цвет названия
		shareAndEmbedTextColor:"#777777",         // цвет тектса овна расшаривания и вставки
		inputBackgroundColor:"#c0c0c0",           // цвет фона поля ввода
		inputColor:"#333333",                     // цвет фона текста ввода

		//loggin
		isLoggedIn:"no",
		playVideoOnlyWhenLoggedIn:"no",
		loggedInMessage:"Please login to view this video.",

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
		showContextmenu:'yes',
		showScriptDeveloper:"no",
		contextMenuBackgroundColor:"#ebebeb",
		contextMenuBorderColor:"#ebebeb",
		contextMenuSpacerColor:"#CCC",
		contextMenuItemNormalColor:"#888888",
		contextMenuItemSelectedColor:"#000",
		contextMenuItemDisabledColor:"#BBB"
});
if(audio_player.play()){
	audio_player.parentElement.classList.add("audio_is_played")
}
on('#ajax', 'click', '#video_stopped', function(e) {
	video_player.pause();
})

on('#ajax', 'click', '#video_player', function(e) {
	audio_player.pause();
})
