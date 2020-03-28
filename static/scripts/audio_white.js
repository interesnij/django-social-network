		new FWDMSP({
				//main settings
				instanceName:"player1",
				playlistsId:"audio_playlists",
				mainFolderPath:"/static/images/",
				skinPath:"audio_white",
				showSoundCloudUserNameInTitle:"no",   // показывать имя пользователя soundcloud
				showMainBackground:"yes",  						// показать общий фон
				position:"bottom",         						// расположение плеера
				useDeepLinking:"yes",									// использовать глубокие ссылки - защита от перехвата
				useYoutube:"no",											// использовать youtube файлы
				useVideo:"no",												// использовать видео файлы
				rightClickContextMenu:"no",           // показ контекстног меню по щелчку правой кнопкой мыши
				showButtonsToolTips:"no",             // показать всплывающие подсказки кнопок
				addKeyboardSupport:"yes",             // добавить поддержку клавиатуры
				animate:"yes",												// фнимация
				autoPlay:"no",												// автостарт плеера
				loop:"no",														// повтор песни
				shuffle:"no",													// перемешивание треков
				maxWidth:850,                         // максимальная ширина
				volume:.8,														// громкость по умолчанию 80%
				// toolTipsButtonsHideDelay:1.5,      // задержка всплывающих подсказок для кнопок
				// toolTipsButtonFontColor:"#888888", // цвет всплывающих подсказок

				// controller settings
				showControllerByDefault:"yes",        // показать контроллер по умолчанию
				showThumbnail:"yes",                  // показывать миниатюры
				// showFullScreenButton:"yes",        // показывать кнопку включения полноэкранного режима
				showNextAndPrevButtons:"yes",					// показывать кнопки переключения треков
				showSoundAnimation:"yes",							// показывать анимацию музыкального воспроизведения
				showLoopButton:"yes",                 // показывать кнопку повтора треков
				showShuffleButton:"yes",              // показывать кнопку перемешивания треков
				showDownloadMp3Button:"yes",          // показывать кнопку скачивания mp3
				showBuyButton:"yes",                  // показывать кнопку покупки треков
				showShareButton:"no",									// показывать кнопку расшаривания треков
				showMainScrubberAndVolumeScrubberToolTipLabel:"no",  // показывать всплывающее окно громкости и сам скруббер
				expandBackground:"no",              	// развернуть фон
				titleColor:"#000000",                 // цвет названия
				timeColor:"#919191",                  // цвет времени
				scrubbersToolTipLabelBackgroundColor:"#FFFFFF", // фон скруббера громкости
				// scrubbersToolTipLabelFontColor:"#5a5a5a", // цвет всплывающих окон скруббера

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
				showPlaylistItemBuyButton:"yes",     // показать кнопку покупки элемента плейлиста
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

				//password window
				borderColor:"#333333",                // цвет рамки
				mainLabelsColor:"#FFFFFF",            // цвет вводимого текста
				secondaryLabelsColor:"#a1a1a1",       // вторичный цвет вводимого текста
				textColor:"#5a5a5a",                  // цвет текста
				inputBackgroundColor:"#000000",       // фон поля ввода
				inputColor:"#FFFFFF",                 // цвет поля ввода

				//opener settings
				openerAlignment:"right",              // открывание
				showOpener:"yes",                     // показывать эффект
				showOpenerPlayPauseButton:"yes",      // показывать кнопку плей / пауза
				openerEqulizerOffsetLeft:3,           // сдвигание эквалайзера слева
				openerEqulizerOffsetTop:-1,           // сдвигание эквалайзера сверху

				//popup settings
				showPopupButton:"yes",                // показать всплывающую кнопку
				popupWindowBackgroundColor:"#878787", // фон окна всплывающего окна
				popupWindowWidth:850,                 // ширина окна всплывающего окна
				popupWindowHeight:423,                // высота окна всплывающего окна

				//a to b loop
				atbTimeBackgroundColor:"transparent", // цвет фона "от / до"
				atbTimeTextColorNormal:"#888888",     // цвет текста "от / до"
				atbTimeTextColorSelected:"#FFFFFF",   // цвет выбранного текста "от / до"
				atbButtonTextNormalColor:"#888888",   // цвет кнопки "от / до"
				atbButtonTextSelectedColor:"#FFFFFF", // цвет выбранной кнопки "от / до"
				atbButtonBackgroundNormalColor:"#FFFFFF", // цвет фона кнопки "от / до"
				atbButtonBackgroundSelectedColor:"#000000", // цвет фона выбранной кнопки "от / до"
			});
