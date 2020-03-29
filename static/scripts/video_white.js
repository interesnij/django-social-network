
new FWDUVPlayer({
		//main settings
		instanceName:"player_white",
		parentId:"video_player",
		playlistsId:"video_playlists",
		mainFolderPath:"/static",
		skinPath:"images/video_white/",
		displayType:"responsive",                 // тип дисплея (выбран отзывчивый к размерам экрана)
		useVectorIcons:"no",                      // использование векторной графики
		fillEntireVideoScreen:"no",               // заполнение всего экрана видео-роликом
		fillEntireposterScreen:"yes",             // заполнение всего экрана посетром
		goFullScreenOnButtonPlay:"no",            // показывать кнопку включения полноэкранного режима
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
		addKeyboardSupport:"yes",                 // сипользовать поддержку клавиатуры
		autoScale:"yes",                          // автоматическое масштабирование
		showButtonsToolTip:"yes",                 // показывать подсказки для кнопок
		stopVideoWhenPlayComplete:"no",           // остановить плеер после проигрывания последнего ролика
		playAfterVideoStop:"yes",                 // воспроизведение после остановки видео
		autoPlay:"no",                            // автоматический старт проигрывания
		loop:"no",                                // повтор видео сразу
		shuffle:"no",                             // перемешивание видео сразу
		showErrorInfo:"no",                       // показывать информацию об ошибках
		maxWidth:1170,                            // максимальная ширина
		maxHeight:659,                            // максимальная высота
		volume:.8,                                // начальная громкость плеера (1 - 100%)
		buttonsToolTipHideDelay:1.5,              // время задержки пояснительных окон у кнопок
		backgroundColor:"#eeeeee",                // цвет фона
		videoBackgroundColor:"#000000",           // цвет фона видео-секции
		posterBackgroundColor:"#000000",          // цвет фона постера
		buttonsToolTipFontColor:"#FFFFFF",        // цвет фона пояснительных окон у кнопок

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
		playlistPosition:"right",
		showPlaylistByDefault:"yes",
		showPlaylistName:"yes",
		showSearchInput:"yes",
		showLoopButton:"yes",
		showShuffleButton:"yes",
		showPlaylistOnFullScreen:"no",
		showNextAndPrevButtons:"yes",
		showThumbnail:"yes",
		forceDisableDownloadButtonForFolder:"yes",
		addMouseWheelSupport:"yes",
		startAtRandomVideo:"no",
		stopAfterLastVideoHasPlayed:"no",
		addScrollOnMouseMove:"no",
		randomizePlaylist:'no',
		folderVideoLabel:"VIDEO ",
		playlistRightWidth:320,
		playlistBottomHeight:380,
		startAtVideo:0,
		maxPlaylistItems:50,
		thumbnailWidth:71,
		thumbnailHeight:71,
		spaceBetweenControllerAndPlaylist:1,
		spaceBetweenThumbnails:1,
		scrollbarOffestWidth:8,
		scollbarSpeedSensitivity:.5,
		playlistBackgroundColor:"#eeeeee",
		playlistNameColor:"#000000",
		thumbnailNormalBackgroundColor:"#ffffff",
		thumbnailHoverBackgroundColor:"#eeeeee",
		thumbnailDisabledBackgroundColor:"#eeeeee",
		searchInputBackgroundColor:"#F3F3F3",
		searchInputColor:"#888888",
		youtubeAndFolderVideoTitleColor:"#000000",
		folderAudioSecondTitleColor:"#999999",
		youtubeOwnerColor:"#919191",
		youtubeDescriptionColor:"#919191",
		mainSelectorBackgroundSelectedColor:"#000000",
		mainSelectorTextNormalColor:"#000000",
		mainSelectorTextSelectedColor:"#FFFFFFF",
		mainButtonBackgroundNormalColor:"#FFFFFF",
		mainButtonBackgroundSelectedColor:"#000000",
		mainButtonTextNormalColor:"#000000",
		mainButtonTextSelectedColor:"#FFFFFF",
		//controller settings
		showController:"yes",
		showControllerWhenVideoIsStopped:"yes",
		showNextAndPrevButtonsInController:"no",
		showRewindButton:"yes",
		showPlaybackRateButton:"yes",
		showVolumeButton:"yes",
		showTime:"yes",
		showQualityButton:"yes",
		showInfoButton:"yes",
		showDownloadButton:"no",
		showShareButton:"no",
		showEmbedButton:"yes",
		showChromecastButton:"no",
		showFullScreenButton:"yes",
		disableVideoScrubber:"no",
		showScrubberWhenControllerIsHidden:"yes",
		showMainScrubberToolTipLabel:"yes",
		showDefaultControllerForVimeo:"no",
		repeatBackground:"yes",
		controllerHeight:42,
		controllerHideDelay:3,
		startSpaceBetweenButtons:7,
		spaceBetweenButtons:8,
		scrubbersOffsetWidth:2,
		mainScrubberOffestTop:14,
		timeOffsetLeftWidth:5,
		timeOffsetRightWidth:3,
		timeOffsetTop:0,
		volumeScrubberHeight:80,
		volumeScrubberOfsetHeight:12,
		timeColor:"#919191",
		youtubeQualityButtonNormalColor:"#919191",
		youtubeQualityButtonSelectedColor:"#000000",
		scrubbersToolTipLabelBackgroundColor:"#000000",
		scrubbersToolTipLabelFontColor:"#FFFFFF",
		//advertisement on pause window
		aopwTitle:"Advertisement",
		aopwWidth:400,
		aopwHeight:240,
		aopwBorderSize:6,
		aopwTitleColor:"#000000",
		//subtitle
		subtitlesOffLabel:"Субтитры откл.",
		//popup add windows
		showPopupAdsCloseButton:"yes",
		//embed window and info window
		embedAndInfoWindowCloseButtonMargins:15,
		borderColor:"#CDCDCD",
		mainLabelsColor:"#000000",
		secondaryLabelsColor:"#444444",
		shareAndEmbedTextColor:"#777777",
		inputBackgroundColor:"#c0c0c0",
		inputColor:"#333333",
		//loggin
		isLoggedIn:"no",
		playVideoOnlyWhenLoggedIn:"no",
		loggedInMessage:"Please login to view this video.",
		//audio visualizer
		audioVisualizerLinesColor:"#ff9f00",
		audioVisualizerCircleColor:"#FFFFFF",
		//lightbox settings
		lightBoxBackgroundOpacity:.6,
		lightBoxBackgroundColor:"#000000",
		//sticky on scroll
		stickyOnScroll:"no",
		stickyOnScrollShowOpener:"yes",
		stickyOnScrollWidth:"700",
		stickyOnScrollHeight:"394",
		//sticky display settings
		showOpener:"yes",
		showOpenerPlayPauseButton:"yes",
		verticalPosition:"bottom",
		horizontalPosition:"center",
		showPlayerByDefault:"yes",
		animatePlayer:"yes",
		openerAlignment:"right",
		mainBackgroundImagePath:"main-background.png",
		openerEqulizerOffsetTop:-1,
		openerEqulizerOffsetLeft:3,
		offsetX:0,
		offsetY:0,
		//playback rate / speed
		defaultPlaybackRate:1, //0.25, 0.5, 1, 1.25, 1.2, 2
		//cuepoints
		executeCuepointsOnlyOnce:"no",
		//annotations
		showAnnotationsPositionTool:"no",
		//ads
		openNewPageAtTheEndOfTheAds:"no",
		adsButtonsPosition:"left",
		skipToVideoText:"Закрыть через: ",
		skipToVideoButtonText:"Закрыть",
		adsTextNormalColor:"#888888",
		adsTextSelectedColor:"#000000",
		adsBorderNormalColor:"#AAAAAA",
		adsBorderSelectedColor:"#000000",
		//a to b loop
		useAToB:"no",
		atbTimeBackgroundColor:"transparent",
		atbTimeTextColorNormal:"#888888",
		atbTimeTextColorSelected:"#FFFFFF",
		atbButtonTextNormalColor:"#888888",
		atbButtonTextSelectedColor:"#FFFFFF",
		atbButtonBackgroundNormalColor:"#FFFFFF",
		atbButtonBackgroundSelectedColor:"#000000",
		//thumbnails preview
		thumbnailsPreviewWidth:196,
		thumbnailsPreviewHeight:110,
		thumbnailsPreviewBackgroundColor:"#000000",
		thumbnailsPreviewBorderColor:"#666",
		thumbnailsPreviewLabelBackgroundColor:"#666",
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
